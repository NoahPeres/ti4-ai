"""Technology Strategy Card implementation for TI4.

This module implements Rule 91: TECHNOLOGY (Strategy Card) mechanics.
LRR Reference: Rule 91 - TECHNOLOGY (STRATEGY CARD)
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from .constants import Technology

if TYPE_CHECKING:
    from .game_technology_manager import GameTechnologyManager
    from .technology import TechnologyManager


@dataclass
class TechnologyResearchResult:
    """Result of a technology research attempt."""

    success: bool
    technology_researched: Optional[Technology] = None
    resources_spent: int = 0
    command_tokens_spent: int = 0
    error_message: Optional[str] = None


class TechnologyStrategyCard:
    """Implementation of the Technology strategy card.

    LRR Reference: Rule 91 - The "Technology" strategy card allows players to research new technology.
    This card's initiative value is "7."
    """

    def __init__(self) -> None:
        """Initialize the Technology strategy card."""
        pass

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
        technology: Technology,
        game_tech_manager: Optional["GameTechnologyManager"] = None,
    ) -> TechnologyResearchResult:
        """Execute the primary ability of the Technology strategy card.

        Args:
            player_id: The active player executing the primary ability
            technology: The technology to research
            game_tech_manager: Optional game technology manager for full integration

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

    def execute_secondary_ability(
        self,
        player_id: str,
        technology: Technology,
        available_command_tokens: int,
        available_resources: int,
        game_tech_manager: Optional["GameTechnologyManager"] = None,
    ) -> TechnologyResearchResult:
        """Execute the secondary ability of the Technology strategy card.

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
