from typing import List, Any, Dict
from dataclasses import dataclass
from ..CentralProcessor import Registry
from .Instruction import Instruction
@dataclass
class Process:
    data: List[Instruction]
    registers: Registry
    current_instruction: int=0
    @property
    def DATA(self):
        return self.data
    @property
    def REGISTERS(self):
        return self.registers
    def __len__(self):
        return sum(len(i) for i in self.data)#size of process is the sum of the costs of each instruction.