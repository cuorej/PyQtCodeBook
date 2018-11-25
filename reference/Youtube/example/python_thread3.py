#로깅(logging) 패키지 사용한 예제

import logging
import threading
import time

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s (%(threadName)-8s) %(message)s]'

)

def worker1():
    logging.debug('Starting')
    time.sleep(0.5)
    logging.debug('Exit')

def worker2():
    logging.debug('Starting')
    time.sleep(0.5)
    logging.debug('Exit')

t1= threading.Thread(name="service-1", target=worker1) #위의 threadName을 이걸로 지정
t2= threading.Thread(name='service-2', target=worker2)
t3= threading.Thread(target=worker1)

t1.start()
t2.start()
t3.start()
