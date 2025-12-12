from abc import ABC,abstractmethod

class AudioOutputDevice(ABC):
    @abstractmethod
    def playAudio(self,song):
        pass