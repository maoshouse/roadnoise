import time
import traceback
from concurrent.futures.thread import ThreadPoolExecutor

# Consider implement "with"
from roadnoise.logging.application_logger import ApplicationLogger


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
            try:
                self.__logger.log([poller.value for poller in self.__pollers])
                time.sleep(self.__period_seconds)
            except:
                ApplicationLogger.error(traceback.format_exc())
