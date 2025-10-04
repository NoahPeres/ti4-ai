"""
Command token management system for TI4.

This module provides command token management functionality including
fleet pool management with agenda card integration.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_state import GameState


class CommandTokenManager:
    """Manages command token operations with agenda card integration.

    TODO: This class should be moved to test utilities or refactored to delegate
    fleet pool updates to game_state.players[player_id].command_sheet.fleet_pool
    instead of maintaining an independent _fleet_tokens store.
    """

    def __init__(self) -> None:
        """Initialize the command token manager."""
        # Track fleet tokens per player for testing
        self._fleet_tokens: dict[str, int] = {}

    def add_fleet_pool_token(self, player_id: str, game_state: GameState) -> bool:
        """Add a command token to a player's fleet pool.

        Args:
            player_id: The player to add the token for
            game_state: Current game state (for law effect checking)

        Returns:
            True if token was added successfully, False if blocked by laws
        """
        # Check for law effects that might restrict fleet pool tokens
        law_effects = game_state.get_law_effects_for_action(
            "fleet_pool_management", player_id
        )

        # Check for Fleet Regulations law
        for law_effect in law_effects:
            if (
                law_effect.agenda_card
                and law_effect.agenda_card.get_name() == "Fleet Regulations"
            ):
                # Fleet Regulations limits fleet pool to 4 tokens
                current_tokens = self._get_current_fleet_tokens(player_id, game_state)
                if current_tokens >= 4:
                    return False  # Blocked by Fleet Regulations

        # If no restrictions, add the token
        if player_id not in self._fleet_tokens:
            self._fleet_tokens[player_id] = 0
        self._fleet_tokens[player_id] += 1
        return True

    def _get_current_fleet_tokens(self, player_id: str, game_state: GameState) -> int:
        """Get the current number of fleet pool tokens for a player.

        This is a simplified implementation for testing purposes.
        """
        return self._fleet_tokens.get(player_id, 0)

    def spend_strategy_pool_token(
        self, player_id: str, game_state: GameState
    ) -> GameState:
        """Spend a command token from a player's strategy pool.

        Args:
            player_id: The player spending the token
            game_state: Current game state

        Returns:
            New GameState with token spent

        Raises:
            ValueError: If player doesn't exist or has insufficient tokens
        """
        if not player_id:
            raise ValueError("Player ID cannot be empty")

        # Delegate to game state method and return the new state
        return game_state.spend_command_token_from_strategy_pool(player_id, 1)
