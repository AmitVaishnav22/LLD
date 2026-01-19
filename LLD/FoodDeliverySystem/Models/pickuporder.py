from Models.order import Order

class PickupOrder(Order):
    def __init__(self):
        self._address = ""

    def get_type(self):
        return "Pickup"

    def setaddress(self, address):
        self._address = address

    def getaddress(self):
        return self._address