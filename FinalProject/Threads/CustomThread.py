import threading
class CustomThread(threading.Thread):
    def __init__(self, thread_id, registers, queue):
        super().__init__()
        self.thread_id = thread_id
        self.registers = registers
        self.queue = queue