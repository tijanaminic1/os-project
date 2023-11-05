from dataclasses import dataclass
from typing import List, Literal
#Purpose: Move memory from the start list to the end list
#def DMA(start:List,end:List):
#Implement later

@dataclass
class Memory:
    data: List[int]
    def DATA(self):
        return self.data
    def write(self, int start, data):
        pass
    def read(self):
        pass
    #TODO:
    #create a size enforcement protocol.
    #Write in a way to simulate memory limit.
