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
)
