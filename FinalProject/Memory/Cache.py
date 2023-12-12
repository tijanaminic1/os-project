from dataclasses import dataclass
from typing import List, TypeVar, Tuple
from collections.abc import Iterable
from ..Interrupt import Interrupt
from . import Memory
from ..InstructionArchitecture.Instruction import Instruction
from ..InstructionArchitecture.Process import Process
@dataclass
class Cache(Memory):
    partitions: int = 16
    size: int = partitions*16
    data: List[Instruction] = [None]*size
    block_size: int = size//partitions

    #fetch: int -> sublist(data)
    #Purpose: returns a particular block of memory in the cache data
    def fetch(self,arg:int)->List[Instruction]:
        start,end = self.blockify(arg)
        return self.data[start:end]
    #fetch_blocks: iterable(blocks) -> List
    #Purpose: returns a list of blocks (partitions) in the order
    #the relative indices (blocks) were received

    def fetch_blocks(self, *args:Iterable[int])->List[Instruction]:
        return [self.fetch(partition) for partition in args]
    #blockify: size -> Tuple[Int,Int]
    #Purpose: Returns a Tuple that represents a block's start index, and its end index+1
    #Can be used as a range It is an interval
    def blockify(self,size)->Tuple[int,int]:
        size = (size-1) if size>0 else 0
        return (size*self.block_size,(size+1)*self.block_size)
    
    #check: natnum(0,15) -> boolean
    #Purpose: Determine whether or not a block is free
    def check(self, blocknum: int):
        is_none = (lambda x: x is None)
        return all(is_none(index) for index in self.fetch_blocks(blocknum))
    
    #blocks_free: -> natnum
    #Purpos: returns the number of blocks free in the Cache
    def blocks_free(self):
        return sum(self.check(partition) for partition in range(self.partitions))

    def free_block(self, blocknum: int):
        indices = range(*self.blockify(blocknum))
        for index in indices:
            self.data[index] = None
    #set_block: natnum + iterable -> effect!
    #purpose:Sets the block to te values of the given iterable
    #ASSUMPTION: len(iterable) <= block_size
    def set_block(self, blocknum: int, iterable: Iterable):
        indices = range(*self.blockify(blocknum))
        self.data[indices] = [value for value in iterable]
    #allocable: int -> int or Interrupt
    #Purpose: Given a size of a set of instructions,
    #returns an Interrupt if the set of instructions is too
    #large to be processed, or an integer relating to the
    #amount
    def allocable(self,data_size: Process):
        space_needed = (len(data_size)/self.block_size)
        if space_needed > self.partitions:
            raise Interrupt("ProcessTooLarge")
        elif space_needed > self.blocks_free():
            return False
        else:
            return True
    #allocate: Process -> Effect!
    #Purpose: Allocates the given memory info if it can, otherwise raises an Interrupt    
    def allocate(self,input:Process):
        if not self.allocable(len(input)):
            raise Interrupt("CacheBottleneck")
        allocatehere = [block for block in range(self.block_size) if self.check(block)]
        i = 0
        for block in range(len(allocatehere)):
            start,end = self.blockify(i) 
            self.set_block(block,input[start:end])#Effect!: data[i]
            block+=1#Effect! block is incremented
        input.setPARTITIONS(allocatehere)
