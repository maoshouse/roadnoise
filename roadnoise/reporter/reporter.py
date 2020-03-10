import time
from concurrent.futures.thread import ThreadPoolExecutor


class Reporter:
    def __init__(self, pollers, logger, period_seconds):
        self.__threadpool_executor = ThreadPoolExecutor(1)
        self.__pollers = pollers
        self.__logger = logger
        self.__period_seconds = period_seconds
        self.__started = False

    def start(self):
        self.__started = True
        self.__threadpool_executor.submit(self.__report)

    def stop(self):
        self.__started = False

    def __report(self):
        while self.__started:
            self.__logger.log([poller.value for poller in self.__pollers])
            time.sleep(self.__period_seconds)
