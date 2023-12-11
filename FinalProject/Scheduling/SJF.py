from SchedulerTemplate import Scheduler
from typing import List
from ..InstructionArchitecture.Process import Process

class SJF:
    def __init__(self, processes: List[Process] = []):
        self.processes = processes

    def SJP(self, processes: List[Process] = []):

        sorted_processes = sorted(processes, key=lambda x: x.burst_time)

        time = 0
        waiting_time = 0
        turnaround_time = 0

        for process in sorted_processes:
            waiting_time += time
            turnaround_time += waiting_time + process.burst_time
            time += process.burst_time