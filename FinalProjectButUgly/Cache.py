from dataclasses import dataclass, field
from typing import List, TypeVar, Tuple
from collections.abc import Iterable
from Interrupt import Interrupt
from Memory import Memory
from Instruction import Instruction
from Process import Process
from typing import Optional, Dict
@dataclass
class CacheBlock:
    size: int = 16
    instructions: List[Optional[Instruction]] = field(default_factory=lambda: [None] * 16)
    is_free: bool = True

    def allocate(self, instructions: List[Instruction]):
        if len(instructions) > self.size:
            raise Interrupt("BlockOverflow")
        self.instructions = instructions + [None] * (self.size - len(instructions))
        self.is_free = False

    def free(self):
        self.instructions = [None] * self.size
        self.is_free = True
@dataclass
class Cache(Memory):
    partitions: int = 16
    blocks: dict[int, CacheBlock] = field(default_factory=lambda: {i: CacheBlock() for i in range(16)})
    data = None#Default empty cache
    def blocks_free(self) -> int:
        return sum(block.is_free for block in self.blocks.values())

    def allocable(self, process_size: int) -> bool:
        if process_size > self.partitions * self.blocks[0].size:
            raise Interrupt("ProcessTooLarge")
        return process_size <= self.blocks_free() * self.blocks[0].size

    def allocate(self, input_process: Process):
        if not self.allocable(len(input_process.data)):
            raise Interrupt("CacheBottleneck")

        instruction_index = 0
        for block_number, block in self.blocks.items():
            if block.is_free:
                remaining_instructions = input_process.data[instruction_index:]
                block.allocate(remaining_instructions[:block.size])
                instruction_index += block.size
                if instruction_index >= len(input_process.data):
                    break

        if instruction_index < len(input_process.data):
            raise Interrupt("CacheAllocationFailed")
