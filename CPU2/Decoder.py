from . import Memory, Interrupt
import functools

#decoder is a class specifically
#made to decode our assembler language
#into python-executable code.

#You could call this an assembler compiler,
#Decoder, or Disassembler depending on your
#desired nomenclature.
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
        def NOP():
            pass
        instructions = (inst.mnemonic(),(lambda: NOP()),inst.operands())
        match inst:
            case Instruction(name="NOP"):
                pass #this is the proper "NOP" instruction.
            case Instruction(name="ADD"):
                instructions[1] = (lambda a: sum(a))#We return the instruction to be executed and the operands
            case Instruction(name="SUB"):
                instructions[1] = (lambda a: functools.reduce(lambda x,y: x-y,a,initializer=0))
            case Instruction(name="DIV"):
                instructions[1] = (lambda a: functools.reduce(lambda x,y: x/y,a,initializer=0))
            case Instruction(name="MUL"):
                instructions[1] = (lambda a: functools.reduce(lambda x,y: x*y,a, initializer=0))
            case Instruction(name="CMP"):
                instructions[1] = (lambda a,b: 1 if a>b \
                    else -1 if a<b else 0)
            case Instruction(name="AND"):
                instructions[1] = (lambda x,y: x and y)
            case Instruction(name="OR"):
                instructions[1] = (lambda x,y: x or y)
            case Instruction(name="NOR"):
                instructions[1] = (lambda x,y: not (x or y))
            case Instruction(name="XOR"):
                instructions[1] = (lambda x,y: True if ((x and not y) or (y and not x)) else False)
            case Instruction(name="NAND"):
                instructions[1] = (lambda x,y: not (x and y))
            case Instruction(name="MOV"):
                pass
            case Instruction(name="RET"): #terminates the execution of a procedure and transfers control through a back-link on the stack to the program that originally invoked the procedure
                pass
            case Instruction(name="JMP"):
                instructions[1] = (lambda a,b: b)
            case Instruction(name="JLE"):#If val(SP) <= 0 then change Program Counter
                instructions[1] = (lambda a,b: b if a<=0 else None)
            case Instruction(name="JE"):
                instructions[1] = (lambda a,b: b if a==0 else None)
            case Instruction(name="JGE"):
                instructions[1] = (lambda a,b: b if a>=0 else None)
            case Instruction(name="JL"):
                instructions[1] = (lambda a,b: b if a<0 else None)
            case Instruction(name="JG"):
                instructions[1] = (lambda a,b: b if a>0 else None)
            case Instruction(name="JNE"):
                instructions[1] = (lambda a,b: b if a!=0 else None)
            case Instruction(name="PRINT"):
                instructions[1] = (lambda: Interrupt("PRINT"))
            case Instruction(name="INPUT"):
                instructions[1] = (lambda: Interrupt("INPUT"))
            case _:
                raise InstructionError
