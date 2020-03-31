import time
from concurrent.futures.thread import ThreadPoolExecutor

from readerwriterlock import rwlock


class Poller:
    def __init__(self, device, period_seconds=0.5):
        self.__threadpool_executor = ThreadPoolExecutor(1)
        self.__device = device
        self.__period_seconds = period_seconds
        self.__started = False
        self.__value_lock = rwlock.RWLockFair()
        self.__value = None

    def start(self):
        self.__started = True
        self.__threadpool_executor.submit(self.__poll)

    def stop(self):
        self.__started = False

    @property
    def value(self):
        with self.__value_lock.gen_rlock():
            print("got rlock")
            return self.__value

    def __poll(self):
        while self.__started:
            with self.__value_lock.gen_wlock():
                print("got wlock")
                value = self.__device.read()
                if value is not None:
                    print("got value ", value)
                    self.__value = value
            time.sleep(self.__period_seconds)
