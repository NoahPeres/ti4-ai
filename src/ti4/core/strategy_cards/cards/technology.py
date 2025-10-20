"""Technology Strategy Card implementation for TI4.

This module implements Rule 91: TECHNOLOGY (Strategy Card) mechanics.
LRR Reference: Rule 91 - TECHNOLOGY (STRATEGY CARD)
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional

from ...constants import Technology
from ..base_strategy_card import BaseStrategyCard, StrategyCardAbilityResult
from ..strategic_action import StrategyCardType

if TYPE_CHECKING:
    from ...game_state import GameState
    from ...game_technology_manager import GameTechnologyManager
    from ...technology import TechnologyManager


@dataclass
class TechnologyResearchResult:
    """Result of a technology research attempt."""

    success: bool
    technology_researched: Technology | None = None
    resources_spent: int = 0
    command_tokens_spent: int = 0
    error_message: str | None = None


class TechnologyStrategyCard(BaseStrategyCard):
    """Implementation of the Technology strategy card.

    LRR Reference: Rule 91 - The "Technology" strategy card allows players to research new technology.
    This card's initiative value is "7."
    """

    def __init__(self) -> None:
        """Initialize the Technology strategy card."""
        pass

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
        return 7

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
            **kwargs: Additional parameters (technology, game_tech_manager)

        Returns:
            Result of the primary ability execution

        LRR Reference: Rule 91.2 - The active player can research one technology
        """
        # Extract parameters from kwargs for backward compatibility
        technology = kwargs.get("technology")
        game_tech_manager = kwargs.get("game_tech_manager")

        if technology is None:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="Technology parameter is required for Technology strategy card primary ability",
            )

        # Execute the technology research
        result = self._execute_technology_research(
            player_id, technology, game_tech_manager, is_primary=True
        )

        # Convert to standard StrategyCardAbilityResult
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
            **kwargs: Additional parameters (technology, available_command_tokens, available_resources, game_tech_manager)

        Returns:
            Result of the secondary ability execution

        LRR Reference: Rule 91.3 - Other players may research one technology by spending command token and resources
        """
        # Extract parameters from kwargs
        technology = kwargs.get("technology")
        available_command_tokens = kwargs.get("available_command_tokens", 0)
        available_resources = kwargs.get("available_resources", 0)
        game_tech_manager = kwargs.get("game_tech_manager")

        if technology is None:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="Technology parameter is required for Technology strategy card secondary ability",
            )

        # Execute the secondary ability research
        result = self._execute_secondary_technology_research(
            player_id,
            technology,
            available_command_tokens,
            available_resources,
            game_tech_manager,
        )

        # Convert to standard StrategyCardAbilityResult
        return StrategyCardAbilityResult(
            success=result.success,
            player_id=player_id,
            resources_spent=result.resources_spent,
            command_tokens_spent=result.command_tokens_spent,
            error_message=result.error_message,
            additional_data={"technology_researched": result.technology_researched},
        )

    def _execute_technology_research(
        self,
        player_id: str,
        technology: Technology,
        game_tech_manager: Optional["GameTechnologyManager"] = None,
        is_primary: bool = True,
    ) -> TechnologyResearchResult:
        """Execute technology research for primary ability.

        Args:
            player_id: The active player executing the primary ability
            technology: The technology to research
            game_tech_manager: Optional game technology manager for full integration
            is_primary: Whether this is primary ability (affects cost)

        Returns:
            Result of the technology research

        LRR Reference: Rule 91.2 - The active player can research one technology of their choice
        """
        # If we have game integration, use it
        if game_tech_manager:
            # Validate the research is possible
            if not game_tech_manager.can_research_technology(player_id, technology):
                return TechnologyResearchResult(
                    success=False,
                    error_message=f"Cannot research {technology.value}: prerequisites not met or already owned",
                )

            # Execute the research through the integrated system
            success = game_tech_manager.research_technology(player_id, technology)
            if success:
                return TechnologyResearchResult(
                    success=True,
                    technology_researched=technology,
                    resources_spent=0,  # First research is free
                )
            else:
                return TechnologyResearchResult(
                    success=False,
                    error_message=f"Failed to research {technology.value}",
                )

        # Fallback for basic functionality without full integration
        return TechnologyResearchResult(
            success=True,
            technology_researched=technology,
            resources_spent=0,  # First research is free
        )

    def _execute_secondary_technology_research(
        self,
        player_id: str,
        technology: Technology,
        available_command_tokens: int,
        available_resources: int,
        game_tech_manager: Optional["GameTechnologyManager"] = None,
    ) -> TechnologyResearchResult:
        """Execute the secondary ability technology research.

        Args:
            player_id: The player executing the secondary ability
            technology: The technology to research
            available_command_tokens: Command tokens available in strategy pool
            available_resources: Resources available to the player
            game_tech_manager: Optional game technology manager for full integration

        Returns:
            Result of the technology research

        LRR Reference: Rule 91.3 - Each other player may research one technology by spending
        one command token from their strategy pool and four resources
        """
        required_command_tokens = 1
        required_resources = 4

        # Validate command token requirements
        if not self._validate_command_tokens(
            available_command_tokens, required_command_tokens
        ):
            return TechnologyResearchResult(
                success=False,
                error_message=f"Insufficient command tokens: need {required_command_tokens}, have {available_command_tokens}",
            )

        # Validate resource requirements
        if not self._validate_resources(available_resources, required_resources):
            return TechnologyResearchResult(
                success=False,
                error_message=f"Insufficient resources: need {required_resources}, have {available_resources}",
            )

        # If we have game integration, use it
        if game_tech_manager:
            # Validate the research is possible
            if not game_tech_manager.can_research_technology(player_id, technology):
                return TechnologyResearchResult(
                    success=False,
                    error_message=f"Cannot research {technology.value}: prerequisites not met or already owned",
                )

            # Execute the research through the integrated system
            success = game_tech_manager.research_technology(player_id, technology)
            if success:
                return TechnologyResearchResult(
                    success=True,
                    technology_researched=technology,
                    command_tokens_spent=required_command_tokens,
                    resources_spent=required_resources,
                )
            else:
                return TechnologyResearchResult(
                    success=False,
                    error_message=f"Failed to research {technology.value}",
                )

        # Fallback for basic functionality without full integration
        return TechnologyResearchResult(
            success=True,
            technology_researched=technology,
            command_tokens_spent=required_command_tokens,
            resources_spent=required_resources,
        )

    def validate_technology_research(
        self, player_id: str, technology: Technology, tech_manager: "TechnologyManager"
    ) -> bool:
        """Validate if a technology can be researched by the player.

        Args:
            player_id: The player attempting to research
            technology: The technology to research
            tech_manager: The technology manager for validation

        Returns:
            True if the technology can be researched

        LRR Reference: Rule 91.2/91.3 - Card allows researching technologies (subject to normal rules)
        """
        # Use existing technology research validation
        return tech_manager.can_research_technology(player_id, technology)

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

    # Backward compatibility methods for existing technology strategy card interface
    def execute_primary_ability_second_research(
        self,
        player_id: str,
        technology: Technology,
        available_resources: int,
        game_tech_manager: Optional["GameTechnologyManager"] = None,
    ) -> TechnologyResearchResult:
        """Execute the second research option of the primary ability.

        Args:
            player_id: The active player
            technology: The technology to research
            available_resources: Resources available to the player
            game_tech_manager: Optional game technology manager for full integration

        Returns:
            Result of the technology research

        LRR Reference: Rule 91.2 - Then may research one additional technology by spending six resources
        """
        required_resources = 6

        # Validate resource requirements
        if not self._validate_resources(available_resources, required_resources):
            return TechnologyResearchResult(
                success=False,
                error_message=f"Insufficient resources: need {required_resources}, have {available_resources}",
            )

        # If we have game integration, use it
        if game_tech_manager:
            # Validate the research is possible
            if not game_tech_manager.can_research_technology(player_id, technology):
                return TechnologyResearchResult(
                    success=False,
                    error_message=f"Cannot research {technology.value}: prerequisites not met or already owned",
                )

            # Execute the research through the integrated system
            success = game_tech_manager.research_technology(player_id, technology)
            if success:
                return TechnologyResearchResult(
                    success=True,
                    technology_researched=technology,
                    resources_spent=required_resources,
                )
            else:
                return TechnologyResearchResult(
                    success=False,
                    error_message=f"Failed to research {technology.value}",
                )

        # Fallback for basic functionality without full integration
        return TechnologyResearchResult(
            success=True,
            technology_researched=technology,
            resources_spent=required_resources,
        )

    def execute_secondary_ability_legacy(
        self,
        player_id: str,
        technology: Technology,
        available_command_tokens: int,
        available_resources: int,
        game_tech_manager: Optional["GameTechnologyManager"] = None,
    ) -> TechnologyResearchResult:
        """Legacy method for secondary ability execution.

        This method maintains backward compatibility with the original interface.
        """
        return self._execute_secondary_technology_research(
            player_id,
            technology,
            available_command_tokens,
            available_resources,
            game_tech_manager,
        )
