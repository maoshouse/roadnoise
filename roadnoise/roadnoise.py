import hid

from .poller.usb_db_poller import USBDbPoller

ID_VENDOR = 0x64bd
ID_PRODUCT = 0x74e3


def main():
    usb_db_meter = __get_usb_decibel_meter()
    usb_db_poller = USBDbPoller("USB Db", usb_db_meter)


def __get_usb_decibel_meter():
    usb_decibel_meter = hid.device()
    usb_decibel_meter.open(ID_VENDOR, ID_PRODUCT)
    assert usb_decibel_meter is not None
    return usb_decibel_meter
