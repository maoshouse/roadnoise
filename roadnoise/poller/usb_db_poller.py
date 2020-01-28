from .poller import Poller


class USBDbPoller(Poller):

    def __init__(self, name, device):
        super().__init__(name)
        self.__device = device

    def poll(self):
        # what happens if the call times out? how do I handle?
        read_value = self.__device.ctrl_transfer(0xC0, 4, 0, 0, 200)
        return self.__determine_db(read_value)

    # https://codereview.stackexchange.com/q/113389
    def __determine_db(self, read_value):
        db = (read_value[0] + ((read_value[1] & 3) * 256)) * 0.1 + 30
        db_as_string = '{0:.2f}'.format(float(db))
        return float(db_as_string)

