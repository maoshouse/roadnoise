import datetime
import gzip
import shutil
from logging.handlers import TimedRotatingFileHandler
from os import listdir, remove
from os.path import dirname, join, exists


class GzipTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, log_root, when, interval, backup_count):
        super().__init__(self.__getLogPath(), when=when, interval=interval, backupCount=backup_count)
        self.__log_root = log_root

    def __getLogPath(self):
        return "{}/{}/report".format(self.__log_root, datetime.utcnow())

    # https://medium.com/@rahulraghu94/overriding-pythons-timedrotatingfilehandler-to-compress-your-log-files-iot-c766a4ace240
    def doRollover(self):
        super(TimedRotatingFileHandler, self).doRollover()
        log_dir = dirname(self.baseFilename)

        to_compress = [
            join(log_dir, f) for f in listdir(log_dir)
        ]

        for f in to_compress:
            if exists(f):
                with open(f, "rb") as _old, gzip.open(f + ".gz", "wb") as _new:
                    shutil.copyfileobj(_old, _new)
                remove(f)
