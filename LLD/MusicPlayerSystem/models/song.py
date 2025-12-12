
class Song:
    def __init__(self,name,artist,path):
        self._name=name
        self._artist=artist
        self._path=path
    
    def getTitle(self):
        return self._name
    
    def getArtist(self):
        return self._artist

    def getPath(self):
        return self._path
        