import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

class Exam(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setGeometry(0, 0, 500, 520)
        self.setWindowTitle('타임벨 테스트')

        self.lbl





app=QApplication(sys.argv)
window=Exam()
window.show()
sys.exit(app.exec_())
