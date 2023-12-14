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
from dataclasses import dataclass
import copy
#Threading and Lock Import
from threading import Thread, Lock
from queue import Queue
#Prettiness Imports
from dataclasses import dataclass, field
from typing import List, Optional
import traceback
import time
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
        print("Initializing system...")
        for program in self.inputs:
            for process in program.data:
                self.load_process_to_ram(process)

    def start(self):
        print("Starting OS...")
        self.thread.start()
        print("OS thread started.")
        # Keep the main thread alive for debugging
        import time
        time.sleep(30)#This is just to force the main thread to stay alive to get juicy outputs.

    def start(self):
        print("Starting OS...")
        self.thread.start()
        print("OS thread started.")
        # Keep the main thread alive for debugging
        import time
        time.sleep(30)

    def run(self):
        print("OS running...")
        while True:
            self.lock.acquire()
            try:
                if not self.process_queue.empty():
                    print("Processing a process from the queue...")
                    self.context_switch(self.process_queue.get())
                    self.execute_process(self.current_process)
                    self.process_queue.task_done()
                else:
                    print("Queue is empty...")
            except Exception as e:
                print(f"Error in run method: {type(e).__name__}, {e}")
                traceback.print_exc()
            finally:
                self.lock.release()
            time.sleep(1)
    def load_process_to_ram(self, process: Process):
        print(f"Loading process {process} into RAM... Size: {len(process)}")
        try:
            self.ram.write(process)
            self.processes.append(process)
        except Interrupt as e:
            print(f"Error loading process to RAM: {e}")
        else:
            self.load_process(process)

    def load_process(self, process: Process):
        print(f"Attempting to load process {process.id} from RAM to Cache... Size: {len(process)}")
        lock_acquired = False
        try:
            if self.cache.allocable(len(process.data)):
                self.cache.allocate(process)
                print(f"Process {process.id} allocated in cache. Cache status: {self.cache.blocks_free()} blocks free.")
                self.lock.acquire()
                lock_acquired = True
                self.scheduler.add_process(process)
                self.process_queue.put(process)
                self.timer.add_process(process.id)
                print(f"Process {process.id} added to queue.")
            else:
                print("Not enough space in cache. Cache status: {self.cache.blocks_free()} blocks free.")
        except Interrupt as e:
            print(f"Error loading process to Cache: {e}")
        finally:
            if lock_acquired:
                self.lock.release()

    def context_switch(self, process: Process):
        print(f"Context switching to process {process.id} with parent {process.get_parent()}")
        if self.current_process:
            self.save_state(self.current_process)
        self.current_process = process
        self.restore_state(process)

    def save_state(self, process: Process):
        # Save the state of the CPU registers to the process
        process.save_state(self.cpu.registers)

    def restore_state(self, process: Process):
        # Restore the state of the CPU registers from the process
        if process.registers:
            self.cpu.registers = process.registers
    """
    def execute_process(self, process: Process):
        self.timer.start(process)
        try:
            while not process.execution_completed():
                address = process.current_instruction_address()
                self.cpu.cycle(address, self.cache)
        except Interrupt as e:
            self.interrupt_stack.push(e)
            self.HANDLE_INTERRUPT_STACK()
        except Exception as e:
            print(f"Error during process execution: {e}")
        finally:
            self.free_cache_blocks(process)  # Free cache blocks used by the process
            self.timer.stop(process)
            self.report_completion(process)
    """
    def execute_process(self, process: Process):
        self.timer.start(process)
        try:
            while not process.execution_completed():
                address = process.current_instruction_address()
                instruction = self.cpu.fetch(address, self.cache)  # Fetch instruction
                decoded = self.cpu.decode(instruction)  # Decode instruction
                self.cpu.execute(decoded)  # Execute instruction
                # Handle any interrupts that may have occurred
                # ...

        except Interrupt as interrupt:
            self.interrupt_stack.push(interrupt)
            self.HANDLE_INTERRUPT_STACK()
        finally:
            self.timer.stop(process)
            self.report_completion(process)

    def free_cache_blocks(self, process: Process):
        for block_number in process.partitions:  # Assuming process tracks its cache partitions
            self.cache.blocks[block_number].free()
    """
    def report_completion(self, process: Process):
        wait_time = self.timer.get_wait_time(process)
        turnaround_time = self.timer.get_turnaround_time(process)
        arrival_time = process.arrival_time
        print(f"Process {process.id}: Wait Time={wait_time}, Turnaround Time={turnaround_time}, Arrival Time={arrival_time}")
    """
    """
    def report_completion(self, process: Process):
        wait_time = self.timer.get_wait_time(process)
        turnaround_time = self.timer.get_turnaround_time(process)
        arrival_time = self.timer.metrics[process.id].arrival_time  # Use arrival time from CPUTimer
        print(f"Process {process.id}: Wait Time={wait_time}, Turnaround Time={turnaround_time}, Arrival Time={arrival_time}")
    """
    def report_completion(self, process: Process):
        wait_time = self.timer.get_wait_time(process)
        turnaround_time = self.timer.get_turnaround_time(process)
        arrival_time = self.timer.metrics[process.id].arrival_time  # Use arrival time from CPUTimer
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
        try:
            interrupt = interruptstack.pop()
            OperatingSystem.HANDLE(interrupt)
        except Exception as e:
            print(f"Error handling helper: {e}")
    def HANDLE_INTERRUPT_STACK(self):
        while len(self.interrupt_stack)>0:
            OperatingSystem.HANDLEHELPER()
    def debug_print_queue(self):
        with self.lock:
            queue_contents = list(self.process_queue.queue)
            print("Current Queue Contents:", queue_contents)
"""
def test_threading():
    print("Testing basic threading...")
    def test_function():
        while True:
            print("Thread is running...")
            time.sleep(1)

    test_thread = Thread(target=test_function)
    test_thread.start()
    time.sleep(30)

# Uncomment to test basic threading
#test_threading()
"""