import unittest
from unittest.mock import Mock

from roadnoise.device.usb_gps_device import USBGpsDevice


class TestUSBGpsDevice(unittest.TestCase):
    VALID_GPRMC_LINE = b'$GPRMC,220516,A,5133.82,N,00042.24,W,173.8,231.8,130694,004.2,W,*70\r\n'
    INVALID_GPRMC_LINE = b'$GPRMC,042223.434,V,,,,,,,140420,,,N*48\r\n'
    INVALID_NMEA_LINE = b'$GPGGA,042224.442,,,,,0,00,,,M,0.0,M,,0000*56\r\n'

    EXPECTED_VALID_GPRMC_DICT = {
        'gps': {
            'time_stamp': 220516,
            'validity': 'A',
            'latitude': 5133.82,
            'latitude_hemisphere': 'N',
            'longitude': 00042.24,
            'longitude_hemisphere': 'W',
            'speed': 173.8,
            'true_course': 231.8,
            'date_stamp': 130694,
            'variation': 004.2,
            'variation_direction': 'W'
        }
    }

    def test_read(self):
        device = Mock()
        device.readline.return_value = self.VALID_GPRMC_LINE
        usb_gps_device = USBGpsDevice("name", device)
        self.assertEqual(self.EXPECTED_VALID_GPRMC_DICT, usb_gps_device.read())

    def test_read_invalid_gprmc(self):
        device = Mock()
        device.readline.return_value = self.INVALID_GPRMC_LINE
        usb_gps_device = USBGpsDevice("name", device)
        self.assertIsNone(usb_gps_device.read())

    def test_read_invalid_nmea(self):
        device = Mock()
        device.readline.return_value = self.INVALID_NMEA_LINE
        usb_gps_device = USBGpsDevice("name", device)
        self.assertIsNone(usb_gps_device.read())
