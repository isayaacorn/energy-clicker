from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Building:
    id: str
    name: str
    price: Decimal
    energy_per_second: Decimal


BUILDINGS = (
    Building('campfire', 'Campfire', Decimal(15), Decimal(0.2)),
    Building('water-wheel', 'Water Wheel', Decimal(130), Decimal(2)),
    Building('coal-mine', 'Coal Mine', Decimal(1.17e3), Decimal(16)),
)
