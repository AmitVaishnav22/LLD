from abc import ABC, abstractmethod


class IOrderFactory(ABC):
    @abstractmethod
    def create_order(self,user,cart,restaurant,memu_items,_payment_strategy,totalcost,orderType):
        pass