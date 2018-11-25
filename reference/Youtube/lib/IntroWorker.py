from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtMultimedia import QSound

class IntroWorker(QObject): ###Pyqt에서는 별도의 쓰레드를 사용할때 qobject를 상속받아 사용한대
    startMsg = pyqtSignal(str,str)
    @pyqtSlot()
    def playBgm(self):
        self.intro = QSound("C:/Users/c8964/Desktop/webcrowling/Section6/resource/intro.wav") # 인스턴스화
        self.intro.play()
        self.startMsg.emit("Anonymous", self.intro.fileName()) #메인에서 introworker 쓰레드 실행될때 실행된거 알려준다.
