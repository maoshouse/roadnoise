import logging

# TODO pass in a Logger interface rather than build a python logger.
import time


class DictLogger:
    def __init__(self, name, log_file_handler):
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(logging.INFO)
        self.__logger.addHandler(log_file_handler)

    def log(self, poller_values):
        if self.__is_valid_values(poller_values):
            log_line = {key: value for mapping in poller_values for key, value in mapping.items()}
            log_line['time'] = time.time_ns() // 1000
            self.__logger.info(log_line)

    def __is_valid_values(self, poller_values):
        return None not in poller_values
