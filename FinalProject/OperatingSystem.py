#Central Processor Imports
from .CentralProcessor.CPU import CPU
from .CentralProcessor.Decoder import Decoder
from .CentralProcessor.Registry import Registry
#Memory Imports
from .Memory.RAM import RAM 
from .Memory.Cache import Cache
from .Memory.DMA import DMA
from .InstructionArchitecture.Process import Process
from .InstructionArchitecture.Program import Program
#Interrupts
from .Interrupt.InterruptStack import InterruptStack
from .Interrupt.Interrupt import Interrupt
#Scheduling
from .Scheduling.SchedulerTemplate import Scheduler
from .Scheduling.CPUTimer import CPUTimer
from .Scheduling.FCFSScheduler import FCFSScheduler as FirstComeFirstServe
from .Scheduling.HRNScheduler import HRNScheduler as HighestRatio
from .Scheduling.RRScheduler import RRScheduler as RoundRobin
from .Scheduling.SJFScheduler import SJFScheduler as ShortestJobFirst
from .Scheduling.STRScheduler import STRScheduler as ShortestTimeRemaining
from dataclasses import dataclass
import copy
#Threading and Lock Import
from threading import Thread, Lock
from queue import Queue
#Prettiness Imports
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
