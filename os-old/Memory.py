"""
read (proper usage):
CPU and Printer can use freely
write (proper usage):
CPU and Printer may use freely
process (execute):
this is a cpu-exclusive function for
executing assembler written in the printer's format
printers format would look like the following
MOV 10 eax
MULT 10 eax -> ACC = 100
MOV ACC eax

"""
class Memory:
    #Cache, Main Memory(RAM), Hard Disk (HDD)
    def __init__(self):
        self.cache=[0]*512 #"512 KB" cache
        self.ram = [0]*1024 #"1 MB" RAM
    def RAM(self):
        return self.ram
    def CACHE(self):
        return self.cache