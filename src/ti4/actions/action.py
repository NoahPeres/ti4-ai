"""Base action framework for TI4."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ActionResult:
    """Result of executing a player decision."""

    success: bool
    new_state: Any
    message: str | None = None


class PlayerDecision(ABC):
    """Base class for all player decisions and interactions in the game.

    This encompasses Actions, reactions, transactions, choices, and any other
    player interaction that can affect the game state.
    """

    @abstractmethod
    def is_legal(self, state: Any, player_id: Any) -> bool:
        """Check if this decision is legal in the given state for the player."""
        pass

    @abstractmethod
    def execute(self, state: Any, player_id: Any) -> Any:
        """Execute this decision and return the new game state."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get a human-readable description of this decision."""
        pass


class Action(PlayerDecision):
    """Base class for TI4 Actions (Tactical, Strategic, Component).

    Actions are the formal moves taken during the Action Phase of TI4.
    This does not include reactions, transactions, or other player decisions.
    """

    pass
