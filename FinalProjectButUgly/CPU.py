from dataclasses import dataclass
from Decoder import Decoder
from Registry import Registry
from  Instruction import Instruction
from Memory import Memory
from InstructionError import InstructionError
#from Cache import Cache
#from RAM import RAM
from Interrupt import Interrupt
from typing import Any, List, Tuple
from Cache import Cache
from RAM import RAM
"""
#from InterruptStack import InterruptStack
@dataclass
class CPU:
    registers: Registry
    decoder: Decoder
    #fetch: int -> Instruction
    #purpose: gets the instruction stored at the given memory location
    def fetch(self, address: int, memory: Memory)-> Instruction:
        try:
            return self.decoder.fetch(memory, address)
        except Exception as e:
            match e:
                case Interrupt():
                    print("Interrupt!")
                    raise e
                case Exception():
                    print("Exception!")
                    raise e
            raise Interrupt ("CacheMiss",message=self.registers)
    
    def fetch(self, address: int, memory: Memory) -> Instruction:
        try:
            return memory[address]
        except IndexError:
            raise Interrupt("CacheMiss", message=self.registers)
    #decode: Instruction -> Tuple
    #purpose: Decodes an instruction into its mnemonic, 
    #effects, and locates its operands
    def decode(self,inst: Instruction)->Tuple[str,Any,List]:
        return self.decoder.decode(inst)
    #Execute: Instruction -> EFFECT!
    #Purpose: Attempts to execute the given instruction, making use
    #of the Decoder in opcode_parser.py to decode the instruction
    #EFFECT!: Based off of the given Instruction, code will be executed
    #that modifies the CPU state relevant to the Instruction's significance
    #within the opcode vocabulary.
    def execute(self, instruction: Tuple[str,Any,List]):
        reglist = ["A","B","C","D","E","F","PC","SP"] 
        operands = instruction[2] #operands
        fun = instruction[1] #operation
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
                self.registers["SP"] = fun(operands)
            else:
                self.registers[operands[0]] = fun(operands)

        operands = pass_values(operands)
        match instruction[0]:
            case "JMP"|"JLE"|"JE"|"JGE"|"JG"|"JL"|"JNE": #handle jumps
                m = fun(self.registers.__getitem___("SP"),operands[0])
                if m is not None:
                    self.registers.__setitem__("PC",m-1)#set the PC to m-1.
            case "AND"|"OR"|"NOR"|"XOR"|"NAND"|"ADD"|"SUB"|"DIV"|"MUL": #handle boolean statements
                execute_instruction()
            case "RET":
                raise Interrupt(name="Process Complete", data=self.registers)
            case "NOP":
                pass #does nothing, as intended.
            case "PRINT":
                raise fun#raise so the printer can print, CPU can let this get DMA'd
            case "INPUT":
                raise fun#raise so that this doesn't squat on the mutex lock.
            case "MOV":
                raise fun
            case _:
                raise InstructionError
        #if we're performing a jump operation do the following:
    #Purpose: Performs a fetch decode execute cycle.
    def cycle(self,address: int, mem: Memory):
        try:
            self.execute(self.decode(self.fetch(address,mem)))
        except Interrupt as e:
            raise e
        
    #run: -> Effect!
    #Purpose: Executes instructions arriving from
    #memory, then advances the program counter
"""
@dataclass
class CPU:
    registers: Registry
    decoder: Decoder

    def fetch(self, address: int, cache: Cache) -> Instruction:
            try:
                return cache.get_instruction(address)
            except Exception as e:
                match e:
                    case Interrupt():
                        print("Interrupt!")
                        raise e
                    case Exception():
                        print("Exception!")
                        raise e
                raise Interrupt("CacheMiss", message=self.registers)

    def execute(self, instruction: Tuple[str, Any, List]):
        opcode, operation, operands = instruction
        try:
            if opcode in ["JMP", "JLE", "JE", "JGE", "JG", "JL", "JNE"]:
                new_address = operation(*operands)
                if new_address is not None:
                    self.registers["PC"] = new_address - 1
            else:
                result = operation(*operands)
                if isinstance(result, Interrupt):
                    raise result
                else:
                    self.registers["SP"] = result
        except Interrupt as interrupt:
            raise interrupt
        except Exception as e:
            raise InstructionError(f"Error executing instruction: {e}")

    def cycle(self, address: int, mem: Memory):
        try:
            instruction = self.fetch(address, mem)
            decoded_instruction = self.decoder.decode(instruction)
            self.execute(decoded_instruction)
        except Interrupt as e:
            raise e
