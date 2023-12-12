from SchedulerTemplate import Scheduler
from typing import List
from ..InstructionArchitecture.Process import Process
from queue import Queue
class FCFSScheduler(Scheduler):
    def __init__(self):
        self.ready_queue = Queue()
    def add_process(self, process: Process):
        self.ready_queue.put(process)

    def get_next_process(self):
        return self.ready_queue.get() if not self.ready_queue.empty() else None

    def should_preempt(self, current_process: Process, elapsed_time: float) -> bool:
        return False  # No preemption in FCFS
