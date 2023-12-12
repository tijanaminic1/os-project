from .CentralProcessor import CPU, Decoder, Registry
from .Memory import RAM, Cache, DMA
from .InstructionArchitecture.Process import Process
from .InstructionArchitecture.Program import Program
from .Interrupt import InterruptStack, Interrupt
from .Threads import *
from .Scheduling.SchedulerTemplate import Scheduler
from .Scheduling.CPUTimer import CPUTimer
from .Scheduling.FCFSScheduler import FCFSScheduler
from dataclasses import dataclass
import copy

#NOTE: This is a barebones implementation of the operating system
#This is supposed to serve as a roadmap to aid in the programming of
#the operating system.
from threading import Thread, Lock
from queue import Queue
from dataclasses import dataclass, field
from typing import List, Optional
@dataclass
class OperatingSystem:
    cpu: CPU
    ram: RAM
    cache: Cache
    scheduler: Scheduler
    interrupt_stack: InterruptStack
    dma: DMA
    processes: List[Process] = field(default_factory=list)
    process_queue: Queue = field(default_factory=Queue)
    current_process: Optional[Process] = None
    timer: CPUTimer = field(default_factory=CPUTimer)
    lock: Lock = field(default_factory=Lock)

    def __post_init__(self):
        self.thread = Thread(target=self.run, daemon=True)

    def start(self):
        self.thread.start()

    def run(self):
        while True:
            self.lock.acquire()
            if not self.process_queue.empty():
                self.context_switch(self.process_queue.get())
                self.execute_process(self.current_process)
                self.process_queue.task_done()
            self.lock.release()

    def load_process(self, process: Process):
        self.lock.acquire()
        self.processes.append(process)
        self.scheduler.add_process(process)
        self.process_queue.put(process)
        self.lock.release()

    def context_switch(self, process: Process):
        if self.current_process:
            self.save_state(self.current_process)
        self.current_process = process
        self.restore_state(process)

    def execute_process(self, process: Process):
        self.timer.start(process)
        # Process execution logic: Fetch, Decode, Execute cycle
        while not process.execution_completed():
            address = process.current_instruction_address()
            instruction = self.cpu.fetch(address, self.cache, self.ram)
            decoded = self.cpu.decode(instruction)
            self.cpu.execute(decoded)
            process.advance_instruction()
        self.timer.stop(process)
        self.report_completion(process)

    def save_state(self, process: Process):
        # Save the state of the process
        process.save_state(self.cpu.registers)

    def restore_state(self, process: Process):
        # Restore the state of the process
        self.cpu.registers = process.restore_state()

    def report_completion(self, process: Process):
        wait_time = self.timer.get_wait_time(process)
        turnaround_time = self.timer.get_turnaround_time(process)
        arrival_time = process.arrival_time
        print(f"Process {process.id}: Wait Time={wait_time}, Turnaround Time={turnaround_time}, Arrival Time={arrival_time}")

# Placeholder classes
class CPU:
    # Your CPU implementation here
    pass

class RAM:
    # Your RAM implementation here
    pass

class Cache:
    # Your Cache implementation here
    pass

class Scheduler:
    # Your Scheduler implementation here
    pass

class InterruptStack:
    # Your InterruptStack implementation here
    pass

class DMA:
    # Your DMA implementation here
    pass

class CPUTimer:
    # Your CPUTimer implementation here
    pass

class Process:
    # Your Process implementation here
    pass
