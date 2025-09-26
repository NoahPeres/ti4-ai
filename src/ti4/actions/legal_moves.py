"""Legal move generation for TI4."""

from typing import Any

from ti4.actions.action import PlayerDecision
from ti4.actions.strategy_card_actions import (
    SecondaryAbilityDecision,
    StrategyCardActivationDecision,
    StrategyCardSelectionDecision,
)


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
        actions = []

        # Add strategy card actions if coordinator is available
        if hasattr(state, "strategy_card_coordinator"):
            actions.extend(self._generate_strategy_card_decisions(state, player_id))

        return actions

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

    # Backward compatibility aliases
    def generate_legal_decisions(
        self, state: Any, player_id: str
    ) -> list[PlayerDecision]:
        """Backward compatibility alias for generate_legal_actions."""
        return self.generate_legal_actions(state, player_id)

    def generate_legal_decisions_for_phase(
        self, state: Any, player_id: str, phase: Any
    ) -> list[PlayerDecision]:
        """Backward compatibility alias for generate_legal_actions_for_phase."""
        return self.generate_legal_actions_for_phase(state, player_id, phase)

    def filter_legal_decisions(
        self, potential_decisions: list[PlayerDecision], state: Any, player_id: str
    ) -> list[PlayerDecision]:
        """Backward compatibility alias for filter_legal_actions."""
        return self.filter_legal_actions(potential_decisions, state, player_id)

    def _generate_strategy_card_decisions(
        self, state: Any, player_id: str
    ) -> list[PlayerDecision]:
        """Generate strategy card related decisions for a player.

        Args:
            state: Current game state with strategy_card_coordinator
            player_id: ID of the player to generate decisions for

        Returns:
            List of strategy card PlayerDecision objects

        Requirements: 8.4 - Integrate with existing AI decision-making frameworks
        """
        decisions: list[PlayerDecision] = []
        coordinator = state.strategy_card_coordinator

        # Only generate strategy card decisions if coordinator is available
        if coordinator is None:
            return decisions

        # Strategy card selection decisions (during strategy phase)
        if coordinator._strategy_phase_active:
            current_player = coordinator.get_current_selecting_player()
            if current_player == player_id:
                available_cards = coordinator.get_available_cards()
                for card in available_cards:
                    decisions.append(StrategyCardSelectionDecision(card_type=card))

        # Strategy card activation decisions (during action phase)
        player_card = coordinator.get_player_strategy_card(player_id)
        if player_card and coordinator.can_use_primary_ability(player_id, player_card):
            decisions.append(StrategyCardActivationDecision(card_type=player_card))

        # Secondary ability decisions
        secondary_opportunities = coordinator.get_secondary_ability_opportunities(
            player_id
        )
        for opportunity in secondary_opportunities:
            if opportunity.can_use:
                decisions.append(
                    SecondaryAbilityDecision(card_type=opportunity.card_type)
                )

        return decisions
