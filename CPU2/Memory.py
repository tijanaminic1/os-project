from dataclasses import dataclass
from typing import List, Literal, TypeVar, Generic
from . import Interrupt
#Purpose: Move memory from the start list to the end list
#def DMA(start:List,end:List):
#Implement later
T = TypeVar('T')
@dataclass
class Memory:
    data: List[T]
    #DATA: -> list
    #Purpose: returns the list that is memory.
    def DATA(self):
        return self.data
    def write(self, start: int, data: T):
        self.data[start] = data
    def read(self, loc: int):
        return self.data[loc]
    #TO-DO:
    #create a size enforcement protocol.
    #Write in a way to simulate memory limit.

#DMA: Memory, memory operation, start index (optional), data (optional)
#Purpose: Performs direct memory access according to a given predicate (operation)
#Effect!: Potentially modifies memory.
@staticmethod
def DMA(sender: object, memory: Memory, operation="", start=-1, data=None):
    if start == -1:
        return Interrupt("DMAFatalError")
    match operation:
        case "read":
            try:
                return memory.read(start)
            except IndexError:
                return Interrupt("DMAIndexOutOfBounds")
        case "write":
            try:
                memory.write(start,data)
            except IndexError:
                return Interrupt("DMAIndexOutOfBounds")
        case _:
            return Interrupt("DMAFatalError")