from threading import Lock
#Purpose:
#To Act as an bool Lock mechanism.
class BooleanLock:
    def __init__(self):
        self.lock = Lock()

#TODO: Aren't locks a little more robust?