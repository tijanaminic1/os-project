from threading import Lock
from ..InstructionArchitecture import Process
from . import IntLock, CustomThread
from ..Interrupt import Interrupt

class ThreadPool:
    def __init__(self, numOfThreads: int):
        self.threads = [CustomThread() for each in range(numOfThreads)]
        self.lock = Lock()
        self.numAvailable = IntLock(numOfThreads)

    def execute(self, process: Process):
        with self.numAvailable.lock:
            if(self.numAvailable.value <= 0):
                raise Interrupt("ThreadPoolException")
            else:
                pass
            #TODO: Reintegrate with CPU. Use 'process' Parameter of 'execute' where it should be use.
            #Communicate design intent with Andres?