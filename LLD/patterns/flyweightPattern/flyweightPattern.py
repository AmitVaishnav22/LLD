class AsteriodFlyWeight:
    def __init__(self,l,w,wt,col,txt,mat):
        self.length=l
        self.width=w
        self.weight=wt
        self.color=col
        self.texture=txt
        self.material=mat

    def rendor(self,posX,posY,velX,velY):
        print(f"Rendoring Asteriod at posX:{posX}, posY:{posY} with velX:{velX}, velY:{velY} having properties length:{self.length}, width:{self.width}, weight:{self.weight}, color:{self.color}, texture:{self.texture}, material:{self.material}")

    def getMemorySize(self):
        return self.__sizeof__()


class AstroidFlyWeightFactory:
    def __init__(self):
        self.flyweights={}

    def getFlyWeight(self,l,w,wt,col,txt,mat):
        key=f"{l}_{w}_{wt}_{col}_{txt}_{mat}"
        if key not in self.flyweights:
            self.flyweights[key]=AsteriodFlyWeight(l,w,wt,col,txt,mat)
        return self.flyweights[key]

    def getTotalFlyWeights(self):
        return len(self.flyweights)

    def getTotalMemorySize(self):
        total=0
        for fw in self.flyweights.values():
            total+=fw.getMemorySize()
        return total

    def clearFlyWeights(self):
        self.flyweights={}


class AstroidContext:
    def __init__(self,flyweight,posX,posY,velX,velY):
        self.flyweight=flyweight
        self.posX=posX
        self.posY=posY
        self.velX=velX
        self.velY=velY

    def rendor(self):
        self.flyweight.rendor(self.posX,self.posY,self.velX,self.velY)

    def getTotalMemorySize(self):
        return self.__sizeof__() + self.flyweight.getMemorySize()

class SpaceGame:
    def __init__(self):
        self.asteroids=[]

    def spawnAsteroid(self,cnt):
        colors=["Red","Green","Blue"]
        textures=["Smooth","Rough","Cracked"]
        materials=["Iron","Ice","Rock"]
        sizes=[10,20,30]

        for i in range(cnt):
            typ=i%3

            flyweight=AstroidFlyWeightFactory().getFlyWeight(
                sizes[typ],
                sizes[typ],
                sizes[typ]*10,
                colors[typ],
                textures[typ],
                materials[typ]
            )
            asteroid=AstroidContext(
                flyweight=flyweight,
                posX=i*10,
                posY=i*15,
                velX=i*2,
                velY=i*3
            )
            self.asteroids.append(asteroid)

    def renderAsteroids(self):
        for i in range(min(10,len(self.asteroids))):
            self.asteroids[i].rendor()

    def calculateMemoryUsage(self):
        total=0
        for asteroid in self.asteroids:
            total+=asteroid.getTotalMemorySize()
        return total

    def getAsteroidCount(self):
        return len(self.asteroids)

if __name__=="__main__":
    ASTEROID_COUNT=100000

    print("Starting Space Game with Flyweight Pattern")

    game=SpaceGame()
    game.spawnAsteroid(ASTEROID_COUNT)


    game.renderAsteroids()
    print(f"Total Asteroids: {game.getAsteroidCount()}")
    print(f"Total Memory Usage with Flyweight Pattern: {game.calculateMemoryUsage()} bytes")
    print(f"Total Memory in GB with Flyweight Pattern: {game.calculateMemoryUsage()/(1024*1024)} GB")
