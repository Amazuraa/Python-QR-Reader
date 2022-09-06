from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QAction, QToolBar, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPixmap

from PIL import ImageGrab
# from enum import Enum
# from pathlib import Path

import sys
import tkinter as tk
import numpy as np
import cv2
# import asyncio
import webbrowser
# import os
# import shutil

_global_mode = ""


# -- UIs --
class OutputWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None

        self.central_widget = QWidget()               
        self.setCentralWidget(self.central_widget)    
        lay = QVBoxLayout(self.central_widget)

        img_name = imgModeName()
        img_path = img_name
        label = QLabel(self)
        pixmap = QPixmap(img_path)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())

        lay.addWidget(label)

        toolbar = QToolBar("Main toolbar")
        self.addToolBar(toolbar)

        button_action = QAction("New", self)
        button_action.triggered.connect(self.toggle_window)
        toolbar.addAction(button_action)

        t_name = "Scan"
        button_action = QAction(t_name, self)
        button_action.triggered.connect(self.output_action)
        toolbar.addAction(button_action)

    def toggle_window(self):
        if self.w is None:
            self.w = MyWidget(_global_mode)
        self.w.show()
        self.hide()

    def output_action(self):
        executeMode()
        pass

class MyWidget(QtWidgets.QWidget):
    def __init__(self, mode):
        super().__init__()
        self.w = None

        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)

        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.mode = mode
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print('Capturing Image...')
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        img_name = imgModeName()
        img_path = img_name
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save(img_path)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

        self.toggle_window()

    def toggle_window(self):
        self.w = OutputWindow()
        self.w.show()



# -- Controls --
def snipp(mode:str):
    global _global_mode
    _global_mode = mode

    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget(mode)
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())

def executeMode():
    img_path = 'qr_capture.jpg'
    img = cv2.imread(img_path)
    det = cv2.QRCodeDetector()
    res, points, _ = det.detectAndDecode(img)

    webbrowser.register('chrome',
                        None,
                        webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
    webbrowser.open_new_tab(res)
    print(res)
    print("XXX")

def imgModeName():
    img_name = "qr_capture.jpg"
    return img_name

snipp('qr')