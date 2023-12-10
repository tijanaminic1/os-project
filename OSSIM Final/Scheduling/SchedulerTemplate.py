from abc import ABC, abstractmethod

class Scheduler(ABC):
    @abstractmethod
    def schedule(self):
        """
        Implement the scheduling logic to determine the order of execution for processes.
        This method should return a list of processes to be executed.
        """
        pass