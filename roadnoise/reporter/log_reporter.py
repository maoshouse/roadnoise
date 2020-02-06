from roadnoise.reporter.reporter import Reporter


class LogReporter(Reporter):

    def __init__(self, logger):
        super().__init__("Logging Reporter")
        self.__logger = logger

    def report(self, record):
        self.__logger.log(record)
