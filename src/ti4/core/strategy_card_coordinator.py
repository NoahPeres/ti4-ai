"""Strategy card coordinator for Rule 83: STRATEGY CARD system.

This module implements the lightweight coordinator that integrates with existing systems
to provide strategy card assignment, tracking, and initiative order calculation.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .strategic_action import StrategicActionManager, StrategyCardType
else:
    StrategicActionManager = "StrategicActionManager"
    StrategyCardType = "StrategyCardType"


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


@dataclass
class StrategyPhaseSelectionResult:
    """Result of starting a strategy phase selection workflow."""

    success: bool
    current_selecting_player: Optional[str] = None
    available_cards: Optional[list["StrategyCardType"]] = None
    error_message: Optional[str] = None

    def __post_init__(self) -> None:
        """Initialize available_cards if None."""
        if self.available_cards is None:
            self.available_cards = []


@dataclass
class StrategyCardSelectionResult:
    """Result of a strategy card selection operation."""

    success: bool
    player_id: Optional[str] = None
    strategy_card: Optional["StrategyCardType"] = None
    next_selecting_player: Optional[str] = None
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

        # Strategy phase selection state
        self._strategy_phase_active: bool = False
        self._speaker_order: list[str] = []
        self._current_selecting_player_index: int = 0

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

    def _get_strategy_card_type_enum(self) -> type["StrategyCardType"]:
        """Get the StrategyCardType enum, handling circular imports."""
        from .strategic_action import StrategyCardType
        return StrategyCardType

    def _validate_basic_inputs(self, player_id: str, card: Optional["StrategyCardType"]) -> Optional[str]:
        """Validate basic inputs for card operations.

        Args:
            player_id: The player ID to validate
            card: The strategy card to validate

        Returns:
            Error message if validation fails, None if valid
        """
        if not player_id:
            return "Player ID cannot be empty"

        if card is None:
            return "Strategy card cannot be None"

        return None

    def start_strategy_phase_selection(self, speaker_order: list[str]) -> StrategyPhaseSelectionResult:
        """Start the strategy phase card selection workflow.

        Args:
            speaker_order: List of player IDs in speaker order

        Returns:
            StrategyPhaseSelectionResult indicating success or failure

        Requirements: 2.1 - Players can select cards in speaker order during strategy phase
        """
        if not speaker_order:
            return StrategyPhaseSelectionResult(
                success=False,
                error_message="Speaker order cannot be empty"
            )

        self._strategy_phase_active = True
        self._speaker_order = speaker_order.copy()
        self._current_selecting_player_index = 0

        # Get all available strategy cards
        StrategyCardType = self._get_strategy_card_type_enum()
        all_cards = list(StrategyCardType)

        return StrategyPhaseSelectionResult(
            success=True,
            current_selecting_player=speaker_order[0],
            available_cards=all_cards
        )

    def get_available_cards(self) -> list["StrategyCardType"]:
        """Get list of strategy cards that are still available for selection.

        Returns:
            List of unassigned strategy cards

        Requirements: 2.3 - Selected cards are no longer available to other players
        """
        StrategyCardType = self._get_strategy_card_type_enum()
        all_cards = list(StrategyCardType)
        assigned_cards = set(self._card_assignments.values())

        return [card for card in all_cards if card not in assigned_cards]

    def select_strategy_card(self, player_id: str, card: "StrategyCardType") -> StrategyCardSelectionResult:
        """Select a strategy card for a player during the strategy phase.

        Args:
            player_id: The player selecting the card
            card: The strategy card to select

        Returns:
            StrategyCardSelectionResult indicating success or failure

        Requirements: 2.1, 2.2, 2.4 - Speaker order selection, card moves to player area, validation
        """
        # Input validation
        validation_error = self._validate_basic_inputs(player_id, card)
        if validation_error:
            return StrategyCardSelectionResult(
                success=False,
                error_message=validation_error
            )

        if not self._strategy_phase_active:
            return StrategyCardSelectionResult(
                success=False,
                error_message="Strategy phase not started"
            )

        # Check if it's the player's turn
        current_player = self._speaker_order[self._current_selecting_player_index]
        if player_id != current_player:
            return StrategyCardSelectionResult(
                success=False,
                error_message=f"It is not your turn to select. Current player: {current_player}"
            )

        # Check if card is available
        available_cards = self.get_available_cards()
        if card not in available_cards:
            return StrategyCardSelectionResult(
                success=False,
                error_message="Strategy card is not available for selection"
            )

        # Assign the card to the player
        self._card_assignments[player_id] = card

        # Move to next player
        self._current_selecting_player_index += 1
        next_player = None
        if self._current_selecting_player_index < len(self._speaker_order):
            next_player = self._speaker_order[self._current_selecting_player_index]

        return StrategyCardSelectionResult(
            success=True,
            player_id=player_id,
            strategy_card=card,
            next_selecting_player=next_player
        )

    def is_strategy_phase_complete(self) -> bool:
        """Check if the strategy phase card selection is complete.

        Returns:
            True if all players have selected cards, False otherwise

        Requirements: 2.5 - Strategy phase completes when all players have selected cards
        """
        if not self._strategy_phase_active:
            return False

        # Phase is complete when all players in speaker order have selected cards
        return len(self._card_assignments) >= len(self._speaker_order)

    def get_player_strategy_card(self, player_id: str) -> Optional["StrategyCardType"]:
        """Get the strategy card assigned to a player.

        Args:
            player_id: The player to check

        Returns:
            The strategy card assigned to the player, or None if no card assigned

        Requirements: 2.2 - Selected cards move to player's play area
        """
        return self._card_assignments.get(player_id)
