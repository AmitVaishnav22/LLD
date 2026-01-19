from Models.restaurant import Restaurant
from Models.menuItem import MenuItem
from Managers.restaurantManager import RestaurantManager
from Managers.orderManager import OrderManager as om
from Services.NotificationService import NotificationService
from Factories.NowOrderFactory import NowOrderFactory
from Factories.ScheduleOrderFactory import ScheduleOrderFactory
from Strategies.CCPayment import CreditCardPayment
from Strategies.UPIPayment import UPIPayment


class APP:
    def __init__(self):
        self.InitializeSystem()

    def InitializeSystem(self):
        r1=Restaurant("Biriyani House","Delhi")
        r2=Restaurant("Pizza Hut","Delhi")
        r3=Restaurant("Burger King","Delhi")

        r1.add_menu_item(MenuItem(1,"Veg Biriyani",150))
        r1.add_menu_item(MenuItem(2,"Pullav Biriyani",200))
        r2.add_menu_item(MenuItem(3,"Pizza",300))
        r2.add_menu_item(MenuItem(4,"Pepperoni Pizza",350))
        r3.add_menu_item(MenuItem(5,"Veg Burger",120))
        r3.add_menu_item(MenuItem(6,"Vegi Burger",150))
        rm=RestaurantManager.get_instance()
        rm.add_restaurant(r1)
        rm.add_restaurant(r2)
        rm.add_restaurant(r3)

    def searchRestaurantByLoc(self,name):
        rm=RestaurantManager.get_instance()
        return rm.search_by_loc(name)
    
    def selectRestaurant(self,user,res):
        cart=user.get_cart()
        cart.set_restaurant(res)

    def addItemToCart(self,user,itemcode):
        res=user.get_cart().get_restaurant()
        if res is None:
            print("No restaurant selected")
            return
        
        for item in res.get_menu():
            if item.get_code()==itemcode:
                user.get_cart().add_item(item)
                return
        print("Item not found")
    
    def checkOutNow(self,user,order_type,payment_method):
        return self.checkout(user,order_type,payment_method,NowOrderFactory())

    def scheduleOrder(self,user,order_type,payment_method,scheduled_time):
        return self.checkout(user,order_type,payment_method,ScheduledOrderFactory(scheduled_time))

    def checkout(self,user,order_type,payment_method,order_factory):
        cart=user.get_cart()
        restaurant=cart.get_restaurant()
        menu_items=cart.get_items()
        totalcost=cart.get_total_cost()
        _payment_strategy=None

        if payment_method=="Card":
            _payment_strategy=CreditCardPayment("1234-5678-9876-5432","John Doe","123","12/25")
        elif payment_method=="UPI":
            _payment_strategy=UPIPayment("123456@upi")
        else:
            print("Invalid payment method")
            return None

        order=order_factory.create_order(user,cart,restaurant,menu_items,_payment_strategy,totalcost,order_type)
        om.get_instance().addOrder(order)
        #print(order.get_order_id()," created successfully")
        return order

    def payForOrder(self,order):
        payment_status=order.process_payment()
        print("Processing payment...",order.get_total())
        if payment_status:
            NotificationService().notify(order)
            print(f"Payment of amount {order.get_total()} successful for order id {order.get_order_id()}")
        else:
            print("Payment failed")
        
    def printUserCart(self,user):
        print("User Cart Details:")

        for item in user.get_cart().get_items():
            print(f"Item: {item.get_name()}, Price: {item.get_price()}")
        print(f"Total Cost: {user.get_cart().get_total_cost()}")
    

    
