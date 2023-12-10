from Interrupt import Interrupt
from ..Threads import ReadyQueue
from dataclasses import dataclass
from typing import List
@dataclass
class InterruptStack:
    interrupts: List[Interrupt] = []


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
    
    #HANDLE: -> Effect!
    #Purpose: Utilizes Interrupt.Handle's functionality to service the most
    #recently triggered interrupt.
    #If that interrupt raises an interrupt, it will handle the raised interrupt first,
    #then return to the interrupt that triggered the nested interrupt.
    def HANDLE(self):
        interrupt = self.pop()
        try:
            Interrupt.HANDLE(interrupt)
        except Interrupt as e:
            Interrupt.HANDLE(e)
            Interrupt.HANDLE(interrupt)
        #TODO: #1 Look for cases where this may cause an infinite loop.
        #These can be found by looking at Interrupt.HANDLE in Interrupt.py
        #We want strong invariants for our Handle function so that we can
        #reliably service nested interrupts.
#HANDLESTACK: -> Effect!
#Purpose: Tries to service the interrupt stack.
@staticmethod
def HANDLESTACK(stack: InterruptStack):
    while len(stack)>0:
        stack.HANDLE()