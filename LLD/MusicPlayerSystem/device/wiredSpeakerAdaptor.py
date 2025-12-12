from models.song import Song
from external.wiredSpeakerAPI import WiredSpeakerAPI 
from device.audioOutputDevice import AudioOutputDevice

class WiredSpeakerAdaptor(AudioOutputDevice):
    def __init__(self,api:WiredSpeakerAPI):
        self._wiredspeaker_api=api

    def playAudio(self,song:Song):
        payload=f"{song.getTitle()} by {song.getArtist()}"
        self._wiredspeaker_api.playSoundViaSpeaker(payload)