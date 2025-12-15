from abc import ABC,abstractmethod

# templete method is a defined pipeline method which already knows the sequence of tasks exceution
# since to keep track of the sequence we make a boilerplate to excute the steps in sequence no matter
# how they are implemented

class ModelTrainer(ABC):
    
    def trainPipeline(self,path):
        self.loadData(path)
        self.preprocessData()
        self.trainData()
        self.evaluateData()
        self.saveModel()
    
    def loadData(self,path):
        print("[common] loading dataset from ",path)
    
    def preprocessData(self):
        print("[common] preprocessing data")
    
    @abstractmethod
    def trainData(self):
        pass

    @abstractmethod
    def evaluateData(self):
        pass
    
    #@abstractmethod
    def saveModel(self):
        print("[common] saving data in disk as defualt")

class NeuralNetworkTrainer(ModelTrainer):
    def trainData(self):
        print("[NeuralNet] training data")

    def evaluateData(self):
        print("[NeuralNet] evaluation of data")

class DecisionTreeTrainer(ModelTrainer):
    def trainData(self):
        print("[DecisionTree] training data")

    def saveModel(self):
        print("[DecisionTree] saved data in disk as defualt")
    
    def evaluateData(self):
        print("[DecisionTree] evaluation of data")


if __name__=="__main__":
    print("\n--NeuralNetworkTraining--\n")
    ns=NeuralNetworkTrainer()
    ns.trainPipeline("data/images/file")
    print("\n--DecisionTreeTraining--\n")
    ds=DecisionTreeTrainer()
    ds.trainPipeline("data/iris.csv")
