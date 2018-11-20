import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic #ui 불러오는 모듈
#from pyqt_basic_ui import Ui_MainWindow  # pyqt_basic_ui.py 의 클래스를 호출!

form_class=uic.loadUiType('./lib/StopWatch.ui')[0] #이렇게 호출하면 ui 불러오는건데 알필요x


class TestForm(QMainWindow, form_class): #TestForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ =="__main__": #basic.3py main 함수를 킨다면 이란 의미임 if문이있으니까 basic_3 자체가 main이 되서 들어가는거임 다른프로그램에서 호출시 이게 안되는거!!
    app = QApplication(sys.argv)
    window = TestForm()
    window.show()
    app.exec_()
