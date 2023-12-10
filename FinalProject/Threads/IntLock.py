from threading import Lock
#Purpose:
#To Act as an int Lock mechanism.
class IntLock:
    def __init__(self, data: int):
        self.lock = Lock()
        self.value = data

#TODO: Aren't locks a little more robust?