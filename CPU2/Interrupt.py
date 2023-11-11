from dataclasses import dataclass
from typing import Any
@dataclass
class Interrupt:
    name: str #name of interrupt
    data: Any #additional information.
    # items: -> Any
    #Purpose: returns the data category of the interrupt
    def items(self):
        return self.data