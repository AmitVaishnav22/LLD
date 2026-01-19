from Facade import APP
from Models.user import User
from Strategies.UPIPayment import UPIPayment as UPIPaymentStrategy


if __name__ == "__main__":
    app=APP()

    user=User(101,"Alice","Delhi")

    print("user",user.get_name())

    resList=app.searchRestaurantByLoc("Delhi")

    print("Search Results:",resList)
    if len(resList)>0:
        print("Restaurants in Delhi:")
        for res in resList:
            print(f"Restaurant: {res.get_name()}")
            for item in res.get_menu():
                print(f"  Item Code: {item.get_code()}, Name: {item.get_name()}, Price: {item.get_price()}")
    else:
        print("No restaurants found in Delhi")

    app.selectRestaurant(user,resList[0])
    print(f"Selected Restaurant: {resList[0].get_name()}")
    app.addItemToCart(user,1)
    app.addItemToCart(user,2)

    app.printUserCart(user)

    order=app.checkOutNow(user,"Delivery","UPI")

    print("Order Details:",order.get_order_id(),order.get_total())

    app.payForOrder(order)


