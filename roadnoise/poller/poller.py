import time
from concurrent.futures.thread import ThreadPoolExecutor


class Poller:
    def __init__(self, device, period_seconds):
        self.__threadpool_executor = ThreadPoolExecutor(1)
        self.__device = device
        self.__period_seconds = period_seconds
        self.__started = False
        self.__value = None

    def start(self):
        self.__started = True
        self.__threadpool_executor.submit(self.__poll)

    def stop(self):
        self.__started = False

    @property
    def value(self):
        return self.__value

    def __poll(self):
        while self.__started:
            self.__value = self.__device.read()
            print("Polled: ", self.__value)
            time.sleep(self.__period_seconds)
