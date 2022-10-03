from typing import Callable

class State:
    __energy: int
    __energy_observers: list[Callable[[int], None]]

    def __init__(self):
        self.__energy = 0
        self.__energy_observers = []

    def register_energy_observer(self, observer: Callable[[int], None]):
        self.__energy_observers.append(observer)

    @property
    def energy(self) -> int:
        return self.__energy
    
    @energy.setter
    def energy(self, value: int):
        if value < 0:
            self.__energy = 0
        else:
            self.__energy = value
        for i in self.__energy_observers:
            i(self.__energy)
    
    def jsonObject(self) -> dict:
        return {'energy': self.energy}
    
    def importJsonObject(self, jsonObject: dict):
        self.energy = jsonObject['energy']