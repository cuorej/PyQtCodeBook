import threading

#쓰레드(스레드) 실행- 함수형
def thread_run():
    print('Thread running - F')

def thread_run_msg(msg):
    print('Thread running - F', msg)

for i in range(1000):
    t1 = threading.Thread(target=thread_run)
    t2 = threading.Thread(target=thread_run_msg, args=('service',)) # def thread_run_msg 의 msg 가 service가 되는거임 ,튜플은 원소 한개여도 , 써야함
    t1.start()
    t2.start()
