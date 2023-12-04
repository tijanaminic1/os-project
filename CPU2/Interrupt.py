from dataclasses import dataclass
from typing import Any
@dataclass
class Interrupt(Exception):
    name: str #name of interrupt
    data: Any #additional information.
    # items: -> Any
    #Purpose: returns the data category of the interrupt
    def info(self):
        return self.data