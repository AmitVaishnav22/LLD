from abc import ABC,abstractmethod

# consider it as a middleware where someone does some SPECIFIC work on your data and returns you 
# with the expected output

class Reports(ABC):
    @abstractmethod
    def getJsonData(self,string):
        pass

class XmlDataProvider:
    def getXmlFormat(self,data):
        return f"XML Extrater Logic Encoded of {data} "

class XmlDataProviderAdaptor(Reports):
    def __init__(self,xmlDataProvider:XmlDataProvider):
        self._xmlDataProvider=xmlDataProvider
    
    def getJsonData(self,string):
        xml=self._xmlDataProvider.getXmlFormat(string)
        return xml+"converted to json ."
    
class Client:
    def __init__(self,data,report:Reports):
        self._data=data
        self._report=report
    def getReport(self):
        print("Proceed JSON DATA ",self._report.getJsonData(self._data))
    
if __name__=="__main__":
    xml=XmlDataProvider()
    xmlAdaptor=XmlDataProviderAdaptor(xml)
    cli=Client("HI",xmlAdaptor)
    cli.getReport()
