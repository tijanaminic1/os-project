import time
#need four methods:
#start(self)
    #starts timer from current time
#stop(self)
    #stops (pauses) timer
#out(self)
    #prints the current time elapsed.
#reset(self)
    #resets the timer at 0

class CPUTimer:
    def __init__(self):
        self.global_time = time.perf_counter_ns()
        self.timer = 0 #sets the timer to 0

    def start(self):
        self.timer = time.perf_counter_ns() #starts timer
        return self.timer #returns the start time
    def stop(self):
        self.timer.sleep() #puts timer to sleep
    def out(self):
        timeElaspsed = time.perf_counter_ns() - self.timer #subtracts the current time from the start time to find the amount of time passed
        return timeElaspsed #returns the amount of passed time
    def reset(self):
        self.time = 0
    def turnaround_time(self):
        pass
    def burst_time(self):
        pass
    def waiting_time(self):
        pass






