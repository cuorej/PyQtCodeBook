#!/usr/bin/python3

from PyQt5.QtCore import QDate, QTime, QDateTime, Qt

now = QDate.currentDate()

print(now.toString(Qt.ISODate))
print(now.toString(Qt.DefaultLocaleLongDate))

datetime = QDateTime.currentDateTime()
print(datetime.toString())
time = QTime.currentTime()

print(time.toString(Qt.DefaultLocaleLongDate))

print("Local datetime: ", now.toString(Qt.ISODate))
print("Universal datetime: ", datetime.toUTC().toString(Qt.ISODate))
print("The offset from UTC is: {0} seconds".format(datetime.offsetFromUtc()))


class timer(object):
    """Times stuff."""

    def __init__(self):
        self.splits = []
        self.start = 0

    def begin_timer(self):
        self.start = time.time()

    def current_time(self):
        now = time.time() - self.start()
        return now

    def add_split(self):
        now = self.current_time()
        self.splits.append(now)
