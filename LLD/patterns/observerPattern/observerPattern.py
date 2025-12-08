from abc import ABC, abstractmethod

# observer interface
class ISubscriber(ABC):
    @abstractmethod
    def update(self,message:str):
        pass

# observable interface
class IChannel(ABC):
    @abstractmethod
    def subscribe(self,subscriber:ISubscriber):
        pass
    @abstractmethod
    def unsubscribe(self,subscriber:ISubscriber):
        pass
    @abstractmethod
    def notify_subscribers(self,message:str):
        pass

class Channel(IChannel):
    def __init__(self,name):
        self.subscribers = []
        self.name = name
        self.latestVideo = None
    def subscribe(self,subscriber:ISubscriber):
        self.subscribers.append(subscriber)
    def unsubscribe(self,subscriber:ISubscriber):
        self.subscribers.remove(subscriber)
    def notify_subscribers(self):
        for s in self.subscribers:
            s.update()
    def upload_video(self,title:str):
        self.latestVideo=title
        print(f"\n{self.name} uploaded latest video {self.latestVideo}")
        self.notify_subscribers()
    def get_video_data(self):
        return f"\n checkout new video : {self.latestVideo}"

class Subscriber(ISubscriber):
    def __init__(self,name,channel):
        self.name=name
        self.channel=channel
    def update(self):
        print(f"Hey {self.name} , {self.channel.get_video_data()} ")


if __name__=="__main__":
    channel=Channel("yt channel")
    sub1=Subscriber("person1",channel)
    sub2=Subscriber("person2",channel)
    channel.subscribe(sub1)
    channel.subscribe(sub2)
    channel.upload_video("this is new video trending")
    
