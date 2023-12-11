from SchedulerTemplate import Scheduler
from typing import List
from ..InstructionArchitecture.Process import Process

#https://docs.python.org/3/library/itertools.html
#cycle
class RRScheduler:
    def __init__(self, processes: List[Process] = []):
        self.processes = processes

    def RR(self, time_quantum: int):
        processes = self.processes.copy()  # Make a copy to avoid modifying the original list
        time = 0
        waiting_time = 0
        turnaround_time = 0

        while processes:
            current_process = processes[0]

            if current_process.remaining_time <= time_quantum:
                time += current_process.remaining_time
                turnaround_time += time
                waiting_time += turnaround_time - current_process.burst_time
                processes.pop(0)
            else:
                time += time_quantum
                current_process.remaining_time -= time_quantum
                processes.append(current_process)
                processes.pop(0)

        avg_waiting_time = waiting_time / len(self.processes)
        avg_turnaround_time = turnaround_time / len(self.processes)
                
        


    