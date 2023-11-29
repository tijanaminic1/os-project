from typing import List
from . import Instruction, Registers
class Process:
    def __init__(self, data: List[Instruction], registers: Registers):
        self.data = data
        self.registers = registers
    