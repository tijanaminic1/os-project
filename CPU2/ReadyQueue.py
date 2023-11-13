import threading
import time

class ReadyQueue:
    def __init__(self):
        self.processes = []
        self.lock = threading.Lock()

    def enqueue(self, process):
        with self.lock:
            self.processes.append(process)

    def dequeue(self):
        with self.lock:
            if not self.is_empty():
                return self.processes.pop(0)
            else:
                return None

    def is_empty(self):
        with self.lock:
            return len(self.processes) == 0

    def size(self):
        with self.lock:
            return len(self.processes)

class CustomThread(threading.Thread):
    def __init__(self, process, cpu):
        super().__init__()
        self.process = process
        self.cpu = cpu

    def run(self):
        while self.process.has_next_instruction():
            try:
                instruction = self.process.get_next_instruction()
                self.cpu.execute_instruction(instruction)
                time.sleep(1)
            except KeyboardInterrupt:
                print(f"Thread for process {self.process} interrupted. Saving state...")
                break



