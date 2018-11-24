import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu
from PyQt5.QtCore import QCoreApplication


class Exam(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusBar()  #상태창 생성 - 한번더 호출하게되면 상태표시줄 객체를 받아오는형태
        self.statusBar().showMessage("안녕하세요")

        menu=self.menuBar()                 #메뉴 생성
        menu_file = menu.addMenu('File')    #그룹 생성
        menu_edit = menu.addMenu('Edit')    #그룹 생성

        file_exit= QAction('Exit',self)     #메뉴 객체 생성, 아직 메뉴에 추가는 안함
        file_exit.setShortcut('ctrl+Q')     #단축키 설정
        file_exit.setStatusTip("누르면 종료")

        file_exit.triggered.connect(QCoreApplication.instance().quit) #슬록생성



        new_txt = QAction("텍스트 파일",self)
        new_py = QAction("vkdlTjs 파일",self)

        file_new = QMenu('New',self)  #Qaction으로하면 클릭하면 어떤 액션을 만드는거고 QMenu로 하면 하위선택 가능한 또다른 메뉴만드는거 #서브그룹

        file_new.addAction(new_txt)
        file_new.addAction((new_py))

        menu_file.addMenu(file_new)
        menu_file.addAction(file_exit)  #메뉴에 추가 등록함



        self.resize(450,400)


app=QApplication(sys.argv)
window=Exam()
window.show()
sys.exit(app.exec_())
