from dataclasses import dataclass
from . import Registers, Decoder, Interrupt, Memory
from Decoder import Instruction
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
    #decode: Instruction -> 
    def decode(self,inst: Instruction)->(str,function,list):
        return self.decoder.decode(inst)
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
        arithmetic = ["ADD","SUB","DIV","MUL"]
        logic = ["AND","OR","NOR","XOR","NAND"]
        jumps = ["JMP","JLE","JE","JGE","JG","JL","JNE"]
        commands = ["RET","NOP","PRINT","INPUT"]
        
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
        if immediate:
            self.registers.__setitem__("SP",fun(operands))
        else:
            self.registers.__setitem__(operands[0],fun(operands))


            
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