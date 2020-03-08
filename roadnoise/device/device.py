from abc import ABC, abstractmethod


class Device(ABC):
    def __init__(self, name):
        assert name is not None
        self.__name = name

    @property
    def name(self):
        return self.__name

    @abstractmethod
    def read(self):
        pass
