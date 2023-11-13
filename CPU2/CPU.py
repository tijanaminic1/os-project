from dataclasses import dataclass
from . import Registers, Decoder, Interrupt, Memory, ReadyQueue
from Decoder import Instruction, InstructionError
from ReadyQueue import CustomThread, Scheduler, ReadyQueue
@dataclass
class CPU:

    registers: Registers
    decoder: Decoder
    cache: Memory
    RAM: Memory
    #fetch: int -> Instruction
    #purpose: gets the instruction stored at the given memory location
    def fetch(self, address)-> Instruction:
        return self.decoder.fetch(self.cache, address)
    #decode: Instruction -> Tuple
    #purpose: Decodes an instruction into its mnemonic, 
    #effects, and locates its operands
    def decode(self,inst: Instruction)->(str,function,list):
        return self.decoder.decode(inst)
    
    #InterruptHandler: Interrupt -> Any
    #Purpose: Handles interrupts
    def InterruptHandler(i: Interrupt):
        match i:
            case Interrupt(name="PRINT"):
                print(i.items())
            case Interrupt(name="INPUT"):
                input(i.items())
            case Interrupt(name="DMAFatalError"):
                print("DMA failed due to fatal error.")
            case Interrupt(name="DMAIndexOutOfBounds"):
                print("DMA failed! Entry does not exist.")
    #Execute: Instruction -> EFFECT!
    #Purpose: Attempts to execute the given instruction, making use
    #of the Decoder in opcode_parser.py to decode the instruction
    #EFFECT!: Based off of the given Instruction, code will be executed
    #that modifies the CPU state relevant to the Instruction's significance
    #within the opcode vocabulary.
    def execute(self, instruction: (str,function,list) ):
        reglist = ["A","B","C","D","E","F","PC","SP"] 
        operands = instruction[2]
        fun = instruction[1]
        #Check operand1's immediate flag
        immediate = True
        if len(operands) > 0 and operands[0] in reglist:
            immediate = False
        
        #This block translates instructions involving registers.
        #for example, 'ADD A B' would need to find the register
        #values of A and B and pass them.
        #It skips the first value of operands because the first
        #value of operands would be a destination register or immediate.
        #Thus if A was 1 and B was 3, it would become:
        #ADD A 3, or "add 3 to the A register"
        #Effect!: On matched case, the list is updated such that register references
        #are passed by their value.
        def pass_values(l: list) -> list:
            a = 1
            while a < len(operands):
                if l[a] in reglist:
                    l[a] = self.registers.__getitem__(l[a])
                a = a+1
        def execute_instruction():
            if immediate:
                self.registers.__setitem__("SP",fun(operands))
            else:
                self.registers.__setitem__(operands[0],fun(operands))

        operands = pass_values(operands)
        match instruction[0]:
            case "JMP"|"JLE"|"JE"|"JGE"|"JG"|"JL"|"JNE": #handle jumps
                m = fun(self.registers.__getitem___("SP"),operands[0])
                if m is not None:
                    self.registers.__setitem__("PC",m-1)#set the PC to m-1.
            case "AND"|"OR"|"NOR"|"XOR"|"NAND"|"ADD"|"SUB"|"DIV"|"MUL": #handle boolean statements
                execute_instruction()
            case "RET":
                pass
            case "NOP":
                pass #does nothing, as intended.
            case "PRINT":
                self.interruptHandler(Interrupt(name="PRINT",data=operands[2]))
            case "INPUT":
                self.interruptHandler(Interrupt(name="INPUT",data=operands[2]))
            case _:
                raise InstructionError
        #if we're performing a jump operation do the following:


    #run: -> Effect!
    #Purpose: Executes instructions arriving from
    #memory, then advances the program counter

    #TO-DO: Both execute and run will likely have to be integrated
    #to run with Memory, once the class exists and is coded.
    def run(self):
        while True:
            address = self.registers["PC"]
            try:
                next_address, instruction = self.decoder.decode(address)
            except IndexError:
                break
            self.registers["PC"] = next_address
            self.execute(instruction)