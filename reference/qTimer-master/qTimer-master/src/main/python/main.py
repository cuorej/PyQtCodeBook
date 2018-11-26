#!/usr/bin/python3

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


class TimerState(Enum):
    ACTIVE = 1
    INACTIVE = 2
    PAUSED = 3


class FormattedTime(object):
    def __init__(self, minutes, seconds, centiseconds):
        self.minutes = minutes
        self.seconds = seconds
        self.centiseconds = centiseconds
        self.begin = time.time()  #time.time()은 현재 utc기준 초 반환
        self.paused_begin = 0

    def increment_time(self):
        delta = int((time.time() - self.begin) * 100)
        if self.paused_begin != 0:
            paused_delta = time.time() - self.paused_begin
            self.begin += paused_delta
            self.paused_begin = 0

        self.minutes = int(delta / 6000)
        delta -= self.minutes * 6000
        self.seconds = int(delta / 100)
        delta -= self.seconds * 100
        self.centiseconds = delta

    def pause(self):
        self.paused_begin = time.time()

    def __str__(self): #문자열화 함수. 나중에 a=FormattedTime() 으로 객체화 했을때 print(a)시 return문 반환
        return "{0:02d}:{1:02d}:{2:02d}".format(self.minutes, self.seconds,
                                                self.centiseconds)  #02d 는 0을 포함해서 2자씩 int형으로 반환한단소리

    def __len__(self):   #객체의 길이를 반환.
        return len(self.__str__())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.formatted_time = FormattedTime(0, 0, 0)
        self.state = TimerState.INACTIVE
        self.splits = []
        self.init_menus()
        self.init_UI()

    def init_menus(self):

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        fileMenu.addAction(exitAct)

        viewMenu = menubar.addMenu('View')

        viewStatAct = QAction('View statusbar', self, checkable=True)
        viewStatAct.setStatusTip('View statusbar')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.toggle_menu)

        viewMenu.addAction(viewStatAct)

    def init_UI(self):

        wid = QWidget(self)
        self.setCentralWidget(wid)

        QToolTip.setFont(QFont('SansSerif', 10))

        # ---

        self.start_stop_button = QPushButton('Start')
        self.start_stop_button.clicked.connect(self.start_stop)

        # ---

        self.pause_button = QPushButton('Pause')
        self.pause_button.resize(self.pause_button.sizeHint())
        self.pause_button.clicked.connect(self.pause_timer)
        self.pause_button.setEnabled(False)

        # ---

        self.split_button = QPushButton("Split")
        self.split_button.clicked.connect(self.split)
        self.split_button.setEnabled(False)

        # ---

        self.lcd = QLCDNumber(self)
        self.lcd.setMinimumSize(QSize(150, 150))
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.setDigitCount(len(str(self.formatted_time)))
        self.lcd.display(str(self.formatted_time))


        # ---

        self.splits_table = QTableWidget()
        self.splits_table.setMinimumSize(QSize(150, 200))
        self.splits_table.setRowCount(len(self.splits))
        self.splits_table.setColumnCount(1)
        self.splits_table.setShowGrid(False)
        self.splits_table.verticalHeader().setDefaultSectionSize(20)
        self.splits_table.verticalHeader().setVisible(False)
        self.splits_table.horizontalHeader().setVisible(False)
        self.update_splits_table()

        # ---

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.lcd)
        vbox.addWidget(self.splits_table)
        vbox.addWidget(self.start_stop_button)
        vbox.addWidget(self.pause_button)
        vbox.addWidget(self.split_button)

        wid.setLayout(vbox)

        # ---

        self.statusBar().showMessage("")
        self.setGeometry(350, 300, 350, 150)
        self.setWindowTitle('Timer')
        self.setWindowIcon(QIcon('web.png'))

        self.show()

    def start_stop(self):
        if self.state == TimerState.ACTIVE:
            self.state = TimerState.INACTIVE
            self.timer.stop()
            self.sender().setText("Start")
            self.split_button.setEnabled(False)
            self.pause_button.setEnabled(False)
            self.statusBar().showMessage("Timer stopped!")
        elif self.state == TimerState.INACTIVE:
            self.state = TimerState.ACTIVE
            self.reset_timer()
            self.begin_timer()
            self.sender().setText("Stop")
            self.split_button.setEnabled(True)
            self.pause_button.setEnabled(True)
            self.statusBar().showMessage("Timer started!")
        elif self.state == TimerState.PAUSED:
            self.sender().setText("Stop")
            self.state = TimerState.ACTIVE
            self.pause_button.setEnabled(True)
            self.split_button.setEnabled(True)
            self.begin_timer()

    def pause_timer(self):
        self.statusBar().showMessage("Paused!")
        self.start_stop_button.setText("Start")
        self.formatted_time.pause()
        self.pause_button.setEnabled(False)
        self.state = TimerState.PAUSED
        self.timer.stop()

    def split(self):
        now = FormattedTime(self.formatted_time.minutes,
                            self.formatted_time.seconds,
                            self.formatted_time.centiseconds)

        self.splits.append(now)
        self.update_splits_table()

    def update_current_time(self):
        self.formatted_time.increment_time()
        self.lcd.setDigitCount(len(self.formatted_time))
        self.lcd.display(str(self.formatted_time))

    def begin_timer(self):
        self.timer.start(10)
        self.timer.timeout.connect(self.update_current_time)

    def update_splits_table(self):
        row = 0
        for split in self.splits:
            self.item = QTableWidgetItem(str(split))
            self.splits_table.setRowCount(len(self.splits))
            self.splits_table.setItem(row, 0, self.item)
            row = row + 1
        pass

    def reset_timer(self):
        self.splits = []
        self.splits_table.clear()
        self.formatted_time = FormattedTime(0, 0, 0)

    def quit_app(self):
        sys.exit()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.statusBar().showMessage('Moved!')

    def toggle_menu(self, state):
        if state:
            self.statusBar().show()
        else:
            self.statusBar().hide()

    def closeEvent(self, event):

        if self.state == TimerState.ACTIVE or self.state == TimerState.PAUSED:
            reply = QMessageBox.question(
                self, 'Message',
                "Timer running. Are you sure you want to quit?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            event.accept() if reply == QMessageBox.Yes else event.ignore()
        else:
            event.accept()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Space:
            if self.state == TimerState.INACTIVE:
                self.start_stop()
            else:
                self.pause_timer()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(
        "QLCDNumber{color:rgb(255, 255, 255); background-color:rgb(0, 0, 0);} \
        QTableWidget{color:rgb(0, 0, 0)}")
    ex = MainWindow()
    sys.exit(app.exec_())
