from Models.cart import Cart
class User:
    def __init__(self,name,userId,address):
        self._name=name
        self._userId=userId
        self._address=address
        self._cart=Cart()

    def get_name(self):
        return self._name
    
    def set_name(self,n):
        self._name=n

    def get_address(self):
        return self._address

    def set_address(self,add):
        self._address=add

    def get_cart(self):
        return self._cart