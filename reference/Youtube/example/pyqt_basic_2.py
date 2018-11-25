import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * #종료시키고 그런 함수 관장 25번째줄을위함

# Qmainwindow는 QTabWidget 안에 있음
class TestForm(QMainWindow): #QMainWindow를 상속받아온다. Qmainwindow는 위젯보다 좀더 사용자를위해 메뉴판, 상태줄 등을 추가된 윈도우창입니다.
    def __init__(self):
        super().__init__() #부모 도 같이 초기화
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("PyQT Test") #window title 변경
        self.setGeometry(800,400,500,300) #앞의 두개는 모니터 xy축에서 시작하란거 뒤에 두개는 길이높이

        btn_1 = QPushButton("Click1", self) #클릭가능한 버튼 띄운거임
        btn_2 = QPushButton("Click2", self)
        btn_3 = QPushButton("Click3", self)

        btn_1.move(20,20)  # 시작하는 x축, y축
        btn_2.move(20,60)
        btn_3.move(20,100)

        btn_1.clicked.connect(self.btn_1_cliked) # click을해서 signal 발생시 btn_1_cliked란 slot과 연결시키겟다.
        btn_2.clicked.connect(self.btn_2_cliked)
        btn_3.clicked.connect(QCoreApplication.instance().quit) #이미 만들어논 함수를 호출해서 연결시켜준거. 창종료 기능임 이게 Qtcore 함수안에있네
        ##instance 가져와서 quit시키란 의미
        #시그널: 발생 슬롯:처리

'''
PyQt: 대기상태
시그널: 이벤트 ex 버튼을 클릭했다!
SLOT: 이벤트를 처리
'''


    def btn_1_cliked(self):
        QMessageBox.about(self,"message","clicked")


    def btn_2_cliked(self):
        print("Button Cliked!")

if __name__ =="__main__": #basic.2py main 함수를 킨다면 이란 의미임
    app = QApplication(sys.argv)


    window = TestForm()
    window.show()




    app.exec_()
