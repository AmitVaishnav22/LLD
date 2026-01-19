from Factories.IOrderFactory import IOrderFactory
from Models.deliverorder import DeliverOrder
from Models.pickuporder import PickupOrder
from datetime import datetime

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
        #order.set_items(cart)
        order.set_restaurant(restaurant)
        order.set_items(menu_items)
        order.set_payment_strategy(_payment_strategy)
        order.set_total(totalcost)
        order.set_scheduled(datetime.now())
        return order