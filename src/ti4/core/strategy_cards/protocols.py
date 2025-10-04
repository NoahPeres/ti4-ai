"""Protocols for strategy card system integration.

This module defines the interfaces that strategy cards expect from
the game systems they interact with.
"""

from abc import abstractmethod
from typing import Any, Protocol


class ActionCardSystemProtocol(Protocol):
    """Protocol for action card system integration."""

    @abstractmethod
    def draw_action_cards(
        self, player_id: str, count: int, game_state: Any
    ) -> list[str]:
        """Draw action cards for a player.

        Args:
            player_id: The player drawing cards
            count: Number of cards to draw
            game_state: Game state to update

        Returns:
            List of action card identifiers drawn
        """
        ...


class SpeakerSystemProtocol(Protocol):
    """Protocol for speaker system integration."""

    @abstractmethod
    def set_speaker(self, player_id: str) -> Any:  # GameState in actual implementation
        """Set a new speaker.

        Args:
            player_id: The player to become speaker

        Returns:
            New GameState with updated speaker

        Raises:
            ValueError: If player_id doesn't exist
        """
        ...


class CommandTokenSystemProtocol(Protocol):
    """Protocol for command token system integration."""

    @abstractmethod
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
        ...


class AgendaDeckProtocol(Protocol):
    """Protocol for agenda deck system integration."""

    @abstractmethod
    def look_at_top_cards(self, count: int) -> list[str]:
        """Look at the top cards of the agenda deck.

        Args:
            count: Number of cards to look at

        Returns:
            List of agenda card identifiers
        """
        ...

    @abstractmethod
    def rearrange_top_cards(self, cards: list[str]) -> bool:
        """Rearrange the top cards of the agenda deck.

        Args:
            cards: List of card identifiers in new order

        Returns:
            True if cards were successfully rearranged
        """
        ...


class GameStateProtocol(Protocol):
    """Protocol for game state integration with strategy cards."""

    # System access
    action_card_system: ActionCardSystemProtocol
    speaker_system: SpeakerSystemProtocol
    command_token_system: CommandTokenSystemProtocol
    agenda_deck: AgendaDeckProtocol

    # Player validation
    @abstractmethod
    def is_valid_player(self, player_id: str) -> bool:
        """Check if a player ID is valid.

        Args:
            player_id: The player ID to validate

        Returns:
            True if player is valid, False otherwise
        """
        ...
