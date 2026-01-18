class RestaurantManager:
    # singleton pattern once instance globally accross the system
    _instance=None 
    def __init__(self):
        if RestaurantManager._instance is not None:
            return 
        self.restaurants=[]
    
    @staticmethod
    def get_instance():
        if RestaurantManager._instance is None:
            RestaurantManager._instance=RestaurantManager()
        return RestaurantManager._instance

    def add_restaurant(self,res):
        self.restaurants.append(res)

    def search_by_loc(self,location):
        loc=location.lower()
        ans=[]
        for res in self.restaurants:
            #print(res.get_Location().lower(),loc)
            if res.get_Location().lower()==loc:
                ans.append(res)
        return ans 
