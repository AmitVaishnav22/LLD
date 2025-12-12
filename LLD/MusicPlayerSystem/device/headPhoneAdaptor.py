from models.song import Song
from external.headphonesAPI import HeadphonesAPI 
from device.audioOutputDevice import AudioOutputDevice

class HeadphonesAdaptor(AudioOutputDevice):
    def __init__(self,api:HeadphonesAPI):
        self._headphone_api=api

    def playAudio(self,song:Song):
        payload=f"{song.getTitle()} by {song.getArtist()}"
        self._headphone_api.playSoundViaHeadphone(payload)