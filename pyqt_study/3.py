import sys
from PyQt5.QtWidgets import QApplication, QWidget


class Exam(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):


app=QApplication(sys.argv)
window=Exam()
window.show()
sys.exit(app.exec_())
