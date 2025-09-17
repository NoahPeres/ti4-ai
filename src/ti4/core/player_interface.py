"""Player interface abstractions for TI4."""

from abc import ABC, abstractmethod
from typing import Any

from ..actions.action import Action
from .game_state import GameState


class PlayerInterface(ABC):
    """Abstract interface for all player types (AI and human)."""

    @abstractmethod
    def choose_action(self, state: GameState, legal_actions: list[Action]) -> Action:
        """Choose an action from the list of legal actions."""
        pass

    @abstractmethod
    def make_choice(self, state: GameState, choice_context: Any) -> Any:
        """Make a choice in a given context (e.g., combat rolls, agenda votes)."""
        pass


class PlayerStateView:
    """Player-specific view of the game state with information hiding."""

    def __init__(self, player_id: str, game_state: GameState):
        """Initialize the player state view."""
        self.player_id = player_id
        self._game_state = game_state

    @classmethod
    def create_for_player(
        cls, game_state: GameState, player_id: str
    ) -> "PlayerStateView":
        """Create a player state view for a specific player."""
        return cls(player_id, game_state)

    def get_legal_actions(self) -> list[Action]:
        """Get the list of legal actions for this player."""
        # Basic implementation - returns empty list for now
        return []

    def get_visible_information(self) -> dict[str, Any]:
        """Get information visible to this player."""
        # Basic implementation - returns basic game info
        return {
            "player_id": self.player_id,
            "game_phase": self._game_state.phase,
            "players": [p.id for p in self._game_state.players],
        }


class BasicAIPlayer(PlayerInterface):
    """Basic AI player implementation for testing purposes."""

    def __init__(self, player_id: str):
        """Initialize the AI player with a player ID."""
        self.player_id = player_id

    def choose_action(self, state: GameState, legal_actions: list[Action]) -> Action:
        """Choose the first available action (basic implementation)."""
        if not legal_actions:
            raise ValueError("No legal actions available")
        return legal_actions[0]

    def make_choice(self, state: GameState, choice_context: Any) -> Any:
        """Make a default choice (basic implementation)."""
        return None
