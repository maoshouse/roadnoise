import unittest
from unittest.mock import Mock

from roadnoise.poller.usb_db_poller import USBDbPoller


class TestUSBDBPoller(unittest.TestCase):

    def test_poll(self):
        device = Mock()
        device.read.return_value = [1, 2, 3, 4, 5, 6, 7, 8]
        usb_db_poller = USBDbPoller("name", device)
        self.assertEqual(25.8, usb_db_poller.poll())
