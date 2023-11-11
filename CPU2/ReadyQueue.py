# main_script.py
import time
import threading
import Registers

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
    def __init__(self, thread_id, registers, queue, program):
        super().__init__()
        self.thread_id = thread_id
        self.registers = registers
        self.queue = queue
        self.program = program
        self.instruction_pointer = 0

    def run(self):
        while self.instruction_pointer < len(self.program):
            try:
                instruction = self.program[self.instruction_pointer]
                self.execute_instruction(instruction)
                self.instruction_pointer += 1
                time.sleep(1)  # Simulate processing time for each instruction
            except KeyboardInterrupt:
                print(f"Thread {self.thread_id} interrupted. Saving registers and moving to the back of the queue...")
                register_values = self.registers.copy()
                self.registers.save_registers(self.thread_id, register_values)
                self.queue.enqueue(self.thread_id)
                break

    def execute_instruction(self, instruction):
        operation = instruction['operation']
        operand = instruction['operand']

        if operation == 'ADD':
            self.registers['A'] += operand
        elif operation == 'SUB':
            self.registers['B'] -= operand
        # Add more operations as needed

# Example usage:
class Scheduler:
    def __init__(self):
        self.queue = ReadyQueue()
        self.registers = Registers()

    def add_thread(self, thread):
        self.queue.enqueue(thread)

    def start_scheduling(self):
        while True:
            if not self.queue.is_empty():
                thread = self.queue.dequeue()
                thread.start()
                self.queue.enqueue(thread)

# Example programs:
program1 = [
    {'operation': 'ADD', 'operand': 10},
    {'operation': 'SUB', 'operand': 5},
    {'operation': 'ADD', 'operand': 7},
    # Add more instructions as needed
]

program2 = [
    {'operation': 'SUB', 'operand': 3},
    {'operation': 'ADD', 'operand': 8},
    # Add more instructions as needed
]

# Example usage:
queue_instance = ReadyQueue()
scheduler_instance = Scheduler()

thread1 = CustomThread(1, Registers(), queue_instance, program1)
thread2 = CustomThread(2, Registers(), queue_instance, program2)

scheduler_instance.add_thread(thread1)
scheduler_instance.add_thread(thread2)

scheduler_instance.start_scheduling()


