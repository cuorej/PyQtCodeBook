import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * #QTimer
from PyQt5 import uic #ui 불러오는 모듈
#from pyqt_basic_ui import Ui_MainWindow  # pyqt_basic_ui.py 의 클래스를 호출!

form_class=uic.loadUiType('./lib/timer.ui')[0] #이렇게 호출하면 ui 불러오는건데 알필요x


class TestForm(QMainWindow, form_class): #TestForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initSignal()




    def initSignal(self):

        self.startButton.clicked.connect(self.timeStart)
        self.stopButton.clicked.connect(self.timeStop)
        self.resetButton.clicked.connect(self.timeReset)

        self.timer=QTimer()
        self.timer.timeout.connect(self.tChk)


    @pyqtSlot()
    def timeStart(self):
        self.timer = QTimer(self)
        self.timer.start(1000)

if __name__ =="__main__":
    app = QApplication(sys.argv)
    window = TestForm()
    window.show()
    app.exec_()
