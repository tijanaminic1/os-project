from dataclasses import dataclass
from . import Registers
class ReadyQueue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            raise IndexError("Queue is empty")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
@dataclass    
class Thread:
    
    register: Registers #This will do the init stuff for you, unless you've got more to add.
    
    #Methods go here...