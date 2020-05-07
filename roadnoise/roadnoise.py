import traceback

import hid
import serial

from .device.usb_db_device import USBDbDevice
from .device.usb_gps_device import USBGpsDevice
from .exporter.s3_exporter import S3Exporter
from .logging.application_logger import ApplicationLogger
from .logging.dict_logger import DictLogger
from .logging.gzip_timed_rotating_file_handler import GzipTimedRotatingFileHandler
from .poller.poller import Poller
from .reporter.reporter import Reporter

ID_VENDOR = 0x64bd
ID_PRODUCT = 0x74e3


def main():
    ApplicationLogger.initialize_application_logger()
    ApplicationLogger.info("Starting roadnoise.")
    usb_db_device = USBDbDevice("USB Db", get_usb_decibel_meter())
    usb_db_poller = Poller(usb_db_device, period_seconds=0.1)

    usb_gps_device = USBGpsDevice("USB GPS", get_usb_gps())
    usb_gps_poller = Poller(usb_gps_device)

    pollers = [usb_db_poller, usb_gps_poller]
    file_handler = GzipTimedRotatingFileHandler("roadnoise", "logs", "h", 1, 7, compress_on_rollover=False)
    logger = DictLogger("RoadNoiseLog", file_handler)
    reporter = Reporter(pollers, logger, 1)
    reporter.start()
    try:
        while True:
            pass
    except:
        ApplicationLogger.error(traceback.format_exc())
    finally:
        ApplicationLogger.info("Stopping roadnoise.")
        reporter.stop()

    try:
        ApplicationLogger.info("Starting rollover")
        file_handler.doRollover()
        ApplicationLogger.info("Finished rollover, starting export.")
        s3_exporter = S3Exporter(delete_exported=True)
        s3_exporter.export('logs/compressed', 'g1gf49n2fh')
    except:
        ApplicationLogger.error(traceback.format_exc())
        
    exit(0)


def get_usb_decibel_meter():
    usb_decibel_meter = hid.device()
    usb_decibel_meter.open(ID_VENDOR, ID_PRODUCT)
    assert usb_decibel_meter is not None
    return usb_decibel_meter


def get_usb_gps():
    return serial.Serial('/dev/ttyUSB0', 4800, timeout=5)
