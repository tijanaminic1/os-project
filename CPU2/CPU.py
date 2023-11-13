from dataclasses import dataclass
import threading
import time
from ReadyQueue import ReadyQueue, CustomThread
from Decoder import Instruction, InstructionError, Interrupt

from Registers import Registers
from Decoder import Decoder
from Memory import Memory

@dataclass
class CPU:
    registers: 'Registers'
    decoder: 'Decoder'
    cache: 'Memory'
    RAM: 'Memory'

    def __init__(self, registers, decoder, cache, RAM):
        self.registers = registers
        self.decoder = decoder
        self.cache = cache
        self.RAM = RAM
        self.ready_queue = ReadyQueue()

    def fetch(self, address) -> Instruction:
        return self.decoder.fetch(self.cache, address)

    def decode(self, inst: Instruction) -> tuple:
        return self.decoder.decode(inst)

    def interruptHandler(self, i: 'Interrupt') -> None:
        match i:
            case Interrupt(name="PRINT"):
                print(i.items())
            case Interrupt(name="INPUT"):
                input(i.items())
            case Interrupt(name="DMAFatalError"):
                print("DMA failed due to fatal error.")
            case Interrupt(name="DMAIndexOutOfBounds"):
                print("DMA failed! Entry does not exist.")

    def execute_instruction(self, instruction: tuple) -> None:
        reglist = ["A", "B", "C", "D", "E", "F", "PC", "SP"]
        operands = instruction[2]
        fun = instruction[1]
        immediate = True

        if len(operands) > 0 and operands[0] in reglist:
            immediate = False

        def pass_values(l: list) -> list:
            a = 1
            while a < len(operands):
                if l[a] in reglist:
                    l[a] = self.registers.__getitem__(l[a])
                a = a + 1

        def execute_instruction():
            if immediate:
                self.registers.__setitem__("SP", fun(operands))
            else:
                self.registers.__setitem__(operands[0], fun(operands))

        operands = pass_values(operands)
        match instruction[0]:
            case "JMP" | "JLE" | "JE" | "JGE" | "JG" | "JL" | "JNE":
                m = fun(self.registers.__getitem__("SP"), operands[0])
                if m is not None:
                    self.registers.__setitem__("PC", m - 1)
            case "AND" | "OR" | "NOR" | "XOR" | "NAND" | "ADD" | "SUB" | "DIV" | "MUL":
                execute_instruction()
            case "RET":
                pass
            case "NOP":
                pass
            case "PRINT":
                self.interruptHandler(Interrupt(name="PRINT", data=operands[2]))
            case "INPUT":
                self.interruptHandler(Interrupt(name="INPUT", data=operands[2]))
            case _:
                raise InstructionError

    def run(self):
        while True:
            if not self.ready_queue.is_empty():
                process = self.ready_queue.dequeue()
                thread = CustomThread(process, self)
                thread.start()
                self.ready_queue.enqueue(process)

