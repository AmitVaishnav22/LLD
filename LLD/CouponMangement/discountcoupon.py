from abc import ABC,abstractmethod
from enum import Enum


class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self,amount):
        pass

class FlatDiscountStrategy(DiscountStrategy):
    def __init__(self,flat):
        self._flatamount=flat
    def calculate(self,amount):
        return min(amount,self._flatamount)

class PercentageDiscountStrategy(DiscountStrategy):
    def __init__(self,percentage):
        self._percentage=percentage
    def calculate(self,amount):
        return (amount*(self._percentage))//100

class PercentageWithCapStrategy(DiscountStrategy):
    def __init__(self,percentage,cap):
        self._percentage=percentage
        self._cap=cap
    def calculate(self,amount):
        disc=(amount*(self._percentage))//100
        if disc>self._cap:
            return self._cap
        return disc

class StrategyType(Enum):
    FLAT=1
    PERCENTAGE=2
    PERCENTAGEWITHCAP=3

class DiscountStrategyManager:
    _instance=None
    @staticmethod
    def getInstance():
        if DiscountStrategyManager._instance is None:
            DiscountStrategyManager._instance=DiscountStrategyManager()
        return DiscountStrategyManager._instance
    def getStrategy(self,sType,p1,p2):
        if sType==sType.FLAT:
            return FlatDiscountStrategy(p1)
        elif sType==sType.PERCENTAGE:
            return PercentageDiscountStrategy(p1)
        elif sType==sType.PERCENTAGEWITHCAP:
            return PercentageWithCapStrategy(p1,p2)
        return None

class Product:
    def __init__(self,name,category,price):
        self._name=name
        self._category=category
        self._price=price
    def getProductName(self):
        return self._name
    def getProductCategory(self):
        return self._category
    def getProductPrice(self):
        return self._price

class cartItem:
    def __init__(self,product,quantity):
        self._currentProduct=product
        self._quantity=quantity
    def getItemTotal(self):
        return self._currentProduct.getProductPrice()*self._quantity
    def getCurrentProduct(self):
        return self._currentProduct

class Cart:
    def __init__(self):
        self._items=[]
        self._originalTotal=0
        self._currentTotal=0
        self._loyalMember=True
        self._paymentBank=""
    
    def addProductCart(self,product:Product,quantity):
        currentCartItem=cartItem(product,quantity)
        self._items.append(currentCartItem)
        self._originalTotal+=currentCartItem.getItemTotal()
        self._currentTotal+=currentCartItem.getItemTotal()

    def getOriginalTotal(self):
        return self._originalTotal
    
    def getCurrentTotal(self):
        return self._currentTotal

    def applyDiscount(self,d):
        self._currentTotal-=d
        if self._currentTotal<0:
            self._currentTotal=0

    def setLoyalMember(self):
        self._loyalMember=True

    def getIsLoyal(self):
        return self._loyalMember

    def setPaymentBank(self,bank):
        self._paymentBank=bank

    def getPaymentBank(self):
        return self._paymentBank

    def getItems(self):
        return self._items

class Coupon(ABC):

    def __init__(self):
        self._next=None
    def setNext(self,next):
        self._next=next
    def getNext(self):
        return self._next

    def applyDiscount(self,cart):
        if self.isApplicable(cart):
            #print("YESS    ------------------------")
            dis=self.getDiscount(cart)
            #print("DIS --------------------",dis)
            cart.applyDiscount(dis)
            print(f"{self.name()} discount applied {dis}")
            if (not self.isCombinable()):
                return 
        if self._next:
            self._next.applyDiscount(cart)

    @abstractmethod
    def isApplicable(self,cart):
        pass
    @abstractmethod
    def getDiscount(self,cart):
        pass
    def isCombinable(self):
        return True
    @abstractmethod
    def name(self):
        pass

class SeasonalOffer(Coupon):
    def __init__(self,percent,category):
        super().__init__()
        self._percent=percent
        self._category=category
        self._strat=DiscountStrategyManager.getInstance().getStrategy(StrategyType.PERCENTAGE,percent,0)
    
    def isApplicable(self,cart):
        #print("YES")
        for item in cart.getItems():
            #print(item.getCurrentProduct().getProductCategory(),"PP")
            if item.getCurrentProduct().getProductCategory()==self._category:
                #print("YES")
                return True
        return False

    def getDiscount(self,cart):
        subTotal=0
        for item in cart.getItems():
            if item.getCurrentProduct().getProductCategory()==self._category:
                subTotal+=item.getItemTotal()
        #print("---------------",subTotal)
        x= self._strat.calculate(subTotal)
        #print("--------",x)
        return x 
    def name(self):
        return f"[seasonal offer] {self._percent}% off on {self._category}"

class LoyalityDiscount(Coupon):
    def __init__(self,percent):
        super().__init__()
        self._percent=percent
        self._strat=DiscountStrategyManager.getInstance().getStrategy(StrategyType.PERCENTAGE,percent,0)
    
    def isApplicable(self,cart):
        return cart.getIsLoyal()

    def getDiscount(self,cart):
        return self._strat.calculate(cart.getOriginalTotal())
    
    def name(self):
        return f"[loyality offer] {self._percent}% off "

class BulkPurchaseOff(Coupon):
    def __init__(self,threshold,flatoff):
        super().__init__()
        self._threshold=threshold
        self._flatoff=flatoff
        self._strat=DiscountStrategyManager.getInstance().getStrategy(StrategyType.FLAT,flatoff,0)

    def isApplicable(self,cart):
        return cart.getOriginalTotal()>=self._threshold

    def getDiscount(self,cart):
        return self._strat.calculate(cart.getCurrentTotal())

    def name(self):
        return f"[Bulk offer ] flat {self._flatoff} off for above {self._threshold}"

class BankingCoupon(Coupon):
    def __init__(self,bank,minspent,percent,cap):
        super().__init__()
        self._bankname=bank
        self._minspent=minspent
        self._percent=percent
        self._cap=cap
        self._strat=DiscountStrategyManager.getInstance().getStrategy(StrategyType.PERCENTAGEWITHCAP,percent,cap)

    def isApplicable(self,cart):
        return cart.getPaymentBank()==self._bankname and cart.getOriginalTotal()>=self._minspent
    
    def getDiscount(self,cart):
        return self._strat.calculate(cart.getCurrentTotal())
    
    def name(self):
        return f"[Bank offer ] flat {self._percent}% off up to {self._cap} on {self._bankname}"


class CouponManger:
    _instance=None
    @staticmethod
    def getInstance():
        if CouponManger._instance is None:
            CouponManger._instance=CouponManger()
        return CouponManger._instance
    def __init__(self):
        self._head=None

    def registerCoupon(self,coupon):
        if self._head is None:
            self._head=coupon
        else:
            curr=self._head
            while curr.getNext() is not None:
                curr=curr.getNext()
            curr.setNext(coupon)
        
    def getApplicable(self,cart):
        res=[]
        curr=self._head
        while curr:
            if curr.isApplicable(cart):
                res.append(curr.name())
            curr=curr.getNext()
        return res

    def applyAll(self,cart):
        if self._head is not None:
            self._head.applyDiscount(cart)
            return cart.getCurrentTotal()

if __name__=="__main__":

    couponManger=CouponManger.getInstance()
    couponManger.registerCoupon(SeasonalOffer(10,"clothing"))
    couponManger.registerCoupon(LoyalityDiscount(5))
    couponManger.registerCoupon(BulkPurchaseOff(1000,100))
    couponManger.registerCoupon(BankingCoupon("ABC",2000,15,500))

    p1=Product("Winter Jacket", "clothing", 1000)
    p2=Product("Smartphone", "electronics", 20000)
    p3=Product("Jeans", "clothing", 1000)
    p4=Product("Headphones", "electronics", 2000)

    cart=Cart()
    cart.addProductCart(p1,1)
    cart.addProductCart(p2,1)
    cart.addProductCart(p3,2)
    cart.addProductCart(p4,1)

    cart.setPaymentBank("ABC")

    print("Orignial total check-in total",cart.getOriginalTotal())

    
    print("Applicable Coupons")
    res=couponManger.getApplicable(cart)
    for name in res:
        print("-",name)
    
    finalTotal=couponManger.applyAll(cart)

    print(f"final cart total after applying all the available discounts {finalTotal} rs")
