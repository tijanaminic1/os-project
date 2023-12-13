
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
    def NAME(self):
        return self.name
    #MESSAGE: -> Object
    #Purpose: Returns a message that is useful
    #for handling the interrupt.
    def MESSAGE(self):
        return self.message