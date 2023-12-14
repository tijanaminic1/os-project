from Memory import Memory
from Interrupt import Interrupt
from Instruction import Instruction
from InstructionError import InstructionError
import functools
from typing import Tuple, Any
"""
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
"""
class Decoder:
    def fetch(mem_loc: Memory, location: int) -> Instruction:
        try:
            return mem_loc[location]
        except IndexError:
            raise Interrupt("CacheMiss")

    def decode(inst: Instruction) -> Tuple[str, Any, list]:
        opcode = inst.mnemonic()
        operands = inst.operands()

        def operation_for_opcode(opcode):
            match opcode:
                #some arithmetic
                case "ADD":
                    return lambda *args: sum(args)
                case "SUB":
                    return lambda *args: args[0] - sum(args[1:])
                case "DIV":
                    return lambda a, b: a / b
                case "MUL":
                    return lambda a, b: a * b
                #boolean algebra
                case "AND":
                    return lambda a, b: a and b
                case "OR":
                    return lambda a, b: a or b
                case "NOR":
                    return lambda a, b: (not(a or b))
                case "XOR":
                    return lambda a, b: ((a and not b) or (not a and b))
                case "NAND":
                    return lambda a, b: (not(a and b))
                #fun in the namespace
                case "MOV": #like variable assignment
                    return Interrupt(name="MOV interrupt", data=operands)
                case "RET": #or carriage return
                    return Interrupt(name="Process-controlled Termination", data=operands)
                #Jumps
                case "JMP":
                    return lambda a: a
                case "JLE":
                    return lambda a, b: b if a <= 0 else None
                case "JE":
                    return lambda a, b: b if a == 0 else None
                case "JGE":
                    return lambda a, b: b if a >= 0 else None
                case "JG":
                    return lambda a, b: b if a > 0 else None
                case "JL":
                    return lambda a, b: b if a < 0 else None
                case "JNE":
                    return lambda a, b: b if a != 0 else None
                case "PRINT":
                    return Interrupt("PRINT", data=operands)
                case "INPUT":
                    return Interrupt("INPUT", data=operands)
                case _:
                    raise InstructionError(f"Unknown opcode: {opcode}")
                #out of principle I shall not implement PUSH or POP, because a reasoned programmer should be able
                #to think up a way to cleverly use instructions to achieve that ;)
        operation = operation_for_opcode(opcode)
        return opcode, operation, operands