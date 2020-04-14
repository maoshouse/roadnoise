import hid
import serial

from .device.usb_db_device import USBDbDevice
from .device.usb_gps_device import USBGpsDevice
from .logging.dict_logger import DictLogger
from .logging.gzip_timed_rotating_file_handler import GzipTimedRotatingFileHandler
from .poller.poller import Poller
from .reporter.reporter import Reporter

ID_VENDOR = 0x64bd
ID_PRODUCT = 0x74e3


def main():
    usb_db_device = USBDbDevice("USB Db", get_usb_decibel_meter())
    usb_db_poller = Poller(usb_db_device)

    gps_serial = get_usb_gps()
    print("USB GPS: ", gps_serial)
    usb_gps_device = USBGpsDevice("USB GPS", gps_serial)

    usb_gps_poller = Poller(usb_gps_device)
    pollers = [usb_gps_poller]
    file_handler = GzipTimedRotatingFileHandler("roadnoise", ".", "h", 1, 7)
    logger = DictLogger("logger", file_handler)
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


def get_usb_gps():
    return serial.Serial('/dev/ttyUSB0', 4800, timeout=5)
