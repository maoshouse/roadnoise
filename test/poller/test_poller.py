import unittest
from unittest.mock import Mock

from roadnoise.poller.poller import Poller


class TestPoller(unittest.TestCase):
    DEVICE_READ_VALUE = 123

    def test_poll(self):
        device = Mock()
        device.read.return_value = self.DEVICE_READ_VALUE

        poller = Poller(device, 1)

        self.assertIsNone(poller.value)
        poller.start()
        self.assertEqual(self.DEVICE_READ_VALUE, poller.value)
        poller.stop()
