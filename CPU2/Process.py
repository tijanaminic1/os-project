from typing import List
from dataclasses import dataclass
from . import Registers
from Decoder import Instruction
@dataclass
class Process:
    data: List[Instruction]
    registers: Registers
    @property
    def DATA(self):
        return self.data
    @property
    def REGISTERS(self):
        return self.registers