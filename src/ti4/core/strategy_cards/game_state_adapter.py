"""Game state adapter for strategy card integration.

This module provides an adapter that connects strategy cards to the
existing game systems using proper interfaces.
"""

from typing import TYPE_CHECKING, Optional

from ..action_cards import ActionCardManager
from ..agenda_deck import AgendaDeck
from ..agenda_phase import SpeakerSystem
from ..command_tokens import CommandTokenManager

if TYPE_CHECKING:
    from typing import Any as GameState  # Placeholder for now


class StrategyCardGameStateAdapter:
    """Adapter that provides strategy card integration with game systems.

    This adapter implements the protocols expected by strategy cards
    and delegates to the actual game systems.
    """

    def __init__(
        self,
        action_card_system: Optional[ActionCardManager] = None,
        command_token_system: Optional[CommandTokenManager] = None,
        agenda_deck: Optional[AgendaDeck] = None,
        speaker_system: Optional[SpeakerSystem] = None,
        players: Optional[list[str]] = None,
    ) -> None:
        """Initialize the adapter with game systems.

        Args:
            action_card_system: The action card system
            command_token_system: The command token system
            agenda_deck: The agenda deck
            speaker_system: The speaker system
            players: List of valid player IDs
        """
        self.action_card_system = action_card_system or ActionCardManager()
        self.command_token_system = command_token_system or CommandTokenManager()
        self.agenda_deck = agenda_deck or AgendaDeck()
        self.speaker_system = speaker_system or SpeakerSystem()
        self.players = players or []

    def is_valid_player(self, player_id: str) -> bool:
        """Check if a player ID is valid.

        Args:
            player_id: The player ID to validate

        Returns:
            True if player is valid, False otherwise
        """
        return player_id in self.players if self.players else True

    def set_speaker(self, player_id: str) -> bool:
        """Set a new speaker.

        Args:
            player_id: The player to become speaker

        Returns:
            True if speaker was successfully set, False otherwise
        """
        if not self.is_valid_player(player_id):
            return False
        self.speaker_system.set_speaker(player_id)
        return True  # SpeakerSystem.set_speaker returns None, so we assume success

    def draw_action_cards(self, player_id: str, count: int) -> list[str]:
        """Draw action cards for a player.

        Args:
            player_id: The player drawing cards
            count: Number of cards to draw

        Returns:
            List of action card names drawn
        """
        if not self.is_valid_player(player_id):
            return []
        # Use a mock game state for now - in real implementation this would be the actual game state
        mock_game_state = type("MockGameState", (), {})()
        return self.action_card_system.draw_action_cards(
            player_id, count, mock_game_state
        )

    def spend_command_token_from_strategy_pool(
        self, player_id: str, count: int = 1
    ) -> bool:
        """Spend command tokens from strategy pool.

        Args:
            player_id: The player spending tokens
            count: Number of tokens to spend

        Returns:
            True if tokens were successfully spent, False otherwise
        """
        if not self.is_valid_player(player_id):
            return False
        # For now, return True as a placeholder since CommandTokenManager doesn't have this method
        # In a real implementation, this would delegate to the actual command token system
        return True

    def look_at_top_agenda_cards(self, count: int) -> list[str]:
        """Look at the top cards of the agenda deck.

        Args:
            count: Number of cards to look at

        Returns:
            List of agenda card names
        """
        return self.agenda_deck.look_at_top_cards(count)

    def rearrange_top_agenda_cards(self, cards: list[str]) -> bool:
        """Rearrange the top cards of the agenda deck.

        Args:
            cards: List of card names in new order

        Returns:
            True if cards were successfully rearranged
        """
        return self.agenda_deck.rearrange_top_cards(cards)


def create_game_state_adapter_from_game_state(
    game_state: "GameState",
) -> StrategyCardGameStateAdapter:
    """Create a strategy card adapter from an existing game state.

    Args:
        game_state: The game state to adapt

    Returns:
        A strategy card adapter connected to the game state's systems
    """
    # Extract systems from game state if they exist
    action_card_system = getattr(game_state, "action_card_system", None)
    command_token_system = getattr(game_state, "command_token_system", None)
    agenda_deck = getattr(game_state, "agenda_deck", None)
    speaker_system = getattr(game_state, "speaker_system", None)

    # Extract player list if available
    players = []
    if hasattr(game_state, "players"):
        players = list(game_state.players.keys())

    return StrategyCardGameStateAdapter(
        action_card_system=action_card_system,
        command_token_system=command_token_system,
        agenda_deck=agenda_deck,
        speaker_system=speaker_system,
        players=players,
    )
