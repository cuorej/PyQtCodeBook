#일정 시간 간격으로 반복 작업가능한 예제
import time
import threading

def thread_run():
    print('=====', time.ctime(), '=====')
    #개발 하고자 하는 코드 쭈우욱!~
    #############################

    for i in range(1,10000):
        print('Threading running -',i)

    threading.Timer(2.5, thread_run).start() #2.5초마다 실행해!--재귀함수 : 자기 스스로를 다시 호출 def 밖으로 빼면안됨 왜냐면 스스로를 다시 호출해야하니까

thread_run()
