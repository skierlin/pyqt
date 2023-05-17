# coding:utf-8
# 可自己在run（）进行修改，得到自己想要的函数

import cv2
from PyQt5.QtCore import QThread, pyqtSignal
import time
import numpy as np
from detect_def_1 import detection_line_1  # 初级车道线检测函数
from detect_def_2 import detection_line_2, getCameraCalibrationCoefficients  # 高级车道线检测函数


class CounterThread(QThread):
    sin_Result = pyqtSignal(np.ndarray)
    sin_runningFlag = pyqtSignal(int)
    sin_videoList = pyqtSignal(list)
    sin_done = pyqtSignal(int)
    sin_pauseFlag = pyqtSignal(int)

    def __init__(self):
        super(CounterThread, self).__init__()

        self.running_flag = 0
        self.pause_flag = 0
        self.videoList = []

        self.sin_runningFlag.connect(self.update_flag)
        self.sin_videoList.connect(self.update_videoList)
        self.sin_pauseFlag.connect(self.update_pauseFlag)

        # 高级车道线检测函数调用
        self.nx = 9
        self.ny = 6
        self.rets, self.mtx, self.dist, self.rvecs, self.tvecs = getCameraCalibrationCoefficients('camera_cal/calibration*.jpg', self.nx, self.ny)

    def run(self):
        for video in self.videoList:
            cap = cv2.VideoCapture(video)
            frame_count = 0
            while cap.isOpened():
                if self.running_flag:
                    if not self.pause_flag:
                        ret, frame = cap.read()
                        if ret:
                            if frame_count % 1 == 0:
                                a1 = time.time()

                                # 初级车道线检测函数
                                # frame = detection_line_1(frame)

                                # 高级级车道线检测函数
                                frame = detection_line_2(frame, self.mtx, self.dist)

                                self.sin_Result.emit(frame)
                                # out.write(frame)
                                a2 = time.time()
                                # a2与a1差值太小也报错
                                # print(f"fps: {1 / (a2 - a1):.2f}")  # 代码运行帧率
                            frame_count += 1
                        else:
                            break
                    else:
                        time.sleep(0.1)
                else:
                    break

            cap.release()
            # out.release()

            if not self.running_flag:
                break

        if self.running_flag:
            self.sin_done.emit(1)

    def update_pauseFlag(self, flag):
        self.pause_flag = flag

    def update_flag(self, flag):
        self.running_flag = flag

    def update_videoList(self, videoList):
        print("Update videoList!")
        self.videoList = videoList








