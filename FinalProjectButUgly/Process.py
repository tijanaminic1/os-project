from typing import List
from dataclasses import dataclass, field
from Registry import Registry
from Instruction import Instruction
import copy
def generate_process_id():
    generate_process_id.counter += 1
    return generate_process_id.counter
generate_process_id.counter = 0  # Initializing the counter
@dataclass
class Process:
    data: List[Instruction] = field(default_factory=list)
    registers: Registry = field(default_factory=Registry)
    end = 0 
    partitions: List[int] = field(default_factory=list)#List of partitions the created process occupies. determined later.
    parent = None
    id: int = field(default_factory=generate_process_id)  # Unique ID for each process
    _id_counter = 0  # Class-level attribute to generate unique IDs

    @staticmethod
    def generate_id():
        Process._id_counter += 1
        return Process._id_counter - 1
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
    #dunder for making [] usable as set!
    def __setitem__(self,idx,val):
        self.data[idx]=val
    #dunder for making object iterable
    def __iter__(self):
        return iter(self.data)
    #Purpose: saves the given CPU state to the Process.
    #Essential for context switching.
    def save_state(self, registers):
        self.saved_registers = copy.deepcopy(registers)
    #Purpose: Gets the estimated time remaining for a job.
    def remaining_time(self):
        return len(self) - self.registers["PC"]
    def current_instruction_address(self):
        return self.registers["PC"]
    def execution_completed(self):
        return self.remaining_time()==0
    def set_address_space(self, parent_id):
        self.parent = parent_id
    def get_parent(self):
        return self.parent