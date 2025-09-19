"""Strategy card coordinator for Rule 83: STRATEGY CARD system.

This module implements the lightweight coordinator that integrates with existing systems
to provide strategy card assignment, tracking, and initiative order calculation.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .strategic_action import StrategicActionManager, StrategyCardType


# Strategy card initiative numbers according to TI4 rules
STRATEGY_CARD_INITIATIVE_NUMBERS = {
    "leadership": 1,
    "diplomacy": 2,
    "politics": 3,
    "construction": 4,
    "trade": 5,
    "warfare": 6,
    "technology": 7,
    "imperial": 8
}


@dataclass
class StrategyCardAssignmentResult:
    """Result of a strategy card assignment operation."""

    success: bool
    player_id: Optional[str] = None
    strategy_card: Optional["StrategyCardType"] = None
    error_message: Optional[str] = None


class StrategyCardCoordinator:
    """Lightweight coordinator for strategy card system integration.

    Integrates with existing StrategicActionManager to provide:
    - Card assignment and tracking functionality
    - Initiative order calculation as pure function
    - Integration points with existing game state system

    Requirements: 1.1, 1.2, 1.3, 6.1, 6.2
    """

    def __init__(self, strategic_action_manager: "StrategicActionManager") -> None:
        """Initialize the strategy card coordinator.

        Args:
            strategic_action_manager: The existing strategic action manager to integrate with
        """
        self._strategic_action_manager = strategic_action_manager
        self._card_assignments: dict[str, StrategyCardType] = {}
        self._exhausted_cards: set[StrategyCardType] = set()

    def assign_strategy_card(self, player_id: str, card: "StrategyCardType") -> StrategyCardAssignmentResult:
        """Assign a strategy card to a player.

        Args:
            player_id: The player to assign the card to
            card: The strategy card to assign

        Returns:
            StrategyCardAssignmentResult indicating success or failure
        """
        if not player_id:
            return StrategyCardAssignmentResult(
                success=False,
                error_message="Player ID cannot be empty"
            )

        if card is None:
            return StrategyCardAssignmentResult(
                success=False,
                error_message="Strategy card cannot be None"
            )

        # For now, just track the assignment
        self._card_assignments[player_id] = card

        return StrategyCardAssignmentResult(
            success=True,
            player_id=player_id,
            strategy_card=card
        )

    def calculate_initiative_order(self, player_assignments: dict[str, "StrategyCardType"]) -> list[str]:
        """Calculate initiative order based on strategy card assignments.

        This is a pure function that calculates player order based on strategy card
        initiative numbers (1-8).

        Args:
            player_assignments: Dictionary mapping player_id to StrategyCardType

        Returns:
            List of player IDs in initiative order (lowest to highest)

        Requirements: 1.3 - Initiative order calculation as pure function
        """
        if not player_assignments:
            return []

        # Create list of (player_id, initiative_number) tuples
        player_initiatives = []
        for player_id, card in player_assignments.items():
            if not player_id:  # Skip empty player IDs
                continue

            card_name = card.value if hasattr(card, 'value') else str(card)
            initiative_num = STRATEGY_CARD_INITIATIVE_NUMBERS.get(card_name, 999)  # Default high number for unknown cards
            player_initiatives.append((player_id, initiative_num))

        # Sort by initiative number (lowest first)
        player_initiatives.sort(key=lambda x: x[1])

        # Return just the player IDs in order
        return [player_id for player_id, _ in player_initiatives]

    def integrate_with_strategic_actions(self) -> None:
        """Integrate this coordinator with the strategic action manager.

        This creates the integration points between the strategy card system
        and the existing strategic action system.

        Requirements: 6.1, 6.2 - Integration with strategic action system

        Raises:
            ValueError: If strategic action manager is None
        """
        if self._strategic_action_manager is None:
            raise ValueError("Strategic action manager cannot be None")

        # Set up bidirectional integration
        self._strategic_action_manager._strategy_card_coordinator = self
