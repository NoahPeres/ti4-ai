"""Hex coordinate system for TI4 galaxy positioning."""


class HexCoordinate:
    """Represents a position in the hex-based galaxy using axial coordinates."""

    def __init__(self, q: int, r: int) -> None:
        self.q = q
        self.r = r

    def distance_to(self, other: "HexCoordinate") -> int:
        """Calculate the distance to another hex coordinate."""
        return (
            abs(self.q - other.q)
            + abs(self.q + self.r - other.q - other.r)
            + abs(self.r - other.r)
        ) // 2

    def get_neighbors(self) -> list["HexCoordinate"]:
        """Get all six adjacent hex coordinates."""
        directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
        return [HexCoordinate(self.q + dq, self.r + dr) for dq, dr in directions]
