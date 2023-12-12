from typing import List, Any, Dict
from dataclasses import dataclass
from ..CentralProcessor.Registry import Registry
from .Process import Process
#TODO
@dataclass
class Program:
    data: List[Process]
    registry: Registry
    bindings: Dict[str,Any]#dictionary of variable bindings for a program.
    size: 0
    def __post_init__(self):
        self.size = sum(len(process) for process in self.data)
    def reference(self, varname: str):
        return self.bindings.get(varname)
    
    #The size of a program is the size of all of the subprocesses
    #inside that program.
    def __len__(self):
        return self.size
    def __getitem__(self,key):
        return self.data[key]
    def __setitem__(self,key,newvalue):
        self.data[key] = newvalue