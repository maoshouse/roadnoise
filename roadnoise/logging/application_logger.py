import logging

from roadnoise.logging.gzip_timed_rotating_file_handler import GzipTimedRotatingFileHandler


class ApplicationLogger:

    @staticmethod
    def initialize_application_logger():
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        file_handler = GzipTimedRotatingFileHandler("application", "logs", "h", 1, 7)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        application_logger = logging.getLogger('application_log')
        application_logger.setLevel(logging.INFO)
        application_logger.addHandler(console_handler)
        application_logger.addHandler(file_handler)

    @staticmethod
    def info(message):
        logging.getLogger('application_log').info(message)

    @staticmethod
    def error(message):
        logging.getLogger('application_log').error(message)
