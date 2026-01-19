from Models.order import Order

class DeliverOrder(Order):
    def __init__(self):
        self._address = ""

    def get_type(self):
        return "Delivery"

    def setaddress(self,addr):
        self._address=addr
    
    def getaddress(self):
        return self._address
