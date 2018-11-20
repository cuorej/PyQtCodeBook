import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton #무조건 불러와야 하는것들

class Exam(QWidget): #Qwidget을 상속
    def __init__(self):
        super().__init__() #상위 즉 Qwidget의 객체를 생성하고 상위객체에 해당하는 생성자를 호출
        self.initUI()

    def initUI(self):
        btn=QPushButton('abc', self)
        btn.resize(btn.sizeHint()) #적당히 글씨크기로 맞춘다.
        btn.move(20,30) #위치이동
        btn.setToolTip("툴팁입니다.<b>안녕하세요.<b/>") #마우스 갖다대고 기다리면 툴팁띄우는거-html 문법사용가능

        #창크기조절
        self.setGeometry(300,300,400,500) #300,300 지점에 창을 띄우고 가로세로 400 500
        self.setWindowTitle('첫 번째 학습시간') #Title 정하기.





app=QApplication(sys.argv)
window=Exam()
window.show()
sys.exit(app.exec_()) #Main Loop가 끝나는순간 sys.exit가 실행되서 깔끔하게 종료
