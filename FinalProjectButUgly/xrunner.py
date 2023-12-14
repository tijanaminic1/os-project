from Program import Program
from Process import Process
from Instruction import Instruction
import copy
from OperatingSystem import OperatingSystem as OS

from FCFSScheduler import FCFSScheduler as FCFS
from HRNScheduler import HRNScheduler as HRRN
from RRScheduler import RRScheduler as RR
from SJFScheduler import SJFScheduler as SJF
from STRScheduler import STRScheduler as STR
from InterruptStack import InterruptStack
from CPU import CPU
from RAM import RAM
from Cache import Cache
from DMA import DMA
from CPUTimer import CPUTimer
from Decoder import Decoder
from Registry import Registry

# Create instances of each scheduler
fcfs_scheduler = FCFS()
rr_scheduler = RR(time_slice=1.0)  # Example time slice
sjf_scheduler = SJF()
hrn_scheduler = HRRN(timer=CPUTimer())
str_scheduler = STR()

# Sample program and processes
process1 = Process(data=[Instruction("ADD", 5, 3), Instruction("SUB", 10, 2), Instruction("NOP")])
process2 = Process(data=[Instruction("MUL", 4, 2), Instruction("DIV", 20, 5), Instruction("JMP", 0), Instruction("NOP")])
process3 = Process(data=[Instruction("ADD", 5, 3), Instruction("MUL", 4, 2), Instruction("DIV", 20, 5), Instruction("NOP")])
program = Program([process1, process2, process3])

#Stress program and processes
stresspress = Process(data=[Instruction("ADD",1,2,3,4,5,6,7,8,9,10,11,12,13,13,14,14,14,15),Instruction("MUL",20),Instruction("DIV",5)])
program2 = Program([copy.deepcopy(stresspress) for x in range(4)]) #TODO !!!!!range(1-10)!!!!!
# Define a program with multiple processes


cache_mem = Cache(data=None)
if __name__ == "__main__":
    test_this = "fcfs"#TODO: RUn each simulation on 1, 2, 5, 10
    match test_this:
        case "fcfs":
            os_fcfs = OS(cpu=CPU(registers=Registry(),decoder=Decoder()), ram=RAM(), cache=copy.deepcopy(cache_mem), scheduler=fcfs_scheduler, interrupt_stack=InterruptStack(), dma=DMA(), inputs=[copy.deepcopy(program2)])
            os_fcfs.start()
            os_fcfs.end_simulation()  # This will print the CPU utilization
        case "rr":
            os_rr = OS(cpu=CPU(registers=Registry(),decoder=Decoder()), ram=RAM(), cache=copy.deepcopy(cache_mem), scheduler=rr_scheduler, interrupt_stack=InterruptStack(), dma=DMA(), inputs=[copy.deepcopy(program2)])
            os_rr.start()
            os_rr.end_simulation()
        case "sjf":
            os_sjf = OS(cpu=CPU(registers=Registry(),decoder=Decoder()), ram=RAM(), cache=copy.deepcopy(cache_mem), scheduler=sjf_scheduler, interrupt_stack=InterruptStack(), dma=DMA(), inputs=[copy.deepcopy(program2)])
            os_sjf.start()
            os_sjf.end_simulation()
        case "hrn":
            os_hrn = OS(cpu=CPU(registers=Registry(),decoder=Decoder()), ram=RAM(), cache=copy.deepcopy(cache_mem), scheduler=hrn_scheduler, interrupt_stack=InterruptStack(), dma=DMA(), inputs=[copy.deepcopy(program2)])
            os_hrn.start()
            os_hrn.end_simulation()
        case _:
            os_str = OS(cpu=CPU(registers=Registry(),decoder=Decoder()), ram=RAM(), cache=copy.deepcopy(cache_mem), scheduler=str_scheduler, interrupt_stack=InterruptStack(), dma=DMA(), inputs=[copy.deepcopy(program2)])
            os_str.start()
            os_str.end_simulation()

            
        
    #os_rr.start()
    #os_sjf.start()
    #os_hrn.start()
    #os_str.start()