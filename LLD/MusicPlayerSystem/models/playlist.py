from models.song import Song

class Playlist(Song):
    def __init__(self,name:str):
        self._name=name
        self._songList=[]

    def getPlayListName(self):
        return self._name

    def getSongs(self):
        return self._songList

    def getSize(self):
        return len(self._songList)

    def addSongToPlaylist(self,song:Song):
        if not song:
            raise ValueError("Cannot add null song to playlist.")
        self._songList.append(song)
