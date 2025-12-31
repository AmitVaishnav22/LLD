from abc import ABC,abstractmethod
from enum import Enum
import math
import time


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
        return NotificationService._instance
    
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
        for _,inst in self._observers.items():
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
        return [self._ux,self._uy]
    def setUserDistance(self,x,y):
        self._ux=x
        self._uy=y
    def getLocation(self):
        return [self._ux,self._uy]

    def distanceInKM(self,loc2):
        R = 6371  

        lat1, lon1 = math.radians(self._ux), math.radians(self._uy)
        x1,y1 = loc2.getUserDistance()
        lat2, lon2 = math.radians(x1),math.radians(y1)

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
    def getInterestSize(self):
        return len(self._interests)

    def getGender(self):
        return self._gender

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
        print(f"Location {self._location.getUserDistance()}")

class SwipeAction(Enum):
    LEFT=1
    RIGHT=2

class User:
    def __init__(self,uId):
        self._userID=uId
        self._profile=UserProfile()
        self._preference=Preference()
        self._swipeHistory={}
        self._notificatioObserver=UserNotificationObserver(uId)
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
        self._strat=BasicLocationStrategy()

    def setLocationStrat(self,strat):
        self._strat=strat

    def findNearbyUsers(self,loc,maxiD,allUsers):
        return self._strat.findNearbyUsers(loc,maxiD,allUsers)  

# messaging system

class Message:
    def __init__(self,senderId,msg):
        self._senderId=senderId
        self._msg=msg
        self._timestamp=int(time.time() * 1000)
    
    def getSenderId(self):
        return self._senderId
    
    def getContent(self):
        return self._msg

    def getTimeStamp(self):
        return self._timestamp

class ChatRoom:
    def __init__(self,roomId,user1Id,user2Id):
        self._id=roomId
        self._users=[]
        self._users.append(user1Id)
        self._users.append(user2Id)
        self._messages=[]

    def getRoomId(self):
        return self._id

    def addMessage(self,senderId,content):
        msg=Message(senderId,content)
        self._messages.append(msg)

    def hasParticipant(self,userId):
        return userId in self._users

    def getMessages(self):
        return self._messages

    def getParticipants(self):
        return self._users

    def displayChat(self):
        print(f"[Chat Room] {self._id} : ")
        for msg in self._messages:
            print(f"[message] {msg.getTimeStamp()} - {msg.getSenderId()} - {msg.getContent()}")
        print("\n ======= \n")



# matching part

class MatcherType(Enum):
    BASIC=1
    INTEREST_BASED=2
    LOCATION_BASED=3

class Matcher(ABC):
    @abstractmethod
    def calculateScore(self,user1,user2):
        pass

class BasicMatcher(Matcher):
    def calculateScore(self,user1,user2):
        isUser1LikedUser2=user1.getPreference().isInterestedInGender(user2.getProfile().getGender())
        isUser2LikedUser2=user2.getPreference().isInterestedInGender(user1.getProfile().getGender())

        if not isUser1LikedUser2 or not isUser2LikedUser2:
            return 0

        isUser1AgeUser2=user1.getPreference().isAgeInRange(user2.getProfile().getAge())
        isUser2AgeUser1=user2.getPreference().isAgeInRange(user1.getProfile().getAge())

        if not isUser1AgeUser2 or not isUser2AgeUser1:
            return 0

        dist=user1.getProfile().getLocation().distanceInKM(user2.getProfile().getLocation())
        isUser1DistUser2=user1.getPreference().isDistanceAcceptable(dist)
        isUser2DistUser1=user2.getPreference().isDistanceAcceptable(dist)

        if not isUser1DistUser2 or not isUser2DistUser1:
            return 0

        return 0.5

class InterestBasedMatcher(Matcher):
    def calculateScore(self,user1,user2):
        basicBestScore=BasicMatcher().calculateScore(user1,user2)
        if basicBestScore==0:
            return 0
        user1Interest=set()
        for inte in user1.getProfile().getInterests():
            user1Interest.add(inte.getName())
        sharePoint=0
        for inte in user2.getProfile().getInterests():
            if inte.getName() in user1Interest:
                sharePoint+=1
        maxInterests=max(user1.getProfile().getInterestSize(),user2.getProfile().getInterestSize())
        interestScore=0.5*(sharePoint//maxInterests) if maxInterests>0 else 0

        return basicBestScore+interestScore

class LocationBasedMatcher(Matcher):
    def calculateScore(self,user1,user2):
        interestScore=InterestBasedMatcher().calculateScore(user1,user2)
        if interestScore==0:
            return 0
        dist=user1.getProfile().getLocation().distanceInKM(user2.getProfile().getLocation())
        maxiD=min(user1.getPreference().getMaxDist(),user2.getPreference().getMaxDist())
        proximityScore=0.2*(1-(dist//maxiD)) if maxiD>0 else 0
        return interestScore+proximityScore
    
class MatcherFactory:
    def createMatcher(self,type):
        if type==MatcherType.BASIC:
            return BasicMatcher()
        elif type==MatcherType.INTEREST_BASED:
            return InterestBasedMatcher()
        elif type==MatcherType.LOCATION_BASED:
            return LocationBasedMatcher()
        else:
            return BasicMatcher()

class DatingAPP:
    _instance=None 
    @staticmethod
    def getInstance():
        if DatingAPP._instance is None:
            DatingAPP._instance=DatingAPP()
        return DatingAPP._instance

    def __init__(self):
        self._users=[]
        self._chatRooms=[]
        self._userIdMpp={}
        self._matcher=MatcherFactory().createMatcher(MatcherType.LOCATION_BASED)

    def setMatcher(self,type):
        self._matcher=MatcherFactory().createMatcher(type)

    def createUser(self,userId):
        user=User(userId)
        self._userIdMpp[userId]=user
        self._users.append(user)
        return user

    def getUserById(self,userId):
        return self._userIdMpp[userId] if userId in self._userIdMpp else None
    
    def findNearbyUsers(self,userId,maxiD):
        user=self.getUserById(userId)
        if not user:
            return []

        nearByUsers=set(LocationService.getInstance().findNearbyUsers(user.getProfile().getLocation(),maxiD,self._users))

        nearByUsers.remove(user)
        filters=[]
        for otherUser in nearByUsers:
            if not (user.hasInteractedWith(otherUser.getId())):
                score=self._matcher.calculateScore(user,otherUser)
                if score>0:
                    filters.append(otherUser)
        return filters

    def swipe(self,userId,targetUID,action):
        user1=self.getUserById(userId)
        user2=self.getUserById(targetUID)
        if not user1 or not user2:
            print("[Swipe] user not found.")
            return 
        user1.swipe(targetUID,action)

        if action==SwipeAction.RIGHT and user2.hasLiked(userId):
            chatRoomId=userId+"-"+targetUID
            chatRoom=ChatRoom(chatRoomId,userId,targetUID)
            self._chatRooms.append(chatRoom)
            NotificationService.getInstance().notifyUser(userId,f"You have a new match with {user2.getProfile().getName()}!")
            NotificationService.getInstance().notifyUser(targetUID,f"You have a new match with {user1.getProfile().getName()}!")

            return True
        return False

    def getChat(self,user1Id,user2Id):
        for chatRoom in self._chatRooms:
            if chatRoom.hasParticipant(user1Id) and chatRoom.hasParticipant(user2Id):
                return chatRoom
        return None

    def sendMessage(self,senderId,receiverId,content):
        chatRoom=self.getChat(senderId,receiverId)
        if not chatRoom:
            print("[Message] No chat room found between users.")
            return
        chatRoom.addMessage(senderId,content)
        NotificationService.getInstance().notifyUser(receiverId,f"New message from {senderId} : {content}")

    def displayUser(self,userId):
        user=self.getUserById(userId)
        if not user:
            print("User not found.")
            return 
        user.displayProfile()

    def displayChat(self,user1Id,user2Id):
        chatRoom=self.getChat(user1Id,user2Id)
        if not chatRoom:
            print("No chatrooms found.")
            return 
        chatRoom.displayChat()

if __name__=="__main__":
    app=DatingAPP.getInstance()
    user1=app.createUser("user1")
    user2=app.createUser("user2")
    
    profile1=user1.getProfile()
    profile1.setName("Rohan")
    profile1.setAge(28)
    profile1.setGender(Gender.MALE)
    profile1.setBio("i am an engineer")
    profile1.addPhoto("profile/rohan.png")
    profile1.addInterest("Coding","Programming")
    profile1.addInterest("Travel","Lifestyle")
    profile1.addInterest("Music","Entertainment")

    pref1=user1.getPreference()
    pref1.addGenderPreference(Gender.FEMALE)
    pref1.setAgeRange(25,30)
    pref1.setDistance(10)
    pref1.addInterest("Coding")
    pref1.addInterest("Travel")

    
    loc1=Location(1.01,1.02)
    profile1.setLocation(loc1)


    profile2=user2.getProfile()
    profile2.setName("Neha")
    profile2.setAge(27)
    profile2.setGender(Gender.FEMALE)
    profile2.setBio("artist and traveller")
    profile2.addPhoto("profile/neha.png")
    profile2.addInterest("Painting","Art")
    profile2.addInterest("Travel","Lifestyle")
    profile2.addInterest("Music","Entertainment")

    pref2=user2.getPreference()
    pref2.addGenderPreference(Gender.MALE)
    pref2.setAgeRange(27,30)
    pref2.setDistance(10)
    pref2.addInterest("Music")
    pref2.addInterest("Travel")

    
    loc2=Location(1.03,1.04)
    profile2.setLocation(loc2)

    print("----user profiles----\n")
    app.displayUser("user1")
    app.displayUser("user2")

    print("----finding nearby users for user1----\n")
    nearByUsers=app.findNearbyUsers("user1",5)
    print(f"Found {len(nearByUsers)} nearByUsers")
    for user in nearByUsers:
        print(f"-{user.getProfile().getName()}+{user.getId()}")

    print("--SWAP ACTION--")
    print("user1 swips right on user2")
    app.swipe("user1","user2",SwipeAction.RIGHT)

    print("user2 swips right on user1")
    app.swipe("user2","user1",SwipeAction.RIGHT)

    print("--chatroom--")
    app.sendMessage("user1","user2","Hi neha")
    app.sendMessage("user2","user1","Hi rohan")

    app.displayChat("user1","user2")