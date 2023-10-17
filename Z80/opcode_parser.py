from dataclasses import dataclass
from typing import Literal
import json
#Operand defines the nature of an operand within the Z80 instruction set.
@dataclass(frozen=True)
class Operand:

    immediate: bool
    name: str
    bytes: int
    value: int | None
    adjust: Literal["+", "-"] | None

    def create(self, value):
        return Operand(immediate=self.immediate, #See below
                       name=self.name,
                       bytes=self.bytes,
                       value=value,
                       adjust=self.adjust)
    #pretty printer
    def print(self):
        if self.adjust is None:
            adjust = ""
        else:
            adjust = self.adjust
        if self.value is not None:
            if self.bytes is not None:
                val = hex(self.value)
            else:
                val = self.value
            v = val
        else:
            v = self.name
        v = v + adjust
        if self.immediate:
            return v
        return f'({v})'

#Instruction is a dataclass used to store the aspects of an Instruction.
#For example, the ADD instruction would be stored as a class using Instruction.
@dataclass
class Instruction:

    opcode: int #the opcode
    immediate: bool #whether the opcode accesses an immediate value
    operands: list[Operand] #list of operands taken by the opcode
    cycles: list[int] #the cycles the opcode requires
    bytes: int #bytesize of opcode
    mnemonic: str #the opcode's mnemonic, for example 'ADD', 'SUB', 'DIV'
    comment: str = "" #Space for me to comment on the opcode later.

    def create(self, operands):
        return Instruction(opcode=self.opcode,
                           immediate=self.immediate,
                           operands=operands,
                           cycles=self.cycles,
                           bytes=self.bytes,
                           mnemonic=self.mnemonic)
    #pretty printer
    def print(self):
        ops = ', '.join(op.print() for op in self.operands)
        s = f"{self.mnemonic:<8} {ops}"
        if self.comment:
            s = s + f" ; {self.comment:<10}"
        return s
"""
##json parser
class instruction_set:
cbpfilepath = "cbprefixed.json"

# Open and read the JSON file
with open(json_file_path, 'r') as json_file:
    # Load the JSON data into a Python object
    python_object = json.load(json_file)

# Now, 'python_object' contains the equivalent Python data structure

# You can access and manipulate the data like a regular Python object
# For example, if your JSON contains a dictionary with a key "key_name", you can access its value like this:
value = python_object["key_name"]

# Print the Python object to verify the conversion
print(python_object)
"""

class InstructionSet:

  def __init__(self):
    self.cbfilepath = "cbprefixed.json" #the prefixed instruction set
    self.unpfilepath = "unprefixed.json" #the unprefixed instruction set
    self.cbprefixed = {}
    self.unprefixed = {}
    #build_isa: string + dict -> (Effect!)
    #Purpose: Dynamically builds the Z80 instruction set from the given file, adding them or updating the providing dictionary.
    def build_isa(myfile,location):
       with open(myfile,'r') as json_file:
          raw_isa = json.load(json_file)
          for key in raw_isa:
            lst_ops= []
            for x in key["operands"]:
               lst_ops.append(Operand.create(x))
            location[int(key,base=16)]["operands"] = Instruction.create(raw_isa[key]) #build the instruction
            location[int(key,base=16)].operand
    build_isa(self.cbfilepath,self.cbprefixed)
    build_isa(self.unpfilepath,self.unprefixed)
  
  #fromMnemonic: instruction set, str -> dict
  #Purpose: fetches an instruction set based on its mnemonic
  def fromMnemonic(self, isa, mnemonic):
    for key in isa:
       if key.mnemonic == mnemonic:
          return isa[key]
    return self.unprefixed["0x00"] #If the operation with the specified mnemonic is not found, return the "NOP" "No Operation"