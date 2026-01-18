class OrderManager:
    _instance=None

    def __init__(self):
        self.orders=[]

    @staticmethod
    def get_instance():
        if OrderManager._instance is None:
            OrderManager._instance=OrderManager()
        return OrderManager._instance

    def addOrder(self,order):
        self.orders.append(order)

    def listOrders(self):
        print("Listing all the orders")
        for order in self.orders:
            print(f"Order ID: {order.get_type()}, Customer: {order.get_user().get_name()}, Total: {order.get_total()}")

        