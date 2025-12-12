from models.playlist import Playlist
from models.song import Song
from strategies.playStrategy import PlayStrategy

class SequentialPlayStrategy(PlayStrategy):
    def __init__(self):
        self._currentplaylist=None
        self._currentIdx=-1
    
    def setPlaylist(self,playlist:Playlist):
        self._currentplaylist=playlist
        self._currentIdx=-1

    def hasNext(self):
        return (self._currentplaylist is not None) and (self._currentIdx+1 <self._currentplaylist.getSize())
    
    def next(self):
        if not self._currentplaylist or self._currentplaylist.getSize()==0:
            raise RuntimeError("No playlist loaded or playlist is empty.")
        self._currentIdx+=1
        return self._currentplaylist.getSongs()[self._currentIdx]

    def hasPrev(self):
        return (self._currentIdx-1)>0

    def prev(self):
        if self._currentplaylist is None or self._currentplaylist.getSize()==0:
            raise RuntimeError("No playlist loaded or playlist is empty.")
        self._currentIdx-=1
        return self._currentplaylist.getSongs()[self._currentIdx]