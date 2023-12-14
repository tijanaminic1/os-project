from dataclasses import dataclass, field
from typing import Dict
from Process import Process
import time
@dataclass
class ProcessTimeMetrics:
    arrival_time: float = time.perf_counter()
    start_time: float = 0.0
    end_time: float = 0.0
    total_run_time: float = 0.0  # Total time the process has been running

class CPUTimer:
    def __init__(self):
        self.metrics: Dict[int, ProcessTimeMetrics] = {}
        self.simulation_start_time = time.perf_counter()  # Record the start time of the simulation


    def add_process(self, process_id: int):
        self.metrics[process_id] = ProcessTimeMetrics()

    def start(self, process_id: int):
        if process_id in self.metrics:
            if self.metrics[process_id].start_time == 0:
                self.metrics[process_id].start_time = time.perf_counter()

    def stop(self, process_id: int):
        current_time = time.perf_counter()
        metrics = self.metrics[process_id]
        if metrics.start_time != 0:
            metrics.total_run_time += current_time - metrics.start_time
            metrics.end_time = current_time

    def get_wait_time(self, process_id: int) -> float:
        metrics = self.metrics[process_id]
        return metrics.start_time - metrics.arrival_time

    def get_turnaround_time(self, process_id: int) -> float:
        metrics = self.metrics[process_id]
        return metrics.end_time - metrics.arrival_time

    def get_cpu_utilization(self):
        total_run_time = sum(metric.total_run_time for metric in self.metrics.values())
        total_time_elapsed = time.perf_counter() - self.simulation_start_time
        return (total_run_time / total_time_elapsed) * 100 if total_time_elapsed > 0 else 0