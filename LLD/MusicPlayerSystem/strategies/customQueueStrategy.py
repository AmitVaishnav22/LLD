from models.playlist import Playlist
from models.song import Song
from strategies.playStrategy import PlayStrategy
from collections import deque

class CustomQueueStrategy(PlayStrategy):
    def __init__(self):
        self._currentplaylist=None
        self._currentIdx=-1
        self._nextQueue=deque()
        self._history=[]

    # internal helpers

    def _nextSequential(self):
        if self._currentplaylist.getSize()==0:
            raise RuntimeError("Playlist is empty.")
        self._currentIdx+=1
        return self._currentplaylist.getSongs()[self._currentIdx]

    def _previousSequential(self):
        if self._currentplaylist.getSize()==0:
            raise RuntimeError("Playlist is empty.")
        self._currentIdx-=1
        return self._currentplaylist.getSongs()[_currentIdx]

    # interface methods

    def setPlaylist(self,playlist:Playlist):
        self._currentplaylist=playlist
        self._currentIdx=-1
        self._nextQueue=deque()
        self._history=[]

    def hasNext(self):
        return self._currentplaylist is not None and (self._currentIdx+1)<self._currentplaylist.getSize()
    
    def next(self):
        if self._currentplaylist is None or self._currentplaylist.getSize()==0:
            raise RuntimeError("No playlist loaded or playlist is empty.")
        if self._nextQueue:
            song=self._nextQueue.popleft()
            self._history.append(song)
            songs=self._currentplaylist.getSongs()
            for i,s in enumerate(songs):
                if s==song:
                    self._currentIdx=i
                    break
            return song
        return self._nextSequential()

    def hasPrev(self):
        return (self._currentIdx-1)>0

    def prev(self):
        if self._currentplaylist is None or (self._currentplaylist.getSize()==0):
            raise RuntimeError("No playlist loaded or playlist is empty.")
        
        if self._history:
            song=self._history.pop()
            songs=self._currentplaylist.getSongs()
            for i,s in enumerate(songs):
                if s==song:
                    self._currentIdx=i
                    break
            return song
        return self._previousSequential()

    def addToNext(self,song:Song):
        if song is None:
            raise RuntimeError("Cannot enqueue null song.")
        self._nextQueue.append(song)
