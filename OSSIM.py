class CPU:

    ISA ={
        #arithmetic
        'ADD': (lambda a,b: a+b),
        'SUB': (lambda a,b: a-b),
        'DIV': (lambda a,b: a/b),
        'MULT': (lambda a,b: a*b),
        'CMP': (lambda a,b: 1 if a>b \
                else -1 if a<b else 0),
    
    #This part could be reconfigured to use 0, 1 bits
    #for False/True, but at the moment
    #This ISA is configured as-is for the sake
    #of demonstrating an instruction set.
    #Python will interpret '1 or 0' into an integer
    #boolean representation anyway.
    
        #logical operations
        'AND': (lambda a,b: a and b),
        'OR': (lambda a,b: a or b),
        'NOR': (lambda a,b: not (a or b)),
        'XOR': (lambda a,b: not a or not b),
        'NAND': (lambda a,b: not a and not b),
        # instruction operations
        'MOV': (lambda a,b: (a := b)),
        'JMP': (lambda a: self.setPC(a)) }
        #following the x86 instruction set, 
    def __init__(self):
        #Program Registers
        self.acc = 0 #Accumulator Register
        self.pc = 0 #Program Counter (NIR)
        self.ir = '' #Current Instruction Register
        self.mar = 0 #memory address register
        #Memory Data Register: Used for holding information being
        #transferred from memory to CPU, or vice versa.
        self.mdr = 0
        """"
        eax
        ebx
        ecx
        edx
        """
    #Access methods.
    def ACC(self):
        return self.acc
    def PC(self):#12345667778``
        return self.pc
    def IR(self):
        return self.ir
    def MAR(self):
        return self.mar
    def MDR(self):
        return self.mdr
    def setACC(self, new_acc):
        self.acc = new_acc
    def setPC(self, new_pc):
        self.pc = new_pc
    def setIR(self, new_ir):
        self.ir = new_ir
    def setMAR(self,new_mar):
        self.mar = new_mar
    def setMDR(self, new_mdr):
        self.mdr = new_mdr
    #process: string -> (void)
    #Purpose: processes the current instruction
    #EFFECT:
    #1. Changes the state of registers to reflect the input
    #Always changes the program counter (next instruction)
    #Always 
    def process(self,instruction):
        #jump flag
        jf = self.PC()
        instruction = instruction.split(" ")
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
class Memory:
    #Cache, Main Memory(RAM), Hard Disk (HDD)
    def __init__(self):
        self.cache=[0]*1024 #1 MB cache
        self.RAM = [0]*1024*1024
        self.disk = [0]
    def read(self, addr):
        pass
    def write(self, addr):
        pass
class Printer:
    #Display Software, and an Editor, file rwx
    #store the current working memory to a variable inside of the printer's
    #memory if writing a new file
    #if writing a saved file, use DMA to retrieve and resume writing
    #WHEN USER LAUNCHES
    #1. Welcome User!
    #(load) (filename) load a file of the given name into text editor
    #->read, write, edit (DMA)
    #(execute) (filename) will execute code on a file and output to console
    #(logout/poweroff) (turns off (closes the program))
    pass
    #Read/execute
    #CPU-process. CPU would read through the file using the printer,
    #produce an output. Output saved to memory, or printed into the console.
    #2. Memory class
    #Cache, Main Memory (RAM), Hard disk
    #Printer Class has the ability to DMA to put files into memory.