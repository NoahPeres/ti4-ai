"""Base command interface for TI4 game actions."""

from abc import ABC, abstractmethod
from typing import Any

from ..core.game_state import GameState


class GameCommand(ABC):
    """Base interface for all game commands."""

    @abstractmethod
    def execute(self, game_state: GameState) -> GameState:
        """Execute the command and return new game state."""
        pass

    @abstractmethod
    def undo(self, game_state: GameState) -> GameState:
        """Undo the command and return previous game state."""
        pass

    @abstractmethod
    def can_execute(self, game_state: GameState) -> bool:
        """Check if command can be executed in current state."""
        pass

    @abstractmethod
    def get_undo_data(self) -> dict[str, Any]:
        """Get data needed for undo operation."""
        pass

    @abstractmethod
    def serialize(self) -> dict[str, Any]:
        """Serialize command for persistence."""
        pass

    def execute_with_events(
        self, game_state: GameState, event_bus: Any | None = None
    ) -> GameState:
        """Execute the command and publish events if event bus is provided."""
        result = self.execute(game_state)

        if event_bus is not None:
            self._publish_events(event_bus, game_state)

        return result

    @abstractmethod
    def _publish_events(self, event_bus: Any, game_state: GameState) -> None:
        """Publish events related to this command. Override in subclasses."""
        pass
