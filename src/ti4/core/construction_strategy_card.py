"""Construction Strategy Card implementation for TI4.

This module implements the Construction strategy card following the
BaseStrategyCard pattern established for all strategy cards.

LRR Reference: Rule 83 - STRATEGY CARD (Construction)
"""

from typing import TYPE_CHECKING, Any, Optional

from .base_strategy_card import BaseStrategyCard, StrategyCardAbilityResult
from .strategic_action import StrategyCardType

if TYPE_CHECKING:
    from .game_state import GameState


class ConstructionStrategyCard(BaseStrategyCard):
    """Implementation of the Construction strategy card.

    LRR Reference: Rule 83 - The "Construction" strategy card.
    This card's initiative value is "4."
    """

    def __init__(self) -> None:
        """Initialize the Construction strategy card."""
        pass

    def get_card_type(self) -> StrategyCardType:
        """Get the strategy card type.

        Returns:
            StrategyCardType.CONSTRUCTION
        """
        return StrategyCardType.CONSTRUCTION

    def get_initiative_value(self) -> int:
        """Get the initiative value of the Construction strategy card.

        Returns:
            The initiative value (4)

        LRR Reference: Rule 83 - Construction has initiative value "4"
        """
        return 4

    def execute_primary_ability(
        self,
        player_id: str,
        game_state: Optional["GameState"] = None,
        **kwargs: Any,
    ) -> StrategyCardAbilityResult:
        """Execute the primary ability of the Construction strategy card.

        Args:
            player_id: The active player executing the primary ability
            game_state: Optional game state for full integration
            **kwargs: Additional parameters specific to the card

        Returns:
            Result of the primary ability execution

        Note: Specific Construction abilities require manual confirmation
        per manual_confirmation_protocol.md
        """
        # Placeholder implementation - specific abilities need user confirmation
        return StrategyCardAbilityResult(
            success=True,
            player_id=player_id,
            error_message="Construction primary ability implementation requires user confirmation of specific effects",
        )

    def execute_secondary_ability(
        self,
        player_id: str,
        game_state: Optional["GameState"] = None,
        **kwargs: Any,
    ) -> StrategyCardAbilityResult:
        """Execute the secondary ability of the Construction strategy card.

        Args:
            player_id: The player executing the secondary ability
            game_state: Optional game state for full integration
            **kwargs: Additional parameters specific to the card

        Returns:
            Result of the secondary ability execution

        Note: Specific Construction abilities require manual confirmation
        per manual_confirmation_protocol.md
        """
        # Placeholder implementation - specific abilities need user confirmation
        return StrategyCardAbilityResult(
            success=True,
            player_id=player_id,
            error_message="Construction secondary ability implementation requires user confirmation of specific effects",
        )
