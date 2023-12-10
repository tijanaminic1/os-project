#decoder is a class specifically
#made to decode our assembler language
#into python-executable code.

#You could call this an assembler compiler,
#Decoder, or Disassembler depending on your
#desired nomenclature.
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