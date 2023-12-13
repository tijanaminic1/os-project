from abc import ABC, abstractmethod
from queue import Queue
from InstructionArchitecture.Process import Process
class Scheduler(ABC):
    @abstractmethod
    def add_process(self, process: Process):
        pass

    @abstractmethod
    def get_next_process(self):
        pass

    @abstractmethod
    def should_preempt(self, current_process: Process, elapsed_time: float) -> bool:
        pass
