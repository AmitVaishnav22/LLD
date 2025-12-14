from abc import ABC,abstractmethod

# this uses a composite design pattern , where an independent and the composite objects are 
# treated as one , like a single root tree structure , with mutilple functionality

# interface

class FileSystemItem(ABC):
    
    @abstractmethod
    def ls(self,indent):
        pass
    
    @abstractmethod
    def openAll(self,indent):
        pass

    @abstractmethod
    def getSize(self):
        pass

    @abstractmethod
    def cd(self,folderName):
        pass

    @abstractmethod
    def isFolder(self):
        pass

    @abstractmethod
    def getName(self):
        pass

class File(FileSystemItem):
    
    def __init__(self,name,size):
        self._name=name
        self._size=size

    def ls(self,indent=0):
        print((" "*indent)+self._name)

    def openAll(self,indent=0):
        print((" "*indent)+self._name)
    
    def getSize(self):
        return self._size

    def cd(self,folderName):
        return None

    def isFolder(self):
        return False

    def getName(self):
        return self._name

class Folder(FileSystemItem):

    def __init__(self,name):
        self._name=name
        self._children=[]
    
    def add(self,child:FileSystemItem): # adding files inside a folder
        self._children.append(child)
    
    def ls(self,indent=0):
        for child in self._children:
            print((" "*indent)+child.getName())

    def openAll(self,indent=0):
        print(" "*indent+self._name)
        for child in self._children:
            child.openAll(indent+4)
    
    def getSize(self):
        size=0
        for child in self._children:
            size+=child.getSize()
        return size

    def cd(self,folderName):
        #print(self._children[2].getName(),folderName,self._children[2].isFolder())
        for child in self._children:
            if child.isFolder() and child.getName()==folderName:
                return child
        return None

    def isFolder(self):
        return True

    def getName(self):
        return self._name


if __name__=="__main__":
    
    root=Folder("root")
    root.add(File("file1.py",1))
    root.add(File("file2.py",1))
    
    docs=Folder("docs")
    docs.add(File("resumse.pdf",1))
    docs.add(File("text.pdf",1))
    root.add(docs)

    folder=Folder("images")
    folder.add(File("image.png",1))
    root.add(folder)

    #root.ls(0)
    #root.openAll(0)
    #currFolder=root.cd("docs")
    #print(currFolder)
    #currFolder.ls(0)
    #print(root.getName())
    #print(root.getSize())