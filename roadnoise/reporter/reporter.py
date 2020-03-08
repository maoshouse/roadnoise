class Reporter:
    def __init__(self, name, device, logger):
        self.__name = name
        self.__device = device
        self.__logger = logger

    @property
    def name(self):
        return self.__name

    def report(self):
        read_value = self.__device.read()
        self.__logger.log(read_value)
