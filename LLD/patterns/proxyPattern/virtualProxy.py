from abc import ABC,abstractmethod


# proxy pattern is acts as a instance of the server which the client requests
# Virtual Proxy delays the creation and loading of a resource-heavy object until it is actually needed.

class Image(ABC):
    @abstractmethod
    def display(self):
        pass

class RealImage(Image):
    def __init__(self,fileName):
        self._fileName=fileName
        print("[realImage] loading Image file from the disk ",self._fileName)
    # def realImage(self):
    #     self._fileName=file
    #     print("[realImage] loading File from the disk ",self._fileName)
    def display(self):
        print("[realImage] displaying",self._fileName)

class ImageProxy(Image):
    def __init__(self,fileName):
        self._realImage=None 
        self._fileName=fileName
    
    def display(self):
        if self._realImage==None:
            self._realImage=RealImage(self._fileName)
        self._realImage.display()

if __name__=="__main__":
    img=ImageProxy("img.png")
    img.display()

