import hid

from .device.usb_db_device import USBDbDevice
from .logging.csv_logger import CsvLogger
from .logging.gzip_timed_rotating_file_handler import GzipTimedRotatingFileHandler
from .reporter.reporter import Reporter

ID_VENDOR = 0x64bd
ID_PRODUCT = 0x74e3


def main():
    usb_db_poller = USBDbDevice("USB Db", get_usb_decibel_meter())
    pollers = [usb_db_poller]
    file_handler = GzipTimedRotatingFileHandler("roadnoise", ".", "h", 1, 7)
    logger = CsvLogger("logger", file_handler)
    reporter = Reporter(pollers, logger, 1)
    reporter.start()
    try:
        while True:
            pass
    finally:
        reporter.stop()

    exit(0)


def get_usb_decibel_meter():
    usb_decibel_meter = hid.device()
    usb_decibel_meter.open(ID_VENDOR, ID_PRODUCT)
    assert usb_decibel_meter is not None
    return usb_decibel_meter
