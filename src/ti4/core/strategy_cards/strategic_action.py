"""Strategic action system for TI4 strategy card activation.

This module implements Rule 82: STRATEGIC ACTION mechanics according to the TI4 LRR.
Handles strategy card activation, primary/secondary ability resolution, and turn continuation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .coordinator import StrategyCardCoordinator


class StrategyCardType(Enum):
    """Enumeration of all strategy cards in TI4.

    Provides type safety and validation for strategy card names.
    """

    LEADERSHIP = "leadership"
    DIPLOMACY = "diplomacy"
    POLITICS = "politics"
    CONSTRUCTION = "construction"
    TRADE = "trade"
    WARFARE = "warfare"
    TECHNOLOGY = "technology"
    IMPERIAL = "imperial"


@dataclass
class StrategyCard:
    """Represents a strategy card with primary and secondary abilities.

    Contains the card's name and ability descriptions.
    """

    card_type: StrategyCardType
    primary_ability: str
    secondary_ability: str
    _exhausted: bool = field(default=False, init=False, repr=False)

    @property
    def name(self) -> str:
        """Get the string name of the strategy card."""
        return self.card_type.value

    def is_exhausted(self) -> bool:
        """Check if this strategy card is exhausted."""
        return self._exhausted

    def exhaust(self) -> None:
        """Mark this strategy card as exhausted."""
        if self._exhausted:
            raise ValueError("Strategy card is already exhausted")
        self._exhausted = True

    def ready(self) -> None:
        """Mark this strategy card as ready (not exhausted)."""
        self._exhausted = False


@dataclass
class StrategicActionResult:
    """Result of a strategic action activation."""

    success: bool
    resolving_player: str | None = None
    primary_ability_resolved: bool = False
    secondary_abilities_offered: bool = False
    secondary_ability_order: list[str] = field(default_factory=list)
    error_message: str | None = None


@dataclass
class SecondaryAbilityResult:
    """Result of a secondary ability resolution attempt."""

    success: bool
    player: str | None = None
    resolved: bool = False
    skipped: bool = False
    error_message: str | None = None


class StrategicActionManager:
    """Manages strategic actions and strategy card activation according to Rule 82.

    Handles:
    - Strategy card activation and exhaustion (Rule 82.1)
    - Primary and secondary ability resolution (Rule 82.2)
    - Turn continuation and passing requirements (Rule 82.3)
    - Component action integration (Rule 82.2b)
    """

    def __init__(self) -> None:
        """Initialize the strategic action manager."""
        # Track strategy cards assigned to each player
        self._player_strategy_cards: dict[str, dict[str, StrategyCard]] = {}

        # Track player order for secondary ability resolution
        self._player_order: list[str] = []

        # Track game state
        self._action_phase: bool = False

        # Track current strategic action state
        self._current_activation: str | None = None  # Currently activated card
        self._secondary_resolution_order: list[str] = []
        self._secondary_resolution_index: int = 0

        # Strategy card coordinator integration (Rule 83)
        self._strategy_card_coordinator: StrategyCardCoordinator | None = None

    def set_action_phase(self, action_phase: bool) -> None:
        """Set whether the game is in action phase.

        Args:
            action_phase: True if in action phase, False otherwise
        """
        self._action_phase = action_phase

    def set_player_order(self, player_order: list[str]) -> None:
        """Set the player order for secondary ability resolution.

        Args:
            player_order: List of player IDs in clockwise order
        """
        if not player_order:
            raise ValueError("Player order cannot be empty")
        self._player_order = player_order.copy()

    def assign_strategy_card(self, player_id: str, strategy_card: StrategyCard) -> None:
        """Assign a strategy card to a player.

        Args:
            player_id: The player to assign the card to
            strategy_card: The strategy card to assign

        Raises:
            ValueError: If player_id is empty or strategy_card is None
        """
        if not player_id:
            raise ValueError("Player ID cannot be empty")
        if strategy_card is None:
            raise ValueError("Strategy card cannot be None")

        if player_id not in self._player_strategy_cards:
            self._player_strategy_cards[player_id] = {}

        self._player_strategy_cards[player_id][strategy_card.name] = strategy_card

    def can_activate_strategy_card(
        self, player_id: str, card_name: str | StrategyCardType
    ) -> bool:
        """Check if a player can activate a specific strategy card.

        Args:
            player_id: The player attempting activation
            card_name: The name or type of the strategy card

        Returns:
            True if activation is allowed, False otherwise
        """
        if not player_id:
            return False

        # Convert StrategyCardType to string if needed
        card_name_str = (
            card_name.value if isinstance(card_name, StrategyCardType) else card_name
        )

        # Rule 82.1: Must be in action phase
        if not self._action_phase:
            return False

        # Check if player has the card
        if player_id not in self._player_strategy_cards:
            return False

        if card_name_str not in self._player_strategy_cards[player_id]:
            return False

        # Rule 82.1b: Cannot activate exhausted cards
        card = self._player_strategy_cards[player_id][card_name_str]
        return not card.is_exhausted()

    def activate_strategy_card(
        self, player_id: str, card_name: str | StrategyCardType
    ) -> StrategicActionResult:
        """Activate a strategy card and resolve its primary ability.

        Args:
            player_id: The player activating the card
            card_name: The name or type of the strategy card to activate

        Returns:
            StrategicActionResult indicating success or failure
        """
        # Convert StrategyCardType to string if needed
        card_name_str = (
            card_name.value if isinstance(card_name, StrategyCardType) else card_name
        )

        # Validate activation
        if not self.can_activate_strategy_card(player_id, card_name_str):
            return StrategicActionResult(
                success=False,
                error_message=f"Cannot activate strategy card '{card_name_str}' for player '{player_id}'",
            )

        # Get the strategy card
        card = self._player_strategy_cards[player_id][card_name_str]

        # Rule 82.1a: Exhaust the card after activation
        card.exhaust()

        # Rule 82.2: Resolve primary ability
        # Set up secondary ability resolution order
        secondary_order = self._get_secondary_ability_order(player_id)

        return StrategicActionResult(
            success=True,
            resolving_player=player_id,
            primary_ability_resolved=True,
            secondary_abilities_offered=True,
            secondary_ability_order=secondary_order,
        )

    def activate_strategy_card_via_component_action(
        self, player_id: str, card_name: str | StrategyCardType
    ) -> StrategicActionResult:
        """Activate a strategy card via component action.

        Args:
            player_id: The player activating the card
            card_name: The name or type of the strategy card to activate

        Returns:
            StrategicActionResult indicating success or failure
        """
        # Rule 82.2b: Secondary abilities still offered even for component actions
        result = self.activate_strategy_card(player_id, card_name)
        if result.success:
            result.secondary_abilities_offered = True
        return result

    def exhaust_strategy_card(
        self, player_id: str, card_name: str | StrategyCardType
    ) -> None:
        """Manually exhaust a strategy card.

        Args:
            player_id: The player whose card to exhaust
            card_name: The name or type of the strategy card to exhaust
        """
        # Convert StrategyCardType to string if needed
        card_name_str = (
            card_name.value if isinstance(card_name, StrategyCardType) else card_name
        )

        if (
            player_id in self._player_strategy_cards
            and card_name_str in self._player_strategy_cards[player_id]
        ):
            self._player_strategy_cards[player_id][card_name_str].exhaust()

    def is_strategy_card_exhausted(
        self, player_id: str, card_name: str | StrategyCardType
    ) -> bool:
        """Check if a strategy card is exhausted.

        Args:
            player_id: The player whose card to check
            card_name: The name or type of the strategy card

        Returns:
            True if the card is exhausted, False otherwise
        """
        # Convert StrategyCardType to string if needed
        card_name_str = (
            card_name.value if isinstance(card_name, StrategyCardType) else card_name
        )

        if (
            player_id in self._player_strategy_cards
            and card_name_str in self._player_strategy_cards[player_id]
        ):
            return self._player_strategy_cards[player_id][card_name_str].is_exhausted()
        return True  # Non-existent cards are considered "exhausted"

    def resolve_secondary_ability(
        self, player_id: str, card_name: str | StrategyCardType
    ) -> SecondaryAbilityResult:
        """Resolve a secondary ability for a player.

        Args:
            player_id: The player resolving the secondary ability
            card_name: The name or type of the strategy card

        Returns:
            SecondaryAbilityResult indicating success or failure
        """
        if not player_id:
            return SecondaryAbilityResult(
                success=False, error_message="Player ID cannot be empty"
            )

        return SecondaryAbilityResult(
            success=True, player=player_id, resolved=True, skipped=False
        )

    def skip_secondary_ability(
        self, player_id: str, card_name: str | StrategyCardType
    ) -> SecondaryAbilityResult:
        """Skip a secondary ability for a player.

        Args:
            player_id: The player skipping the secondary ability
            card_name: The name or type of the strategy card

        Returns:
            SecondaryAbilityResult indicating the skip was successful
        """
        if not player_id:
            return SecondaryAbilityResult(
                success=False, error_message="Player ID cannot be empty"
            )

        return SecondaryAbilityResult(
            success=True, player=player_id, resolved=False, skipped=True
        )

    def can_continue_turn(self, player_id: str) -> bool:
        """Check if a player can continue their turn.

        Args:
            player_id: The player to check

        Returns:
            True if the player can continue, False if they must pass
        """
        if not player_id:
            return False

        # Rule 82.3a: Can continue if they have unexhausted strategy cards
        if player_id not in self._player_strategy_cards:
            return False

        for card in self._player_strategy_cards[player_id].values():
            if not card.is_exhausted():
                return True

        return False

    def must_pass(self, player_id: str) -> bool:
        """Check if a player must pass.

        Args:
            player_id: The player to check

        Returns:
            True if the player must pass, False otherwise
        """
        # Rule 82.3b: Must pass if no strategy cards or all exhausted
        return not self.can_continue_turn(player_id)

    def _get_secondary_ability_order(self, active_player: str) -> list[str]:
        """Get the order for secondary ability resolution.

        Args:
            active_player: The player who activated the strategy card

        Returns:
            List of player IDs in clockwise order, excluding the active player
        """
        if not self._player_order or active_player not in self._player_order:
            return []

        # Find active player's position
        active_index = self._player_order.index(active_player)

        # Create clockwise order starting from the next player
        secondary_order = []
        for i in range(1, len(self._player_order)):
            next_index = (active_index + i) % len(self._player_order)
            secondary_order.append(self._player_order[next_index])

        return secondary_order

    def _convert_to_strategy_card_type(
        self, card: str | StrategyCardType
    ) -> StrategyCardType | None:
        """Convert a card name or type to StrategyCardType enum.

        Args:
            card: The card name (string) or StrategyCardType enum

        Returns:
            StrategyCardType enum if conversion successful, None otherwise
        """
        if card is None:
            return None

        try:
            return (
                card if isinstance(card, StrategyCardType) else StrategyCardType(card)
            )
        except (ValueError, AttributeError):
            return None

    def can_activate_strategy_card_via_coordinator(
        self, player_id: str, card: str | StrategyCardType
    ) -> bool:
        """Check if a player can activate a strategy card via coordinator.

        Args:
            player_id: The player attempting activation
            card: The name or type of the strategy card

        Returns:
            True if activation is allowed, False otherwise

        Requirements: 4.2, 6.2 - Integration with strategy card coordinator
        """
        # Input validation
        if not player_id or card is None:
            return False

        if self._strategy_card_coordinator is None:
            return False

        # Convert to StrategyCardType
        card_type = self._convert_to_strategy_card_type(card)
        if card_type is None:
            return False

        return self._strategy_card_coordinator.can_use_primary_ability(
            player_id, card_type
        )

    def activate_strategy_card_via_coordinator(
        self, player_id: str, card: str | StrategyCardType
    ) -> StrategicActionResult:
        """Activate a strategy card via coordinator integration.

        This method integrates with the strategy card coordinator to validate
        and execute strategic actions, ensuring proper card exhaustion.

        Args:
            player_id: The player activating the card
            card: The name or type of the strategy card to activate

        Returns:
            StrategicActionResult indicating success or failure

        Requirements: 6.3 - Card exhaustion during strategic action resolution
        """
        # Convert to StrategyCardType
        card_type = self._convert_to_strategy_card_type(card)
        if card_type is None:
            return StrategicActionResult(
                success=False,
                error_message=f"Invalid strategy card: {card}",
            )

        # Validate activation via coordinator
        if not self.can_activate_strategy_card_via_coordinator(player_id, card_type):
            return StrategicActionResult(
                success=False,
                error_message=f"Cannot activate strategy card '{card_type.value}' for player '{player_id}' via coordinator",
            )

        # Rule 82.1: Must be in action phase
        if not self._action_phase:
            return StrategicActionResult(
                success=False,
                error_message="Cannot activate strategy card outside of action phase",
            )

        # Exhaust the card via coordinator
        if self._strategy_card_coordinator is not None:
            self._strategy_card_coordinator.exhaust_strategy_card(player_id, card_type)

        # Rule 82.2: Resolve primary ability and set up secondary ability resolution
        secondary_order = self._get_secondary_ability_order(player_id)

        return StrategicActionResult(
            success=True,
            resolving_player=player_id,
            primary_ability_resolved=True,
            secondary_abilities_offered=True,
            secondary_ability_order=secondary_order,
        )

    def set_strategy_card_coordinator(
        self, coordinator: "StrategyCardCoordinator"
    ) -> None:
        """Set the strategy card coordinator for integration.

        Args:
            coordinator: The strategy card coordinator to integrate with

        Requirements: 6.1, 6.2 - Integration with strategic action system
        """
        self._strategy_card_coordinator = coordinator

    def execute_strategic_action(
        self, player_id: str, game_state: Any
    ) -> StrategicActionResult:
        """Execute a strategic action for a player.

        Args:
            player_id: The player executing the strategic action
            game_state: Current game state

        Returns:
            Result of the strategic action execution

        Requirements: 6.1 - Integration with strategic action system
        """
        # Basic validation
        if not player_id:
            return StrategicActionResult(
                success=False, error_message="Player ID cannot be empty"
            )

        # If coordinator is available, use it for validation
        if self._strategy_card_coordinator is not None:
            # Get player's strategy card
            player_card = self._strategy_card_coordinator.get_player_strategy_card(
                player_id
            )
            if player_card is None:
                return StrategicActionResult(
                    success=False,
                    error_message=f"Player {player_id} has no strategy card assigned",
                )

            # Check if card can be activated
            if not self._strategy_card_coordinator.can_use_primary_ability(
                player_id, player_card
            ):
                return StrategicActionResult(
                    success=False,
                    error_message=f"Player {player_id} cannot use primary ability of {player_card}",
                )

            # Activate via coordinator
            return self.activate_strategy_card_via_coordinator(player_id, player_card)

        # Fallback for backward compatibility
        return StrategicActionResult(
            success=False, error_message="No strategy card coordinator available"
        )
