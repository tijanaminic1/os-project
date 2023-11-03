

class Instruction:

    #default constructor
    def __init__(self):
        self.name = "NOP"
        self.arguments = []
    #Non-default constructor.
    def __init__(self,*args):
        if len(args) == 0:
            self.name = "NOP"
            self.arguments = []
        elif len(args) == 1:
            self.
        else:
            match args[0]:
                case "ADD":
                    pass
                case "SUB":
    #
    @staticmethod def makeInstruction(str):
        word = str.split(" ")
        return Instruction(word)
