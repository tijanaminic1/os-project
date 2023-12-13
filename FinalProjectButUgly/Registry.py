from collections.abc import MutableMapping
from dataclasses import dataclass
@dataclass
class Registry:
    A: int
    B: int
    C: int
    D: int
    E: int
    F: int
    PC: int
    SP: int
    #values: -> List(Registers)
    #Purpose: returns the registers as an iterable (list)
    def values(self):
        return [self.A,self.B,self.C,self.D,self.E,self.F,self.PC,self.SP]
    
    def __iter__(self):
        return iter(self.values())
    def __len__(self):
        return len(self.values())
    #getitem: Register Name -> int
    #purpose: Given a particular register name, it will return the high byte, low byte,
    #or full register.
    def __getitem__(self, key):
        if key in ["A","B","C","D","E","F","PC","SP"]:
            return getattr(self, key)
        else:
            raise KeyError(f"No such register {key}")
    #setitem: [register name] + value -> Effect!
    # Purpose: Modifies the value stored in a given register.
    # Warning: Raises a key-error if a nonexistent location is provided.        
    def __setitem__(self, key, value):
        if key in ["A","B","C","D","E","F","PC","SP"]:
            setattr(self, key, value)
        else:
            raise KeyError(f"No such register {key}")
    #one cannot delete a, register, but @dataclass wants this, so best to include it.
    def __delitem__(self, key):
        raise NotImplementedError("Register deletion is not supported")