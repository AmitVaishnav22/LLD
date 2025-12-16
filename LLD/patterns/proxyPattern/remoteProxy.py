from abc import ABC,abstractmethod

#Remote Proxy provides a local representative for an object that exists in a different address space (remote server).

class DataService(ABC):
    @abstractmethod
    def fetchData(self):
        pass

class RealDataService(DataService):
    def __init__(self):
        print("[RDS] initialising remote service setup ")
    def fetchData(self):
        print("[RDS] Fetching data from the connected Remote Connection \n Data Fetched Successfully")

class ProxyDataService(DataService):
    def __init__(self):
        self._realDataService=RealDataService()
    def fetchData(self):
        self._realDataService.fetchData()

if __name__=="__main__":
    proxyServer=ProxyDataService()
    proxyServer.fetchData()