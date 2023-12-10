from abc import ABC, abstractmethod

class Scheduler(ABC):
    @abstractmethod
    def get_schedule(self):
        """
        Implement the scheduling logic to determine the order of execution for processes.
        This method should return a list of processes to be executed.
        """
        pass
    @abstractmethod
    def current(self):
        """
        you can use this to get the current Process that needs to be executed
        """
        pass
    @abstractmethod
    def add_process(self,new_process):
        """
        boiler plate for adding a process to the scheduler
        """
        pass
    #TODO: add any boiler plate functionality that you want
