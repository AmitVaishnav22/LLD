from core.audioEngine import AudioEngine
from models.playlist import Playlist
from models.song import Song
from strategies.playStrategy import PlayStrategy
from enums.playStrategyType import PlayStrategyType
from enums.deviceType import DeviceType
from managers.deviceManager import DeviceManager
from managers.playlistManager import PlaylistManager
from managers.strategyManager import StrategyManager


class MusicPlayerFacade:
    _instance=None

    def __init__(self):
        self._loadedPlaylist=None
        self._playStrategy=None
        self._audioEngine=AudioEngine()


    @staticmethod
    def getInstance():
        if MusicPlayerFacade._instance is None:
            MusicPlayerFacade._instance=MusicPlayerFacade()
        return MusicPlayerFacade._instance
    
    def connectDevice(self,devicetype:DeviceType):
        DeviceManager.getInstance().connect(devicetype)

    def setPlaylistStrategy(self,strategytype:PlayStrategyType):
        self._playStrategy=StrategyManager.getInstance().getStrategy(strategytype)

    def loadPlaylist(self,name):
        self._loadedPlaylist=PlaylistManager.getInstance().getPlaylist(name)

        if self._loadedPlaylist is None:
            raise RuntimeError("Play strategy not set before loading.")
        
        self._playStrategy.setPlaylist(self._loadedPlaylist)

    def playSong(self,song):
        if not DeviceManager.getInstance().hasOutPutDevice():
            raise RuntimeError("No audio device connected.")
        device=DeviceManager.getInstance().getOutputDevice()
        self._audioEngine.play(device,song)

    def pauseSong(self,song):
        if self._audioEngine.getCurrentSongTitle()!=song.getTitle():
            raise RuntimeError(
                f"Cannot pause \"{song.getTitle()}\"; not currently playing."
            )
        self._audioEngine.pause()

    def playAllTracks(self):
        if self._loadedPlaylist is None:
            raise RuntimeError("No playlist loaded.")

        while self._playStrategy.hasNext():
            nextSong=self._playStrategy.next()
            device=DeviceManager.getInstance().getOutputDevice()
            self._audioEngine.play(device,nextSong)
        
        print(f"Completed playlist: {self._loadedPlaylist.getPlayListName()}")

    def playNextTrack(self):
        if self._loadedPlaylist is None:
            raise RuntimeError("No playlist loaded.")
        
        if self._playStrategy.hasNext():
            nextSong=self._playStrategy.next()
            device=DeviceManager.getInstance().getOutputDevice()
            self._audioEngine.play(device,nextSong)
        else:
            print(f"Completed playlist: {self._loadedPlaylist.getPlayListName()}")

    def playPreviousTrack(self):
        if self._loadedPlaylist is None:
            raise RuntimeError("No playlist loaded.")
        
        if self._playStrategy.hasPrev():
            prevSong=self._playStrategy.prev()
            device=DeviceManager.getInstance().getOutputDevice()
            self._audioEngine.play(device,prevSong)
        else:
            print(f"Completed playlist: {self._loadedPlaylist.getPlayListName()}")
        
    def enqueueNext(self,song):
        self._playStrategy.addToNext(song)


