import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox #메시지박스 띄우는것
from PyQt5.QtCore import QCoreApplication #여기서 특정 이벤트를 관장하는 메서드.


class Exam(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn=QPushButton("push me!", self)
        btn.resize(btn.sizeHint())
        btn.move(50,50)
        btn.clicked.connect(QCoreApplication.instance().quit) #프로그램 종료-버튼누르면 종료

        self.resize(500,500)
        self.setWindowTitle('wow nice') #창 title: 이거만 해줘도 대충 가운데 띄워준대

    def closeEvent(self, QCloseEvent): #창 x 버튼 누를때 발생시키는거

        ans = QMessageBox.question(self,"종료확인","종료하시겠습니까?",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if ans ==QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.


app=QApplication(sys.argv)
window=Exam()
window.show()
sys.exit(app.exec_())
