import random

from .device import Device


class USBDbDevice(Device):
    GET_STATE_REQUEST = [0xb3, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 0, 0, 0, 0]

    def __init__(self, name, device):
        super().__init__(name)
        self.__device = device

    def read(self):
        print("im trying to read")
        self.__device.write(self.GET_STATE_REQUEST)
        read_value = self.__device.read(8)
        if len(read_value) == 8:
            return {'db': self.__determine_db(read_value)}

    def __determine_db(self, read_value):
        return (read_value[0] << 8 | read_value[1]) / 10
