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
        self.timer = 0 #sets the timer to 0
    def start(self):
        self.timer = time.perf_counter_ns() #starts timer
        return self.timer #returns the start time
    def stop(self):
        self.timer.sleep() #puts timer to sleep
    def out(self):
        timeElaspsed = time.perf_counter_ns() - self.timer #subtracts the current time from the start time to find the amount of time passed
        return timeElaspsed #returns the amount of passed time
    def reset(self): #write a test file and test the timer when done pls
        self.time = 0






