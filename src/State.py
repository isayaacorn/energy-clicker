from decimal import Decimal
from typing import Callable


class State:
    __energy: Decimal
    __energy_observers: list[Callable[[Decimal], None]]
    
    __energy_per_second: Decimal
    __energy_per_second_observers: list[Callable[[Decimal], None]]

    def __init__(self):
        self.__energy = Decimal(0)
        self.__energy_observers = []

        self.__energy_per_second = Decimal(0)
        self.__energy_per_second_observers = []

    def register_energy_observer(self, observer: Callable[[Decimal], None]):
        self.__energy_observers.append(observer)

    @property
    def energy(self) -> Decimal:
        return self.__energy

    @energy.setter
    def energy(self, value: Decimal):
        if value < 0:
            self.__energy = Decimal(0)
        else:
            self.__energy = value
        for i in self.__energy_observers:
            i(self.__energy)

    def register_energy_per_second_observer(self, observer: Callable[[Decimal], None]):
        self.__energy_per_second_observers.append(observer)

    @property
    def energy_per_second(self) -> Decimal:
        return self.__energy_per_second

    @energy_per_second.setter
    def energy_per_second(self, value: Decimal):
        self.__energy_per_second = value
        for i in self.__energy_per_second_observers:
            i(self.__energy_per_second)

    def tick(self):
        self.energy += self.energy_per_second

    def json_object(self) -> dict:
        return {
            'energy': float(self.energy),
            'eps': float(self.energy_per_second)
        }

    def import_json_object(self, json_object: dict):
        self.energy = Decimal(json_object['energy'])
        self.energy_per_second = Decimal(json_object['eps'])
