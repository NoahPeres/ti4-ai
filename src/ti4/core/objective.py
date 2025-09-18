"""Objective card system for TI4."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_state import GameState
    from .game_phase import GamePhase


@dataclass(frozen=True)
class Objective:
    """Represents an objective card in TI4."""

    id: str
    name: str
    description: str
    points: int
    is_public: bool
    scoring_phase: "GamePhase"


class CompletableObjective(ABC):
    """Abstract base class for objectives that can check their own completion."""

    @abstractmethod
    def is_completed_by(self, game_state: "GameState", player_id: str) -> bool:
        """Check if this objective is completed by the given player."""
        pass

    @abstractmethod
    def get_objective(self) -> Objective:
        """Get the underlying Objective data."""
        pass
