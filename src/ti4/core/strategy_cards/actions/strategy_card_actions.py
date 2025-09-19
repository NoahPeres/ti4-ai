"""Strategy card decisions for AI decision-making integration.

This module provides PlayerDecision implementations for strategy card operations,
integrating with the existing AI decision-making framework.

Requirements: 8.4 - Integrate with existing AI decision-making frameworks
"""

from dataclasses import dataclass
from typing import Any

from src.ti4.actions.action import ActionResult, PlayerDecision

from ..strategic_action import StrategyCardType


@dataclass(frozen=True)
class StrategyCardSelectionDecision(PlayerDecision):
    """Decision for selecting a strategy card during the strategy phase.

    Integrates strategy card selection with the AI decision-making framework.

    Requirements: 8.4 - Integrate with existing AI decision-making frameworks
    """

    card_type: StrategyCardType

    def is_legal(self, state: Any, player_id: Any) -> bool:
        """Check if this strategy card selection is legal.

        Args:
            state: Current game state (should have strategy_card_coordinator)
            player_id: The player attempting the selection

        Returns:
            True if the selection is legal, False otherwise
        """
        if not hasattr(state, "strategy_card_coordinator"):
            return False

        coordinator = state.strategy_card_coordinator

        # Check if it's the player's turn to select
        current_player = coordinator.get_current_selecting_player()
        if current_player != str(player_id):
            return False

        # Check if the card is available
        available_cards = coordinator.get_available_cards()
        return self.card_type in available_cards

    def execute(self, state: Any, player_id: Any) -> ActionResult:
        """Execute the strategy card selection.

        Args:
            state: Current game state (should have strategy_card_coordinator)
            player_id: The player making the selection

        Returns:
            ActionResult indicating success or failure
        """
        if not hasattr(state, "strategy_card_coordinator"):
            return ActionResult(
                success=False,
                new_state=state,
                message="Game state does not have strategy card coordinator",
            )

        coordinator = state.strategy_card_coordinator
        result = coordinator.select_strategy_card(player_id, self.card_type)

        return ActionResult(
            success=result.success,
            new_state=state,  # State is modified in place
            message=result.error_message
            if not result.success
            else f"Selected {self.card_type.value}",
        )

    def get_description(self) -> str:
        """Get a human-readable description of this decision.

        Returns:
            Description of the strategy card selection
        """
        return f"Select {self.card_type.value} strategy card"


@dataclass(frozen=True)
class StrategyCardActivationDecision(PlayerDecision):
    """Decision for activating a strategy card during the action phase.

    Integrates strategy card activation with the AI decision-making framework.

    Requirements: 8.4 - Integrate with existing AI decision-making frameworks
    """

    card_type: StrategyCardType

    def is_legal(self, state: Any, player_id: Any) -> bool:
        """Check if this strategy card activation is legal.

        Args:
            state: Current game state (should have strategy_card_coordinator)
            player_id: The player attempting the activation

        Returns:
            True if the activation is legal, False otherwise
        """
        if not hasattr(state, "strategy_card_coordinator"):
            return False

        coordinator = state.strategy_card_coordinator
        return bool(coordinator.can_use_primary_ability(str(player_id), self.card_type))

    def execute(self, state: Any, player_id: Any) -> ActionResult:
        """Execute the strategy card activation.

        Args:
            state: Current game state (should have strategic_action_manager)
            player_id: The player making the activation

        Returns:
            ActionResult indicating success or failure
        """
        if not hasattr(state, "strategic_action_manager"):
            return ActionResult(
                success=False,
                new_state=state,
                message="Game state does not have strategic action manager",
            )

        manager = state.strategic_action_manager
        result = manager.activate_strategy_card_via_coordinator(
            player_id, self.card_type
        )

        return ActionResult(
            success=result.success,
            new_state=state,  # State is modified in place
            message=result.error_message
            if not result.success
            else f"Activated {self.card_type.value}",
        )

    def get_description(self) -> str:
        """Get a human-readable description of this decision.

        Returns:
            Description of the strategy card activation
        """
        return f"Activate {self.card_type.value} strategy card"


@dataclass(frozen=True)
class SecondaryAbilityDecision(PlayerDecision):
    """Decision for using a secondary ability of another player's strategy card.

    Integrates secondary ability usage with the AI decision-making framework.

    Requirements: 8.4 - Integrate with existing AI decision-making frameworks
    """

    card_type: StrategyCardType

    def is_legal(self, state: Any, player_id: Any) -> bool:
        """Check if this secondary ability usage is legal.

        Args:
            state: Current game state (should have strategy_card_coordinator)
            player_id: The player attempting to use the secondary ability

        Returns:
            True if the usage is legal, False otherwise
        """
        if not hasattr(state, "strategy_card_coordinator"):
            return False

        coordinator = state.strategy_card_coordinator
        return bool(
            coordinator.can_use_secondary_ability(str(player_id), self.card_type)
        )

    def execute(self, state: Any, player_id: Any) -> ActionResult:
        """Execute the secondary ability usage.

        Args:
            state: Current game state (should have strategy_card_coordinator)
            player_id: The player using the secondary ability

        Returns:
            ActionResult indicating success or failure
        """
        if not hasattr(state, "strategy_card_coordinator"):
            return ActionResult(
                success=False,
                new_state=state,
                message="Game state does not have strategy card coordinator",
            )

        coordinator = state.strategy_card_coordinator
        success = coordinator.use_secondary_ability(player_id, self.card_type)

        return ActionResult(
            success=success,
            new_state=state,  # State is modified in place
            message=f"Used secondary ability of {self.card_type.value}"
            if success
            else "Failed to use secondary ability",
        )

    def get_description(self) -> str:
        """Get a human-readable description of this decision.

        Returns:
            Description of the secondary ability usage
        """
        return f"Use secondary ability of {self.card_type.value} strategy card"
