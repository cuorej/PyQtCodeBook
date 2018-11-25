import threading

#쓰레드 실행 - 클래스형

class Thread_Run(threading.Thread): #Thread 를 상속받아서 안에서 사용하면되는거임
    def run(self):
        print('Thread runninc - C')



for i in range(100):
    t= Thread_Run() #클래스의 instance 화
    #쓰레드 시작
    t.start()
