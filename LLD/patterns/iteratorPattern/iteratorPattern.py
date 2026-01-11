from abc import abstractmethod,ABC 

class Iterator(ABC):
    @abstractmethod
    def hasNext(self):
        pass
    def next(self):
        pass

class Iterable(ABC):
    @abstractmethod
    def getIterable(self):
        pass

class LinkedList(Iterable):
    def __init__(self,val):
        self.val=val
        self.next=None
    
    def getIterable(self):
        return LinkedListIterator(self)
    
class LinkedListIterator(Iterator):
    def __init__(self,head):
        self.curr=head

    def hasNext(self):
        return self.curr is not None

    def next(self):
        val=self.curr.val
        self.curr=self.curr.next
        return val

class BinaryTree(Iterable):
    def __init__(self,val):
        self.val=val
        self.left=None
        self.right=None

    def getIterable(self):
        return BinaryTreeIterator(self)

class BinaryTreeIterator(Iterator):
    def __init__(self,root):
        self.stack=[]
        self.pushLeft(root)

    def pushLeft(self,node):
        while node:
            self.stack.append(node)
            node=node.left
    
    def hasNext(self):
        return len(self.stack)>0

    def next(self):
        node=self.stack.pop()
        val=node.val
        if node.right:
            self.pushLeft(node.right)
        return val
    
class Song:
    def __init__(self,title,artist):
        self.title=title
        self.artist=artist

class PlayList(Iterable):

    def __init__(self):
        self.songs=[]

    def addSong(self,s):
        self.songs.append(s)

    def getIterable(self):
        return PlayListIterator(self.songs)

class PlayListIterator(Iterator):
    def __init__(self,songs):
        self.songs=songs
        self.idx=0

    def hasNext(self):
        return self.idx<len(self.songs)
    
    def next(self):
        song=self.songs[self.idx]
        self.idx+=1
        return {song.title,song.artist}

if __name__=="__main__":
    l1=LinkedList(1)
    l1.next=LinkedList(2)
    l1.next.next=LinkedList(3)

    it1=l1.getIterable()
    print("LinkedList:")
    while it1.hasNext():
        print(it1.next(),end=" ")
    print("\n")

    root=BinaryTree(2)
    root.left=BinaryTree(1)
    root.right=BinaryTree(3)

    it2=root.getIterable()
    print("BinaryTree :")
    while it2.hasNext():
        print(it2.next(),end=" ")
    print("\n")


    pl=PlayList()
    pl.addSong(Song("t1","a1"))
    pl.addSong(Song("t2","a2"))
    print("Playlist Songs :")
    it3=pl.getIterable()
    while it3.hasNext():
        print(it3.next(),end=" ")
    print("\n")

        

