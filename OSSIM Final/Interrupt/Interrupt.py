
class Interrupt(Exception):
    def _init__(self,name,message):
        self.name = name
        self.message = message
    #NAME: -> Str
    #Purpose: Returns the name of the Interrupt,
    #which, alongide its message, is used to handle it.
    #Interrupt names provide identification, while
    #interrupt messages provide vital data used
    #for their handling scheme.
    @property.getter
    def NAME(self):
        return self.name
    #MESSAGE: -> Object
    #Purpose: Returns a message that is useful
    #for handling the interrupt.
    @property.getter
    def MESSAGE(self):
        return self.message
#HANDLE: Interrupt -> Effect!
#Purpose: When an interrupt is signalled,
#the HANDLE(Interrupt) function defines an
#approach to deal with the particular interrupt
@staticmethod
def HANDLE(interrupt: Interrupt):
    match interrupt:
        case Interrupt(name="PRINT"):
            print(interrupt.MESSAGE())
        case Interrupt(name="INPUT"):
            input(interrupt.MESSAGE())
        case Interrupt(name="DMAFatalError"):#TODO: Estalish recovery protocol for DMA failure.
            print("DMA failed due to fatal error.")
        case Interrupt(name="DMAIndexOutOfBounds"): #This is also a type of Page Fault
            print("DMA failed! Entry does not exist.")
        case Interrupt(name="ProcessTooLarge"):#TODO: Generally a fatal error, unless we do VRAM.
            print("Process too large to fit in the cache!")
        case Interrupt(name="CacheBottleneck"):#TODO: Integrate this with scheduling algorithm. It is a scheduling issue.
            print("Not enough space to fit"f" {interrupt.data} right now.")