"""Legal move generation for TI4."""

from typing import Any

from src.ti4.actions.action import PlayerDecision


class LegalMoveGenerator:
    """Generates legal moves for players based on game state and phase.

    This class provides the core functionality for determining what actions
    are available to players at any given point in the game, filtering by
    game phase and player state as required.
    """

    def generate_legal_actions(
        self, state: Any, player_id: str
    ) -> list[PlayerDecision]:
        """Generate all legal actions for a player in the current state.

        Args:
            state: Current game state
            player_id: ID of the player to generate actions for

        Returns:
            List of legal PlayerDecision objects available to the player
        """
        # For now, return empty list - will be expanded as more actions are implemented
        return []

    def generate_legal_actions_for_phase(
        self, state: Any, player_id: str, phase: Any
    ) -> list[PlayerDecision]:
        """Generate legal actions for a player in a specific game phase.

        Args:
            state: Current game state
            player_id: ID of the player to generate actions for
            phase: Specific game phase to filter actions for

        Returns:
            List of legal PlayerDecision objects available in the specified phase
        """
        # For now, return empty list - will be expanded as phase-specific actions are implemented
        return []

    def filter_legal_actions(
        self, potential_actions: list[PlayerDecision], state: Any, player_id: str
    ) -> list[PlayerDecision]:
        """Filter a list of potential actions to only include legal ones.

        Args:
            potential_actions: List of actions to filter
            state: Current game state
            player_id: ID of the player attempting the actions

        Returns:
            List containing only the legal actions from the input list
        """
        return [
            action for action in potential_actions if action.is_legal(state, player_id)
        ]
