import time
from concurrent.futures.thread import ThreadPoolExecutor


# Consider implement "with"
class Reporter:
    def __init__(self, pollers, logger, period_seconds):
        self.__threadpool_executor = ThreadPoolExecutor(1)
        self.__pollers = pollers
        self.__logger = logger
        self.__period_seconds = period_seconds
        self.__started = False

    def start(self):
        self.__started = True
        for poller in self.__pollers:
            poller.start()
        self.__threadpool_executor.submit(self.__report)

    def stop(self):
        for poller in self.__pollers:
            poller.stop()
        self.__started = False

    def __report(self):
        while self.__started:
            record = [poller.value for poller in self.__pollers]
            if self.__should_log(record):
                self.__logger.log(record)
            time.sleep(self.__period_seconds)

    def __should_log(self, record):
        record_set = set(record)
        return not (len(record_set) == 1 and None in record_set)
