from abc import ABC,abstractmethod

#component interface
class Character(ABC):
    @abstractmethod
    def get_abilities(self):
        pass

#concreate class
class Mario(Character):
    def get_abilities(self):
        return "Mario "

class characterDecorator(Character):
    def __init__(self,charactor):
        self.charactor=charactor
    def get_abilities(self):
        return self.charactor.get_abilities()

class HeightUp(characterDecorator):
    def get_abilities(self):
        #print("super",super().get_abilities(),super())
        return super().get_abilities()+"with HeightUp "

class GunPowerUp(characterDecorator):
    def get_abilities(self):
        return super().get_abilities()+"with GunPowerUp "

class StarPowerUp(characterDecorator):
    def get_abilities(self):
        return super().get_abilities()+"with start power "
    
if __name__=="__main__":
    mario=Mario()
    print("mario",mario)
    print("basic character ",mario.get_abilities())
    mario=GunPowerUp(mario)
    print("gun power ", mario.get_abilities())
    mario=HeightUp(mario)
    print("gun power + heightup ",mario.get_abilities())
    mario=StarPowerUp(mario)
    print("gun power + heightup + starpower ",mario.get_abilities())

