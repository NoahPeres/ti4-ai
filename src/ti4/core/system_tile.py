"""
System Tile implementation for Rule 88: SYSTEM TILES

Rule 88: A system tile represents an area of the galaxy. Players place system tiles during setup to create the game board.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ti4.core.planet import Planet  # type: ignore[import-untyped]


class TileColor(Enum):
    """Tile back colors as defined in Rule 88.1"""

    GREEN = "green"  # Home systems and faction-specific tiles (88.2)
    BLUE = "blue"  # Systems containing one or more planets (88.3)
    RED = "red"  # Anomalies or systems without planets (88.4)


class TileType(Enum):
    """Types of system tiles"""

    HOME_SYSTEM = "home_system"  # Green-backed home systems (88.2)
    PLANET_SYSTEM = "planet_system"  # Blue-backed systems with planets (88.3)
    ANOMALY = "anomaly"  # Red-backed anomaly systems (88.4)
    EMPTY_SYSTEM = "empty_system"  # Red-backed systems without planets (88.4)
    HYPERLANE = "hyperlane"  # Double-sided hyperlane tiles (88.7)


class SystemTile:
    """
    Represents a system tile as defined in Rule 88.

    A system tile represents an area of the galaxy. Players place system tiles
    during setup to create the game board.
    """

    def __init__(
        self,
        tile_id: str,
        color: TileColor | None,
        tile_type: TileType,
        faction: str | None = None,
    ):
        """
        Initialize a SystemTile.

        Args:
            tile_id: Unique identifier for the tile
            color: Back color of the tile (green/blue/red or None for hyperlanes)
            tile_type: Type of the tile
            faction: Faction for home system tiles (optional)
        """
        self.tile_id = tile_id
        self.color = color
        self.tile_type = tile_type
        self.faction = faction
        self.planets: list[Planet] = []
        self.adjacent_tiles: set[SystemTile] = set()

        # Validate color and type consistency per Rule 88
        self._validate_color_type_consistency()

    def _validate_color_type_consistency(self) -> None:
        """Validate that tile color and type are consistent with Rule 88."""
        if self.color == TileColor.GREEN and self.tile_type != TileType.HOME_SYSTEM:
            raise ValueError("Green tiles must be home systems (Rule 88.2)")

        if self.color == TileColor.BLUE and self.tile_type != TileType.PLANET_SYSTEM:
            raise ValueError("Blue tiles must be planet systems (Rule 88.3)")

        if self.color == TileColor.RED and self.tile_type not in [
            TileType.ANOMALY,
            TileType.EMPTY_SYSTEM,
        ]:
            raise ValueError("Red tiles must be anomalies or empty systems (Rule 88.4)")

    def add_planet(self, planet: Planet) -> None:
        """Add a planet to this system tile (Rule 88.5)."""
        self.planets.append(planet)

    def has_planets(self) -> bool:
        """Check if this tile contains planets (Rule 88.3, 88.5)."""
        return len(self.planets) > 0

    def contains_planet(self, planet_name: str) -> bool:
        """Check if this tile contains a specific planet."""
        return any(planet.name == planet_name for planet in self.planets)

    def is_home_system(self) -> bool:
        """Check if this is a home system tile (Rule 88.2)."""
        return self.tile_type == TileType.HOME_SYSTEM

    def is_anomaly(self) -> bool:
        """Check if this is an anomaly tile (Rule 88.4)."""
        return self.tile_type == TileType.ANOMALY

    def is_hyperlane(self) -> bool:
        """Check if this is a hyperlane tile (Rule 88.7)."""
        return self.tile_type == TileType.HYPERLANE

    def is_system(self) -> bool:
        """Check if this is a system tile (not a hyperlane) (Rule 88.7)."""
        return self.tile_type != TileType.HYPERLANE

    def has_space_area(self) -> bool:
        """Check if this tile has a space area (Rule 88.6)."""
        # All system tiles have space areas, hyperlanes do not
        return self.is_system()

    def can_hold_ships(self) -> bool:
        """Check if ships can be placed in this tile's space area (Rule 88.6)."""
        return self.has_space_area()

    def has_crossing_lines(self) -> bool:
        """Check if this tile has crossing lines (hyperlane property) (Rule 88.7)."""
        return self.is_hyperlane()

    def add_adjacent_tile(self, tile: SystemTile) -> None:
        """Add an adjacent tile (for Rule 6 adjacency support)."""
        self.adjacent_tiles.add(tile)

    def __str__(self) -> str:
        """String representation of the tile."""
        color_str = self.color.value.upper() if self.color else "None"
        type_str = self.tile_type.value.upper()
        return f"SystemTile({self.tile_id}, {color_str}, {type_str})"

    def __repr__(self) -> str:
        """Detailed representation of the tile."""
        return self.__str__()
