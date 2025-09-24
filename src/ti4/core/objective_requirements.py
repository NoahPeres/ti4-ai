"""Objective requirement validation system for TI4 (Rules 61.9-61.10)."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_state import GameState


@dataclass(frozen=True)
class ObjectiveRequirement(ABC):
    """Abstract base class for objective requirements."""

    @abstractmethod
    def is_fulfilled_by(self, game_state: "GameState", player_id: str) -> bool:
        """Check if this requirement is fulfilled by the given player."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get a human-readable description of this requirement."""
        pass


@dataclass(frozen=True)
class SpendResourcesRequirement(ObjectiveRequirement):
    """Requirement to spend a certain amount of resources (Rule 61.10)."""

    amount: int

    def is_fulfilled_by(self, game_state: "GameState", player_id: str) -> bool:
        """Check if player can spend the required resources."""
        # For now, return False - we need resource tracking system
        # TODO: Implement resource spending validation when resource system is available
        return False

    def get_description(self) -> str:
        """Get description of resource spending requirement."""
        return f"Spend {self.amount} resources"


@dataclass(frozen=True)
class SpendInfluenceRequirement(ObjectiveRequirement):
    """Requirement to spend a certain amount of influence (Rule 61.10)."""

    amount: int

    def is_fulfilled_by(self, game_state: "GameState", player_id: str) -> bool:
        """Check if player can spend the required influence."""
        # For now, return False - we need influence tracking system
        # TODO: Implement influence spending validation when influence system is available
        return False

    def get_description(self) -> str:
        """Get description of influence spending requirement."""
        return f"Spend {self.amount} influence"


@dataclass(frozen=True)
class SpendTokensRequirement(ObjectiveRequirement):
    """Requirement to spend command tokens (Rule 61.10)."""

    amount: int
    token_type: str  # "command", "strategy", etc.

    def is_fulfilled_by(self, game_state: "GameState", player_id: str) -> bool:
        """Check if player can spend the required tokens."""
        # For now, return False - we need token tracking system
        # TODO: Implement token spending validation when token system is available
        return False

    def get_description(self) -> str:
        """Get description of token spending requirement."""
        return f"Spend {self.amount} {self.token_type} tokens"


@dataclass(frozen=True)
class ControlPlanetsRequirement(ObjectiveRequirement):
    """Requirement to control a certain number of planets."""

    count: int
    planet_type: str = "any"  # "any", "cultural", "industrial", "hazardous", "home"
    exclude_home: bool = False

    def is_fulfilled_by(self, game_state: "GameState", player_id: str) -> bool:
        """Check if player controls the required planets."""
        # For now, return False - we need planet control tracking system
        # TODO: Implement planet control validation when planet system is available
        return False

    def get_description(self) -> str:
        """Get description of planet control requirement."""
        desc = f"Control {self.count} {self.planet_type} planets"
        if self.exclude_home:
            desc += " (excluding home system)"
        return desc


@dataclass(frozen=True)
class DestroyUnitsRequirement(ObjectiveRequirement):
    """Requirement to destroy units (Rule 61.9)."""

    count: int
    unit_type: str = "any"  # "any", "ship", "ground_force", "fighter", etc.

    def is_fulfilled_by(self, game_state: "GameState", player_id: str) -> bool:
        """Check if player has destroyed the required units."""
        # For now, return False - we need unit destruction tracking system
        # TODO: Implement unit destruction validation when combat system tracks destruction
        return False

    def get_description(self) -> str:
        """Get description of unit destruction requirement."""
        unit_desc = self.unit_type if self.unit_type != "any" else "units"
        return f"Destroy {self.count} {unit_desc}"


@dataclass(frozen=True)
class WinCombatRequirement(ObjectiveRequirement):
    """Requirement to win combat in specific locations."""

    count: int
    combat_type: str = "any"  # "any", "space", "ground"
    location_type: str = "any"  # "any", "home_system", "anomaly", etc.

    def is_fulfilled_by(self, game_state: "GameState", player_id: str) -> bool:
        """Check if player has won the required combats."""
        # For now, return False - we need combat tracking system
        # TODO: Implement combat victory validation when combat system tracks wins
        return False

    def get_description(self) -> str:
        """Get description of combat victory requirement."""
        combat_desc = (
            f"{self.combat_type} combat" if self.combat_type != "any" else "combat"
        )
        location_desc = (
            f" in {self.location_type}" if self.location_type != "any" else ""
        )
        return f"Win {self.count} {combat_desc}{location_desc}"


@dataclass(frozen=True)
class TechnologyRequirement(ObjectiveRequirement):
    """Requirement to have certain technologies."""

    count: int
    tech_type: str = (
        "any"  # "any", "unit_upgrade", "biotic", "cybernetic", "propulsion", "warfare"
    )

    def is_fulfilled_by(self, game_state: "GameState", player_id: str) -> bool:
        """Check if player has the required technologies."""
        # For now, return False - we need technology tracking system
        # TODO: Implement technology validation when technology system is available
        return False

    def get_description(self) -> str:
        """Get description of technology requirement."""
        tech_desc = (
            f"{self.tech_type} technologies"
            if self.tech_type != "any"
            else "technologies"
        )
        return f"Have {self.count} {tech_desc}"


class ObjectiveRequirementValidator:
    """Validates whether objective requirements are met by a player."""

    def validate_requirements(
        self,
        game_state: "GameState",
        player_id: str,
        requirements: list[ObjectiveRequirement],
    ) -> bool:
        """
        Validate if all requirements are met by the player.

        Args:
            game_state: Current game state
            player_id: ID of the player to validate
            requirements: List of requirements to validate

        Returns:
            True if all requirements are met, False otherwise
        """
        if not requirements:
            return True

        for requirement in requirements:
            if not requirement.is_fulfilled_by(game_state, player_id):
                return False
        return True

    def get_unfulfilled_requirements(
        self,
        game_state: "GameState",
        player_id: str,
        requirements: list[ObjectiveRequirement],
    ) -> list[ObjectiveRequirement]:
        """
        Get list of unfulfilled requirements for a player.

        Args:
            game_state: Current game state
            player_id: ID of the player to check
            requirements: List of requirements to check

        Returns:
            List of unfulfilled requirements
        """
        unfulfilled = []
        for requirement in requirements:
            if not requirement.is_fulfilled_by(game_state, player_id):
                unfulfilled.append(requirement)
        return unfulfilled
