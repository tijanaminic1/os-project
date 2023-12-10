import unittest, random
from hypothesis import example, given, settings, HealthCheck, assume
from hypothesis.strategies import integers, composite, sampled_from, lists, SearchStrategy
from ..InstructionArchitecture import Instruction
from ..CentralProcessor import Decoder
@composite
def random_instruction(draw):
    instruction_keys = ["NOP", #0
    "ADD", "SUB", "MUL", "DIV",#1-4
    "AND", "OR", "NOR", "XOR", "NAND",#5-9
    "MOV", "RET", #10-11
    "JMP", "JLE", "JE", "JGE", "JL", "JG", "JNE",#12-18
    "PRINT", "INPN", "INPS"]#19-21

    mnemonic = random.sample(instruction_keys,1)

    
    

