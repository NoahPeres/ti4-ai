"""Player management for TI4."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Player:
    """Represents a player in a TI4 game."""

    id: str
    faction: str

    def is_valid(self) -> bool:
        """Validate the player data."""
        return True
