#Central Processor Imports
from CPU import CPU
from Decoder import Decoder
from Registry import Registry
#Memory Imports
from RAM import RAM 
from Cache import Cache
from DMA import DMA
from Process import Process
from Program import Program
#Interrupts
from InterruptStack import InterruptStack
from Interrupt import Interrupt
#Scheduling
from SchedulerTemplate import Scheduler
from CPUTimer import CPUTimer
from FCFSScheduler import FCFSScheduler as FirstComeFirstServe
from HRNScheduler import HRNScheduler as HighestRatio
from RRScheduler import RRScheduler as RoundRobin
from SJFScheduler import SJFScheduler as ShortestJobFirst
from STRScheduler import STRScheduler as ShortestTimeRemaining
from dataclasses import dataclass
import copy
#Threading and Lock Import
from threading import Thread, Lock
from queue import Queue
#Prettiness Imports
from dataclasses import dataclass, field
from typing import List, Optional
class OperatingSystem:
    def __init__(self, cpu, ram, cache, scheduler, interrupt_stack, dma, processes=None, inputs=None):
        self.cpu = cpu
        self.ram = ram
        self.cache = cache
        self.scheduler = scheduler
        self.interrupt_stack = interrupt_stack
        self.dma = dma
        self.processes = processes if processes is not None else []
        self.inputs = inputs if inputs is not None else []
        self.process_queue = Queue()
        self.current_process = None
        self.timer = CPUTimer()
        self.lock = Lock()
        self.thread = Thread(target=self.run, daemon=True)
        self.initialize_system()

    def initialize_system(self):
        # Load programs and their processes into RAM
        for program in self.inputs:
            for process in program.data:
                self.load_process_to_ram(process)
    def initialize_system(self):
        for program in self.inputs:
            for process in program.data:
                self.load_process_to_ram(process)
    def load_process_to_ram(self, process: Process):
        try:
            self.ram.write(process)
        except Interrupt as e:
            print(f"Error loading process to RAM: {e}")
            return
        self.processes.append(process)
    def start(self):
        self.thread.start()

    def run(self):
        while True:
            self.lock.acquire()#mutexclustion guaranteed with lock
            if not self.process_queue.empty():#if there are processes to process
                self.context_switch(self.process_queue.get())#get the first process on the queue
                self.execute_process(self.current_process)#execute it
                self.process_queue.task_done()#mark the task as complete
            self.lock.release() #lock released by program after execution completes.

    def load_process(self, process: Process):
        # Load process from RAM to Cache before execution
        if self.cache.allocable(len(process)):  # Check if cache has space
            try:
                self.cache.allocate(process)  # Load process to cache
                # Continue with existing load_process logic
                self.lock.acquire()  # Acquire the lock
                self.processes.append(process)  # Append the process to the processes
                self.scheduler.add_process(process)  # Schedule the process
                self.process_queue.put(process)  # Add the process to the process_queue
                self.lock.release()  # Release the lock
            except Interrupt as e:
                print(f"Error loading process to Cache: {e}")
        else:
            print("Not enough space in cache")

    def context_switch(self, process: Process):
        if self.current_process:#If current_process is a Process
            self.save_state(self.current_process)#save its state
        self.current_process = process#switch the current process to the input
        self.restore_state(process)#update the CPU Register to pick up where the task left off.

    def execute_process(self, process: Process):
        self.timer.start(process)
        # Process execution logic: Fetch, Decode, Execute cycle
        while not process.execution_completed():#While the process is not finished --- Shouldn't the Processbe controlled by the Scheduler?
            try:
                address = process.current_instruction_address()#address = current instruction address (Bug?)
                self.cpu.cycle(address,self.cache) #A CPU cycle
            except Interrupt as e:
                self.interrupt_stack.push(e)
                OperatingSystem.HANDLE_INTERRUPT_STACK()
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

    #HANDLE: Interrupt -> Effect!
    #Purpose: When an interrupt is signalled,
    #the HANDLE(Interrupt) function defines an
    #approach to deal with the particular interrupt
    def HANDLE(self, interrupt: Interrupt):
        match interrupt:
            case Interrupt(name="PRINT"):
                print(interrupt.MESSAGE())
            case Interrupt(name="INPUT"):
                input(interrupt.MESSAGE())
            case Interrupt(name="DMAIndexOutOfBounds"): #This is also a type of Page Fault
                print("DMA failed! Entry does not exist.")
            case Interrupt(name="ProcessTooLarge"):#TODO: Generally a fatal error, unless we do VRAM.
                print("Process too large to fit in the cache!")
            case Interrupt(name="CacheBottleneck"):#TODO: Integrate this with scheduling algorithm. It is a scheduling issue.
                print("Not enough space to fit"f" {interrupt.MESSAGE()} right now.")
            case Interrupt(name="CacheMiss"):
                try:
                    return self.current_process[interrupt.MESSAGE()["PC"]]
                except Exception:
                    raise Interrupt("Segmentation Fault")
            case Interrupt(name="MOV interrupt"):
                DMA.SEND(self.current_process,interrupt.MESSAGE())
            case Interrupt(name="Process-controlled Termination"):
                print("Process under "f"{self.current_process.parent()} finished.")
            case Interrupt(name="WriteOutOfBounds"):
                print("Write out of bounds")
            case Interrupt(name="ReadOutOfBounds"):
                print("Read Out of Bounds")
            case Interrupt(name="PageFault"):
                print("Page fault")
            case Interrupt(name="RAMCapacityWarning"):
                print("RAM capacity warning")
            case Interrupt(name="SegmentationFault"):
                print("Segmentation Fault")


    @staticmethod
    def HANDLEHELPER(interruptstack: InterruptStack):
        interrupt = interruptstack.pop()
        try:
            OperatingSystem.HANDLE(interrupt)
        except Interrupt as e:
            OperatingSystem.HANDLE(e)
            OperatingSystem.HANDLE(interrupt)
    def HANDLE_INTERRUPT_STACK(self):
        while len(self.interrupt_stack)>0:
            OperatingSystem.HANDLEHELPER()

     