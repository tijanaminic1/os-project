from time import time
from dataclasses import dataclass, field
from typing import Dict
from ..InstructionArchitecture.Process import Process
@dataclass
class ProcessTimeMetrics:
    arrival_time: float
    start_time: float = 0.0
    end_time: float = 0.0
    total_run_time: float = 0.0  # Total time the process has been running

class CPUTimer:
    def __init__(self):
        self.metrics: Dict[int, ProcessTimeMetrics] = {}

    def add_process(self, process: Process):
        self.metrics[process.id] = ProcessTimeMetrics(arrival_time=time())

    def start(self, process: Process):
        if self.metrics[process.id].start_time == 0:
            self.metrics[process.id].start_time = time()

    def stop(self, process: Process):
        current_time = time()
        metrics = self.metrics[process.id]
        if metrics.start_time != 0:
            metrics.total_run_time += current_time - metrics.start_time
            metrics.end_time = current_time

    def get_wait_time(self, process: Process) -> float:
        metrics = self.metrics[process.id]
        return metrics.start_time - metrics.arrival_time

    def get_turnaround_time(self, process: Process) -> float:
        metrics = self.metrics[process.id]
        return metrics.end_time - metrics.arrival_time

    def get_total_run_time(self, process: Process) -> float:
        return self.metrics[process.id].total_run_time
