import logging


class CsvLogger:
    def __init__(self, name, log_file_handler):
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(logging.INFO)
        self.__logger.addHandler(log_file_handler)

    def log(self, record):
        self.__logger.info(",".join(record))
