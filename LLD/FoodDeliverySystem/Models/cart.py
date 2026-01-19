class Cart:
    def __init__(self):
        self._restaurant=None
        self._items=[]

    def add_item(self,item):
        if self._restaurant is None:
            print("Cart does not have an restaurant , set an restuarant")
            return 
        self._items.append(item)

    def get_total_cost(self):
        total=0
        for item in self._items:
            total+=item.get_price()
        return total

    def is_empty(self):
        return len(self._items)==0 or self._restaurant==None

    def clear(self):
        self._items=[]
        self._restaurant=None
    
    def set_restaurant(self,res):
        self._restaurant=res

    def get_restaurant(self):
        return self._restaurant

    def get_items(self):
        return self._items
        