from SchedulerTemplate import Scheduler
from typing import List
from ..InstructionArchitecture.Process import Process
class FCFSScheduler(Scheduler):
    def __init__(self, processes: List[Process]=[]):
        self.processes = processes
    def add_process(self,process:Process):
        return self.__init__(self.processes+[process])
    def current(self):
        return self.processes[0]
    def remove_process(self):
        return self.__init__(self.processes[1:])
