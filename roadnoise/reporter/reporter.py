from abc import ABC, abstractmethod


class Reporter(ABC):
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @abstractmethod
    def report(self):
        pass


