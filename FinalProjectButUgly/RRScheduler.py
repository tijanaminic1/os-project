from SchedulerTemplate import Scheduler
from typing import List
from Process import Process
from queue import Queue
#https://docs.python.org/3/library/itertools.html
#cycle
class RRScheduler(Scheduler):
    def __init__(self, time_slice: float):
        self.ready_queue = Queue()
        self.time_slice = time_slice

    def add_process(self, process: Process):
        self.ready_queue.put(process)

    def get_next_process(self):
        return self.ready_queue.get() if not self.ready_queue.empty() else None

    def should_preempt(self, current_process: Process, elapsed_time: float) -> bool:
        return elapsed_time >= self.time_slice

        


    