import unittest, random
from hypothesis import example, given, settings, HealthCheck, assume
from hypothesis.strategies import integers, composite, sampled_from, lists, SearchStrategy, text, characters
from ..InstructionArchitecture import Instruction
from ..CentralProcessor import Decoder
from ..CentralProcessor import Registry

instruction_keys = ["NOP", #0
    "ADD", "SUB", "MUL", "DIV",#1-4
    "AND", "OR", "NOR", "XOR", "NAND",#5-9
    "MOV", "RET", #10-11
    "JMP", "JLE", "JE", "JGE", "JL", "JG", "JNE",#12-18
    "PRINT", "INPN", "INPS"]#19-21
mathematical = instruction_keys[1:5]
booleanalgebra = instruction_keys[5:10]
process_control = instruction_keys[10:12]
jumps = instruction_keys[12:19]
inputcontrol = instruction_keys[19:]
@composite
def random_instruction(draw):
    #The following line gets a random opcode, using its mnemonic
    #for the purposes of testing
    mnemonic = random.sample(instruction_keys,1)
    min_value=0
    max_value=100
    def m():
        return draw(integers(min_value=min_value,max_value=max_value))
    #The following line creates a set of Registers with randomly filled integer values.
    #purpose is to create a Registry to test inputs against.
    register_state = Registry(A=m(),B=m(),C=m(),D=m(),E=m(),F=m(),PC=m(),SP=m())
    test_case = (register_state,None)
    #The following decides what random data to fill the instruction with, given a the random opcode 'mnemonic'
    match mnemonic:
        case "JMP"|"JLE"|"JE"|"JGE"|"JG"|"JL"|"JNE": #gen jump test
            test_case[1] 
        case "AND"|"OR"|"NOR"|"XOR"|"NAND": #gen boolean test
            test_case[1]
        case "ADD"|"SUB"|"DIV"|"MUL": #gen math test
            test_case[1]
        case "RET": #gen RET test
            test_case[1] = NotImplemented
        case "PRINT":
            test_case[1] = text(alphabet=characters())
        case "INPUT":
            test_case[1] = "this is input block"
        case _:
            test_case[1] = []#occurs when 'nop' is random selected.
