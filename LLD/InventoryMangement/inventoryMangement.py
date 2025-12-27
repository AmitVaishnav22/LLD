from abc import ABC,abstractmethod
import math

class Product:
    
    def __init__(self,sku,name,price):
        self._sku=sku
        self._name=name
        self._price=price

    def getProductSku(self):
        return self._sku

    def getProductName(self):
        return self._name

    def getProductPrice(self):
        return self._price

class ProductFactory:
    def createProduct(self,sku):
        _name=""
        _price=0.0

        if sku==101:
            _name="Apple"
            price=20
        elif sku==102:
            _name="Banana"
            _price=10
        elif sku==103:
            _name="Chocolate"
            _price=50
        elif sku==201:
            _name="T-shirt"
            _price=500
        elif sku==202:
            _name="Jeans"
            _price=1000
        else:
            _name="Item"+str(sku)
            _price=100
        return Product(sku,_name,_price)

class InventoryStore(ABC):
    @abstractmethod
    def addProduct(self,p:Product,q):
        pass
    def removeProduct(self,sku,q):
        pass
    def checkStock(self,sku):
        pass
    def listAllAvailableProducts(self):
        pass

class DBInventoryStore(InventoryStore):
    def __init__(self):
        self._stock={}
        self._products={}

    def addProduct(self,p,q):
        sku=p.getProductSku()
        if sku not in self._products:
            self._products[sku]=p
        if sku in self._stock:
            self._stock[sku]+=q
        else:
            self._stock[sku]=q  
    
    def removeProduct(self,sku,q):
        if sku not in self._stock:
            return 
        currentQ=self._stock[sku]
        self._stock[sku]-=q
        remaining=currentQ-q
        if remaining>0:
            self._stock[sku]=remaining
        else:
            del self._stock[sku]
            del self._products[sku]

    def checkStock(self,sku):
        return self._stock[sku] if sku in self._stock else 0

    def listAllAvailableProducts(self):
        available=[]
        for sku,q in self._stock.items():
            if q<=0:
                continue
            if sku not in self._products:
                continue
            product=self._products[sku]
            available.append(product)
        return available


class InventoryManager:
    def __init__(self,store):
        self._store=store
    def addStock(self,sku,q):
        prod=ProductFactory().createProduct(sku)
        self._store.addProduct(prod,q)
        print(f"[InventoryManager] Added sku {sku} qnt {q}")
    def removeStock(self,sku,q):
        self._store.removeProduct(sku,q)
    def checkStock(self,sku):
        return self._store.checkStock(sku)
    def getAvailableProducts(self):
        return self._store.listAllAvailableProducts()


class ReplenishStrategy(ABC):
    @abstractmethod
    def replenish(self,itemsToReplenish,inventoryManager):
        pass

class ThresholdReplenishStrategy(ReplenishStrategy):
    def __init__(self,threshold):
        self._threshold=threshold
    def replenish(self,itemsToReplenish,inventoryManager):
        print("[ThresholdStrat] checking items.....")
        
        for sku,q in itemsToReplenish.items():
            current=inventoryManager.checkStock(sku)
            if current<self._threshold:
                inventoryManager.addStock(sku,q)
                print(f"[ThresholdStrat] sku->{sku} got replenish from {current} to {q}")
    def weeklyreplenish(self,itemsToReplenish,inventoryManager):
        print("[WeeklyStrat] being called on the itemsToReplenish")

class DarkStore:
    def __init__(self,name,ux,uy,mgr):
        self._name=name
        self._ux=ux
        self._uy=uy
        self._inventoryManager=mgr(DBInventoryStore())
        self._replenishStrat=None

    def distanceTo(self,x,y):
        return math.sqrt((self._ux-x)*(self._ux-x)+(self._uy-y)*(self._uy-y))

    def runReplenish(self,itemsToReplenish):
        if self._replenishStrat!=None:
            self._replenishStrat.replenish(itemsToReplenish,self._inventoryManager)
    
    def getAllProducts(self):
        return self._inventoryManager.getAvailableProducts()
    
    def checkStock(self,sku):
        return self._inventoryManager.checkStock(sku)

    def removeStock(self,sku,q):
        return self._inventoryManager.removeStock(sku,q)

    def addStock(self,sku,q):
        return self._inventoryManager.addStock(sku,q)

    def setReplenishStrat(self,strat):
        self._replenishStrat=strat

    def getName(self):
        return self._name
    def getInventoryManager(self):
        return self._inventoryManager
    def getLocation(self):
        return (self._ux,self._uy)

class DarkStoreManager:
    _instance=None
    @staticmethod
    def getInstance():
        if DarkStoreManager._instance is None:
            DarkStoreManager._instance=DarkStoreManager()
        return DarkStoreManager._instance

    def __init__(self):
        self._darkstores=[]

    def registerDarkStore(self,ds):
        self._darkstores.append(ds)

    def getNearbyDarkStores(self,ux,uy,maxDistance):
        distList=[]
        for ds in self._darkstores:
            dist=ds.distanceTo(ux,uy)
            if dist<=maxDistance:
                distList.append([dist,ds])
        distList.sort()
        res=[]
        for d,ds in distList:
            res.append(ds)        
        return res

class Cart:
    def __init__(self):
        self._items=[]
    def addItem(self,sku,q):
        prod=ProductFactory().createProduct(sku)
        self._items.append([prod,q])
        print(f"[Cart] added sku{sku} quantity {q}")
    def getTotal(self):
        total=0
        for item,q in self._items:
            total+=(item.getProductPrice()*q)
        return total
    def getItems(self):
        return self._items

class User:
    def __init__(self,name,x,y):
        self._name=name
        self._x=x 
        self._y=y 
        self._cart=Cart()

    def getUserName(self):
        return self._name
    def getX(self):
        return self._x
    def getY(self):
        return self._y

    def getCart(self):
        return self._cart
    
class DeliveryPatner:
    def __init__(self,name):
        self._name=name
    def getDeliveryPatnerName(self):
        return self._name

class Order:
    _nextId=1
    def __init__(self,user):
        self._orderId=Order._nextId
        Order._nextId+=1
        self._user=user
        self._items=[]
        self._patners=[]
        self._totalAmount=0

class OrderManager:
    _instance=None
    @staticmethod
    def getInstance():
        if OrderManager._instance is None:
            OrderManager._instance=OrderManager()
        return OrderManager._instance

    def __init__(self):
        self._orders=[]

    def placeOrder(self,user,cart):
        print(f"[OrderManager] placing order for {user.getUserName()}")

        requestedItems=cart.getItems()
        maxiD=5
        nearByStores=DarkStoreManager.getInstance().getNearbyDarkStores(user.getX(),user.getY(),maxiD)
        if len(nearByStores)==0:
            print("No near By DarkStores found from your location")
            return 
        firstStore=nearByStores[0]
        allInFirst=True
        for prod,q in requestedItems:
            sku=prod.getProductSku()
            if firstStore.checkStock(sku)<q:
                allInFirst=False
                break

        order=Order(user)
        if allInFirst:
            print(f"All items found at {firstStore.getName()}")
            for prod,q in requestedItems:
                sku=prod.getProductSku()
                firstStore.removeStock(sku,q)
                order._items.append((prod,q))
            order._totalAmount=cart.getTotal()
            order._patners.append(DeliveryPatner("Patner1"))
            print(f"Assigned Patner : {order._patners[0].getDeliveryPatnerName()}")
        
        else:
            print("Splitting order across stores....")
            allItems={}
            for prod,q in requestedItems:
                sku=prod.getProductSku()
                if sku in allItems:
                    allItems[sku]+=q
                else:
                    allItems[sku]=q
            patnerId=1

            for store in nearByStores:
                if not allItems:
                    break
                print(f"Checking {store.getName()}")
                toErase=[]
                for sku, qty in list(allItems.items()):
                    availableQ=store.checkStock(sku)
                    if availableQ<=0:
                        continue
                    takenQ=min(availableQ,qty)
                    store.removeStock(sku,takenQ)
                    print(f"Taking sku {sku} quantity {takenQ} from {store.getName()}")
                    order._items.append((ProductFactory().createProduct(sku),takenQ))
                    if qty>takenQ:
                        allItems[sku]=qty-takenQ
                    else:
                        toErase.append(sku)
                for sku in toErase:
                    del allItems[sku]
                
                if toErase:
                    pname="Patner"+str(patnerId)
                    patnerId+=1
                    order._patners.append(DeliveryPatner(pname))
                    print(f"Assigned Patner : {pname} for store {store.getName()}")
            if allItems:
                print("Could not fullfil the order, some items are missing")
                for sku, qty in allItems.items():
                    print(f"SKU {sku} x{qty}")
            total=0
            for prod,q in order._items:
                total+=(prod.getProductPrice()*q)
            order._totalAmount=total
        print(f"[OrderManager] Order {order._orderId} Summary ::")
        print(f"User: {user.getUserName()}\n  Items:")

        for prod,q in order._items:
            print(f"{prod.getProductName()} (SKU:{prod.getProductSku()}) x{q} @ {prod.getProductPrice()} each")
        print(f"Total Amount: {order._totalAmount}")
        print("Delivery Patners:")
        for patner in order._patners:
            print(f"- {patner.getDeliveryPatnerName()}")
        self._orders.append(order)

    def getOrders(self):
        return self._orders

class ZeptoHelper:
    def showAllItems(self,user):
        print(f"[ZeptoHelper] Showing all items for user {user.getUserName()} with in 5 KM")
        dsManager=DarkStoreManager.getInstance()
        nearByStores=dsManager.getNearbyDarkStores(user.getX(),user.getY(),5)
        skutoPrice={}
        skutoName={}
        for ds in nearByStores:
            for prod in ds.getAllProducts():
                sku=prod.getProductSku()
                if sku not in skutoPrice:
                    skutoPrice[sku]=prod.getProductPrice()
                    skutoName[sku]=prod.getProductName()
        for sku, price in skutoPrice.items():
            name=skutoName[sku]
            print(f"SKU:{sku} Name:{name} Price:{price}")

    def initialize(self):
        dsManager=DarkStoreManager.getInstance()

        ds1=DarkStore("DarkStore1",0,0,InventoryManager)
        ds1.setReplenishStrat(ThresholdReplenishStrategy(10))
        ds1.addStock(101,50)
        ds1.addStock(102,30)
        ds1.addStock(201,20)
        dsManager.registerDarkStore(ds1)

        ds2=DarkStore("DarkStore2",3,4,InventoryManager)
        ds2.setReplenishStrat(ThresholdReplenishStrategy(10))
        ds2.addStock(101,20)
        ds2.addStock(103,40)
        ds2.addStock(202,15)
        dsManager.registerDarkStore(ds2)

        ds3=DarkStore("DarkStore3",10,10,InventoryManager)
        ds3.setReplenishStrat(ThresholdReplenishStrategy(10))
        ds3.addStock(102,25)
        ds3.addStock(201,30)
        ds3.addStock(202,20)
        dsManager.registerDarkStore(ds3)

if __name__=="__main__":
    zepto=ZeptoHelper()
    zepto.initialize()

    user1=User("Alice",1,1)
    print(f"User with {user1.getUserName()} logged in ")

    zepto.showAllItems(user1)

    print("Adding items to cart...")
    cart=user1.getCart()
    cart.addItem(101,5)
    cart.addItem(102,10)
    cart.addItem(201,2)

    cart2=user1.getCart()
    cart2.addItem(101,30)
    cart2.addItem(103,5)
    cart2.addItem(202,10)

    OrderManager.getInstance().placeOrder(user1,cart)

    # splting order
    OrderManager.getInstance().placeOrder(user1,cart2)
    print("Demo Completed.")
