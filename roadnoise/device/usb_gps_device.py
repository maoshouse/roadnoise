import traceback

from .device import Device
# https://www.egr.msu.edu/classes/ece480/capstone/spring15/group14/uploads/4/2/0/3/42036453/wilsonappnote.pdf
from ..logging.application_logger import ApplicationLogger


class USBGpsDevice(Device):
    NMEA_GPGGA = '$GPGGA'
    NMEA_GPRMC = '$GPRMC'
    GPRMC_OK = 'A'

    def __init__(self, name, device):
        super().__init__(name)
        self.__device = device

    def read(self):
        read_value = self.__get_gps_data_array()
        if read_value is not None and self.__is_gprmc(read_value) and self.__is_gprmc_valid(read_value):
            gps_value = self.__parse_gprmc(read_value)
            return {'gps': gps_value} if gps_value is not None else None

    def __get_gps_data_array(self):
        try:
            line = self.__device.readline()
            return [value.strip() for value in bytearray(line).decode().split(',')]
        except UnicodeDecodeError:
            ApplicationLogger.error(traceback.format_exc())

    def __is_gprmc(self, read_value):
        return self.NMEA_GPRMC == read_value[0]

    def __parse_gprmc(self, read_value):
        try:
            latitude_hemisphere = read_value[4]
            longitude_hemisphere = read_value[6]

            latitude = float(read_value[3]) / 100
            if latitude_hemisphere == 'S':
                latitude *= -1
            longitude = float(read_value[5]) / 100
            if longitude_hemisphere == 'W':
                longitude *= -1

            return {
                'time_stamp': float(read_value[1]),
                'validity': read_value[2],
                'latitude': latitude,
                'longitude': longitude,
                'speed': float(read_value[7]) / 1.944,
                'true_course': float(read_value[8]),
                'date_stamp': float(read_value[9]),
            }
        except ValueError:
            ApplicationLogger.error("ValueError for read value")

    def __is_gprmc_valid(self, read_value):
        return self.GPRMC_OK == read_value[2]
