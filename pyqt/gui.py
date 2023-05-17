# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1203, 554)

        # 窗口部件，在mainWindow叠加矩形子窗口（后一个可以遮挡前一个）
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 实现加载图片,在主函数中调用
        self.label_image = QtWidgets.QLabel(self.centralwidget)
        self.label_image.setGeometry(QtCore.QRect(10, 10, 960, 540))  # QtCore.QRect（左上角的点、宽和高）
        self.label_image.setStyleSheet("background-color: rgb(233, 185, 110);")
        self.label_image.setText("")

        # 自己添加的一个新窗口，可以自定义贴图
        # pix = QPixmap('2.jpg')
        # scaredPixmap = pix.scaled(185, 300, QtCore.Qt.KeepAspectRatio)  # 调整大小
        # self.label_image_0 = QtWidgets.QLabel(self.centralwidget)
        # self.label_image_0.setGeometry(QtCore.QRect(1000, 45, 185, 250))  # QtCore.QRect（左上角的点、宽和高）
        # self.label_image_0.setStyleSheet("background-color: rgb(255, 255, 255);")  # 白色背景
        # self.label_image_0.setPixmap(scaredPixmap)

        # 对齐方式：居中
        self.label_image.setAlignment(QtCore.Qt.AlignCenter)
        self.label_image.setObjectName("label_image")

        # 在self.centralwidget窗口上叠加新的子窗口self.widget
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(1020, 360, 151, 181))
        self.widget.setObjectName("widget")

        # QVBoxLayout可以在垂直方向上排列控件
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # 设置按键openVideo
        self.pushButton_openVideo = QtWidgets.QPushButton(self.widget)
        self.pushButton_openVideo.setObjectName("pushButton_openVideo")
        self.verticalLayout.addWidget(self.pushButton_openVideo)

        # 设置按键start
        self.pushButton_start = QtWidgets.QPushButton(self.widget)
        self.pushButton_start.setObjectName("pushButton_start")
        self.verticalLayout.addWidget(self.pushButton_start)

        # 设置按键pause
        self.pushButton_pause = QtWidgets.QPushButton(self.widget)
        self.pushButton_pause.setObjectName("pushButton_pause")
        self.verticalLayout.addWidget(self.pushButton_pause)

        mainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Detection of Lane"))
        self.pushButton_openVideo.setText(_translate("mainWindow", "Open Video"))
        self.pushButton_start.setText(_translate("mainWindow", "Start"))
        self.pushButton_pause.setText(_translate("mainWindow", "Pause"))
