from SchedulerTemplate import Scheduler
from Process import Process
class SJFScheduler(Scheduler):
    def __init__(self):
        self.ready_queue = []

    def add_process(self, process: Process):
        self.ready_queue.append(process)
        self.ready_queue.sort(key=lambda p: len(p))

    def get_next_process(self):
        return self.ready_queue.pop(0) if self.ready_queue else None

    def should_preempt(self, current_process: Process, elapsed_time: float) -> bool:
        return False
