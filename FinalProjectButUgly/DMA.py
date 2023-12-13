from Memory import Memory
from Cache import Cache
from RAM import RAM
from Process import Process
from Interrupt import Interrupt

class DMA:
    @staticmethod
    def SEND(source: Process, message, destination: RAM):
        try:
            binding_var, binding_value = message
            destination[source.parent()][binding_var] = binding_value
        except KeyError:
            raise Interrupt("DMAIndexOutOfBounds")
    @staticmethod
    def REQUEST(source: Process, message, destination: RAM):
        try:
            return destination[source.parent()][message]
        except KeyError:
            raise Interrupt("DMAIndexOutOfBounds")
