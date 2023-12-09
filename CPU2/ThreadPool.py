from threading import Thread, Lock
from typing import List
import threading
from Process import Process
from Interrupt import Interrupt
class BooleanLock:
    def __init__(self):
        self.lock = Lock()
        self.value = False

class IntLock:
    def __init__(self, data: int):
        self.lock = Lock()
        self.value = data
class CustomThread(threading.Thread):
    def __init__(self, execute: BooleanLock, runnables: List[Process]):
        super().__init__()
        self.execute = execute
        self.runnables = runnables
    def run(self):
        try:
            with self.execute.lock:
                while(self.execute.value or not self.runnables.isEmpty()):
                  process = self.runnables.pop()
                  process.run()
        except ThreadPoolException:
            pass # implement this later

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