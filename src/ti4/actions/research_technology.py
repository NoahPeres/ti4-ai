"""Research technology action for TI4 - Integrated with Rule 90 TechnologyManager."""

from dataclasses import dataclass
from typing import Any

from ..core.constants import Technology
from ..core.game_technology_manager import GameTechnologyManager
from .action import Action


@dataclass(frozen=True)
class ResearchTechnologyAction(Action):
    """Action to research a technology using Rule 90 mechanics with game state integration."""

    technology: Technology

    def is_legal(self, state: Any, player_id: str) -> bool:
        """Check if this technology can be researched by the player.

        Uses Rule 90 TechnologyManager with game state integration.
        """
        # Basic validation
        if not state or not player_id:
            return False

        player_state = state.get_player_state(player_id)
        if not player_state:
            return False

        # Use integrated technology manager
        game_tech_manager = GameTechnologyManager(state)
        return game_tech_manager.can_research_technology(player_id, self.technology)

    def execute(self, state: Any, player_id: str) -> Any:
        """Execute the technology research and return new game state.

        Uses Rule 90 TechnologyManager with full game state integration.
        """
        from copy import deepcopy

        # Validate the action can be performed
        if not self.is_legal(state, player_id):
            raise ValueError(
                f"Cannot research {self.technology.value}: prerequisites not met"
            )

        # Create new state
        new_state = deepcopy(state)

        # Use integrated technology manager
        game_tech_manager = GameTechnologyManager(new_state)
        success = game_tech_manager.research_technology(player_id, self.technology)

        if not success:
            raise ValueError(f"Failed to research {self.technology.value}")

        return new_state

    def get_description(self) -> str:
        """Get a human-readable description of this action."""
        return f"Research {self.technology.value}"
