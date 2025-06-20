import gzip
import os
import shutil
from logging.handlers import TimedRotatingFileHandler
from os.path import dirname, join, exists
from pathlib import Path


class GzipTimedRotatingFileHandler(TimedRotatingFileHandler):

    def __init__(self, file_name_prefix, log_root, when, interval, backup_count, compress_on_rollover=True):
        super().__init__(self.__get_log_path(file_name_prefix + ".log", log_root), when=when, interval=interval,
                         backupCount=backup_count)
        self.__file_name_prefix = file_name_prefix
        self.__log_root = log_root
        self.__compress_on_rollover = compress_on_rollover

    # https://medium.com/@rahulraghu94/overriding-pythons-timedrotatingfilehandler-to-compress-your-log-files-iot-c766a4ace240
    def doRollover(self):
        super().doRollover()
        self.rollover_logs()

    def rollover_logs(self):
        log_dir = dirname(self.baseFilename)
        files_to_rollover = [join(log_dir, file) for file in os.listdir(log_dir) if
                             file.startswith(self.__file_name_prefix) and not file.endswith((".gz", ".log"))]
        for file in files_to_rollover:
            if exists(file):
                if self.__compress_on_rollover:
                    with open(file, "rb") as to_compress, gzip.open(self.__get_rollover_path(file), "wb") as compressed:
                        shutil.copyfileobj(to_compress, compressed)
                else:
                    with open(file, "rb") as to_compress, open(self.__get_rollover_path(file), "wb") as non_compressed:
                        shutil.copyfileobj(to_compress, non_compressed)
                os.remove(file)

    def __get_log_path(self, file_name, log_root):
        Path(log_root).mkdir(parents=True, exist_ok=True)
        return log_root + "/" + file_name

    def __get_rollover_path(self, file):
        if self.__compress_on_rollover:
            rollover_dir = "{}/compressed".format(self.__log_root)
            Path(rollover_dir).mkdir(parents=True, exist_ok=True)
            return "{}/{}.gz".format(rollover_dir, file.split('/')[-1])
        else:
            rollover_dir = "{}/non_compressed".format(self.__log_root)
            Path(rollover_dir).mkdir(parents=True, exist_ok=True)
            return "{}/{}".format(rollover_dir, file.split('/')[-1])
