from .poller import Poller


# https://www.egr.msu.edu/classes/ece480/capstone/spring15/group14/uploads/4/2/0/3/42036453/wilsonappnote.pdf

class USBGpsPoller(Poller):

    def __init__(self, name, device):
        super().__init__(name)
        self.__device = device

    def poll(self):
        return ['4807.038', 'N', '01131.000', 'E']
