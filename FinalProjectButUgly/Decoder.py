from Memory import Memory
from Interrupt import Interrupt
from Instruction import Instruction
from InstructionError import InstructionError
import functools
from typing import Tuple, Any
class Decoder:
    #fetch: Memory + 
    def fetch(mem_loc: Memory, location: int) -> Instruction:
        try:
            return mem_loc[location]
        except IndexError:
            pass#IMPLEMENT LATER
    def decode(inst: Instruction)->Tuple[str,Any,list]:
        #lets me pass a no argument function.
        def NOP():
            pass
        instructions = (inst.mnemonic(),(lambda: NOP()),inst.operands())
        match inst:
            case Instruction(name="NOP"):
                pass #this is the proper "NOP" instruction.
            case Instruction(name="ADD"):
                instructions[1] = (lambda a: sum(a))#We return the instruction to be executed and the operands
            case Instruction(name="SUB"):
                instructions[1] = (lambda a: functools.reduce(lambda x,y: x-y,a,initializer=0))
            case Instruction(name="DIV"):
                instructions[1] = (lambda a: functools.reduce(lambda x,y: x/y,a,initializer=0))
            case Instruction(name="MUL"):
                instructions[1] = (lambda a: functools.reduce(lambda x,y: x*y,a, initializer=0))
            case Instruction(name="CMP"):
                instructions[1] = (lambda a,b: 1 if a>b \
                    else -1 if a<b else 0)
            case Instruction(name="AND"):
                instructions[1] = (lambda x,y: x and y)
            case Instruction(name="OR"):
                instructions[1] = (lambda x,y: x or y)
            case Instruction(name="NOR"):
                instructions[1] = (lambda x,y: not (x or y))
            case Instruction(name="XOR"):
                instructions[1] = (lambda x,y: True if ((x and not y) or (y and not x)) else False)
            case Instruction(name="NAND"):
                instructions[1] = (lambda x,y: not (x and y))
            case Instruction(name="MOV"):
                instructions[1] = Interrupt(name="MOV interrupt",data=instructions[2])
            case Instruction(name="RET"): #terminates the execution of a procedure and transfers control through a back-link on the stack to the program that originally invoked the procedure
                instructions[1] = Interrupt(name="Process-controlled Termination",data=instructions[2])
            case Instruction(name="JMP"):
                instructions[1] = (lambda a,b: b)
            case Instruction(name="JLE"):#If val(SP) <= 0 then change Program Counter
                instructions[1] = (lambda a,b: b if a<=0 else None)
            case Instruction(name="JE"):
                instructions[1] = (lambda a,b: b if a==0 else None)
            case Instruction(name="JGE"):
                instructions[1] = (lambda a,b: b if a>=0 else None)
            case Instruction(name="JL"):
                instructions[1] = (lambda a,b: b if a<0 else None)
            case Instruction(name="JG"):
                instructions[1] = (lambda a,b: b if a>0 else None)
            case Instruction(name="JNE"):
                instructions[1] = (lambda a,b: b if a!=0 else None)
            case Instruction(name="PRINT"):
                instructions[1] =  Interrupt("PRINT",data=instructions[2])
            case Instruction(name="INPUT"):
                instructions[1] =  Interrupt("INPUT",data=instructions[2])
            case _:
                raise InstructionError
        return instructions
