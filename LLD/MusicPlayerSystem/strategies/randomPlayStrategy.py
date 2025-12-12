import random 
from models.playlist import Playlist
from models.song import Song
from strategies.playStrategy import PlayStrategy

class RandomPlayStrategy(PlayStrategy):
    def __init__(self):
        self._currentplaylist=None
        self._remaining_songs=[]
        self._history=[]
        self._random=random.Random()
    
    def setPlaylist(self,playlist:Playlist):
        self._currentplaylist=playlist
        if playlist is None or playlist.getSize()==0:
            self._remaining_songs=[]
            self._history=[]
            return []
        self._remaining_songs=list(playlist.getSongs())
        self._history=[]

    def hasNext(self):
        return self._currentplaylist is not None and len(self._remaining_songs)>0

    def next(self):
        if self._currentplaylist is None or self._currentplaylist.getSize()==0:
            raise RuntimeError("No playlist loaded or playlist is empty.")
        if not self._remaining_songs:
            raise RuntimeError("No songs left to play.")
        idx=self._random.randint(0, len(self._remaining_songs) - 1)
        selected_song=self._remaining_songs[idx]
        last_index=len(self._remaining_songs) - 1
        self._remaining_songs[idx]=self._remaining_songs[last_index]
        self._remaining_songs.pop()
        self._history.append(selected_song)
        return selected_song

    def hasPrev(self):
        return len(self._history)>0

    def prev(self):
        if not self._history:
            raise RuntimeError("No previous song available.")
        return self._history.pop()

