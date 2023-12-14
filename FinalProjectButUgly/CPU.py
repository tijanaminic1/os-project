from dataclasses import dataclass
from Decoder import Decoder
from Registry import Registry
from  Instruction import Instruction
from Memory import Memory
from InstructionError import InstructionError
#from Cache import Cache
#from RAM import RAM
from Interrupt import Interrupt
from typing import Any, List, Tuple
from Cache import Cache
from RAM import RAM
from Process import Process
import copy
@dataclass
class CPU:
    registers: Registry
    decoder: Decoder
    #Fetch may look like it doesn't go for an address, but under the hood
    #in cache.get_instruction, the addressing occurs.
    def fetch(self, process: Process, cache: Cache) -> Instruction:
        try:
            return cache.get_instruction(process)
        except Interrupt as e:
            raise e
        except Exception as f:
            raise f

    def execute(self, instruction: Tuple[str, Any, List]):
        opcode, operation, operands = instruction
        try:
            if opcode in ["JMP", "JLE", "JE", "JGE", "JG", "JL", "JNE"]:
                new_address = operation(*operands)
                if new_address is not None:
                    self.registers["PC"] = new_address - 1
            else:
                result = operation(*operands)
                if isinstance(result, Interrupt):
                    raise result
                else:
                    self.registers["SP"] = result
        except Interrupt as interrupt:
            raise interrupt
        except Exception as e:
            raise InstructionError(f"Error executing instruction: {e}")

    def cycle(self, process: Process, mem: Memory):
        try:
            instruction = self.fetch(process, mem)
            decoded_instruction = self.decoder.decode(instruction)
            self.execute(decoded_instruction)
        except Exception as e:
            if isinstance(e,Interrupt):
                raise Interrupt("Fuck")
            else:
                raise e
