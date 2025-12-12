from strategies.playStrategy import PlayStrategy
from strategies.customQueueStrategy import CustomQueueStrategy
from strategies.randomPlayStrategy import RandomPlayStrategy
from strategies.sequentialPlayStrategy import SequentialPlayStrategy
from enums.playStrategyType import PlayStrategyType

class StrategyManager:
    _instance=None
    def __init__(self):
        self._sequentialPlayStrategy=SequentialPlayStrategy()
        self._randomPlayStrategy=RandomPlayStrategy()
        self._customQueueStrategy=CustomQueueStrategy()

    @staticmethod
    def getInstance():
        if StrategyManager._instance is None:
            StrategyManager._instance=StrategyManager()
        return StrategyManager._instance

    def getStrategy(self,type):
        if type==PlayStrategyType.SEQUENTIAL:
            return self._sequentialPlayStrategy
        elif type==PlayStrategyType.RANDOM:
            return self._randomPlayStrategy
        else:
            return self._customQueueStrategy
            

