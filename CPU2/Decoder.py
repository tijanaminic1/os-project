#decoder is a class specifically
#made to decode our assembler language
#into python-executable code.

#You could call this an assembler compiler,
#Decoder, or Disassembler depending on your
#desired nomenclature.
from . import Memory
import functools

class InstructionError(Exception):
    pass
#Instruction Set is mapped 1:1, so
#it is possible to use an instruction's mnemonic
#to find its hex value, and a hex value to find the mnemonic.
name_to_number = {
    #Default
    "NOP" : 0x00,
    #Arithmetic
    "ADD" : 0x01,
    "SUB" : 0x02,
    "MUL" : 0x03,
    "DIV" : 0x04,
    #Logic
    'AND': 0x05,
    'OR': 0x06,
    'NOR': 0x07,
    'XOR': 0x08,
    'NAND': 0x09,
    #Intraprocess Execution Instructions
    'MOV': 0xA,
    'RET': 0xB,#finishes execution
    'JMP': 0xC,
    'JLE': 0xD,
    'JE':  0xE,
    'JGE': 0xF,
    'JL':  0x10,
    'JG':  0x11,
    'JNE': 0x12,
    'PRINT':0x13,
    'INPN': 0x14,
    'INPS': 0x15
}
#This is the dictionary variant to go from the CPU storage # to the 
#mnemonic for the operation.
number_to_name = dict(zip(name_to_number.values(),name_to_number.keys()))


class Instruction:
    #default constructor
    def __init__(self):
        self.name = "NOP"
        self.arguments = []
        self.size = 0
    #Non-default constructor.
    def __init__(self,*args):
        if len(args) == 0:
            self.__init__()
        elif len(args) == 1:
            self.name = args[0]
            self.arguments = []
            self.size = 1
        else:
            self.name = args[0]
            self.arguments = args[1:]
            self.size = len(args)
    #mnemonic: -> string
    #purpose: returns the name of an instruction
    def mnemonic(self):
        return self.name
    #operands: -> list
    #purpose: returns the operands taken by the instruction.
    def operands(self):
        return self.arguments
    #size: -> int
    #purpose: returns the number of operands the instruction has
    def size(self):
        return self.size
@staticmethod 
def makeInstruction(str):
    word = str.split(" ")
    return Instruction(word)
class Decoder:
    #fetch: Memory + 
    def fetch(mem_loc: Memory, location: int) -> Instruction:
        try:
            return mem_loc[location]
        except IndexError:
            pass#IMPLEMENT LATER
    def decode(inst: Instruction)->(str,function, list):
        #lets me pass a no argument function.
        def helper():
            pass
        instructions = (inst.mnemonic(),(lambda: helper()),inst.operands())
        match inst:
            case Instruction(name="NOP"):
                pass #this is the proper "NOP" instruction.
            case Instruction(name="ADD"):
                return (inst.mnemonic(),(lambda a: sum(a)),inst.operands()) #We return the instruction to be executed and the operands
            case Instruction(name="SUB"):
                return (inst.mnemonic(),(lambda a: functools.reduce(lambda x,y: x-y, a,initializer=0)),inst.operands())
            case Instruction(name="DIV"):
                return (inst.mnemonic(),)
            case Instruction(name="MUL"):
                pass
            case Instruction(name="CMP"):
                pass
            case Instruction(name="AND"):
                pass
            case Instruction(name="OR"):
                pass
            case Instruction(name="NOR"):
                pass
            case Instruction(name="XOR"):
                pass
            case Instruction(name="NAND"):
                pass
            case Instruction(name="MOV"):
                pass
            case Instruction(name="RET"):
                pass
            case Instruction(name="JMP"):
                pass
            case Instruction(name="JLE"):
                pass
            case Instruction(name="JE"):
                pass
            case Instruction(name="JGE"):
                pass
            case Instruction(name="JL"):
                pass
            case Instruction(name="JG"):
                pass
            case Instruction(name="JNE"):
                pass
            case Instruction(name="PRINT"):
                pass
            case Instruction(name="INPUT"):
                pass
            case _:
                raise InstructionError
