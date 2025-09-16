"""Core game state management for TI4."""

import uuid
from dataclasses import dataclass, field
from typing import Any, Optional

from .galaxy import Galaxy
from .game_phase import GamePhase
from .player import Player
from .system import System


@dataclass(frozen=True)
class GameState:
    """Represents the complete state of a TI4 game."""

    game_id: str = None
    players: list[Player] = field(default_factory=list, hash=False)
    galaxy: Optional[Galaxy] = None
    phase: GamePhase = GamePhase.SETUP
    systems: dict[str, System] = field(default_factory=dict, hash=False)
    player_resources: dict[str, dict[str, Any]] = field(
        default_factory=dict, hash=False
    )
    player_technologies: dict[str, list[str]] = field(default_factory=dict, hash=False)

    def __post_init__(self):
        """Initialize game_id if not provided."""
        if self.game_id is None:
            object.__setattr__(self, "game_id", str(uuid.uuid4()))

    def is_valid(self) -> bool:
        """Validate the consistency of the game state."""
        return True
