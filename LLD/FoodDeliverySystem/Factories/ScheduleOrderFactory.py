
class ScheduleOrderFactory(IOrderFactory):
    def __init__(self,scheduled_time):
        self.scheduled_time=scheduled_time

    def create_order(self,user,cart,restaurant,menu_items,_payment_strategy,totalcost,orderType):
        order=None
        if orderType=="Deliver":
            deliverOrder=DeliverOrder()
            deliverOrder.setaddress(user.get_address())
            order=deliverOrder
        else:
            pickupOrder=PickupOrder()
            pickupOrder.set_restaurant_address(restaurant.get_Location())
            order=pickupOrder

        order.set_user(user)
        order.set_cart(cart)
        order.set_restaurant(restaurant)
        order.set_menu_items(menu_items)
        order.set_payment_strategy(_payment_strategy)
        order.set_total_cost(totalcost)
        order.set_scheduled_time(self.scheduled_time)
        return order
    