import time

class CPUTimer:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.total_executed_time = 0  # Total time for which processes have been executed

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()
        self.total_executed_time += self.end_time - self.start_time

    def get_burst_time(self):
        return self.end_time - self.start_time

    def get_total_executed_time(self):
        return self.total_executed_time

    # Other methods for calculating waiting time, turnaround time, etc.,
    # depending on how you track process arrival and completion
