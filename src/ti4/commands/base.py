"""Base command interface for TI4 game actions."""

from abc import ABC, abstractmethod
from typing import Any, Dict

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
    def get_undo_data(self) -> Dict[str, Any]:
        """Get data needed for undo operation."""
        pass
    
    @abstractmethod
    def serialize(self) -> Dict[str, Any]:
        """Serialize command for persistence."""
        pass