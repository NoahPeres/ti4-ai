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
        game_state: Optional["GameState"] = None,
        action_card_system: Optional[ActionCardManager] = None,
        command_token_system: Optional[CommandTokenManager] = None,
        agenda_deck: Optional[AgendaDeck] = None,
        speaker_system: Optional[SpeakerSystem] = None,
        players: Optional[list[str]] = None,
    ) -> None:
        """Initialize the adapter with game systems.

        Args:
            game_state: The current game state (for real integrations)
            action_card_system: The action card system
            command_token_system: The command token system
            agenda_deck: The agenda deck
            speaker_system: The speaker system
            players: List of valid player IDs
        """
        self._game_state = game_state
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

        # If we have a real game state, use it and update our reference
        if (
            hasattr(self, "_game_state")
            and self._game_state is not None
            and hasattr(self._game_state, "set_speaker")
        ):
            try:
                new_state = self._game_state.set_speaker(player_id)
                self._game_state = new_state  # Update our reference
                return True
            except ValueError:
                return False

        # Fallback to speaker system
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

        # Use the real game state if available
        if self._game_state:
            # Update our game state reference with the new state
            new_state = self._game_state.draw_action_cards(player_id, count)
            self._game_state = new_state
            # Return the actual card names that were added
            if (
                hasattr(new_state, "player_action_cards")
                and player_id in new_state.player_action_cards
            ):
                player_cards = new_state.player_action_cards[player_id]
                # Return the last 'count' cards that were added
                if len(player_cards) >= count:
                    result: list[str] = player_cards[-count:]
                    return result
                else:
                    result_all: list[str] = player_cards
                    return result_all
            return [f"action_card_{i + 1}" for i in range(count)]
        else:
            # Fallback to action card system
            return self.action_card_system.draw_action_cards(player_id, count, None)

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

        # If we have a command token system, delegate to it
        if self.command_token_system:
            # The CommandTokenManager expects a game_state parameter
            # We need to bridge between the protocol interface and the manager interface
            if hasattr(self, "_game_state") and self._game_state is not None:
                try:
                    # Use the new immutable interface that returns GameState
                    updated_state = (
                        self._game_state.spend_command_token_from_strategy_pool(
                            player_id, count
                        )
                    )
                    # Update our internal state reference
                    self._game_state = updated_state
                    return True
                except ValueError:
                    # Player doesn't exist or insufficient tokens
                    return False
            else:
                # No game state available - cannot verify or spend tokens
                import logging

                logging.warning(
                    f"Cannot spend token for {player_id}: no game_state available"
                )
                return False

        # Fallback for testing without command token system
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
        players = [player.id for player in game_state.players]

    return StrategyCardGameStateAdapter(
        action_card_system=action_card_system,
        command_token_system=command_token_system,
        agenda_deck=agenda_deck,
        speaker_system=speaker_system,
        players=players,
    )
