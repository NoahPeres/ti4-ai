"""Core game state management for TI4."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GameState:
    """Represents the complete state of a TI4 game."""

    def is_valid(self) -> bool:
        """Validate the consistency of the game state."""
        return True
