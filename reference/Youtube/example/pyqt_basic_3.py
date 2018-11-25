import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore

# Qmainwindow는 QTabWidget 안에 있음
class TestForm(QMainWindow):
    def __init__(self):
        super().__init__() #부모 도 같이 초기화
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("PyQT Test") #window title 변경
        self.setGeometry(800,400,500,500) #앞의 두개는 모니터 xy축에서 시작하란거 뒤에 두개는 길이높이

        label_1 = QLabel("입력테스트",self) #str 띄우는거임
        label_2 = QLabel("출력테스트",self)

        label_1.move(20,20)
        label_2.move(20,60)

##########EDIT box 하는방법 가져오기##########
        self.lineEdit = QLineEdit("기본setting값",self) #Default 값 26분부터 다시봐봐 입력된 값이 다른데서 참조할거아냐? 그래서 self붙인 (강의 26:30)바바

        self.plainEdit = QtWidgets.QPlainTextEdit(self)
        #self.plainEdit.setReadOnly(True) #이렇게하면 쓰기안되는 박스만생성

        self.lineEdit.move(150,20)
        self.plainEdit.setGeometry(QtCore.QRect(20,90,361,231)) #규모가 커서 setGeometry 가 존재 Qplaintextedit뿐만아니라 qlineedit도 존재한다 22,24번째줄 같이보면됨

        self.lineEdit.textChanged.connect(self.lineEditChanged) # text가 체인지되면 시그널 발생시킨다 어떤시그널이냐면 lineEditChanged 이건 내가 새로 함수로 정의를 내리면됨
        self.lineEdit.returnPressed.connect(self.LineEditEnter) # returnpressed 즉, 엔터 쳣을때 시그널 발생시킨다


        #상태바를 붙여줘야지 된다 (status의 상태바) --> 창에는 보이지않음 이걸 어떻게 사용하는진 좀더지켜봐
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def lineEditChanged(self):
        self.statusBar.showMessage(self.lineEdit.text())
        ###개중요 십중요!!! 이거때문에 죄다 self. 붙이는거임 self 안붙였으면 lineEdit 불러와봣자 저장 된거없음 생각해보자
        ### self가 없엇다면 지역변수기때문에 다른함수로 넘어오면서

    def LineEditEnter(self):
        a=self.lineEdit.text()
        print(a)
        b=a.split()
        b.append('x')
        self.plainEdit.appendPlainText('name:'+b[0]+' '+'phone:'+b[1]) # 엔터치는 그순간의 lineEdit의 text를 plainEdit박스 안에다 출력시켜라 참고로 append는 줄바꿈인데
        ###insertPlainText는 줄바꿈없음
        self.lineEdit.clear()

if __name__ =="__main__": #basic.3py main 함수를 킨다면 이란 의미임 if문이있으니까 basic_3 자체가 main이 되서 들어가는거임 다른프로그램에서 호출시 이게 안되는거!!
    app = QApplication(sys.argv)
    window = TestForm()
    window.show()




    app.exec_()
