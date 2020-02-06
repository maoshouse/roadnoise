import unittest
from array import array
from unittest.mock import Mock

from roadnoise.poller.usb_db_poller import USBDbPoller


class TestUSBDBPoller(unittest.TestCase):

    def test_poll(self):
        device = Mock()
        device.ctrl_transfer.return_value = array('B', [142, 2, 192, 192])
        usb_db_poller = USBDbPoller("name", device)
        assert usb_db_poller.poll() is not None
