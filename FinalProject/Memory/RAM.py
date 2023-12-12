from . import Memory
from ..InstructionArchitecture import Program
from ..Interrupt import Interrupt
class RAM(Memory):
    def __init__(self, size):
        self.data = [None] * size  # Initializing RAM with a given size

    def read(self, address):
        # Add error handling for out-of-bounds access
        return self.data[address]

    def write(self, address, value):
        # Add error handling for out-of-bounds access
        self.data[address] = value

    # Additional methods like allocation, deallocation can be added
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