from ..Threads import CustomThread, ReadyQueue
from ..InstructionArchitecture import Registry
class FCFS:
    def __init__(self):
        self.queue = ReadyQueue()
        self.registers = Registry() 

    #purpose: Adds thread (by id) to the back of the queue
    def add_thread(self, thread_id):
        self.queue.enqueue(thread_id)

    #start_scheduling: -> effect! 
    def start_scheduling(self):
        while True:
            if not self.queue.is_empty():
                thread_id = self.queue.dequeue()
                thread = CustomThread(thread_id, self.registers, self.queue)
                thread.start()
                self.queue.enqueue(thread_id)
    #TODO: Complete integration with CPU.