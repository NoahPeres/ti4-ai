"""Game controller for managing TI4 game flow."""

from typing import Optional

from src.ti4.commands.manager import CommandManager
from src.ti4.core.game_phase import GamePhase
from src.ti4.core.player import Player
from src.ti4.core.strategy_card import STANDARD_STRATEGY_CARDS, StrategyCard


class GameController:
    """Manages game flow and turn order for TI4."""

    def __init__(self, players: list[Player]):
        """Initialize the game controller with players."""
        if not players:
            raise ValueError("At least one player is required")
        self._players = players
        self._current_player_index = 0
        self._current_phase = GamePhase.SETUP
        self._available_strategy_cards = list(STANDARD_STRATEGY_CARDS)
        self._selected_strategy_cards: dict[str, StrategyCard] = {}
        self._consecutive_passes = 0
        self._command_manager = CommandManager()

    def get_turn_order(self) -> list[Player]:
        """Get the current turn order."""
        return self._players

    def get_current_player(self) -> Player:
        """Get the currently active player."""
        return self._players[self._current_player_index]

    def advance_turn(self) -> None:
        """Advance to the next player in turn order."""
        self._current_player_index = (self._current_player_index + 1) % len(
            self._players
        )

    def _validate_player_exists(self, player_id: str) -> None:
        """Validate that a player exists in the game."""
        if not any(player.id == player_id for player in self._players):
            from .exceptions import InvalidPlayerError

            raise InvalidPlayerError(f"Player '{player_id}' not found in game")

    def is_player_activated(self, player_id: str) -> bool:
        """Check if a specific player is currently activated."""
        self._validate_player_exists(player_id)
        current_player = self.get_current_player()
        return current_player.id == player_id

    def pass_turn(self, player_id: str) -> None:
        """Allow a player to pass their turn."""
        if not self.is_player_activated(player_id):
            raise ValueError(f"Player '{player_id}' is not currently active")

        self.advance_turn()

    def start_strategy_phase(self) -> None:
        """Start the strategy phase."""
        self._current_phase = GamePhase.STRATEGY
        # Reset strategy card selections
        self._available_strategy_cards = list(STANDARD_STRATEGY_CARDS)
        self._selected_strategy_cards = {}

    def get_available_strategy_cards(self) -> list[StrategyCard]:
        """Get the list of available strategy cards."""
        return list(self._available_strategy_cards)

    def select_strategy_card(self, player_id: str, card_id: int) -> None:
        """Allow a player to select a strategy card."""
        self._validate_player_exists(player_id)

        # Find the card
        card = next(
            (c for c in self._available_strategy_cards if c.id == card_id), None
        )
        if card is None:
            raise ValueError(f"Strategy card with id {card_id} is not available")

        # Assign card to player and remove from available
        self._selected_strategy_cards[player_id] = card
        self._available_strategy_cards.remove(card)

    def get_player_strategy_card(self, player_id: str) -> Optional[StrategyCard]:
        """Get the strategy card selected by a player."""
        return self._selected_strategy_cards.get(player_id)

    def get_strategy_phase_turn_order(self) -> list[Player]:
        """Get turn order based on strategy card initiative values."""
        # Create list of (player, initiative) pairs
        player_initiatives = []
        for player in self._players:
            card = self._selected_strategy_cards.get(player.id)
            if card:
                player_initiatives.append((player, card.initiative))

        # Sort by initiative (lowest first)
        player_initiatives.sort(key=lambda x: x[1])

        # Return just the players in order
        return [player for player, _ in player_initiatives]

    def is_strategy_phase_complete(self) -> bool:
        """Check if all players have selected strategy cards."""
        return len(self._selected_strategy_cards) == len(self._players)

    def start_action_phase(self) -> None:
        """Start the action phase."""
        self._current_phase = GamePhase.ACTION

    def get_current_phase(self) -> str:
        """Get the current game phase."""
        return self._current_phase.value

    def _validate_action_preconditions(self, player_id: str) -> None:
        """Validate that a player can take an action."""
        self._validate_player_exists(player_id)

        if not self.is_player_activated(player_id):
            raise ValueError(f"Player '{player_id}' is not currently active")

        if self._current_phase != GamePhase.ACTION:
            raise ValueError("Not currently in action phase")

    def _reset_consecutive_passes(self) -> None:
        """Reset the consecutive passes counter."""
        self._consecutive_passes = 0

    def take_tactical_action(self, player_id: str, action_data: str) -> None:
        """Allow a player to take a tactical action."""
        self._validate_action_preconditions(player_id)
        self._reset_consecutive_passes()

        # For now, just advance the turn after taking an action
        self.advance_turn()

    def take_strategic_action(self, player_id: str, action_type: str) -> None:
        """Allow a player to take a strategic action."""
        self._validate_action_preconditions(player_id)
        self._reset_consecutive_passes()

        # For now, just advance the turn after taking an action
        self.advance_turn()

    def pass_action_phase_turn(self, player_id: str) -> None:
        """Allow a player to pass their turn in action phase."""
        self._validate_action_preconditions(player_id)

        # Increment consecutive passes
        self._consecutive_passes += 1

        # For now, just advance the turn
        self.advance_turn()

    def is_action_phase_complete(self) -> bool:
        """Check if action phase is complete (all players passed consecutively)."""
        return self._consecutive_passes >= len(self._players)
    
    def undo_last_action(self) -> bool:
        """Undo the last action taken. Returns True if successful."""
        try:
            # For now, we don't have a game state to pass, so we'll use None
            # This will be improved when we have proper game state management
            self._command_manager.undo_last_command(None)
            return True
        except ValueError:
            # No commands to undo
            return False
    
    def redo_last_action(self) -> bool:
        """Redo the last undone action. Returns True if successful."""
        # For now, we don't have redo functionality implemented
        # This would require a separate redo stack in CommandManager
        return False
    
    def get_action_history(self) -> list:
        """Get the history of actions taken."""
        return self._command_manager.get_command_history()
