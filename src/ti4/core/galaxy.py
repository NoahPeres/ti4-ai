"""Galaxy structure for TI4 game board."""

from .hex_coordinate import HexCoordinate


class Galaxy:
    """Represents the hex-based galaxy game board."""

    def __init__(self) -> None:
        self.systems: dict[HexCoordinate, str] = {}

    def place_system(self, coordinate: HexCoordinate, system_id: str) -> None:
        """Place a system at the given hex coordinate."""
        self.systems[coordinate] = system_id
