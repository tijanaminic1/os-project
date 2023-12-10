from SchedulerTemplate import Scheduler
from typing import List
from ..InstructionArchitecture.Process import Process

#https://docs.python.org/3/library/itertools.html
#cycle
class RRScheduler(Scheduler):
    def __init__(self, processes: List[Process] = []):
        self.processes = processes

    def RR(self, processes:List[Process], process:Process, time_quantum: int):

        remaining_time = process.burst_time
        time = 0
        waiting_time = 0
        turnaround_time = 0

        while processes:
            current_process = self.processes[0]

            if current_process.remaining_time <= time_quantum:
                time += current_process.remaining_time
                turnaround_time += time
                waiting_time += turnaround_time - current_process.burst_time
            else:
                time += time_quantum
                current_process.remaining_time -= time_quantum
                processes.append(current_process)
                
        


    