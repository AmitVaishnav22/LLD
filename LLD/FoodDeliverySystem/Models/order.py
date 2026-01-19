from abc import ABC,abstractmethod

class Order(ABC):
    _idx=1
    def __init__(self):
        Order._idx+=1
        self._order_id=Order._idx
        self._user = None
        self._restaurant = None
        self._items = []
        self._payment_strategy = None
        self._total = 0.0
        self._scheduled = ""

    def process_payment(self):
        if self._payment_strategy is not None:
            self._payment_strategy.pay(self._total)
            return True
        else:
            print("Please choose a payment mode first")
            return False

    @abstractmethod
    def get_type(self):
        pass

    def get_order_id(self):
        return Order._idx

    def set_user(self, user):
        self._user = user

    def get_user(self):
        return self._user

    def set_restaurant(self, restaurant):
        self._restaurant = restaurant

    def get_restaurant(self):
        return self._restaurant

    def set_items(self, items):
        self._items = items
        self._total = 0
        for item in items:
            self._total += item.get_price()

    def get_items(self):
        return self._items

    def set_payment_strategy(self, strategy):
        self._payment_strategy = strategy

    def set_scheduled(self, scheduled_time):
        self._scheduled = scheduled_time

    def get_scheduled(self):
        return self._scheduled

    def get_total(self):
        return self._total

    def set_total(self, total):
        self._total = total