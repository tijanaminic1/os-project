from . import Memory
from ..InstructionArchitecture.Program import Program
from ..Interrupt import Interrupt
from typing import List

#By using dictionaries, memory is dynamically alloated across RAM
#and accessed via relative indexing.
#This creates an easy implementation of dynamic partitioning
#To see what static partitions look like, view Cache.
class RAM(Memory):
    #ASSUMPTION: Init is called with a value 
    def __init__(self, data_matrix: List[Program]):
        self.data = data_matrix
        self.size = sum(len(value) for value in self.data)
        self.capacity = self.size*16 if self.size>4096 else 4096
        self.pid_key = 0
    #get: str -> Program
    #Purpose: To get the process id out of RAM
    def read(self, PROCESS_ID: int)->Program:
        try:
            return self.data[PROCESS_ID]
        except KeyError:
            raise Interrupt("PageFault")
    #load: Program -> Effect!
    #Purpose: To write a new program into the RAM
    def write(self, program: Program):
        program_size = len(program)
        if self.size+program_size > self.capacity:
            raise Interrupt("RAMCapacityWarning")
        else:
            self.data[len(self.data)] = program
            self.size+=program_size
    #free: int -> Effect!
    #Purpose: To free up the RAM memory
    def free(self,PROCESS_ID:int):
        try:
            self.size -= self.data[PROCESS_ID]
            del self.data[PROCESS_ID]
        except KeyError:
            raise Interrupt("PageFault")
    
    #clear: -> Effect!
    #Purpose: clears the entire RAM.
    def clear(self):
        self.data = {}
    
    def __iter__(self):
        return iter(self.data)
