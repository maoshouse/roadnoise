from readerwriterlock import rwlock


class ThreadSafeValue:
    def __init__(self, value=None):
        self.__value = value
        self.__value_lock = rwlock.RWLockFair()

    @property
    def value(self):
        with self.__value_lock.gen_rlock():
            return self.__value

    @value.setter
    def value(self, value):
        with self.__value_lock.gen_wlock():
            self.__value = value
