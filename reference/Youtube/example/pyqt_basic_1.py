import sys
from PyQt5.QtWidgets import *   #QTwidget모듈에는 GUI 프로그래밍을 위한 여러 클래스가 이미 정의되어있

app = QApplication(sys.argv) #지금 파일이 실행되는 경로
print(sys.argv) #sys.argv[0]: 현재 파이썬 소스 출
print(app)

label=QLabel("Hello PyQt5")
label.show() #app 을 실행시켜야 안에 버튼들이 보이지!!! 그래서! 윈도우 화면 출력하는 메서드

print("Before Loop")
app.exec_() # 이걸실행해야 보여 무한루프 즉 이벤트 루프 생성 이것은 QApplication 클래스의 메서드야
print("After Loop") #app.exec_() 는 윈도우에 종속되서 루프 무한반복되서 기다림 따라서 after loop 안뜸
