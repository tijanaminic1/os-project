from collections.abc import MutableMapping
from dataclasses import dataclass
import opcode_parser
REGISTERS_LOW = {"F": "AF", "C": "BC", "E": "DE", "L": "HL"}
REGISTERS_HIGH = {"A": "AF", "B": "BC", "D": "DE", "H": "HL"}
REGISTERS = {"AF", "BC", "DE", "HL", "PC", "SP"}
FLAGS = {"c": 4, "h": 5, "n": 6, "z": 7}
@dataclass
class Registers(MutableMapping):
    AF: int #AF register
    BC: int #BC register
    DE: int #...  ...
    HL: int #...  ...
    PC: int #...  ...
    SP: int #SP register

    #values: -> list
    #Purpose: Returns a list of register values, indexed in order in the manner the Z80 CPU would
    def values(self):
        return [self.AF, self.BC, self.DE, self.HL, self.PC, self.SP]

    #Returns an interator of self.values
    def __iter__(self):
        return iter(self.values())

    #Gets the length of self.values.
    def __len__(self):
        return len(self.values())
    #getitem: Register Name -> int
    #purpose: Given a particular register name, it will return the high byte, low byte,
    #or full register.
    """

    High registers are bit-shifted 8 bits to the right, which yields the value we want

    Low registers are bitwise ANDed with the mask 0xFF as that matches the low 8 bits.

    Flags are instead shifted by their position in AF so the bit we care about is put in the right-most position where we can bitwise AND with 1 to check if it is set or not.

    Requests for 16-bit registers is a simple matter of returning that value, unmodified.

    Everything else is a KeyError

    """
    def __getitem__(self, key):
        if key in REGISTERS_HIGH:
            register = REGISTERS_HIGH[key]
            return getattr(self, register) >> 8
        elif key in REGISTERS_LOW:
            register = REGISTERS_LOW[key]
            return getattr(self, register) & 0xFF
        elif key in FLAGS:
            flag_bit = FLAGS[key]
            return self.AF >> flag_bit & 1
        else:
            if key in REGISTERS:
                return getattr(self, key)
            else:
                raise KeyError(f"No such register {key}")
    #setitem: [register name] + value -> Effect!
    # Purpose: Modifies the value stored in a given register.
    # Warning: Raises a key-error if a nonexistent location is provided.        
    def __setitem__(self, key, value):
        if key in REGISTERS_HIGH:
            register = REGISTERS_HIGH[key]
            current_value = self[register]
            setattr(self, register, (current_value & 0x00FF | (value << 8)) & 0xFFFF)
        elif key in REGISTERS_LOW:
            register = REGISTERS_LOW[key]
            current_value = self[register]
            setattr(self, register, (current_value & 0xFF00 | value) & 0xFFFF)
        elif key in FLAGS:
            assert value in (0, 1), f"{value} must be 0 or 1"
            flag_bit = FLAGS[key]
            if value == 0:
                self.AF = self.AF & ~(1 << flag_bit)
            else:
                self.AF = self.AF | (1 << flag_bit)
        else:
            if key in REGISTERS:
                setattr(self, key, value & 0xFFFF)
            else:
                raise KeyError(f"No such register {key}")
    #one cannot delete a, register, but @dataclass wants this, so best to include it.
    def __delitem__(self, key):
        raise NotImplementedError("Register deletion is not supported")
    
#Simple Error class
class InstructionError(Exception):
    pass


@dataclass
class CPU:

    registers: Registers
    decoder: Decoder

    #Execute: Instruction -> EFFECT!
    #Purpose: Attempts to execute the given Z80 instruction, making use
    #of the Decoder in opcode_parser.py to decode the instruction
    #EFFECT!: Based off of the given Instruction, code will be executed
    #that modifies the CPU state relevant to the Instruction's significance
    #within the Z80 opcode vocabulary.
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