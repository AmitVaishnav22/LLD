from abc import ABC, abstractmethod

class IPaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass
        