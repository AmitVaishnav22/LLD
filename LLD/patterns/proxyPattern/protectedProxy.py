from abc import ABC,abstractmethod

#Protected Proxy controls access to the real object by checking permissions before forwarding the request.

class DocumentReader(ABC):
    @abstractmethod
    def unlockPDF(self,filePath,password):
        pass

class RealDocumentReader(DocumentReader):
    def unlockPDF(self,filePath,password):
        print("[RDR] unlocking file at ",filePath)
        print("[RDR] pdf unlocket with password")
        print("[RDR] pdf displayed")

class User:
    def __init__(self,userName,isPremium):
        self._userName=userName
        self._isPremium=isPremium
    def isPremium(self):
        return self._isPremium

class ProxyDocumentReader(DocumentReader):
    def __init__(self,user):
        self._realDocumentReader=RealDocumentReader()
        self._currentUser=user
    def unlockPDF(self,filePath,password):
        if self._currentUser.isPremium()==False:
            print("OOPS this feature is not available , upgrade to premium")
        else:
            self._realDocumentReader.unlockPDF(filePath,password)

if __name__=="__main__":
    user1=User("guest1",True)
    user2=User("guest2",False)
    pdf1=ProxyDocumentReader(user1)
    pdf1.unlockPDF("./open.pdf","123")
    pdf2=ProxyDocumentReader(user2)
    pdf2.unlockPDF("./open.pdf","123")