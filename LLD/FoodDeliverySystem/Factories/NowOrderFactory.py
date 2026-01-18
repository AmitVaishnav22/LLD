class NowOrderFactory(IOrderFactory):

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
        order.set_order_time(datetime.now())
        return order