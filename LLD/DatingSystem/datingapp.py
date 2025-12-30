from abc import ABC,abstractmethod
from enum import Enum
import math


# notification pattern

class NotificationObserver(ABC):
    @abstractmethod
    def update(self,message):
        pass

class UserNotificationObserver(NotificationObserver):
    def __init__(self,userId):
        self._uId=userId
    def update(self,message):
        print(f"[Notification] notification for {self._uId} - {message}")
    
class NotificationService:
    _instance=None 
    @staticmethod
    def getInstance():
        if NotificationService._instance is None:
            NotificationService._instance=NotificationService()
        return NotificationService._instance()
    
    def __init__(self):
        self._observers={}

    def registerObserver(self,userId,observer):
        if userId not in self._observers:
            self._observers[userId]=observer
    
    def removeObserver(self,userId):
        if userId in self._observers:
            del self._observers[userId]

    def notifyUser(self,userId,message):
        observerInst=self._observers[userId]
        if not observerInst:
            print("[Notification] No user registerd to be notifed.")
        observerInst.update(message)

    def notifyAll(self,message):
        for inst in self._observers:
            inst.update(message)


class Gender(Enum):
    MALE=1
    FEMALE=2
    NONBINARY=3
    OTHER=4

class Location:
    def __init__(self,ux,uy):
        self._ux=ux
        self._uy=uy
    def getUserDistance(self):
        return (self._ux,self._uy)
    def setUserDistance(self,x,y):
        self._ux=x
        self._uy=y

    def distanceInKM(self,loc2):
        R = 6371  

        lat1, lon1 = math.radians(self._ux), math.radians(self._uy)
        lat2, lon2 = math.radians(loc2.getUserDistance())

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (math.sin(dlat / 2) ** 2 +
             math.cos(lat1) * math.cos(lat2) *
             math.sin(dlon / 2) ** 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

class Interest:
    def __init__(self,name,category):
        self._name=name
        self._category=category

    def getName(self):
        return self._name

    def getCategory(self):
        return self._category

class Preference:
    def __init__(self):
        self._InterestedIn=set()
        self._interests=set()
        self._minAge=18
        self._maxAge=100
        self._maxDist=100.0

    def addGenderPreference(self,gender):
        self._InterestedIn.add(gender)
    
    def removeGenderPreference(self,gender):
        self._InterestedIn.remove(gender)

    def setAgeRange(self,mini,maxi):
        self._minAge=mini
        self._maxAge=maxi
    
    def setDistance(self,dist):
        self._maxDist=dist

    def addInterest(self,interest):
        self._interests.add(interest)

    def removeInterest(self,interest):
        self._interests.remove(interest)

    def isInterestedInGender(self,gender):
        return gender in self._InterestedIn

    def isAgeInRange(self,age):
        return self._minAge<=age<=self._maxAge

    def isDistanceAcceptable(self,dist):
        return dist<=self._maxDist

    def getInterest(self):
        return self._interests

    def getInterestedIn(self):
        return self._InterestedIn

    def getMinAge(self):
        return self._minAge

    def getMaxAge(self):
        return self._maxAge

    def getMaxDist(self):
        return self._maxDist

class UserProfile:
    def __init__(self):
        self._name=""
        self._age=0
        self._gender=Gender.OTHER
        self._photos=set()
        self._interests=set()
        self._location=None
        self._bio=""

    def setName(self,name):
        self._name=name

    def setGender(self,gender):
        self._gender=gender

    def setAge(self,age):
        self._age=age

    def setBio(self,bio):
        self._bio=bio

    def addPhoto(self,photoURL):
        self._photos.add(photoURL)

    def removePhoto(self,photoURL):
        self._photos.remove(photoURL)

    def addInterest(self,name,category):
        interest=Interest(name,category)
        self._interests.add(interest)

    def removeInterest(self,name):
        toRemove = set()
        for i in self._interests:
            if i.getName() == name:
                toRemove.add(i)
        self._interests -= toRemove
    
    def setLocation(self,loc):
        self._location=loc

    def getName(self):
        return self._name

    def getAge(self):
        return self._age

    def getPhotos(self):
        return self._photos

    def getBio(self):
        return self._bio

    def getLocation(self):
        return self._location

    def getInterests(self):
        return self._interests

    def display(self):
        print("-----Profile-----\n")
        print("\nName :",self._name)
        print("\nAge :",self._age)
        print("Gender :")
        if self._gender==Gender.MALE:
            print("Male\n")
        elif self._gender==Gender.FEMALE:
            print("Female\n")
        elif self._gender==Gender.NONBINARY:
            print("NonBinary\n")
        else:
            print("Others\n")
        print("Bio :",self._bio)
        print("Photos")
        for pic in self._photos:
            print(" ",pic)
        print("\n")
        print("Interests")
        for intt in self._interests:
            print(f"{intt.getName()}")
        print("\n")
        print(f"Location {self._location.getLocation()}")

class SwipeAction(Enum):
    LEFT=1
    RIGHT=1

class User:
    def __init__(self,uId):
        self._userID=uId
        self._profile=UserProfile()
        self._preference=Preference()
        self._swipeHistory={}
        self._notificatioObserver=UserNotificationObserver()
        NotificationService.getInstance().registerObserver(uId,self._notificatioObserver)
    
    def getId(self):
        return self._userID

    def getProfile(self):
        return self._profile

    def getPreference(self):
        return self._preference

    def swipe(self,uid2,action):
        self._swipeHistory[uid2]=action

    def hasLiked(self,uid2):
        if uid2 in self._swipeHistory and self._swipeHistory[uid2]==SwipeAction.RIGHT:
            return True
        return False

    def hasDisliked(self,uid2):
        if uid2 in self._swipeHistory and self._swipeHistory[uid2]==SwipeAction.LEFT:
            return True
        return False

    def hasInteractedWith(self,uid2):
        return uid2 in self._swipeHistory

    def displayProfile(self):
        self._profile.display()

class LocationStrategy(ABC):
    @abstractmethod
    def findNearbyUsers(self,loc,maxiD,allUsers):
        pass

class BasicLocationStrategy(LocationStrategy):
    def findNearbyUsers(self,loc,maxiD,allUsers):
        nearByUsers=set()
        for user in allUsers:
            dist=loc.distanceInKM(user.getProfile().getLocation())
            if dist<=maxiD:
                nearByUsers.add(user)
        return nearByUsers

class LocationService:
    _instance=None
    @staticmethod
    def getInstance():
        if LocationService._instance is None:
            LocationService._instance=LocationService()
        return LocationService._instance

    def __init__(self):
        self._strat=None

    def setLocationStrat(self,strat):
        self._strat=strat

    def findNearbyUsers(self,loc,maxiD,allUsers):
        return self._start.findNearbyUsers(loc,maxiD,allUsers)  