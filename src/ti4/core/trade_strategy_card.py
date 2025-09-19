"""Trade Strategy Card implementation for TI4.

This module implements the Trade strategy card following the
BaseStrategyCard pattern established for all strategy cards.

LRR Reference: Rule 83 - STRATEGY CARD (Trade)
"""

from typing import TYPE_CHECKING, Any, Optional

from .base_strategy_card import BaseStrategyCard, StrategyCardAbilityResult
from .strategic_action import StrategyCardType

if TYPE_CHECKING:
    from .game_state import GameState


class TradeStrategyCard(BaseStrategyCard):
    """Implementation of the Trade strategy card.

    LRR Reference: Rule 83 - The "Trade" strategy card.
    This card's initiative value is "5."
    """

    def __init__(self) -> None:
        """Initialize the Trade strategy card."""
        pass

    def get_card_type(self) -> StrategyCardType:
        """Get the strategy card type.

        Returns:
            StrategyCardType.TRADE
        """
        return StrategyCardType.TRADE

    def get_initiative_value(self) -> int:
        """Get the initiative value of the Trade strategy card.

        Returns:
            The initiative value (5)

        LRR Reference: Rule 83 - Trade has initiative value "5"
        """
        return 5

    def execute_primary_ability(
        self,
        player_id: str,
        game_state: Optional["GameState"] = None,
        **kwargs: Any,
    ) -> StrategyCardAbilityResult:
        """Execute the primary ability of the Trade strategy card.

        Args:
            player_id: The active player executing the primary ability
            game_state: Optional game state for full integration
            **kwargs: Additional parameters specific to the card

        Returns:
            Result of the primary ability execution

        Note: Specific Trade abilities require manual confirmation
        per manual_confirmation_protocol.md
        """
        # Placeholder implementation - specific abilities need user confirmation
        return StrategyCardAbilityResult(
            success=True,
            player_id=player_id,
            error_message="Trade primary ability implementation requires user confirmation of specific effects",
        )

    def execute_secondary_ability(
        self,
        player_id: str,
        game_state: Optional["GameState"] = None,
        **kwargs: Any,
    ) -> StrategyCardAbilityResult:
        """Execute the secondary ability of the Trade strategy card.

        Args:
            player_id: The player executing the secondary ability
            game_state: Optional game state for full integration
            **kwargs: Additional parameters specific to the card

        Returns:
            Result of the secondary ability execution

        Note: Specific Trade abilities require manual confirmation
        per manual_confirmation_protocol.md
        """
        # Placeholder implementation - specific abilities need user confirmation
        return StrategyCardAbilityResult(
            success=True,
            player_id=player_id,
            error_message="Trade secondary ability implementation requires user confirmation of specific effects",
        )
