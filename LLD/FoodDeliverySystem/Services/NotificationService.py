class NotificationService:
    def __init__(self):
        pass
    def notify(self, order):
        print(f"Notification: Your order with ID {order.get_type()} has been placed successfully.")
        print(f"Total Cost: {order.get_total()}"
              f" and will be delivered to {order.get_user().get_address()}.")
        items=order.get_items()
        print("Order Details:")
        for item in items:
            print(f"- {item.get_name()}: ${item.get_price()}")
        print("Thank you for ordering with us!")
    