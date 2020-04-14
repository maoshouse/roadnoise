from .device import Device


# https://www.egr.msu.edu/classes/ece480/capstone/spring15/group14/uploads/4/2/0/3/42036453/wilsonappnote.pdf

class USBGpsDevice(Device):
    NMEA_GPGGA = '$GPGGA'
    NMEA_GPRMC = '$GPRMC'
    GPRMC_OK = 'A'

    def __init__(self, name, device):
        super().__init__(name)
        self.__device = device

    def read(self):
        print("reading gps")
        read_value = [value.strip() for value in bytearray(self.__device.readline()).decode().split(',')]
        if self.__is_gprmc(read_value) and self.__is_gprmc_valid(read_value):
            gprmc = self.__parse_gprmc(read_value)
            print(gprmc)
            return {'gps': gprmc}

    def __is_gprmc(self, read_value):
        return self.NMEA_GPRMC == read_value[0]

    def __parse_gprmc(self, read_value):
        return {
            'time_stamp': int(read_value[1]),
            'validity': read_value[2],
            'latitude': float(read_value[3]),
            'latitude_hemisphere': read_value[4],
            'longitude': float(read_value[5]),
            'longitude_hemisphere': read_value[6],
            'speed': float(read_value[7]),
            'true_course': float(read_value[8]),
            'date_stamp': int(read_value[9]),
            'variation': float(read_value[10]),
            'variation_direction': read_value[11]
        }

    def __is_gprmc_valid(self, read_value):
        return self.GPRMC_OK == read_value[2]
