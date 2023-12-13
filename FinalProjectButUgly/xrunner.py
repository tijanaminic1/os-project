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
# Example instructions
add_instruction = Instruction("ADD", 5, 3)  # Adds 5 and 3
sub_instruction = Instruction("SUB", 10, 2) # Subtracts 2 from 10
mul_instruction = Instruction("MUL", 4, 2)  # Multiplies 4 and 2
div_instruction = Instruction("DIV", 20, 5) # Divides 20 by 5
jmp_instruction = Instruction("JLE", 0)     # Jump to the beginning
nop_instruction = Instruction("NOP")        # Does nothing

# Process with simple arithmetic operations
process1 = Process([add_instruction, sub_instruction, nop_instruction])

# Process with more complex operations
process2 = Process([mul_instruction, div_instruction, jmp_instruction, nop_instruction])

# Process with mixed operations
process3 = Process([add_instruction, mul_instruction, div_instruction, nop_instruction])

# Define a program with multiple processes
program = Program([process1, process2, process3])
program2 = copy.deepcopy(program)
program3 = copy.deepcopy(program)
program4 = copy.deepcopy(program)
program5 = copy.deepcopy(program)

if __name__ == "__main__":
    fcfs = OS(cpu=CPU(), ram=RAM(),cache=Cache(),scheduler=FCFS(),interrupt_stack=InterruptStack(),dma=DMA(),processes=[],)