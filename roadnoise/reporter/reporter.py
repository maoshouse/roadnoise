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
        for poller in self.__pollers:
            poller.start()
        self.__threadpool_executor.submit(self.__report)
        print("started reporter")

    def stop(self):
        for poller in self.__pollers:
            poller.stop()
        self.__started = False

    def __report(self):
        print("entering report method.")
        while self.__started:
            print("reporting to log.")
            self.__logger.log(['a', 'b', 'c'])
            self.__logger.log(self.__pollers[0].value)
            print("reported to log.")

            # time.sleep(self.__period_seconds)
