import sys
class CPU:
    #Instruction Set Architecture
    ISA ={
        #register access:
        'IR': self.IR(),
        'EAX': self.getReg("EAX"),
        'EBX': self.getReg("EBX"),
        'ECX': self.getReg("ECX"),
        'EDX': self.getReg("EDX"),
        'RE4': self.getReg("RE4"),
        'RE5': self.getReg("RE5"),
        'RE6': self.getReg("RE6"),
        'RE7': self.getReg("RE7"),
        'USR': self.getReg("USR"),
        "UNR": self.getReg("UNR"),
        #arithmetic:
        'ADD': (lambda a,b: a+b),
        'SUB': (lambda a,b: a-b),
        'DIV': (lambda a,b: a/b),
        'MULT': (lambda a,b: a*b),
        'CMP': (lambda a,b: 1 if a>b \
                else -1 if a<b else 0),
        #logical operations
        'AND': (lambda a,b: a and b),
        'OR': (lambda a,b: a or b),
        'NOR': (lambda a,b: not (a or b)),
        'XOR': (lambda a,b: not a or not b),
        'NAND': (lambda a,b: not a and not b),
        # instruction operations
        'MOV': (lambda a,b: (a := b)),
        'RET': self.PREG("ACC"),#Returns the result of the most recent operation on ACC
        'JMP': (lambda a: self.setPC(a)),
        'JLE': (lambda a: self.setPC(a) if self.PREG("ACC") <= 0),
        'JE': (lambda a: self.setPC(a) if self.PREG("ACC") == 0),
        'JGE': (lambda a: self.setPC(a) if self.PREG("ACC") >= 0),
        'JL': (lambda a: self.setPC(a) if self.PREG("ACC") < 0),
        'JG': (lambda a: self.setPC(a) if self.PREG("ACC") == 1),
        'JNE': (lambda a: self.setPC(a) if not self.PREG("ACC") == 0),
        #I/O
        'PRNT': (lambda a: print(a)),
        'INPT': (lambda a,b: setREG(a,input()))
        }
        #following the x86 instruction set, 
    def __init__(self):
        #some immediate cache registers
        #this is modeled off of x86 architecture,
        #but it'd be overkill to emulate all x86 registers.
        #there are going to be 10 of them, named as:
        #EAX,EBX,ECX,EDX,RE4,RE5,RE6,RE7,USR,UNR
        self.reg = [0]*10
        #As for Program Registers, there will be 6
        self.preg = [0]*6
        #preg[0] = ACC = ACCUMULATOR REGISTER
        #preg[1] = PC/NIR = PROGRAM COUNTER/NEXT INSTRUCTION REGISTER
        #preg[2] = IR = CURRENT INSTRUCTION REGISTER
        #preg[3] = MAR = MEMORY ADDRESS REGISTER
        #preg[4] = MDR = MEMORY DATA REGISTER
    #Access methods.
    #getRegister ("getReg")
    #Designed this way so that the dictionary calls a function
    #rather than being passed a reference, so that it can automatically
    #update as the CPU executes code
    def PREG(self, register):
        reglist = ["ACC","PC","IR","MAR","MDR"]
        return self.preg[reglist.index(register)]
    def setPREG(self, register,value):
        ISA[register] = value
    #REG: string -> value
    #Purpose: Gets the value of the specified register.
    def REG(self, register):
        reglist = ["EAX","EBX","ECX","EDX","RE4","RE5","RE6","RE7","USR","UNR"]
        return self.reg[reglist.index(register)]
    def setREG(self, register, value):
        ISA[register] = value
    def setACC(self, new_acc):
        self.preg[0] = new_acc
    def setPC(self, new_pc):
        self.preg[1] = new_pc
    def setIR(self, new_ir):
        self.preg[2] = new_ir
    def setMAR(self,new_mar):
        self.preg[3] = new_mar
    def setMDR(self, new_mdr):
        self.preg[4] = new_mdr
    #process: string -> (void)
    #Purpose: processes the current instruction
    #EFFECT:
    #Changes the state of registers to reflect the input
    #Always changes the program counter (next instruction)
    def process(self,instruction):
        #jump flag
        jf = self.PREG("PC")
        line = instruction.split(" ")
        opcode = line[0]
        operand1 = ""
        operand2 = ""
        #parseOperand: string -> operand
        #Purpose: Converts a segment of OSSembler operand code. Valid OSSembler operands are registers, integers, and floats
        def parseOperand(item):
            if item not in ISA.keys():
                if "." in item:
                    return float(item)
                else:
                    return int(item)
            else:
                return item

        if len(line) == 3:
            operand1 = parseOperand(line[1])
            operand2 = parseOperand(line[2])
            op = 3
        elif len(line) == 2:
            operand1 = parseOperand(line[1])
            op = 2
        if op == 3:
            ISA[opcode](operand1,operand2)
        elif op == 2:
            ISA[opcode](operand1)
        #first element is instruction
        #second element is operand 1
        #third is operand 2

        #ISA[instruction[0]]()
        pass
    #Design Process:
    #1. Printer Class
    #-> R/W files
    #-->when writing a new file, DMA-process
    #-->text typed is stored to main memory via DMA
    #-->text can then be saved into hard disk
