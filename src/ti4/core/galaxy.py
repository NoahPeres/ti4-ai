"""Galaxy structure for TI4 game board."""

from typing import Optional

from .hex_coordinate import HexCoordinate


class Galaxy:
    """Represents the hex-based galaxy game board."""

    def __init__(self) -> None:
        self.systems: dict[HexCoordinate, str] = {}

    def place_system(self, coordinate: HexCoordinate, system_id: str) -> None:
        """Place a system at the given hex coordinate."""
        self.systems[coordinate] = system_id

    def get_system_coordinate(self, system_id: str) -> Optional[HexCoordinate]:
        """Get the coordinate of a system by its ID."""
        for coord, sid in self.systems.items():
            if sid == system_id:
                return coord
        return None

    def are_systems_adjacent(self, system_id1: str, system_id2: str) -> bool:
        """Check if two systems are adjacent to each other."""
        coord1 = self.get_system_coordinate(system_id1)
        coord2 = self.get_system_coordinate(system_id2)

        if coord1 is None or coord2 is None:
            return False

        return coord1.distance_to(coord2) == 1
