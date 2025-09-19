"""Base strategy card implementation pattern for TI4.

This module implements the base strategy card class that follows the
TechnologyStrategyCard pattern for all 8 strategy cards.

LRR Reference: Rule 83 - STRATEGY CARD
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional

from .strategic_action import StrategyCardType

if TYPE_CHECKING:
    from .game_state import GameState


@dataclass
class StrategyCardAbilityResult:
    """Result of a strategy card ability execution."""

    success: bool
    player_id: Optional[str] = None
    resources_spent: int = 0
    command_tokens_spent: int = 0
    error_message: Optional[str] = None
    additional_data: Optional[dict[str, Any]] = None


class BaseStrategyCard(ABC):
    """Base class for all strategy card implementations.

    Follows the TechnologyStrategyCard pattern to provide a consistent
    interface for all 8 strategy cards in TI4.

    LRR Reference: Rule 83 - Strategy cards provide primary and secondary abilities
    """

    @abstractmethod
    def get_card_type(self) -> StrategyCardType:
        """Get the strategy card type.

        Returns:
            The StrategyCardType enum value for this card
        """
        pass

    @abstractmethod
    def get_initiative_value(self) -> int:
        """Get the initiative value of this strategy card.

        Returns:
            The initiative value (1-8)

        LRR Reference: Rule 83 - Each strategy card has an initiative number
        """
        pass

    @abstractmethod
    def execute_primary_ability(
        self,
        player_id: str,
        game_state: Optional["GameState"] = None,
        **kwargs: Any,
    ) -> StrategyCardAbilityResult:
        """Execute the primary ability of this strategy card.

        Args:
            player_id: The active player executing the primary ability
            game_state: Optional game state for full integration
            **kwargs: Additional parameters specific to the card

        Returns:
            Result of the primary ability execution

        LRR Reference: Rule 83 - The active player can use the primary ability
        """
        pass

    @abstractmethod
    def execute_secondary_ability(
        self,
        player_id: str,
        game_state: Optional["GameState"] = None,
        **kwargs: Any,
    ) -> StrategyCardAbilityResult:
        """Execute the secondary ability of this strategy card.

        Args:
            player_id: The player executing the secondary ability
            game_state: Optional game state for full integration
            **kwargs: Additional parameters specific to the card

        Returns:
            Result of the secondary ability execution

        LRR Reference: Rule 83 - Other players can use the secondary ability
        """
        pass

    def get_name(self) -> str:
        """Get the string name of the strategy card.

        Returns:
            The string name of the card
        """
        return self.get_card_type().value

    def validate_primary_ability_usage(
        self, player_id: str, game_state: Optional["GameState"] = None
    ) -> bool:
        """Validate if a player can use the primary ability.

        Args:
            player_id: The player attempting to use the primary ability
            game_state: Optional game state for validation

        Returns:
            True if the player can use the primary ability

        LRR Reference: Rule 83 - Only the card owner can use primary abilities
        """
        # Basic validation - concrete implementations can override
        return True

    def validate_secondary_ability_usage(
        self, player_id: str, game_state: Optional["GameState"] = None
    ) -> bool:
        """Validate if a player can use the secondary ability.

        Args:
            player_id: The player attempting to use the secondary ability
            game_state: Optional game state for validation

        Returns:
            True if the player can use the secondary ability

        LRR Reference: Rule 83 - Other players can use secondary abilities
        """
        # Basic validation - concrete implementations can override
        return True

    def _validate_resources(self, available: int, required: int) -> bool:
        """Validate if player has sufficient resources.

        Args:
            available: Resources available to the player
            required: Resources required for the action

        Returns:
            True if player has sufficient resources
        """
        return available >= required

    def _validate_command_tokens(self, available: int, required: int) -> bool:
        """Validate if player has sufficient command tokens.

        Args:
            available: Command tokens available to the player
            required: Command tokens required for the action

        Returns:
            True if player has sufficient command tokens
        """
        return available >= required
