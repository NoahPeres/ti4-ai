"""Galaxy structure for TI4 game board."""

from typing import Optional

from .hex_coordinate import HexCoordinate
from .system import System


class Galaxy:
    """Represents the hex-based galaxy game board."""

    def __init__(self) -> None:
        self.systems: dict[HexCoordinate, str] = {}
        self.system_objects: dict[str, System] = {}  # Registry of system objects

    def place_system(self, coordinate: HexCoordinate, system_id: str) -> None:
        """Place a system at the given hex coordinate."""
        self.systems[coordinate] = system_id

    def register_system(self, system: System) -> None:
        """Register a system object in the galaxy."""
        self.system_objects[system.system_id] = system

    def get_system_coordinate(self, system_id: str) -> Optional[HexCoordinate]:
        """Get the coordinate of a system by its ID."""
        for coord, sid in self.systems.items():
            if sid == system_id:
                return coord
        return None

    def get_system(self, system_id: str) -> Optional[System]:
        """Get a system object by its ID."""
        return self.system_objects.get(system_id)

    def are_systems_adjacent(self, system_id1: str, system_id2: str) -> bool:
        """Check if two systems are adjacent to each other."""
        # Check physical adjacency first
        coord1 = self.get_system_coordinate(system_id1)
        coord2 = self.get_system_coordinate(system_id2)

        if coord1 is None or coord2 is None:
            return False

        # Physical adjacency
        if coord1.distance_to(coord2) == 1:
            return True

        # Check wormhole adjacency (stub implementation - always returns False for now)
        # This will be the focus of our RED phase test
        return self._check_wormhole_adjacency(system_id1, system_id2)

    def _check_wormhole_adjacency(self, system_id1: str, system_id2: str) -> bool:
        """Check if two systems are adjacent via wormholes."""
        system1 = self.get_system(system_id1)
        system2 = self.get_system(system_id2)
        
        if system1 is None or system2 is None:
            return False
        
        # Check if both systems have any matching wormholes
        for wormhole1 in system1.wormholes:
            if system2.has_wormhole(wormhole1):
                return True
        
        return False
