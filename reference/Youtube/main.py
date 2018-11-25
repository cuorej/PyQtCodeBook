import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QUrl, QThread ##initSignal 로그인부분 함수 처리하기위해 한것이다.
from PyQt5 import uic
from PyQt5 import QtGui
from lib.YouViewerLayout import Ui_MainWindow
from lib.AuthDialog import AuthDialog #파일의 AuthDialog 가져와~
from lib.IntroWorker import IntroWorker

import re
import datetime
import pytube
from PyQt5.QtMultimedia import QSound

#form_class = uic.loadUiType("C:/Users/c8964/Desktop/webcrowling/Section6/ui/you_viewer_v1.0.ui")[0]

class Main(QMainWindow, Ui_MainWindow):
#Qmainwindow를 상송받고, Ui_MainWindow 경로 가져와
    def __init__(self):
        super().__init__()

        #초기화
        self.setupUi(self)

        #초기잠금
        self.initAuthLock() #인증안누르면 잠금 안풀리는거 --당근 함수로 넘어가면됨

        #시그널 초기화
        self.initSignal()

        #로그인 관련 전역변수 선언
        self.user_id = None
        self.user_pw = None
        #재생 여부 flag 전역번수 만들기
        self.is_play = False #처음엔 상영중이 아닐태니 아님

        #Youtube 관련작업 변수 지정
        self.youtb = None
        self.youtb_fsize = 0

        #배경음악 Thread 작업 선언
        #vvvQthread 사용 안할경우
        #QSound.play("C:/Users/c8964/Desktop/webcrowling/Section6/resource/intro.wav")  #--> 이렇게하면 메인쓰레드 걸리면 노래가 멈춤 따라서 쓰레드 필요
        self.initIntroThread()


##기본 UI 비활성화
    def initAuthLock(self): #잠금에대한 함수를 여기다 짜주면돼
        self.previewButton.setEnabled(False) # 위에보면 Ui_MainWindow 상속받았기 때문에 가능하다. setenable이 false이므로 잠금이 걸려있다.
        self.fileNavButton.setEnabled(False)
        self.streamCombobox.setEnabled(False)
        self.startButton.setEnabled(False)
        self.calendarWidget.setEnabled(False)
        self.urlTextEdit.setEnabled(False)
        self.pathTextEdit.setEnabled(False)
        self.showStatusMsg('인증안됨') #이거에대한것도 함수로 아래만들어주겟지
##기본 UI 활성화
    def initAuthActive(self):
        self.previewButton.setEnabled(True)
        self.fileNavButton.setEnabled(True)
        self.streamCombobox.setEnabled(True)
        ##self.startButton.7setEnabled(True) 시작버튼이므로 얘는 우선 빼자 왜냐면 뭐 url 넣어야 시작이 활성화되는게 나으니까!
        self.calendarWidget.setEnabled(True)
        self.urlTextEdit.setEnabled(True)
        self.pathTextEdit.setEnabled(True)
        self.showStatusMsg('인증완료')

    def showStatusMsg(self,msg):    ##status 상태 보여주는거
        self.statusbar.showMessage(msg)

    #시그널 초기화
    def initSignal(self):
        self.loginButton.clicked.connect(self.authCheck)
        self.previewButton.clicked.connect(self.load_url) #확인버튼 누르면 url 띄우는 시그널 만들어보자
        self.exitButton.clicked.connect(QtCore.QCoreApplication.instance().quit) #종료버튼 누르면 꺼지는거
        self.webEngineView.loadProgress.connect(self.showProgressBrowserLoading)
        self.fileNavButton.clicked.connect(self.selectDownPath)
        self.calendarWidget.clicked.connect(self.append_date)
        self.startButton.clicked.connect(self.downloadYoutb)

    #인트로 쓰레드 초기화 및 활성화
    def initIntroThread(self):
        #worker 선언
        self.introObj = IntroWorker() #인스턴스화
        #Qthread 선언
        self.introThread = QThread() #pyqt5에서 제공하는 qthread를 인스턴스화

        #우리가 만든 IntroWorker를 Thread로 전환
        self.introObj.moveToThread(self.introThread) #moveToThread는 Introworker의 Qobject 에 있고 그렇기 때문에 IntroWorker에서 qobject 상속받음

        #시그널 연결-이부분은 안만들어도되는데 공부할겸 보여주는거(쓰레드와 통신)
        self.introObj.startMsg.connect(self.showIntroInfo)

        #Thread 시작 메소드 연결
        self.introThread.started.connect(self.introObj.playBgm)

        #Thread 스타트버튼
        self.introThread.start()

    #인트로 쓰레드 signal 발생
    def showIntroInfo(self, userName, fileName):
        self.plainTextEdit.appendPlainText("Program Started by : "+userName)
        self.plainTextEdit.appendPlainText("Playing intro information is : ")
        self.plainTextEdit.appendPlainText(fileName)



    @pyqtSlot() #이게 있으면 이 함수가 slot인걸 알려주는 알림문-외국 유명프로그램은 이거 다표기해놈-이게 있고 없고 차이가 좀있는데 나중에 언젠가 알게될거래..공부열심히하면 ㅠ
    def authCheck(self):
        dlg = AuthDialog()
        dlg.exec_() #누르면 새창으로 띄우는거
        self.user_id = dlg.user_id ##개씹중요... 클래스 강의 다시들으면서 생각해봐
        #내가 좀 정리해보자면.. AuthDialog에 self로 dlg 넘겻고 그로인해 저장된 변수 dlg.user_id가 여기 변수로 로딩된것.
        self.user_pw = dlg.user_pw

        # 이 부분에서 필요한 경우 실제 로컬 DB 또는 서버 연동 후
        # 유저 정보 및 사용 유효기간을 체크하는 코드를 넣어주세요.
        # code
        # code-하지만 이건 main.py 에서 구현하느게 낫다. 왜냐면 여기는 딱 로그인하는 부분에 대한 py이므로 더 객체지향형
        #print('id: %s pw: %s' %(self.user_id,self.user_pw)) 이걸로 확인해보면됨

        if True:
            self.initAuthActive()
            self.loginButton.setText("인증완료")
            self.loginButton.setEnabled(False) #로그인박스 누르고나면 인증완료로 바꾸고 디스에이블
            self.urlTextEdit.setFocus(True)
            self.append_log_msg("login Success")
        else:
            QMessageBox.about(self, "인증오류", "아이디 또는 비밀번호 인증 오류") #두번재칸은 메세지창의 타이틀 세번쩨칸은 내용

    def load_url(self):
        url = self.urlTextEdit.text().strip()
        v=re.compile('^https://www.youtube.com/?')
        if self.is_play:          #재생눌러서 영상중일때 is_play =True되고 그상태에서 stop 만들어줘야함 누르면 아래것들 실행된단소리
            self.append_log_msg('Stop Click')
            self.webEngineView.load(QUrl("about:blank"))
            self.previewButton.setText("재생")
            self.is_play=False
            self.urlTextEdit.clear()
            self.urlTextEdit.setFocus(True)
            self.startButton.setEnabled(False)
            self.streamCombobox.clear()
            self.progressBar_2.setValue(0)
            self.showStatusMsg("인증완료")
        else:
            if v.match(url) is not None: #또 if쓰는이유는 유튜브 url이 아니라 다른거 쓸까 v정규식 과 matching 됫을때 none값이 아니면 정확히 매칭됫단소리
                self.append_log_msg('Play Click')
                self.webEngineView.load(QUrl(url))
                self.showStatusMsg(url+"재생 중")
                self.previewButton.setText("중지")
                self.is_play=True
                self.startButton.setEnabled(True) # 이제 스타트버튼 켜줘야지
                self.initialYouWork(url) #pytube 쓰는거 함수 쓰기

            else: #사용자가 이상한 주소 넣을경우
                QMessageBox.about(self, "URL 형식오류","Youtube 주소형식이 아닙니다.")
                self.urlTextEdit.clear()
                self.urlTextEdit.setFocus(True)

    def initialYouWork(self,url): #pytube 참조 section2
        video_list = pytube.YouTube(url)
        #로딩바 계산
        video_list.register_on_progress_callback(self.showProgressDownLoading) #pytube 고유 메서드임






        self.youtb = video_list.streams.all()
        self.streamCombobox.clear()
        for q in self.youtb:
            tmp_list, str_list = [], []
            tmp_list.append(str(q.mime_type or '')) #있으면 출력하고 없으면 공백
            tmp_list.append(str(q.res or ''))
            tmp_list.append(str(q.fps or ''))
            tmp_list.append(str(q.abr or ''))

            #print(tmp_list) #이렇게 출력하면 공백들 다 보임
            str_list = [x for x in tmp_list if x !=''] #tmp_list 순회하면서 공백이 아닌거만 넣어
            #print(str_list)
            #####콤보박스 넣어주자 이제 ####
            self.streamCombobox.addItem(','.join(str_list))
            ###########################






    def append_log_msg(self,act): # 공통으로 쓰기때문에 들여쓰기 한번나와야함
        now=datetime.datetime.now()
        nowDatetime = now.strftime("%Y-%m-%d %H:%M:%S")
        app_msg=self.user_id + ' : ' +act + ' -(' + nowDatetime+')'
        print(app_msg)
        self.plainTextEdit.appendPlainText(app_msg) #insertPlainText는 줄바꿈없음

        #활동 로그 저장(또는 DB를 사용 추천)
        with open('C:/Users/c8964/Desktop/webcrowling/Section6/log/log.txt','a') as f: #쓸때마다 누적이되니까 'w'가 아니라 'a'-append
            f.write(app_msg+'\n')

    @pyqtSlot(int)
    def showProgressBrowserLoading(self,v):
        self.progressBar.setValue(v)

    @pyqtSlot()
    def selectDownPath(self):
        #파일선택-경로선택이아니라 뭔가 열기위한 파일을 선택하는법
        #fname=QFileDialog.getOpenFileName(self)
        #self.pathTextEdit.setText(fname[0])

        #파일경로
        fpath=QFileDialog.getExistingDirectory(self,'Select Directory')
        self.pathTextEdit.setText(fpath)


    @pyqtSlot() #달력을 쓰는법
    def append_date(self):
        cur_date=self.calendarWidget.selectedDate()
        #print('click date',self.calendarWidget.selectedDate().toString())
        #print('cur_date',cur_date)
        print(str(cur_date.year())+'-'+str(cur_date.month())+'-'+str(cur_date.day()))
        self.append_log_msg('Calendar Click')

    @pyqtSlot()
    def downloadYoutb(self):
        down_dir = self.pathTextEdit.text().strip() #text로 가져와서 공백제거
        if down_dir is None or down_dir == '' or not down_dir:
            QMessageBox.about(self,'경로선택', '다운로드 받을 경로를 선택하세요.') ##경로선택은 툴팁, 세번째거가 메인 텍스트문
            return None

        self.youtb_fsize = self.youtb[self.streamCombobox.currentIndex()].filesize #파일사이즈 인텍스
        print('fsize', self.youtb_fsize)
        self.youtb[self.streamCombobox.currentIndex()].download(down_dir)
        self.append_log_msg('Download Click')

#다운로드 로딩바 계산 100 -> 90 80 70 - - - - 10 0
    def showProgressDownLoading(self, stream, chunk, finle_handle, bytes_remaining):
        print(int(self.youtb_fsize - bytes_remaining))
        print('bytes_remaining',bytes_remaining)
        self.progressBar_2.setValue(int(((self.youtb_fsize - bytes_remaining) / self.youtb_fsize)*100))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    you_viewer_main = Main()
    you_viewer_main.show()
    app.exec_()

#32분임
