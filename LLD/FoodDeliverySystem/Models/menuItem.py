class MenuItem:
    
    def __init__(self,code,name,price):
        self.code=code
        self.name=name
        self.price=price
    
    def get_code(self):
        return self.code
    
    def set_code(self,c):
        self.code=c
    
    def get_name(self):
        return self.name
    
    def set_name(self,n):
        self.name=n
    
    def get_price(self):
        return self.price
    
    def set_price(self,p):
        self.price=p
