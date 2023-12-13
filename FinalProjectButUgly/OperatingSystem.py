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
            self.lock.acquire()#mutexclustion guaranteed with lock
            if not self.process_queue.empty():#if there are processes to process
                self.context_switch(self.process_queue.get())#get the first process on the queue
                self.execute_process(self.current_process)#execute it
                self.process_queue.task_done()#mark the task as complete
            self.lock.release() #lock released by program after execution completes.

    def load_process(self, process: Process):#Why are both run() and load_process() managing the Lock()?
        self.lock.acquire()#acquire the lock
        self.processes.append(process)#append the process to the processes
        self.scheduler.add_process(process)#schedule the process
        self.process_queue.put(process)#add the process to the process_queue
        self.lock.release()#release the lock

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

                
            #TODO: #1 Look for cases where this may cause an infinite loop.
            #These can be found by looking at Interrupt.HANDLE in Interrupt.py
            #We want strong invariants for our Handle function so that we can
            #reliably service nested interrupts.
    #HANDLESTACK: -> Effect!
    #Purpose: Tries to service the interrupt stack.