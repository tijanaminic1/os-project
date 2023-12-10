class Instruction:
    def __init__(self,*args):
        match len(args):
            case 0: #0 supplied arguments
                self.name = "NOP"
                self.arguments = []
                self.size = 0
            case 1:#1 supplied arguments
                self.name = args[0]
                self.arguments = []
                self.size = 1
            case _:# 2+supplied arguments
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
    def __len__(self):
        return self.size
@staticmethod 
def makeInstruction(str):
    word = str.split(" ")
    return Instruction(word)