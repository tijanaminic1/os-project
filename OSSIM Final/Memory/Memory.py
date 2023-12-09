from dataclasses import dataclass
from typing import List, Literal, TypeVar, Generic, Tuple, Dict
from collections.abc import Iterable
from ..Interrupt import Interrupt
T = TypeVar['T']
@dataclass
class Memory:
    data: List[T]#self.data

    #DATA: -> List[T]
    #Purpose: Returns the length of the list
    def __len__(self):
        return len(self.data)
    @property
    def DATA(self)->List[T]:
        return self.data
    
    @data.setter
    #write: int T -> void
    #Purpose: To overwrite a number of elements on the list
    def write(self, start_index: int, data: T or Iterable[T])->Memory:
        try:
            if isinstance(data,Iterable):
                for idx in range(len(data)):
                    #Effect!: data[index+i] is set to data[i]
                    self.data[start_index+idx] = data[idx]
            else:
                self.data[start_index] = data
        except IndexError:
            raise Interrupt("WriteOutOfBounds")
    #read: int -> T
    #purpose: returns the element of the list under the given index
    @data.getter
    def read(self,index:int)->T:
        try:
            return self.data[index]
        except IndexError:
            raise Interrupt("ReadOutOfBounds")
    #free: -> Effect!
    #purpose: clears the memory
    @data.deleter
    def free(self):
        self.data = map(lambda x: (x := None),self.data) #Effect! Memory is cleared.