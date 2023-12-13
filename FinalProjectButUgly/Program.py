from typing import List, Any, Dict
from dataclasses import dataclass, field
from Registry import Registry
from Process import Process
#TODO
@dataclass
class Program:
    data: List[Process] = field(default_factory=list)
    registry: Registry = field(default_factory=Registry)
    bindings: Dict[str,Any] = field(default_factory=dict)#dictionary of variable bindings for a program.
    size: int = 0
    address_space=None
    def __post_init__(self):
        self.size = sum(len(process) for process in self.data)
    def reference(self, varname: str):
        return self.bindings.get(varname)
    #The size of a program is the size of all of the subprocesses
    #inside that program.
    def __len__(self):
        return sum(len(process) for process in self.data)
    def __getitem__(self,key):
        return self.data[key]
    def __setitem__(self,key,newvalue):
        self.data[key] = newvalue
    def set_address_space(self, ads):
        self.address_space=ads
        for datum in self.data:
            datum.set_address_space(ads)