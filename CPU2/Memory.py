from dataclasses import dataclass
from typing import List, Literal, TypeVar, Generic
#Purpose: Move memory from the start list to the end list
#def DMA(start:List,end:List):
#Implement later
T = TypeVar('T')
@dataclass
class Memory:
    data: List[T]
    def DATA(self):
        return self.data
    def write(self, start: int, data: T):
        pass
    def read(self):
        pass
    #TO-DO:
    #create a size enforcement protocol.
    #Write in a way to simulate memory limit.
