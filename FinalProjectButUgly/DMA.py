from Memory import Memory
from Cache import Cache
from RAM import RAM
from Interrupt import Interrupt
#DMA: source (Object)#TODO
class DMA:
    @staticmethod
    def SEND(client, destination: Memory):
        match destination:
            case Cache():
                pass
            case RAM():
                pass
            case Memory():
                pass
            case _:
                raise Interrupt("DMASendError")
    @staticmethod
    def REQUEST(client, source: Memory):
        match source:
            case Cache():
                pass
            case RAM():
                pass
            case Memory():
                pass
            case _:
                raise Interrupt("DMAReceiveError")
