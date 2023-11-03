from dataclasses import dataclass
from typing import List, Literal
#Purpose: Move memory from the start list to the end list
#def DMA(start:List,end:List):
#Implement later


@dataclass
class Memory:
    RAM: List[int]
    cache: List[int]

    def RAM(self):
        return self.RAM
    def cache(self):
        return self.cache
    #TODO:
    #create a size enforcement protocol.
    #Write in a way to simulate memory limit.
