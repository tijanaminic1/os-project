from .SchedulerTemplate import Scheduler
from ..InstructionArchitecture import Process
class STRScheduler(Scheduler):
    def __init__(self):
        self.ready_queue = []

    def add_process(self, process: Process):
        self.ready_queue.append(process)

    def get_next_process(self):
        self.ready_queue.sort(key=lambda p: p.remaining_time)
        return self.ready_queue.pop(0) if self.ready_queue else None

    def should_preempt(self, current_process: Process, elapsed_time: float) -> bool:
        return any(p.remaining_time < current_process.remaining_time for p in self.ready_queue)
