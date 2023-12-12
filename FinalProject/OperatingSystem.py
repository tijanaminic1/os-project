from .CentralProcessor import CPU, Decoder, Registry
from .Memory import RAM, Cache, DMA
from .InstructionArchitecture import InstructionError, Process
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
@dataclass
class OperatingSystem:
    cpu: CPU=CPU(registers=Registry(),decoder=Decoder())
    ram: RAM=RAM()
    cache: Cache=Cache()
    scheduler: Scheduler=FCFSScheduler()
    interrupt_stack: InterruptStack=InterruptStack()
    dma: DMA=DMA()
    timer: CPUTimer=CPUTimer()
    processes: List[Process] = field(default_factory=list)

    def boot(self):
        # Initialize system components
        self.initialize_components()

    def initialize_components(self):
        # Set up CPU, RAM, Cache, etc.
        pass

    def run(self):
        # Main loop to run the operating system
        while True:
            self.handle_interrupts()
            process = self.scheduler.get_next_process()
            if process:
                self.execute_process(process)

    def handle_interrupts(self):
        # Check and handle any pending interrupts
        if self.interrupt_stack:
            self.interrupt_stack.HANDLESTACK()

    def execute_process(self, process: Process):
        # Execute the given process
        self.timer.start()
        # Process execution logic
        self.timer.stop()
        # Update process and system statistics

    def load_process(self, process: Process):
        # Add a new process to the system
        self.processes.append(process)
        self.scheduler.add_process(process)

    def terminate_process(self, process: Process):
        # Terminate a given process
        self.processes.remove(process)
        self.scheduler.remove_process(process)

    # Additional methods for DMA operations, memory management, etc.