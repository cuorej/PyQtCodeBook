import sys
import sip
import time
from enum import Enum
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QMessageBox,
                             QPushButton, QDesktopWidget, QMainWindow, qApp,
                             QAction, QVBoxLayout, QLCDNumber, QTableWidget,
                             QTableWidgetItem)
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon

class Human( ):
    '''인간'''
    def __init__( self, name, weight ):
        '''초기화 함수'''
        self.name = name
        self.weight = weight

    def __str__( self ):
        '''문자열화 함수'''
        return "{} ( 몸무게 {}kg )".format( self.name, self.weight )

    def __len__(self):
        return len(self.__str__())

person=Human("최형준",60)
print(person)
print(len(person))

timer=QTimer()
print(timer)