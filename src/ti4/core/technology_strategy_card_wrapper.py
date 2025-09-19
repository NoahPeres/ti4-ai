"""Technology Strategy Card wrapper for BaseStrategyCard compatibility.

This module wraps the existing TechnologyStrategyCard to make it compatible
with the BaseStrategyCard pattern while preserving existing functionality.

LRR Reference: Rule 91 - TECHNOLOGY (STRATEGY CARD)
"""

from typing import TYPE_CHECKING, Any, Optional

from .base_strategy_card import BaseStrategyCard, StrategyCardAbilityResult
from .strategic_action import StrategyCardType
from .technology_strategy_card import (
    TechnologyStrategyCard as OriginalTechnologyStrategyCard,
)

if TYPE_CHECKING:
    from .game_state import GameState


class TechnologyStrategyCard(BaseStrategyCard):
    """Wrapper for the existing TechnologyStrategyCard to follow BaseStrategyCard pattern.

    This maintains compatibility with existing Rule 91 implementation while
    providing the BaseStrategyCard interface.

    LRR Reference: Rule 91 - The "Technology" strategy card.
    This card's initiative value is "7."
    """

    def __init__(self) -> None:
        """Initialize the Technology strategy card wrapper."""
        self._original_card = OriginalTechnologyStrategyCard()

    def get_card_type(self) -> StrategyCardType:
        """Get the strategy card type.

        Returns:
            StrategyCardType.TECHNOLOGY
        """
        return StrategyCardType.TECHNOLOGY

    def get_initiative_value(self) -> int:
        """Get the initiative value of the Technology strategy card.

        Returns:
            The initiative value (7)

        LRR Reference: Rule 91.0 - This card's initiative value is "7"
        """
        return self._original_card.get_initiative_value()

    def execute_primary_ability(
        self,
        player_id: str,
        game_state: Optional["GameState"] = None,
        **kwargs: Any,
    ) -> StrategyCardAbilityResult:
        """Execute the primary ability of the Technology strategy card.

        Args:
            player_id: The active player executing the primary ability
            game_state: Optional game state for full integration
            **kwargs: Additional parameters specific to the card

        Returns:
            Result of the primary ability execution

        LRR Reference: Rule 91.2 - The active player can research one technology
        """
        # Extract parameters for the original implementation
        technology = kwargs.get("technology")
        game_tech_manager = kwargs.get("game_tech_manager")

        if technology is None:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="Technology parameter required for primary ability",
            )

        # Use the original implementation
        result = self._original_card.execute_primary_ability(
            player_id, technology, game_tech_manager
        )

        # Convert to BaseStrategyCard result format
        return StrategyCardAbilityResult(
            success=result.success,
            player_id=player_id,
            resources_spent=result.resources_spent,
            command_tokens_spent=result.command_tokens_spent,
            error_message=result.error_message,
            additional_data={"technology_researched": result.technology_researched},
        )

    def execute_secondary_ability(
        self,
        player_id: str,
        game_state: Optional["GameState"] = None,
        **kwargs: Any,
    ) -> StrategyCardAbilityResult:
        """Execute the secondary ability of the Technology strategy card.

        Args:
            player_id: The player executing the secondary ability
            game_state: Optional game state for full integration
            **kwargs: Additional parameters specific to the card

        Returns:
            Result of the secondary ability execution

        LRR Reference: Rule 91.3 - Other players may research one technology
        """
        # Extract parameters for the original implementation
        technology = kwargs.get("technology")
        available_command_tokens = kwargs.get("available_command_tokens", 0)
        available_resources = kwargs.get("available_resources", 0)
        game_tech_manager = kwargs.get("game_tech_manager")

        if technology is None:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="Technology parameter required for secondary ability",
            )

        # Use the original implementation
        result = self._original_card.execute_secondary_ability(
            player_id,
            technology,
            available_command_tokens,
            available_resources,
            game_tech_manager,
        )

        # Convert to BaseStrategyCard result format
        return StrategyCardAbilityResult(
            success=result.success,
            player_id=player_id,
            resources_spent=result.resources_spent,
            command_tokens_spent=result.command_tokens_spent,
            error_message=result.error_message,
            additional_data={"technology_researched": result.technology_researched},
        )
