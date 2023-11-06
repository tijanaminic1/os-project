import Registers
import time
import threading

class ReadyQueue:
    def __init__(self):
        self.items = []
        self.lock = threading.Lock()

    def enqueue(self, item):
        with self.lock:
            self.items.append(item)

    def dequeue(self):
        with self.lock:
            if not self.is_empty():
                return self.items.pop(0)
            else:
                raise IndexError("Queue is empty")

    def is_empty(self):
        with self.lock:
            return len(self.items) == 0

    def size(self):
        with self.lock:
            return len(self.items)

class CustomThread(threading.Thread):
    def __init__(self, thread_id, registers, queue):
        super().__init__()
        self.thread_id = thread_id
        self.registers = registers
        self.queue = queue

    def run(self):
        while True:
            try:
                # Your thread code here
                print(f"Thread {self.thread_id} is running...")
                time.sleep(1)
            except KeyboardInterrupt:  # Interrupt the thread using keyboard interrupt (Ctrl+C)
                print(f"Thread {self.thread_id} interrupted. Saving registers and moving to the back of the queue...")
                register_values = {}
                self.registers.save_registers(self.thread_id, register_values)
                self.queue.enqueue(self.thread_id)
                break

class Scheduler:
    def __init__(self):
        self.queue = ReadyQueue()
        self.registers = Registers() 

    def add_thread(self, thread_id):
        self.queue.enqueue(thread_id)

    def start_scheduling(self):
        while True:
            if not self.queue.is_empty():
                thread_id = self.queue.dequeue()
                thread = CustomThread(thread_id, self.registers, self.queue)
                thread.start()
                self.queue.enqueue(thread_id)

