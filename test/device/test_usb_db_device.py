import unittest
from unittest.mock import Mock

from roadnoise.device.usb_db_device import USBDbDevice


class TestUSBDBDevice(unittest.TestCase):

    def test_poll(self):
        device = Mock()
        device.read.return_value = [1, 2, 3, 4, 5, 6, 7, 8]
        usb_db_device = USBDbDevice("name", device)
        self.assertEqual(25.8, usb_db_device.read())
