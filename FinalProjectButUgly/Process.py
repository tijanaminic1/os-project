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
    @property
    def DATA(self):
        return self.data
    @property
    def REGISTERS(self):
        return self.registers
    @property
    def PARTITIONS(self):
        return self.partitions
    def setPARTITIONS(self,value):
        self.partitions = value
    def __len__(self):
        return self.end
    def __getitem__(self,arg):
        return self.data[arg]
    def __iter__(self):
        return iter(self.data)
    #Purpose: saves the given CPU state to the Process.
    #Essential for context switching.
    def save_state(self, a_registry):
        self.registers=a_registry
    #Purpose: Gets the estimated time remaining for a job.
    @property
    def remaining_time(self):
        return len(self) - self.registers["PC"]