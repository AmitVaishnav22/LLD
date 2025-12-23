from abc import ABC,abstractmethod


class Engine(ABC):
    @abstractmethod
    def start(self):
        pass

class PetrolEngine(Engine):
    def start(self):
        print("Petrol engine started")

class DieselEngine(Engine):
    def start(self):
        print("Diesel engine started")

class ElectricEngine(Engine):
    def start(self):
        print("Electric engine started")

class Car(ABC):
    def __init__(self,engine:Engine):
        self._engine=engine

    @abstractmethod
    def drive(self):
        pass

class Sedan(Car):
    def drive(self):
        self._engine.start()
        print("Driving a sedan")

class SUV(Car):
    def drive(self):
        self._engine.start()
        print("Driving an SUV")

if __name__ == "__main__":
    petrolengine = PetrolEngine()
    dieselengine = DieselEngine()
    electricengine = ElectricEngine()

    sedanwithpetrol = Sedan(petrolengine)
    sedanwithpetrol.drive()

    suvwithdiesel = SUV(dieselengine)
    suvwithdiesel.drive()

    sedanwithelectric = Sedan(electricengine)
    sedanwithelectric.drive()