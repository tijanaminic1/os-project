from typing import List, Any, Dict
from dataclasses import dataclass
from ..CentralProcessor import Registry
from .Process import Process
#TODO
@dataclass
class Program:
    data: List[Process]
    bindings: Dict[str,Any]#dictionary of variable bindings for a program.

    def reference(self, varname: str):
        return self.bindings.get(varname)
    
    #The size of a program is the size of all of the subprocesses
    #inside that program.
    def __len__(self):
        return sum(len(process) for process in self.data)