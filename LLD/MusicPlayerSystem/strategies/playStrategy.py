from abc import ABC,abstractmethod
from models.playlist import Playlist
from models.song import Song


class PlayStrategy(ABC):
    @abstractmethod
    def setPlaylist(self,playlist:Playlist):
        pass 
    
    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def hasNext(self):
        pass

    @abstractmethod
    def prev(self):
        pass

    @abstractmethod
    def hasPrev(self):
        pass 

    def addToNext(self,song:Song):  # only used in custom strategy
        pass