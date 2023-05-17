import cv2
from PIL import Image, ImageTk
import numpy as np


##################
# 检测部分
#################
# 定义一个感兴趣区域
def region_interest(img, region):
    # 创立一个掩码
    mask = np.zeros_like(img)

    # 多通道
    if len(img.shape) > 2:
        channel_count = img.shape[2]
        ignore_mask_color = (255,)*channel_count
    # 单通道
    else:
        ignore_mask_color = 255

    # 图像填充,全白
    cv2.fillPoly(mask, region, ignore_mask_color)

    # 进行与操作
    mask_img = cv2.bitwise_and(img, mask)
    return mask_img


# 计算左右车道线直线方程，计算左右车道线的上下边界
def draw_lines(img, lines, color, thickness):
    left_lines_x = []
    left_lines_y = []
    right_lines_x = []
    right_lines_y = []
    line_y_max = 0
    line_y_min = 999
    for line in lines:
        for x1, y1, x2, y2 in line:
            if y1 > line_y_max:
                line_y_max = y1
            if y2 > line_y_max:
                line_y_max = y2
            if y1 < line_y_min:
                line_y_min = y1
            if y2 < line_y_min:
                line_y_min = y2
            k = (y2 - y1)/(x2 - x1)
            if k < -0.3:
                left_lines_x.append(x1)
                left_lines_y.append(y1)
                left_lines_x.append(x2)
                left_lines_y.append(y2)
            elif k > 0.3:
                right_lines_x.append(x1)
                right_lines_y.append(y1)
                right_lines_x.append(x2)
                right_lines_y.append(y2)
    # 最小二乘直线拟合
    left_line_k, left_line_b = np.polyfit(left_lines_x, left_lines_y, 1)
    right_line_k, right_line_b = np.polyfit(right_lines_x, right_lines_y, 1)

    # 根据直线方程和最大、最小的y值反算对应的x
    cv2.line(img,
             (int((line_y_max - left_line_b)/left_line_k), line_y_max),
             (int((line_y_min - left_line_b)/left_line_k), line_y_min),
             color, thickness)
    cv2.line(img,
             (int((line_y_max - right_line_b)/right_line_k), line_y_max),
             (int((line_y_min - right_line_b)/right_line_k), line_y_min),

             color, thickness)


# 车道线检测总函数
def detection_line_1(img):
    # BGR转换灰度图，opencv中为BGR格式
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # canny算子进行边缘提取,"有横线遗留"加大low_threshold的值,40->100
    low_threshold = 100
    high_threshold = 150
    eager_img = cv2.Canny(gray_img, low_threshold, high_threshold)

    # 感兴趣区域选择，报TypeError: expected non-empty vector for x错，将apex的第二个值降低，310->300
    left_bottom = [0, img.shape[0]]
    right_bottom = [img.shape[1], img.shape[0]]
    apex = [img.shape[1]/2, 305]

    # 一个多边形为2维数组，多个多边形为3维数组
    region = np.array([[left_bottom, right_bottom, apex]], dtype=np.int32)
    mask_img = region_interest(eager_img, region)

    # 霍夫变换->检测直线
    rho = 2  # distance resolution in pixels of the Hough grid
    theta = np.pi/180  # angular resolution in radians of the Hough grid
    threshold = 15     # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 40  # minimum number of pixels making up a line
    max_line_gap = 20    # maximum gap in pixels between connectable line segments

    # Hough Transform 检测线段，线段两个端点的坐标存在lines中
    lines = cv2.HoughLinesP(mask_img, rho, theta, threshold, np.array([]),
                                min_line_length, max_line_gap)

    # 复制一个原图
    img_copy = np.copy(img)
    # 绘制变换后的线（霍夫变换）
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img_copy, (x1, y1), (x2, y2), color=[255, 0, 0], thickness=6)  # 将线段绘制在img上

    # 拟合左右车道线方程
    draw_lines(img_copy, lines, color=[255, 0, 0], thickness=6)
    return img_copy
