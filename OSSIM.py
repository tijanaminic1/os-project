import sys
from typing import List
class Interrupt:
    def __init__(self, str, args):
        self.interrupt = str
        self.args = args
class CPU:
        #following the x86 instruction set, 
    def __init__(self):
        #ten general purpose registers, named as:
        #EAX,EBX,ECX,EDX,RE4,RE5,RE6,RE7,USR,UNR
        self.reg = [0]*10
        #As for Program Registers, there will be 6
        self.preg = [0]*6
        #preg[0] = ACC = ACCUMULATOR REGISTER
        #preg[1] = PC/NIR = PROGRAM COUNTER/NEXT INSTRUCTION REGISTER
        #preg[2] = IR = CURRENT INSTRUCTION REGISTER
        #preg[3] = MAR = MEMORY ADDRESS REGISTER
        #preg[4] = MDR = MEMORY DATA REGISTER
    #hitReg: register name, registry -> int
    #Purpose: Returns the index of the program registry on the CPU
    def hitReg(self,register,registry):
        return registry.index(register)
    #PREG: reg name -> data
    #Purpose: gets the data stored on the given program register
    def PREG(self, register):
        return self.preg[self.hitReg(register,["ACC","PC","IR","MAR","MDR"])]
    #Purpose: mutates the given register to the given value
    def setPREG(self, register,value):
        self.preg[self.hitReg(register,["ACC","PC","IR","MAR","MDR"])] = value
    #REG: string -> value
    #Purpose: Gets the value of the specified register.
    def REG(self, register):
        if register == "ACC":
            return self.preg[0]
        else:
            return self.reg[self.hitReg(register,["EAX","EBX","ECX","EDX","RE4","RE5","RE6","RE7","USR","UNR"])]
    def setREG(self, register, value):
        if value in ["EAX","EBX","ECX","EDX","RE4","RE5","RE6","RE7","USR","UNR"]:
            self.reg[self.hitReg(register,["EAX","EBX","ECX","EDX","RE4","RE5","RE6","RE7","USR","UNR"])] = self.REG(value)
        elif value == "ACC":
            self.reg[self.hitReg(register,["EAX","EBX","ECX","EDX","RE4","RE5","RE6","RE7","USR","UNR"])] = self.PREG(value)
        else:
            self.reg[self.hitReg(register,["EAX","EBX","ECX","EDX","RE4","RE5","RE6","RE7","USR","UNR"])] = value
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
    #serves to iterate the program counter
    def iterate(self):
        self.setIR(self.PREG("PC")) #increment current instruction register
        self.setPC(self.PREG("PC")+1) #increment program counter
    ##FDE Cycle
    #int -> datum
    #Purpose: Given a place to fetch memory from (cache,ram),
    #return the instruction arriving from said idx.
    def fetch(self,memoryloc: List,idx):
        return memoryloc[idx]
    #decode: Instruction -> list[opcode,operand, operand, ...]
    #Purpose: Decodes an instruction passed to this function into
    #one operable by the CPU.
    def decode(self,instruction):
        line = instruction.split(" ")
        opcode = line[0]
        inst = [opcode] #decoded instructions
        #parseOperand: string -> operand
        #Purpose: Converts a segment of OSSembler operand code. Valid OSSembler operands are registers, integers, and floats
        def parseOperand(item):
            if item not in self.ISA.keys():
                if "." in item:
                    try:
                        return float(item)
                    except ValueError:
                        return item
                else:
                    try:
                        return int(item)
                    except ValueError:
                        return item
            else:
                return item
        if len(line) == 3:
            inst.append(parseOperand(line[1]))
            inst.append(parseOperand(line[2]))
            return inst
        elif len(line)==2:
            inst.append(parseOperand(line[1]))
            return inst
        else:
            return inst
    #execute: opcode, operand, operand -> (Effect)
    #Purpose: Performs the CPU-operable instruction
    #Instructions have various effects, I suggest reading
    #the instruction set. Generally the instructions
    def execute(self,opcode,operand1,operand2):
        if operand1 is None:
            self.ISA[opcode]()
        elif operand2 is None:
            self.ISA[opcode](operand1)
        else:
            self.ISA[opcode](operand1,operand2)
    #process: string -> (void)
    #Purpose: processes the current instruction
    #EFFECT:
    #Changes the state of registers to reflect the input
    #Always changes the program counter (next instruction)
    def process(self,instruction,memoryset):
        #jump flag
        jf = self.PREG("PC")
        while True:
            try:
                operation = self.decode(self.fetch(memoryset,instruction))
                if operation[0] not in ["ADD","SUB","DIV","MULT","CMP","AND","OR","NOR","XOR","NAND"]:
                    self.execute(operation[0],operation[1],operation[2])
                else:
                    self.setACC(self.execute(operation[0],operation[1],operation[2]))
                #the following code is structured as is to handle jumps.
                if jf == self.PREG("PC"):
                    self.iterate()
                    self.process(self.PREG("IR"),memoryset)
                else:
                    t = self.PREG("PC")
                    self.setIR(t)
                    self.setPC(t+1)
                    self.process(self.PREG("IR"),memoryset)
            except IndexError:
                break
    #Instruction Set Architecture
    def ISA(self):
        my_architecture = {
            #register access:
            'ACC': self.PREG("ACC"),
            'IR': self.PREG("IR"),
            'EAX': self.REG("EAX"),
            'EBX': self.REG("EBX"),
            'ECX': self.REG("ECX"),
            'EDX': self.REG("EDX"),
            'RE4': self.REG("RE4"),
            'RE5': self.REG("RE5"),
            'RE6': self.REG("RE6"),
            'RE7': self.REG("RE7"),
            'USR': self.REG("USR"),
            "UNR": self.REG("UNR"),
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
            'MOV': (lambda a,b: self.setREG(a,b)),
            'RET': Interrupt("RET"),#finishes execution
            'JMP': (lambda a: self.setPC(a)),
            'JLE': (lambda a: self.setPC(a) if self.PREG("ACC") <= 0 else None),
            'JE': (lambda a: self.setPC(a) if self.PREG("ACC") == 0 else None),
            'JGE': (lambda a: self.setPC(a) if self.PREG("ACC") >= 0 else None),
            'JL': (lambda a: self.setPC(a) if self.PREG("ACC") < 0 else None),
            'JG': (lambda a: self.setPC(a) if self.PREG("ACC") == 1 else None),
            'JNE': (lambda a: self.setPC(a) if not self.PREG("ACC") == 0 else None),
            #I/O
            'PRNT': (lambda a: print(a)),
            'INPN': Interrupt("InputNumber"),#(lambda a,b: self.setREG(a,input())) }
            'INPS': Interrupt("InputString")}
class Memory:
    #Cache, Main Memory(RAM)
    def __init__(self):
        self.cache=[None]*512 #"512 KB" cache
        self.ram = [None]*10 #"10 MB" RAM. Represented as such
        #because RAM will be a list of program states, {"CPU_State":CPU,"INSTRUCTIONS":instructions}
    def RAM(self):
        return self.ram
    #Cache functions
    def CACHE(self):
        return self.cache
#TODO: needs
#InterruptHandler
#Memory Management
#
class OSSIM:
    def __init__(self):
        self.memory = Memory()
        self.cache = self.memory.cache #Cache is always a list of instructions
        self.RAM = self.memory.ram #RAM is always a list of program states
        self.CPU = CPU()
        self.cacheptr = 0
    def cacheToRAM(self,start,end):
        if not self.cache[9] == None:
             self.InterruptHandler(Interrupt("RAMFull"))
        else:
            for x in range(len(self.cache)):
                if x == None:
    def lineToCache(self,start,end):
    #performs a DMA operation
    def DMA(self,file,location):


    def InterruptHandler(self, i: Interrupt):

        pass
#Consider the main to be the Operating System's kernel,
#I always assume that enough CPU resources are available
#to submit commands to the kernel, as well as to execute it
#because otherwise the code would get /very/ messy for this
#simple uniprogramming operating system.
if __name__ == "__main__":
    os = OSSIM()
    programs = ["open","execute","touch","append"] #and bye

    print("Hello user! Welcome to OSSIM, the only Operating System to use the OSSembler Architecture.")
    while True:
        uinput = input().split(" ")
        if uinput[0] not in programs and not uinput[0] == "bye":
            print("Unrecognized program. System update (hopefully) coming soon.")
            print("Please use a supported application, such as open, execute, author, or append. You may submit bye to logout.")
        elif uinput[0] == "bye":
            sys.close()
        elif len(uinput) > 1:
            if uinput[0] in programs:
                    try:
                        if uinput[0] == "open": #prints contents of file to interface
                            print("Contents of "+ uinput[1] + ":")
                            print("========================")
                            with open(uinput[1], 'r') as fin:
                                print(fin.read())
                            print("========================")
                        elif uinput[0] == "touch": #makes new file of given name
                            pass
                        elif uinput[0] == "append":#opens existing file 
                            with open(uinput[1], 'a+') as fin:
                                fin.writelines(input(uinput[1] + " opened. Enter line to append to document."))
                            print("=============File updated.===============")
                        else:#execute runs a file using the CPU

                            with open(uinput[1], 'r') as fin:
                                for line in fin:
                                    ###


                    except IOError:
                        inter = Interrupt("FileNotFound")
                    

