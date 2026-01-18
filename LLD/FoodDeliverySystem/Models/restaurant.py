class Restaurant:
    # static variable for incrementing ids
    idx=0
    def __init__(self,name,loc):
        self._name=name
        self._loc=loc
        self.resID=Restaurant.idx
        Restaurant.idx+=1
        self.menu=[]

    def get_name(self):
        return self._name

    def set_name(self,n):
        self._name=n

    def get_Location(self):
        return self._loc

    def set_Location(self,loc):
        self._loc=loc

    def add_menu_item(self,item):
        self.menu.append(item)

    def get_menu(self):
        return self.menu