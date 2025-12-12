from models.playlist import Playlist
from models.song import Song

class PlaylistManager:
    _instance=None
    def __init__(self):
        self._playlists={}
    
    @staticmethod
    def getInstance():
        if PlaylistManager._instance is None:
            PlaylistManager._instance=PlaylistManager()
        return PlaylistManager._instance

    def createPlayList(self,name:str):
        if name in self._playlists:
            raise RuntimeError(f'Playlist "{name}" already exists.')
        self._playlists[name]=Playlist(name)

    def addSongToPlaylist(self,playlistname,song:Song):
        if playlistname not in self._playlists:
            raise RuntimeError(f'Playlist "{playlistname}" not found.')
        self._playlists[playlistname].addSongToPlaylist(song)

    def getPlaylist(self,playlistname:str):
        if playlistname not in self._playlists:
            raise RuntimeError(f'Playlist "{name}" not found.')
        return self._playlists[playlistname]
