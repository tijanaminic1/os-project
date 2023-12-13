from Interrupt import Interrupt
from dataclasses import dataclass, field
from typing import List
@dataclass
class InterruptStack:
    interrupts: List[Interrupt] = field(default_factory=list)
    def __len__(self):
        return len(self.interrupts)
    #enqueue: interrupt -> Effect!
    #Purpose: Pushes interrupt to front of stack.
    def push(self,interrupt: Interrupt):
        self.interrupts.insert(0,interrupt)
    #pop: -> Effect!
    #Purpose: removes the first value of the interrupt stack
    #and returns it. Good usage in the interrupt handling scheme.
    def pop(self):
        return self.interrupts.pop(0)
