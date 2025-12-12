from models.song import Song
from managers.playlistManager import PlaylistManager
from musicPlayerFacade import MusicPlayerFacade

class MusicPlayerApplication:
    _instance=None

    def __init__(self):
        self._songLibrary=[]
    
    @staticmethod
    def getInstance():
        if MusicPlayerApplication._instance is None:
            MusicPlayerApplication._instance=MusicPlayerApplication()
        return MusicPlayerApplication._instance

    def createSongInLibrary(self,name,artist,path):
        newSong=Song(name,artist,path)
        self._songLibrary.append(newSong)

    def findSongByTittle(self,name):
        for s in self._songLibrary:
            if s.getTitle()==name:
                return s
        return None

    def createPlayList(self,playlistname):
        PlaylistManager.getInstance().createPlayList(playlistname)

    def addSongToPlaylist(self,playlistname,name):
        song=self.findSongByTittle(name)
        if song is None:
            raise RuntimeError(f'Song "{songTitle}" not found in library.')
        PlaylistManager.getInstance().addSongToPlaylist(playlistname,song)

    def connectAudioDevice(self,devicetype):
        MusicPlayerFacade.getInstance().connectDevice(devicetype)

    def selectPlayStrategy(self,strategytype):
        MusicPlayerFacade.getInstance().setPlaylistStrategy(strategytype)

    def loadPlaylist(self,playlistname):
        MusicPlayerFacade.getInstance().loadPlaylist(playlistname)
    
    def playSingleSong(self,name):
        song=self.findSongByTittle(name)
        if song is None:
            raise RuntimeError(f'Song "{songTitle}" not found.')
        MusicPlayerFacade.getInstance().playSong(song)

    def pauseCurrentSong(self,name):
        song=self.findSongByTittle(name)
        if song is None:
            raise RuntimeError(f'Song "{songTitle}" not found.')
        MusicPlayerFacade.getInstance().pauseSong(song)
    
    def playAllTracksInPlaylist(self):
        MusicPlayerFacade.getInstance().playAllTracks()

    def playPreviousTrackInPlaylist(self):
        MusicPlayerFacade.getInstance().playPreviousTrack()

    def queueSongNext(self,name):
        song=self.findSongByTittle(name)
        if song is None:
            raise RuntimeError(f'Song "{name}" not found.')
        MusicPlayerFacade.getInstance().enqueueNext(song)

