class Reporter:
    def __init__(self, name, poller, logger):
        self.__name = name
        self.__poller = poller
        self.__logger = logger

    @property
    def name(self):
        return self.__name

    def report(self):
        polled_value = self.__poller.poll()
        self.__logger.log(polled_value)
