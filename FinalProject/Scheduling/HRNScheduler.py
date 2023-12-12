from .SchedulerTemplate import Scheduler
from ..InstructionArchitecture.Process import Process
import time
class HRNScheduler(Scheduler):
    def __init__(self, timer: CPUTimer):
        self.ready_queue = []
        self.timer = timer

    def add_process(self, process: Process):
        self.ready_queue.append(process)

    def get_next_process(self):
        now = time()
        self.ready_queue.sort(key=lambda p: ((now - self.timer.metrics[p.id].arrival_time) + len(p)) / len(p), reverse=True)
        return self.ready_queue.pop(0) if self.ready_queue else None

    def should_preempt(self, current_process: Process, elapsed_time: float) -> bool:
        return False
