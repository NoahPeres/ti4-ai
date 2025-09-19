"""Strategy card coordinator for Rule 83: STRATEGY CARD system.

This module implements the lightweight coordinator that integrates with existing systems
to provide strategy card assignment, tracking, and initiative order calculation.
"""

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..game_phase import GamePhase
    from .strategic_action import StrategicActionManager, StrategyCardType
else:
    StrategicActionManager = "StrategicActionManager"
    StrategyCardType = "StrategyCardType"
    GamePhase = "GamePhase"


@dataclass
class StrategyCardInformation:
    """Comprehensive information about a strategy card for AI decision-making.

    Requirements: 8.1, 8.4 - Provides card names, initiative numbers, current owners,
    and comprehensive card information.
    """

    card_type: "StrategyCardType"
    name: str
    initiative_number: int
    current_owner: Optional[str] = None
    is_exhausted: bool = False


@dataclass
class StrategyCardGameStateAnalysis:
    """Analysis of the current strategy card game state for AI strategic planning.

    Requirements: 8.5 - Strategy card assignments are clearly accessible for game state analysis.
    """

    total_assigned_cards: int
    total_available_cards: int
    initiative_order: list[str]
    lowest_initiative_player: Optional[str] = None
    highest_initiative_player: Optional[str] = None


@dataclass
class StrategyCardEvaluationData:
    """Evaluation data for a strategy card to support AI decision-making.

    Requirements: 8.2, 8.4 - AI has access to card properties and comprehensive information.
    """

    card_type: "StrategyCardType"
    initiative_number: int
    is_available: bool
    strategic_value: float  # Relative strategic value (0.0 to 1.0)
    synergy_potential: float  # Potential for synergies (0.0 to 1.0)


@dataclass
class InitiativeOrderAnalysis:
    """Analysis of initiative order implications for AI strategic planning.

    Requirements: 8.3, 8.5 - AI knows player selections and can analyze game state.
    """

    initiative_order: list[str]
    first_player: Optional[str] = None
    last_player: Optional[str] = None
    turn_advantages: Optional[list[str]] = None

    def __post_init__(self) -> None:
        """Initialize turn_advantages if None."""
        if self.turn_advantages is None:
            self.turn_advantages = []


@dataclass
class SecondaryAbilityOpportunity:
    """Information about secondary ability opportunities for AI evaluation.

    Requirements: 8.2, 8.4 - AI has access to comprehensive card information.
    """

    card_type: "StrategyCardType"
    owner: str
    can_use: bool


# Strategy card initiative numbers according to TI4 rules
STRATEGY_CARD_INITIATIVE_NUMBERS = {
    "leadership": 1,
    "diplomacy": 2,
    "politics": 3,
    "construction": 4,
    "trade": 5,
    "warfare": 6,
    "technology": 7,
    "imperial": 8,
}

# Multi-player game constants (Requirements 7.2)
MIN_PLAYER_COUNT = 3
MAX_PLAYER_COUNT = 8
TOTAL_STRATEGY_CARDS = 8  # Total number of strategy cards in TI4


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

        # Game phase integration
        self._current_game_phase: Optional[GamePhase] = None

        # Strategy card state tracking (Requirements 4.1-4.5)
        self._player_card_states: dict[str, dict[StrategyCardType, bool]] = {}

        # Secondary ability participation tracking (Requirements 5.5)
        self._secondary_ability_participants: dict[StrategyCardType, list[str]] = {}

        # Logging integration (Requirements 9.4)
        self._logger = logging.getLogger(f"{__name__}.StrategyCardCoordinator")

    def assign_strategy_card(
        self, player_id: str, card: "StrategyCardType"
    ) -> StrategyCardAssignmentResult:
        """Assign a strategy card to a player.

        Args:
            player_id: The player to assign the card to
            card: The strategy card to assign

        Returns:
            StrategyCardAssignmentResult indicating success or failure
        """
        # Enhanced input validation
        validation_error = self._validate_basic_inputs(player_id, card)
        if validation_error:
            return StrategyCardAssignmentResult(
                success=False, error_message=validation_error
            )

        # Check if card is already assigned to another player
        for existing_player, existing_card in self._card_assignments.items():
            if existing_card == card and existing_player != player_id:
                error_msg = f"Strategy card {card.value} is already assigned to player {existing_player}"
                self._logger.warning(
                    "Strategy card assignment failed: card already assigned",
                    extra={
                        "structured_data": {
                            "operation": "assign_strategy_card",
                            "requested_player": player_id,
                            "requested_card": card.value,
                            "current_owner": existing_player,
                            "error": "card_already_assigned",
                        }
                    },
                )
                return StrategyCardAssignmentResult(
                    success=False, error_message=error_msg
                )

        # Track the assignment
        self._card_assignments[player_id] = card

        # Initialize card state as readied (Requirement 4.1)
        if player_id not in self._player_card_states:
            self._player_card_states[player_id] = {}
        self._player_card_states[player_id][card] = (
            True  # True = readied, False = exhausted
        )

        return StrategyCardAssignmentResult(
            success=True, player_id=player_id, strategy_card=card
        )

    def calculate_initiative_order(
        self, player_assignments: dict[str, "StrategyCardType"]
    ) -> list[str]:
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

            card_name = card.value if hasattr(card, "value") else str(card)
            initiative_num = STRATEGY_CARD_INITIATIVE_NUMBERS.get(
                card_name, 999
            )  # Default high number for unknown cards
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

    def _validate_basic_inputs(
        self, player_id: str, card: Optional["StrategyCardType"]
    ) -> Optional[str]:
        """Validate basic inputs for card operations.

        Args:
            player_id: The player ID to validate
            card: The strategy card to validate

        Returns:
            Error message if validation fails, None if valid
        """
        # Enhanced player ID validation
        if player_id is None:
            return "Player ID cannot be None"

        if not isinstance(player_id, str):
            return "Player ID must be a string"

        if not player_id.strip():
            return "Player ID cannot be empty"

        if card is None:
            return "Strategy card cannot be None"

        return None

    def start_strategy_phase_selection(
        self, speaker_order: list[str]
    ) -> StrategyPhaseSelectionResult:
        """Start the strategy phase card selection workflow.

        Args:
            speaker_order: List of player IDs in speaker order

        Returns:
            StrategyPhaseSelectionResult indicating success or failure

        Requirements: 2.1 - Players can select cards in speaker order during strategy phase
        Requirements: 7.2 - System handles any number of players from 3-8
        Requirements: 9.1 - Comprehensive input validation
        """
        # Validate speaker order
        validation_error = self._validate_speaker_order(speaker_order)
        if validation_error:
            return StrategyPhaseSelectionResult(
                success=False, error_message=validation_error
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
            available_cards=all_cards,
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

    def select_strategy_card(
        self, player_id: str, card: "StrategyCardType"
    ) -> StrategyCardSelectionResult:
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
                success=False, error_message=validation_error
            )

        if not self._strategy_phase_active:
            return StrategyCardSelectionResult(
                success=False,
                error_message="Strategy phase not started. Please start strategy phase selection first using start_strategy_phase_selection()",
            )

        # Check if it's the player's turn
        current_player = self._speaker_order[self._current_selecting_player_index]
        if player_id != current_player:
            return StrategyCardSelectionResult(
                success=False,
                error_message=f"It is not your turn to select. Current player: {current_player}",
            )

        # Check if card is available
        available_cards = self.get_available_cards()
        if card not in available_cards:
            return StrategyCardSelectionResult(
                success=False,
                error_message="Strategy card is not available for selection",
            )

        # Assign the card to the player
        self._card_assignments[player_id] = card

        # Initialize card state as readied (Requirement 4.1)
        if player_id not in self._player_card_states:
            self._player_card_states[player_id] = {}
        self._player_card_states[player_id][card] = (
            True  # True = readied, False = exhausted
        )

        # Move to next player
        self._current_selecting_player_index += 1
        next_player = None
        if self._current_selecting_player_index < len(self._speaker_order):
            next_player = self._speaker_order[self._current_selecting_player_index]

        return StrategyCardSelectionResult(
            success=True,
            player_id=player_id,
            strategy_card=card,
            next_selecting_player=next_player,
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

    def get_action_phase_initiative_order(self) -> list[str]:
        """Get initiative order for action phase.

        Returns player IDs in initiative order based on their strategy card numbers.
        This method provides the initiative order specifically for action phase use.

        Returns:
            List of player IDs in initiative order (lowest to highest)

        Requirements: 3.3, 3.5 - Initiative order returns player IDs in correct sequence,
        calculated from current card assignments
        """
        return self._get_current_initiative_order()

    def get_status_phase_initiative_order(self) -> list[str]:
        """Get initiative order for status phase.

        Returns player IDs in initiative order based on their strategy card numbers.
        This method provides the initiative order specifically for status phase use.

        Returns:
            List of player IDs in initiative order (lowest to highest)

        Requirements: 3.3, 3.5 - Initiative order returns player IDs in correct sequence,
        calculated from current card assignments
        """
        return self._get_current_initiative_order()

    def _get_current_initiative_order(self) -> list[str]:
        """Get current initiative order based on card assignments.

        This helper method reduces code duplication between phase-specific methods.
        The separate public methods maintain semantic clarity - in the future,
        different phases might require different initiative order logic.

        Returns:
            List of player IDs in initiative order (lowest to highest)
        """
        return self.calculate_initiative_order(self._card_assignments)

    def set_current_game_phase(self, phase: "GamePhase") -> None:
        """Set the current game phase for integration with game phase management.

        Args:
            phase: The current game phase

        Requirements: Integration with existing game phase management system
        """
        self._current_game_phase = phase

    def get_current_game_phase(self) -> Optional["GamePhase"]:
        """Get the current game phase.

        Returns:
            The current game phase, or None if not set

        Requirements: Integration with existing game phase management system
        """
        return self._current_game_phase

    # Strategy Card State Management Methods (Requirements 4.1-4.5)

    def _has_assigned_card(self, player_id: str, card: "StrategyCardType") -> bool:
        """Check if a player has a specific strategy card assigned and tracked.

        Args:
            player_id: The player to check
            card: The strategy card to check

        Returns:
            True if the player has the card assigned and tracked, False otherwise
        """
        if not player_id or card is None:
            return False
        return (
            player_id in self._player_card_states
            and card in self._player_card_states[player_id]
        )

    def is_strategy_card_readied(
        self, player_id: str, card: "StrategyCardType"
    ) -> bool:
        """Check if a strategy card is in readied state.

        Args:
            player_id: The player whose card to check
            card: The strategy card to check

        Returns:
            True if the card is readied, False otherwise

        Requirements: 4.5 - System accurately reports readied/exhausted status
        """
        if not self._has_assigned_card(player_id, card):
            return False
        return self._player_card_states[player_id][card]

    def is_strategy_card_exhausted(
        self, player_id: str, card: "StrategyCardType"
    ) -> bool:
        """Check if a strategy card is in exhausted state.

        Args:
            player_id: The player whose card to check
            card: The strategy card to check

        Returns:
            True if the card is exhausted, False otherwise

        Requirements: 4.5 - System accurately reports readied/exhausted status
        """
        if not self._has_assigned_card(player_id, card):
            return False
        return not self._player_card_states[player_id][card]

    def exhaust_strategy_card(self, player_id: str, card: "StrategyCardType") -> None:
        """Exhaust a strategy card (mark as used).

        Args:
            player_id: The player whose card to exhaust
            card: The strategy card to exhaust

        Requirements: 4.2 - Strategic actions cause strategy cards to become exhausted
        """
        if self._has_assigned_card(player_id, card):
            self._player_card_states[player_id][card] = False  # False = exhausted

    def ready_strategy_card(self, player_id: str, card: "StrategyCardType") -> None:
        """Ready a strategy card (mark as available for use).

        Args:
            player_id: The player whose card to ready
            card: The strategy card to ready

        Requirements: 4.4 - Status phase readies all strategy cards for next round
        """
        if self._has_assigned_card(player_id, card):
            self._player_card_states[player_id][card] = True  # True = readied

    def ready_all_strategy_cards(self) -> None:
        """Ready all strategy cards for the next round.

        Requirements: 4.4 - Status phase readies all strategy cards for next round
        """
        for player_id in self._player_card_states:
            for card in self._player_card_states[player_id]:
                self._player_card_states[player_id][card] = True  # True = readied

    def can_use_primary_ability(self, player_id: str, card: "StrategyCardType") -> bool:
        """Check if a player can use the primary ability of their strategy card.

        Args:
            player_id: The player to check
            card: The strategy card to check

        Returns:
            True if the player can use the primary ability, False otherwise

        Requirements: 4.3 - Exhausted cards cannot use primary abilities again this round
        """
        # Input validation
        if not player_id or card is None:
            return False

        # Must have the card assigned
        if player_id not in self._card_assignments:
            return False
        if self._card_assignments[player_id] != card:
            return False

        # Card must be readied (not exhausted)
        return self.is_strategy_card_readied(player_id, card)

    # Secondary Ability Framework Methods (Requirements 5.1-5.5)

    def can_use_secondary_ability(
        self, player_id: str, card: "StrategyCardType"
    ) -> bool:
        """Check if a player can use the secondary ability of a strategy card.

        Args:
            player_id: The player to check
            card: The strategy card to check

        Returns:
            True if the player can use the secondary ability, False otherwise

        Requirements: 5.2 - Other players can only access secondary abilities
        Requirements: 5.3 - System rejects attempts to use primary ability of another player's card
        """
        # Input validation
        validation_error = self._validate_basic_inputs(player_id, card)
        if validation_error:
            return False

        # Player cannot use secondary ability of their own card
        if (
            player_id in self._card_assignments
            and self._card_assignments[player_id] == card
        ):
            return False

        # Card must be assigned to someone (available for secondary use)
        if card not in self._card_assignments.values():
            return False

        return True

    def use_secondary_ability(self, player_id: str, card: "StrategyCardType") -> bool:
        """Use a secondary ability and track participation.

        Args:
            player_id: The player using the secondary ability
            card: The strategy card whose secondary ability to use

        Returns:
            True if successful, False otherwise

        Requirements: 5.5 - System tracks which players have participated in ability resolution
        """
        # Validate secondary ability usage
        if not self.can_use_secondary_ability(player_id, card):
            return False

        # Initialize and track participation
        self._ensure_participation_tracking_initialized(card)
        self._add_participant_if_not_exists(player_id, card)

        return True

    def _ensure_participation_tracking_initialized(
        self, card: "StrategyCardType"
    ) -> None:
        """Ensure participation tracking is initialized for a card.

        Args:
            card: The strategy card to initialize tracking for
        """
        if card not in self._secondary_ability_participants:
            self._secondary_ability_participants[card] = []

    def _add_participant_if_not_exists(
        self, player_id: str, card: "StrategyCardType"
    ) -> None:
        """Add a participant to the tracking list if not already present.

        Args:
            player_id: The player to add
            card: The strategy card to add participation for
        """
        if player_id not in self._secondary_ability_participants[card]:
            self._secondary_ability_participants[card].append(player_id)

    def get_secondary_ability_participants(self, card: "StrategyCardType") -> list[str]:
        """Get list of players who have participated in secondary ability for a card.

        Args:
            card: The strategy card to check

        Returns:
            List of player IDs who have used the secondary ability

        Requirements: 5.5 - System tracks which players have participated in ability resolution
        """
        return self._secondary_ability_participants.get(card, [])

    # Multi-Player Game Support Methods (Requirements 7.1-7.5)

    def _validate_speaker_order(self, speaker_order: list[str]) -> Optional[str]:
        """Validate speaker order for multi-player game support.

        Args:
            speaker_order: List of player IDs in speaker order

        Returns:
            Error message if validation fails, None if valid

        Requirements: 7.2, 9.1 - Player count validation, comprehensive input validation
        """
        # Check for empty speaker order
        if not speaker_order:
            return "Speaker order cannot be empty"

        # Validate player count bounds
        player_count_error = self._validate_player_count_bounds(len(speaker_order))
        if player_count_error:
            return player_count_error

        # Validate for duplicate player IDs
        duplicate_error = self._validate_no_duplicate_players(speaker_order)
        if duplicate_error:
            return duplicate_error

        # Validate individual player IDs
        player_id_error = self._validate_player_ids(speaker_order)
        if player_id_error:
            return player_id_error

        return None

    def _validate_player_count_bounds(self, player_count: int) -> Optional[str]:
        """Validate that player count is within acceptable bounds.

        Args:
            player_count: Number of players to validate

        Returns:
            Error message if invalid, None if valid
        """
        if player_count < MIN_PLAYER_COUNT:
            return f"Minimum {MIN_PLAYER_COUNT} players required, got {player_count}"

        if player_count > MAX_PLAYER_COUNT:
            return f"Maximum {MAX_PLAYER_COUNT} players allowed, got {player_count}"

        return None

    def _validate_no_duplicate_players(self, speaker_order: list[str]) -> Optional[str]:
        """Validate that there are no duplicate player IDs in speaker order.

        Args:
            speaker_order: List of player IDs to validate

        Returns:
            Error message if duplicates found, None if valid
        """
        if len(set(speaker_order)) != len(speaker_order):
            return "Duplicate player IDs are not allowed in speaker order"
        return None

    def _validate_player_ids(self, speaker_order: list[str]) -> Optional[str]:
        """Validate that all player IDs are valid.

        Args:
            speaker_order: List of player IDs to validate

        Returns:
            Error message if any invalid player ID found, None if all valid
        """
        for player_id in speaker_order:
            if player_id is None:
                return "Player ID cannot be None"
            if not isinstance(player_id, str) or not player_id.strip():
                return "Player ID cannot be empty or invalid"
        return None

    def get_player_count(self) -> int:
        """Get the current number of players in the game.

        Returns:
            Number of players in current speaker order

        Requirements: 7.4 - System adapts card availability based on player count
        """
        return len(self._speaker_order)

    def get_expected_unselected_cards_count(self) -> int:
        """Get the expected number of unselected cards based on player count.

        Returns:
            Number of cards that will remain unselected

        Requirements: 7.1 - Games with fewer than 8 players leave some strategy cards unselected
        """
        return max(0, TOTAL_STRATEGY_CARDS - self.get_player_count())

    def get_speaker_order(self) -> list[str]:
        """Get the current speaker order.

        Returns:
            List of player IDs in speaker order

        Requirements: 7.3 - System supports flexible player ordering
        """
        return self._speaker_order.copy()

    def get_current_selecting_player(self) -> Optional[str]:
        """Get the player who is currently selecting a strategy card.

        Returns:
            Player ID of current selecting player, or None if phase not active

        Requirements: 7.3 - System supports flexible player ordering
        """
        if (
            not self._strategy_phase_active
            or self._current_selecting_player_index >= len(self._speaker_order)
        ):
            return None
        return self._speaker_order[self._current_selecting_player_index]

    def reset_strategy_phase(self) -> None:
        """Reset the strategy phase for a new game.

        Requirements: 7.4 - System adapts card availability based on player count changes
        """
        self._strategy_phase_active = False
        self._speaker_order = []
        self._current_selecting_player_index = 0
        self._card_assignments = {}
        self._exhausted_cards = set()
        self._player_card_states = {}
        self._secondary_ability_participants = {}

    def reset_round(self) -> None:
        """Reset strategy cards for a new round.

        Returns all strategy cards to the common play area and clears player assignments.

        Requirements: 10.1 - When a new round begins, all strategy cards SHALL be returned to the common play area
        """
        # Clear all card assignments - returns cards to common play area
        self._card_assignments = {}

        # Clear all card states
        self._player_card_states = {}

        # Clear secondary ability participation tracking
        self._secondary_ability_participants = {}

        # Reset strategy phase state but preserve speaker order for next round
        self._strategy_phase_active = False
        self._current_selecting_player_index = 0

    def is_valid_player_count(self, player_count: int) -> bool:
        """Check if a player count is valid for TI4.

        Args:
            player_count: Number of players to validate

        Returns:
            True if valid player count, False otherwise

        Requirements: 7.2 - System handles any number of players from 3-8
        """
        return MIN_PLAYER_COUNT <= player_count <= MAX_PLAYER_COUNT

    def get_minimum_player_count(self) -> int:
        """Get the minimum number of players for TI4.

        Returns:
            Minimum player count (3)

        Requirements: 7.2 - System handles any number of players from 3-8
        """
        return MIN_PLAYER_COUNT

    def get_maximum_player_count(self) -> int:
        """Get the maximum number of players for TI4.

        Returns:
            Maximum player count (8)

        Requirements: 7.2 - System handles any number of players from 3-8
        """
        return MAX_PLAYER_COUNT

    # AI Information Access Methods (Requirements 8.1-8.5)

    def get_strategy_card_information(
        self, card: "StrategyCardType"
    ) -> StrategyCardInformation:
        """Get comprehensive information about a specific strategy card for AI decision-making.

        Args:
            card: The strategy card to get information about

        Returns:
            StrategyCardInformation with comprehensive card details

        Requirements: 8.1 - System provides card names, initiative numbers, and current owners
        Requirements: 8.4 - System provides comprehensive card information
        """
        if card is None:
            raise ValueError("Strategy card cannot be None")

        # Get card name and initiative number
        card_name = card.value if hasattr(card, "value") else str(card)
        initiative_number = STRATEGY_CARD_INITIATIVE_NUMBERS.get(card_name, 999)

        # Find current owner
        current_owner = None
        for player_id, assigned_card in self._card_assignments.items():
            if assigned_card == card:
                current_owner = player_id
                break

        # Check if card is exhausted
        is_exhausted = False
        if current_owner and current_owner in self._player_card_states:
            is_exhausted = not self._player_card_states[current_owner].get(
                card, True
            )  # True = readied, False = exhausted

        return StrategyCardInformation(
            card_type=card,
            name=card_name,
            initiative_number=initiative_number,
            current_owner=current_owner,
            is_exhausted=is_exhausted,
        )

    def get_all_strategy_cards_information(self) -> list[StrategyCardInformation]:
        """Get information about all strategy cards for AI evaluation.

        Returns:
            List of StrategyCardInformation for all 8 strategy cards

        Requirements: 8.2 - AI has access to all available cards and their properties
        """
        StrategyCardType = self._get_strategy_card_type_enum()
        all_cards = list(StrategyCardType)

        return [self.get_strategy_card_information(card) for card in all_cards]

    def get_player_strategy_card_assignments(self) -> dict[str, "StrategyCardType"]:
        """Get all player strategy card assignments for AI strategic planning.

        Returns:
            Dictionary mapping player IDs to their assigned strategy cards

        Requirements: 8.3 - AI knows which cards other players have selected
        """
        return self._card_assignments.copy()

    def get_available_cards_for_ai(self) -> list[StrategyCardInformation]:
        """Get information about available cards for AI selection evaluation.

        Returns:
            List of StrategyCardInformation for available cards

        Requirements: 8.2 - AI has access to all available cards and their properties
        """
        available_cards = self.get_available_cards()
        return [self.get_strategy_card_information(card) for card in available_cards]

    def analyze_strategy_card_game_state(self) -> StrategyCardGameStateAnalysis:
        """Analyze the current strategy card game state for AI strategic planning.

        Returns:
            StrategyCardGameStateAnalysis with strategic insights

        Requirements: 8.5 - Strategy card assignments are clearly accessible for game state analysis
        """
        total_assigned = len(self._card_assignments)
        total_available = len(self.get_available_cards())
        initiative_order = self._get_current_initiative_order()

        lowest_initiative_player = initiative_order[0] if initiative_order else None
        highest_initiative_player = initiative_order[-1] if initiative_order else None

        return StrategyCardGameStateAnalysis(
            total_assigned_cards=total_assigned,
            total_available_cards=total_available,
            initiative_order=initiative_order,
            lowest_initiative_player=lowest_initiative_player,
            highest_initiative_player=highest_initiative_player,
        )

    def get_strategy_card_evaluation_data(
        self, card: "StrategyCardType"
    ) -> StrategyCardEvaluationData:
        """Get evaluation data for a strategy card to support AI decision-making.

        Args:
            card: The strategy card to evaluate

        Returns:
            StrategyCardEvaluationData with strategic assessment

        Requirements: 8.2, 8.4 - AI has access to card properties and comprehensive information
        """
        if card is None:
            raise ValueError("Strategy card cannot be None")

        card_name = card.value if hasattr(card, "value") else str(card)
        initiative_number = STRATEGY_CARD_INITIATIVE_NUMBERS.get(card_name, 999)
        is_available = card in self.get_available_cards()

        # Calculate strategic value based on initiative number (lower = higher value)
        strategic_value = 1.0 - (initiative_number - 1) / 7.0  # Normalize to 0.0-1.0

        # Calculate synergy potential (simplified heuristic)
        synergy_potential = 0.5  # Default moderate synergy potential

        return StrategyCardEvaluationData(
            card_type=card,
            initiative_number=initiative_number,
            is_available=is_available,
            strategic_value=strategic_value,
            synergy_potential=synergy_potential,
        )

    def get_initiative_order_analysis(self) -> InitiativeOrderAnalysis:
        """Get analysis of initiative order implications for AI strategic planning.

        Returns:
            InitiativeOrderAnalysis with initiative insights

        Requirements: 8.3, 8.5 - AI knows player selections and can analyze game state
        """
        initiative_order = self._get_current_initiative_order()
        first_player = initiative_order[0] if initiative_order else None
        last_player = initiative_order[-1] if initiative_order else None

        # Generate turn advantages (simplified analysis)
        turn_advantages = []
        for i, player in enumerate(initiative_order):
            if i == 0:
                turn_advantages.append(f"{player}: First player advantage")
            elif i == len(initiative_order) - 1:
                turn_advantages.append(f"{player}: Last player flexibility")
            else:
                turn_advantages.append(f"{player}: Mid-order positioning")

        return InitiativeOrderAnalysis(
            initiative_order=initiative_order,
            first_player=first_player,
            last_player=last_player,
            turn_advantages=turn_advantages,
        )

    def get_secondary_ability_opportunities(
        self, player_id: str
    ) -> list[SecondaryAbilityOpportunity]:
        """Get secondary ability opportunities for a player.

        Args:
            player_id: The player to evaluate opportunities for

        Returns:
            List of SecondaryAbilityOpportunity objects

        Requirements: 8.2, 8.4 - AI has access to comprehensive card information
        """
        if not player_id:
            return []

        opportunities = []
        for owner, card in self._card_assignments.items():
            if (
                owner != player_id
            ):  # Can only use secondary abilities of other players' cards
                can_use = self.can_use_secondary_ability(player_id, card)
                opportunities.append(
                    SecondaryAbilityOpportunity(
                        card_type=card, owner=owner, can_use=can_use
                    )
                )

        return opportunities

    # Error Handling and Validation Methods (Requirements 9.1-9.5)

    def validate_system_state(self) -> None:
        """Validate the current system state for consistency.

        Requirements: 9.3 - System detects and reports state inconsistencies

        Raises:
            StrategyCardStateError: If state inconsistencies are detected
        """
        from ..exceptions import StrategyCardStateError

        # Check for orphaned card states (cards in state tracking but not assigned)
        for player_id, card_states in self._player_card_states.items():
            for card in card_states:
                if (
                    player_id not in self._card_assignments
                    or self._card_assignments[player_id] != card
                ):
                    error_msg = f"State inconsistency detected: Player {player_id} has state for card {card.value} but card is not assigned"
                    self._logger.error(
                        "Strategy card state inconsistency detected",
                        extra={
                            "structured_data": {
                                "operation": "validate_system_state",
                                "inconsistency_type": "orphaned_card_state",
                                "player_id": player_id,
                                "card": card.value,
                                "error": "state_inconsistency",
                            }
                        },
                    )
                    raise StrategyCardStateError(
                        error_msg, context={"player_id": player_id, "card": card.value}
                    )

        # Check for assigned cards without state tracking
        for player_id, card in self._card_assignments.items():
            if (
                player_id not in self._player_card_states
                or card not in self._player_card_states[player_id]
            ):
                raise StrategyCardStateError(
                    f"State inconsistency detected: Player {player_id} has card {card.value} assigned but no state tracking",
                    context={"player_id": player_id, "card": card.value},
                )

        # Check for duplicate card assignments
        assigned_cards = list(self._card_assignments.values())
        if len(assigned_cards) != len(set(assigned_cards)):
            duplicates = [
                card for card in assigned_cards if assigned_cards.count(card) > 1
            ]
            raise StrategyCardStateError(
                f"State inconsistency detected: Duplicate card assignments found: {[card.value for card in set(duplicates)]}",
                context={"duplicate_cards": [card.value for card in set(duplicates)]},
            )
