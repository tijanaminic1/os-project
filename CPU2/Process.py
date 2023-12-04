from typing import List, Any, Dict
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
    def __len__(self):
        return len(self.data)#size of process
@dataclass
class Program:
    data: List[Process]
    bindings: Dict[str,Any]#dictionary of variable bindings for a program.

    #
    def reference(self, varname: str):
        return self.bindings.get(varname)
