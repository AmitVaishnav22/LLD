from abc import ABC,abstractmethod

# assume a single source / entry running multiple dependencies, like turning on systems , game engines etc

# subsystems

class PowerSupply:
    def providePower(self):
        print("Providing Power to the System")
    
class CoolingSystem:
    def startFans(self):
        print("Cooling Fans Strarted")

class CPU:
    def initialise(self):
        print("CPU initialised")

class Memory:
    def selfTest(self):
        print("Memory self test passed ")

class HardDrive:
    def spinUp(self):
        print("Hard Drive Spinned Up")

class BIOS:
    # def __init__(self,cpu:CPU,memory:Memory):
    #     self._cpu=cpu
    #     self._memory=memory
    def boot(self,cpu:CPU,memory:Memory):
        print("Booting the system")
        cpu.initialise()
        memory.selfTest()

class OperatingSystem:
    def load(self):
        print("OS Loaded to the memory")
    
class ComputerFacade:
    def __init__(self):
        self._powersupply=PowerSupply()
        self._coolingsystem=CoolingSystem()
        self._cpu=CPU()
        self._memory=Memory()
        self._harddrive=HardDrive()
        self._bios=BIOS()
        self._os=OperatingSystem()

    def startComputer(self):
        print("---- Starting Computer ----")
        self._powersupply.providePower()
        self._coolingsystem.startFans()
        self._bios.boot(self._cpu,self._memory)
        self._harddrive.spinUp()
        self._os.load()
        print("---- computer booted successfully ----")

if __name__=="__main__":
    # client
    computer=ComputerFacade()
    computer.startComputer()