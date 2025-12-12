class AudioEngine:
    def __init__(self):
        self._current_song=None
        self._song_is_paused=None

    def getCurrentSongTitle(self):
        if not self._current_song:
            return ""
        return self._current_song.getTitle()

    def is_paused(self):
        return self._song_is_paused
        
    def play(self,audiodevice,song):
        if song is None:
            raise RuntimeError("Cannot play a null song.")
        if self._song_is_paused and song==self._current_song:
            self._song_is_paused=False
            print(f"Resuming song: {song.getTitle()}")
            audiodevice.playAudio(song)
            return
        self._current_song=song
        self._song_is_paused=False
        print(f"Playing song: {song.getTitle()}")
        audiodevice.playAudio(song)

    def pause(self):
        if self._current_song is None:
            raise RuntimeError("No song is currently playing to pause.")

        if self._song_is_paused:
            raise RuntimeError("Song is already paused.")
        
        self._song_is_paused = True
        print(f"Pausing song: {self._current_song.getTitle()}")
        
        
