"""Research technology action for TI4."""

from dataclasses import dataclass
from typing import Any

from ..core.technology import Technology, TechnologyTree
from .action import Action


@dataclass(frozen=True)
class ResearchTechnologyAction(Action):
    """Action to research a technology."""

    technology: Technology

    def is_legal(self, state: Any, player_id: Any) -> bool:
        """Check if this technology can be researched by the player."""
        if not state or not player_id:
            return False

        player_state = state.get_player_state(player_id)
        if not player_state:
            return False

        tree = TechnologyTree()
        player_technologies = list(player_state.technologies)
        return tree.can_research(self.technology, player_technologies)

    def execute(self, state: Any, player_id: Any) -> Any:
        """Execute the technology research and return new game state."""
        from copy import deepcopy

        # Validate that the action is legal before executing
        if not self.is_legal(state, player_id):
            raise ValueError(
                f"Cannot research {self.technology.name}: prerequisites not met"
            )

        # Create a deep copy of the state to maintain immutability
        new_state = deepcopy(state)

        # Add the technology to the player's collection
        player_state = new_state.get_player_state(player_id)
        if player_state:
            # Check if technology is already researched (shouldn't happen if validation is correct)
            if self.technology.name not in player_state.technologies:
                player_state.technologies.add(self.technology.name)

        return new_state

    def get_description(self) -> str:
        """Get a human-readable description of this action."""
        return f"Research {self.technology.name}"
