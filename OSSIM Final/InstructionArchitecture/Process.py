from typing import List, Any, Dict
from dataclasses import dataclass
from ..CentralProcessor import Registry
from .Instruction import Instruction
@dataclass
class Process:
    data: List[Instruction]
    registers: Registry
    @property
    def DATA(self):
        return self.data
    @property
    def REGISTERS(self):
        return self.registers
    def __len__(self):
        return len(self.data)#size of process