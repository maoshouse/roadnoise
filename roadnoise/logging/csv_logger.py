import logging

# TODO pass in a Logger interface rather than build a python logger.
import sys


class CsvLogger:
    def __init__(self, name, log_file_handler):
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(logging.INFO)
        self.__logger.addHandler(log_file_handler)

    def log(self, record):
        print("logging: ", record)
        try:
            self.__logger.info(",".join(record))
        except:
            print("Unexpected error:", sys.exc_info()[0])
        print("logged: ", record)
