from models.song import Song
from external.bluetoothSpeakerAPI import BluetoothSpeakerAPI 
from device.audioOutputDevice import AudioOutputDevice

class BluetoothSpeakerAdaptor(AudioOutputDevice):
    def __init__(self,api:BluetoothSpeakerAPI):
        self._bluetooth_api=api
        
    def playAudio(self,song:Song):
        payload=f"{song.getTitle()} by {song.getArtist()}"
        self._bluetooth_api.playSoundViaBluetooth(payload)