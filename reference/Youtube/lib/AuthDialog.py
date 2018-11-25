import sys
from PyQt5.QtWidgets import *

class AuthDialog(QDialog): #QDialog 상속
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.user_id =None  #변수 선언 : 왜냐면 다른데서 참조하려고 self가 있어야 스코프가 맞아서 다른데서 쓸수잇다.
        self.user_pw =None

    def setupUI(self): #ui 쓰지말고 직접짜보자~
        self.setGeometry(300,900,300,100)
        self.setWindowTitle("Sign In")
        self.setFixedSize(300,100)

        label1=QLabel('Id:')
        label2=QLabel("Password:")

        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QLineEdit() ## 비밀번호
        self.lineEdit2.setEchoMode(QLineEdit().Password) #password 부분 ***표시하는 공식(그냥암기해)

        self.pushButton = QPushButton("로그인")
        self.pushButton.clicked.connect(self.submitLogin) #시그널 연결 아래 def submitLogin 바바

        layout=QGridLayout() # 바둑판식 배열로 자동으로 이쁘게 해줌
        layout.addWidget(label1,0,0) # 0,0 은 1행 1열
        layout.addWidget(self.lineEdit1,0,1)
        layout.addWidget(self.pushButton,0,2)

        layout.addWidget(label2,1,0)
        layout.addWidget(self.lineEdit2,1,1)

        self.setLayout(layout)

    def submitLogin(self):
        self.user_id = self.lineEdit1.text()  #아이디 치면 변수 self.user_id에 저장
        self.user_pw = self.lineEdit2.text()  #비번 치면 변수 self.user_pw에 저장
        #print(self.user_pw)

        ###아이디 안치거나 비어있으면 인증오류 띄우는문
        if self.user_id is None or self.user_id == '' or not self.user_id: #selfuserid 있으면 not에 걸려 통과
            QMessageBox.about(self,"인증오류","ID를 입력해주세요")
            self.lineEdit1.setFocus(True) # focus를 주어 아이디 없을때 커서가 다시 아이디 창에 가있도록 하는것.
            return None # 이게없으면 이 함수의 self.close()로 빠져나가 무한루프에서 빠져나가버림
        if self.user_pw is None or self.user_pw == '' or not self.user_pw: #selfuserid 있으면 not에 걸려 통과
            QMessageBox.about(self,"인증오류","pw를 입력해주세요")
            self.lineEdit2.setFocus(True)
            return None

        # 이 부분에서 필요한 경우 실제 로컬 DB 또는 서버 연동 후
        # 유저 정보 및 사용 유효기간을 체크하는 코드를 넣어주세요.
        # code
        # code-하지만 이건 main.py 에서 구현하느게 낫다. 왜냐면 여기는 딱 로그인하는 부분에 대한 py이므로 더 객체지향형

        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loginDialog = AuthDialog()
    loginDialog.show()
    app.exec_()
