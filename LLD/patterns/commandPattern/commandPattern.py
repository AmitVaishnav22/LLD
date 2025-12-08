from abc import ABC,abstractmethod

# command design pattern is used in bool reversable undo patterns

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    @abstractmethod
    def undo(self):
        pass

# concete classes light and fan
class Light:
    def on(self):
        print("Light is On !!")
    def off(self):
        print("Light is Off !!")

class Fan:
    def on(self):
        print("Fan is On !!")
    def off(self):
        print("Fan is Off !!")

class LightCommand(Command):
    def __init__(self):
        self.light=Light()
    def execute(self):
        self.light.on()
    def undo(self):
        self.light.off()

class FanCommand(Command):
    def __init__(self):
        self.fan=Fan()
    def execute(self):
        self.fan.on()
    def undo(self):
        self.fan.off()

# Remote Controller with static buttons
class RemoteController:
    def __init__(self,n):
        self.num=n
        self.buttons=[None]*self.num
        self.isToggeled=[False]*self.num
    def setCommand(self,i,command:Command):
        if i>=0 and i<self.num:
            self.buttons[i]=command
            self.isToggeled[i]=False
    def pressButton(self,i):
        if i>=0 and i<self.num:
            if self.buttons[i] is None:
                print("Command not initialised")
                return
            if not self.isToggeled[i]:
                self.buttons[i].execute()
            else:
                self.buttons[i].undo()
        return None
    
if __name__=="__main__":
    light=LightCommand()
    fan=FanCommand()
    remote=RemoteController(5) # remote controller with 5 working buttons
    remote.setCommand(1,light)
    remote.setCommand(2,fan)
    remote.pressButton(1)
    remote.pressButton(2)
    remote.pressButton(3)
