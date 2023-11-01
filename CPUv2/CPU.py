from dataclasses import dataclass
from . import Registers, Decoder, Instruction
@dataclass
class CPU:

    registers: Registers
    decoder: Decoder

    #is TO-DO
    def fetch(self, address):
        pass
    #is TO-DO
    def decode(self):
        pass
    #Execute: Instruction -> EFFECT!
    #Purpose: Attempts to execute the given instruction, making use
    #of the Decoder in opcode_parser.py to decode the instruction
    #EFFECT!: Based off of the given Instruction, code will be executed
    #that modifies the CPU state relevant to the Instruction's significance
    #within the opcode vocabulary.
    def execute(self, instruction: Instruction):
        # Python 3.10 or higher is required for this code.
        #3.10 supports match/case statements
        #whereas Python<3.10 would require 
        match instruction:
            #TO-DO: Add more instructions, based off of the Z80 opcodes.
            #its gonna stink
            #While all of the Z80's opcodes are in loaded json, this CPU sim
            #really, really, won't need them and so only the most important
            #one's will end up being written. It'll be fun to go back and actually
            #code the rest of the instructions to build a functional GameBoy emulator, but it would likely
            #take more time than is possible to complete in a semester.
            case Instruction(mnemonic="NOP"):
                pass

            case _:
                raise InstructionError(f"Cannot execute {instruction}")
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