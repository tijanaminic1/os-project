from typing import List, Any, Dict
from dataclasses import dataclass
from Registry import Registry
from Instruction import Instruction
@dataclass
class Process:
    data: List[Instruction]
    registers: Registry
    end = 0 
    partitions: List[int]#List of partitions the created process occupies. determined later.

    def __post_init__(self):
        self.end = sum(len(i) for i in self.data)
    #Purpose: self.data getter
    def DATA(self):
        return self.data
    #Purpose: self.registers getter
    def REGISTERS(self):
        return self.registers
    #Purpose: self.PARTITIONS getter (set associate addressing)
    def PARTITIONS(self):
        return self.partitions
    #Purpose: self.partitions setter
    def setPARTITIONS(self,value):
        self.partitions = value
    #dunder for length of Process
    def __len__(self):
        return self.end
    #dunder for making object [] usable
    def __getitem__(self,arg):
        return self.data[arg]
    #dunder for making object iterable
    def __iter__(self):
        return iter(self.data)
    #Purpose: saves the given CPU state to the Process.
    #Essential for context switching.
    def save_state(self, a_registry):
        self.registers=a_registry
    #Purpose: Gets the estimated time remaining for a job.
    def remaining_time(self):
        return len(self) - self.registers["PC"]
    def current_instruction_address(self):
        return self.registers["PC"]
    def execution_completed(self):
        return self.remaining_time()==0