import sys
from dataclasses import dataclass
from typing import Literal
import pytest
import opcode_parser
@dataclass
class Decoder:

    data: bytes
    address: int
    prefixed_instructions: dict
    instructions: dict

    @classmethod
    def create(cls, opcode_file: Path, data: bytes, address: int = 0):
        # Loads the opcodes from the opcode file
        prefixed = InstructionSet().cbprefixed
        unprefixed = InstructionSet().unprefixed
        return cls(
            prefixed_instructions=prefixed,
            instructions=regular,
            data=data,
            address=address,
        )

    def read(self, address: int, count: int = 1):
        """
        Reads `count` bytes starting from `address`.
        """
        if 0 <= address + count <= len(self.data):
            v = self.data[address : address + count]
            return int.from_bytes(v, sys.byteorder)
        else:
            raise IndexError(f'{address=}+{count=} is out of range')

    def decode(self, address: int):
        """
        Decodes the instruction at `address`.
        """
        opcode = None
        decoded_instruction = None
        opcode = self.read(address)
        address += 1
        # 0xCB is a special prefix instruction. Read from
        # prefixed_instructions instead and increment address.
        if opcode == 0xCB:
            opcode = self.read(address)
            address += 1
            instruction = self.prefixed_instructions[opcode]
        else:
            instruction = self.instructions[opcode]
        new_operands = []
        for operand in instruction.operands:
            if operand.bytes is not None:
                value = self.read(address, operand.bytes)
                address += operand.bytes
                new_operands.append(operand.copy(value))
            else:
                # No bytes; that means it's not a memory address
                new_operands.append(operand)
        decoded_instruction = instruction.copy(operands=new_operands)
        return address, decoded_instruction

@pytest.fixture
def make_decoder(request):
    def make(data: bytes, address: int = 0):
        opcode_file = Path(request.config.rootdir) / "etc/opcodes.json"
        return Decoder.create(opcode_file=opcode_file, data=data, address=address)
    return make

def test_decoder_nop_instruction(make_decoder):
    decoder = make_decoder(data=bytes.fromhex("00"))
    new_address, instruction = decoder.decode(0x0)
    assert new_address == 0x1
    assert instruction == Instruction(
        opcode=0x0,
        immediate=True,
        operands=[],
        cycles=[4],
        bytes=1,
        mnemonic="NOP",
        comment="",
    )