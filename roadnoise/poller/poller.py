import json
import time
import traceback
from concurrent.futures.thread import ThreadPoolExecutor

from roadnoise.logging.application_logger import ApplicationLogger
from roadnoise.model.thread_safe_value import ThreadSafeValue


class Poller:
    def __init__(self, device, period_seconds=0.5):
        self.__threadpool_executor = ThreadPoolExecutor(1)
        self.__device = device
        self.__period_seconds = period_seconds
        self.__started = False
        self.__value = ThreadSafeValue()

    def start(self):
        self.__started = True
        self.__threadpool_executor.submit(self.__poll)

    def stop(self):
        self.__started = False

    @property
    def value(self):
        return self.__value.value

    def __poll(self):
        while self.__started:
            try:
                value = self.__device.read()
                print('{}: Read: {}'.format(self.__device.name(), json.dumps(value)))
                if value is not None:
                    self.__value.value = value
                time.sleep(self.__period_seconds)
            except:
                ApplicationLogger.error(traceback.format_exc())
