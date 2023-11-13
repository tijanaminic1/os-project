import time
import threading
import Registers

class Instruction:
    def __init__(self, operation, operand):
        self.operation = operation
        self.operand = operand

class Registers:
    def __init__(self):
        self.register_state = {Registers}

    def save_registers(self, thread_id, values):
        # Implement logic to save register values
        pass

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
    def __init__(self, thread_id, registers, queue, process):
        super().__init__()
        self.thread_id = thread_id
        self.registers = registers
        self.queue = queue
        self.process = process

    def run(self):
        while True:
            try:
                # Your thread code here
                instruction = self.process.get_next_instruction(self.thread_id)
                if instruction:
                    print(f"Thread {self.thread_id} executing instruction: {instruction.operation} {instruction.operand}")
                    # Implement logic to execute instruction and update register state
                else:
                    print(f"Thread {self.thread_id} finished execution. Moving to the back of the queue...")
                    self.queue.enqueue(self.thread_id)
                    break
                time.sleep(1)
            except KeyboardInterrupt:  
                print(f"Thread {self.thread_id} interrupted. Saving registers and moving to the back of the queue...")
                register_values = {}  # Replace with actual register values
                self.registers.save_registers(self.thread_id, register_values)
                self.queue.enqueue(self.thread_id)
                break

class Process:
    def __init__(self, instructions):
        self.instructions = instructions
        self.current_instruction_index = 0

    def get_next_instruction(self, thread_id):
        if self.current_instruction_index < len(self.instructions):
            next_instruction = self.instructions[self.current_instruction_index]
            self.current_instruction_index += 1
            return next_instruction
        else:
            return None

class Scheduler:
    def __init__(self):
        self.queue = ReadyQueue()
        self.registers = Registers() 

    def add_thread(self, thread_id, instructions):
        process = Process(instructions)
        self.queue.enqueue((thread_id, process))

    def start_scheduling(self):
        while True:
            if not self.queue.is_empty():
                thread_id, process = self.queue.dequeue()
                thread = CustomThread(thread_id, self.registers, self.queue, process)
                thread.start()
                self.queue.enqueue((thread_id, process))

# Example usage:
scheduler = Scheduler()

# Add threads with instructions
scheduler.add_thread(1, [Instruction("ADD", 10), Instruction("SUB", 5), Instruction("MULT", 2)])
scheduler.add_thread(2, [Instruction("ADD", 5), Instruction("DIV", 2)])

# Start scheduling
scheduler.start_scheduling()

