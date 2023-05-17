import cv2
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from gui import *
from counter import CounterThread


class App(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.setupUi(self)
        self.label_image_size = (self.label_image.geometry().width(), self.label_image.geometry().height())
        self.video = None

        # button function
        self.pushButton_openVideo.clicked.connect(self.open_video)
        self.pushButton_start.clicked.connect(self.start_stop)
        self.pushButton_pause.clicked.connect(self.pause)
        self.pushButton_start.setEnabled(False)
        self.pushButton_pause.setEnabled(False)

        # some flags
        self.running_flag = 0
        self.pause_flag = 0
        self.lance_switch = 0
        self.car_switch = 0

        #
        self.counterThread = CounterThread()
        self.counterThread.sin_Result.connect(self.show_image_label)

    # 打开视频文件
    def open_video(self):
        openfile_name = QFileDialog.getOpenFileName(self, 'Open video', '', 'Video files(*.avi , *.mp4)')
        self.videoList = [openfile_name[0]]
        vid = cv2.VideoCapture(self.videoList[0])

        # 只显示，不进行视频播放
        while vid.isOpened():
            ret, frame = vid.read()
            if ret:
                self.show_image_label(frame)
                vid.release()
                break

        # 启动Start和Pause按键
        self.pushButton_start.setText("Start")
        self.pushButton_start.setEnabled(True)
        self.pushButton_pause.setText("Pause")
        self.pushButton_pause.setEnabled(True)

    # 开始播放与停止按键
    def start_stop(self):
        # 播放
        if self.running_flag == 0:
            # start
            self.running_flag = 1
            self.pause_flag = 0
            self.pushButton_start.setText("Stop")
            self.pushButton_openVideo.setEnabled(False)

            # emit new parameter to counter thread
            self.counterThread.sin_runningFlag.emit(self.running_flag)
            self.counterThread.sin_videoList.emit(self.videoList)
            # start counter thread
            self.counterThread.start()
            self.pushButton_pause.setEnabled(True)

        # 停止
        elif self.running_flag == 1:  # push pause button
            # stop system
            self.running_flag = 0
            self.counterThread.sin_runningFlag.emit(self.running_flag)
            self.pushButton_openVideo.setEnabled(True)
            self.pushButton_start.setText("Start")

    # 暂停播放与继续按键
    def pause(self):
        if self.pause_flag == 0:
            self.pause_flag = 1
            self.pushButton_pause.setText("Continue")
            self.pushButton_start.setEnabled(False)

        else:
            self.pause_flag = 0
            self.pushButton_pause.setText("Pause")
            self.pushButton_start.setEnabled(True)

        self.counterThread.sin_pauseFlag.emit(self.pause_flag)

    # 画面显示
    def show_image_label(self, img_np):
        img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        img_np = cv2.resize(img_np, self.label_image_size)
        frame = QImage(img_np, self.label_image_size[0], self.label_image_size[1], QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.label_image.setPixmap(pix)
        self.label_image.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = App()
    myWin.show()
    sys.exit(app.exec_())


