from .CentralProcessor import CPU, Decoder, Registry
from .Memory import RAM, Cache
from .InstructionArchitecture import InstructionError
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
    ram: RAM
    cache: Cache
    cpu: CPU
    monitor: CPU = CPU(registers=Registry(), 
                       decoder=Decoder(), 
                       cache=copy.copy(cpu.cache), 
                       RAM=copy.copy(cpu.RAM))#A monitor is an inferior CPU with its own registers and instruction set
                        #But it accesses the same memory as the main CPU.
                        #Its purpose is to perform clerical tasks such as scheduling 
    interrupt_stack: InterruptStack
    cpu_timer: CPUTimer
    scheduler: Scheduler
    def load_programs(self, programs):
        # Load programs into memory
        for program in programs:
            self.ram.load_program(program)

    def run(self):
        # Main simulation loop
        try:
            while True:
                # Get a list of processes from the scheduler
                processes_to_execute = self.scheduler.schedule()

                # Load processes into the CPU
                self.cpu.load_processes(processes_to_execute)

                # Start CPU timer
                self.cpu_timer.start()

                # Execute processes
                self.cpu.execute()

                # Stop CPU timer
                self.cpu_timer.stop()

        except KeyboardInterrupt:
            # Handle keyboard interrupt gracefully
            print("Simulation interrupted. Exiting.")
        except Interrupt as i:
            self.interrupt_stack.push(i)
            InterruptStack.HANDLESTACK(self.interrupt_stack)

    def display_statistics(self):
        # Display statistics from the CPU timer
        print("Turnaround Time:", self.cpu_timer.turnaround_time())
        print("Burst Time:", self.cpu_timer.burst_time())
        print("Waiting Time:", self.cpu_timer.waiting_time())

#TODO: Full integration of project folders:
#CentralProcessor
#InstructionArchitecture
#Interrupt
#Therads
#Scheduling
#into a complete Operating System Simulator.

my_os = OperatingSystem(scheduler=FCFSScheduler([]))