import sys
"""
read (proper usage):
CPU and Printer can use freely
write (proper usage):
CPU and Printer may use freely
process (execute):
this is a cpu-exclusive function for
executing assembler written in the printer's format
printers format would look like the following
MOV 10 eax
MULT 10 eax -> ACC = 100
MOV ACC eax

"""
#an Interrupt is an object
#representing a system interrupt, it also sends a strategy to
#the OSSIM to handle said interrupt, by signing its name.
class Interrupt:
    def __init__(self, str, args):
        self.interrupt = str
        self.args = args

class Memory:
    #Cache, Main Memory(RAM)
    def __init__(self):
        self.cache=[None]*512 #"512 KB" cache
        self.ram = [None]*1024 #"1 MB" RAM
    def RAM(self):
        return self.ram
    #Cache functions
    def CACHE(self):
        return self.cache
    #Purpose: Frees the memory on the given interval
    def FREE(self,memory_loc,start,end):
        for x in range(start-end):
            memory_loc[x+start] = None
    def READ(self,start,end):
        try:
            if start - end > len(self.cache):#if the resulting memory segment can't be on the cache
                mem = self.ram[start:end] #grab it from the RAM
                self.FREE(self.ram,start,end)
                return mem
            else:
                mem = self.cache[start:end]
                self.FREE(self.cache,start,end)
                return mem
        except IndexError:
            return Interrupt("MemoryDNE")
    def WRITE(self,start,end):
        try:
            


class CPU:
    
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
    #Designed this way so that the dictionary calls a function
    #rather than being passed a reference, so that it can automatically
    #update as the CPU executes code
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
    def fetch(self,memoryloc,idx):
        return memoryloc[idx]
    #decode: Instruction -> list[opcode,operand, operand, ...]
    #Purpose: Decodes an instruction passed to this function into
    #one operable by the CPU.
    def decode(self,instruction):
        line = instruction.split(" ")
        opcode = line[0]
        operand1 = None
        operand2 = None
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
                self.execute(operation[0],operation[1],operation[2])
                #the following code is structured as is to handle jumps.
                if jf == self.PREG("PC"):
                    self.iterate()
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
    class OSSIM:
        #An OSSIM is a simple, simulated operating system.
        #It includes a CPU, Memory, and its own dedicated storage system to manage memory buffers
        #across the cache and RAM.
        def __init__(self):
            self.cpu = CPU()
            self.memory = Memory()
            buffers = [] #Essentially a program call stack. Applications, processes, and scripts queue up for CPU time.
            current = None #the current buffer, which contains a program, or operation.
        #Memory Manager
        def addBuffer(self,start,end):
            return {"start":start,"end":end}
        #Interrupt Handler
        def InterruptHandler(self,inter):
            if inter == Interrupt("MemoryDNE"):
                print("Operation cannot be read from buffer. Terminating program.")

            elif inter == Interrupt("InputNumber"):
                self.cpu.setREG("UNR",input())
            elif inter == Interrupt("InputString"):
                self.cpu.setREG("USR",input())
            elif inter == Interrupt("RET"):
                print("Program Complete! Result:")
                print(self.cpu.PREG("ACC"))
                if len(self.buffers) > 0:
                    self.current = self.buffers.pop(0)
                   

        pass
    #Design Process:
    #1. Printer Class
    #-> R/W files
    #-->when writing a new file, DMA-process
    #-->text typed is stored to main memory via DMA
    #-->text can then be saved into hard disk
