import usb.core

from .poller.usb_db_poller import USBDbPoller


def main():
    usb_db_meter = __get_usb_decibel_meter()
    usb_db_poller = USBDbPoller("USB Db", usb_db_meter)

def __get_usb_decibel_meter():
    vendor_id = "abc"
    product_id = "123";
    usb_decibel_meter = usb.core.find(idVendor=vendor_id, idProduct=product_id)
    assert usb_decibel_meter is not None
    return usb_decibel_meter