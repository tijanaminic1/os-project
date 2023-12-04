from dataclasses import dataclass
from typing import List, Literal, TypeVar, Generic, Tuple, Dict
from collections.abc import Iterable
from . import Interrupt, Instruction, Process, Program
#Purpose: Move memory from the start list to the end list
#def DMA(start:List,end:List):
#Implement later
T = TypeVar('T')
@dataclass
class Memory:
    data: List[T]
    #DATA: -> list
    #Purpose: returns the list that is memory.
    @property
    def DATA(self):
        return self.data
    @DATA.setter
    def write(self, start: int, data: T):
        self.data[start] = data
    @DATA.getter
    def read(self, loc: int):
        return self.data[loc]
    #clear: -> Effect!
    #purpose: clears the cache.
    @DATA.deleter
    def clear(self):
        self.data = []
@dataclass
class Cache(Memory):
    partitions: int = 10
    size: int = partitions*100
    data: List[T] = [None]*size
    block_size: int = size//partitions
    #blockify: int -> tuple[int,int]
    def blockify(self,size)->Tuple[int,int]:
        return (size*self.block_size,(size+1)*self.block_size)
    #fetch: int -> sublist(data)
    #Purpose: returns a particular block of memory in the cache data
    def fetch(self,arg:int)->List[T]:
        start,end = self.blockify(arg)
        return self.data[start:end]
    #fetch_blocks: List[int] -> List[T]
    #Purpose: Fetches blocks of memory, according
    #to what is provided, the memory is returned in the order given.
    #For Example:
    #If I asked for (0,1,2)
    #I would get List[Block 0 + Block 1 + Block 2]
    #But if I asked for (1,0,2)
    #I would get List[Block 1 + Block 0 + Block 2]
    def fetch_blocks(self, *args:Iterable[int])->List[T]:
        return [self.fetch(partition) for partition in args]
    #check: int -> bool
    #Given an integer representing the number of the memory partition,
    #it returns True if the block is free, false if it is not
    def check(self,arg:int)->bool:
        is_none = (lambda x: x is None)
        return all(is_none(value) for value in self.fetch(arg))
    #blocks_free:->int
    def blocks_free(self):
        return sum([self.check(partition) for partition in range(self.partitions)])
    #free: int -> Effect!
    #purpose: Frees a block of memory.
    def free(self,arg:int):
        for index in range(self.block_size*arg,self.block_size*(arg+1)):
            self.data[index] = None
    #allocable: int -> int or Interrupt
    #Purpose: Given a size of a set of instructions,
    #returns an Interrupt if the set of instructions is too
    #large to be processed, or an integer relating to the
    #amount
    def allocable(self,data_size: int):
        space_needed = (len(data_size)/self.block_size)
        if space_needed > self.partitions:
            raise Interrupt("ProcessTooLarge")
        elif space_needed > self.blocks_free():
            return False
        else:
            return True
    #allocate: List -> Effect!
    #Purpose: Allocates the given memory info.
    def allocate(self,input: List[T]):
        if not self.allocable(len(input)):
            raise Interrupt("CacheBottleneck")
        inputsegment = 0 # a = the number of blocks allocated
        memorylocations = [] #the list of memory locations where the data will be stored.
        for block in range(self.block_size):
            if self.check(block):
                d_start, d_stop = self.blockify(block)
                i_start, i_stop = self.blockify(inputsegment)
                self.data[d_start:d_stop]=input[i_start:i_stop]
                inputsegment+=1
                memorylocations.append(block)
        raise Interrupt(name="PassAllocationData",data=memorylocations)
class RAM(Memory):
    def __init__(self,data_matrix:Dict[int,Program]):
        self.data = data_matrix
        self.size = len(self.data)
    #get: str -> Program
    #Purpose: To get the process id out of RAM
    def read(self, PROCESS_ID: int)->Program:
        try:
            return self.data[PROCESS_ID]
        except KeyError:
            raise Interrupt("SegmentationFault")
    #load: Program -> Effect!
    #Purpose: To write a new program into the RAM
    def write(self, program: Program):
        self.data[len(self.data)] = program
    #free: int -> Effect!
    #Purpose: To free up the RAM memory
    def free(self,PROCESS_ID:int):
        self.data.discard(PROCESS_ID)
#DMA: Memory, memory operation, start index (optional), data (optional)
#Purpose: Performs direct memory access according to a given predicate (operation)
#Effect!: Potentially modifies memory.
@staticmethod
def DMA(sender: object, memory: Memory, operation="", start=-1, data=None):
    if start == -1:
        raise Interrupt("DMAFatalError",data=sender)
    try:
        match operation:
            case "read":
                return memory.read(start)
            case "write":
                memory.write(start,data)
            case _:
                raise Interrupt("DMAFatalError",data=sender)
    except IndexError:
        raise Interrupt("DMAIndexOutOfBounds",data=sender)
