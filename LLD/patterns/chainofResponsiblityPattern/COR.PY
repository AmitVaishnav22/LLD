from abc import ABC,abstractmethod

# Chain of Responsibility (CoR) is a pattern where a request is passed along a chain of handlers.
# Each handler decides whether to process the request or pass it to the next handler in the chain. This decouples the sender of the request from its receivers.

class MoneyHandler(ABC):
    def __init__(self):
        self._nextHandler=None
    def setHandler(self,nextHandler):
        self._nextHandler=nextHandler
    @abstractmethod
    def dispence(self,amount):
        pass

class OneThousandHandler(MoneyHandler):
    def __init__(self,numOfNotes):
        self._nom=numOfNotes
    def dispence(self,amount):
        requiredNotes=amount//1000
        if requiredNotes>self._nom:
            requiredNotes=self._nom
            self._nom=0
        else:
            self._nom-=requiredNotes
        if requiredNotes>0:
            print(f"Dispensing {requiredNotes} notes of 1000.")
        remainingAmount=amount-(requiredNotes*1000)
        if remainingAmount>0:
            if (self._nextHandler):
                self._nextHandler.dispence(remainingAmount)
            else:
                print(f"Remaining Amount of {remainingAmount} cant be fulfilled")
        
class FiveHundredHandler(MoneyHandler):
    def __init__(self,numOfNotes):
        self._nom=numOfNotes
    def dispence(self,amount):
        requiredNotes=amount//500
        if requiredNotes>self._nom:
            requiredNotes=self._nom
            self._nom=0
        else:
            self._nom-=requiredNotes
        if requiredNotes>0:
            print(f"Dispensing {requiredNotes} notes of 500.")
        remainingAmount=amount-(requiredNotes*500)
        if remainingAmount>0:
            if (self._nextHandler):
                self._nextHandler.dispence(remainingAmount)
            else:
                print(f"Remaining Amount of {remainingAmount} cant be fulfilled")
        
class TwoHundredHandler(MoneyHandler):
    def __init__(self,numOfNotes):
        self._nom=numOfNotes
    def dispence(self,amount):
        requiredNotes=amount//200
        if requiredNotes>self._nom:
            requiredNotes=self._nom
            self._nom=0
        else:
            self._nom-=requiredNotes
        if requiredNotes>0:
            print(f"Dispensing {requiredNotes} notes of 200.")
        remainingAmount=amount-(requiredNotes*200)
        if remainingAmount>0:
            if (self._nextHandler):
                self._nextHandler.dispence(remainingAmount)
            else:
                print(f"Remaining Amount of {remainingAmount} cant be fulfilled")
        
class OneHundreadHandler(MoneyHandler):
    def __init__(self,numOfNotes):
        self._nom=numOfNotes
    def dispence(self,amount):
        requiredNotes=amount//100
        if requiredNotes>self._nom:
            requiredNotes=self._nom
            self._nom=0
        else:
            self._nom-=requiredNotes
        if requiredNotes>0:
            print(f"Dispensing {requiredNotes} notes of 100.")
        remainingAmount=amount-(requiredNotes*100)
        if remainingAmount>0:
            if (self._nextHandler):
                self._nextHandler.dispence(remainingAmount)
            else:
                print(f"Remaining Amount of {remainingAmount} cant be fulfilled")
        
if __name__=="__main__":
    oneThou=OneThousandHandler(5)
    fiveHun=FiveHundredHandler(5)
    twoHund=TwoHundredHandler(5)
    oneHund=OneHundreadHandler(5)
    oneThou.setHandler(fiveHun)
    fiveHun.setHandler(twoHund)
    twoHund.setHandler(oneHund)
    oneHund.setHandler(None)
    targetAmount=9000
    oneThou.dispence(targetAmount)
