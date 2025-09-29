from enum import Enum
from typing import Protocol


class PlanetTrait(Enum):
    """Planet traits that determine exploration deck."""

    CULTURAL = "cultural"
    HAZARDOUS = "hazardous"
    INDUSTRIAL = "industrial"
    FRONTIER = "frontier"


class ExplorationCardProtocol(Protocol):
    trait: PlanetTrait
