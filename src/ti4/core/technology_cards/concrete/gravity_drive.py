"""
Gravity Drive technology implementation.

This module implements the Gravity Drive technology card using the
enum-based specification system for consistent behavior.

CONFIRMED SPECIFICATIONS - DO NOT MODIFY WITHOUT USER APPROVAL:
- Color: Blue technology
- Prerequisites: 1 Blue prerequisite
- Ability: After you activate a system, modify unit movement stats temporarily
- Effect: Mandatory movement enhancement
"""

from typing import Optional

from ti4.core.abilities import Ability
from ti4.core.constants import Faction, Technology
from ti4.core.technology import TechnologyColor
from ti4.core.technology_cards.abilities_integration import (
    create_ability_from_specification,
)
from ti4.core.technology_cards.base.passive_tech import PassiveTechnologyCard
from ti4.core.technology_cards.specifications import (
    TechnologySpecification,
    TechnologySpecificationRegistry,
)


class GravityDrive(PassiveTechnologyCard):
    """
    Gravity Drive technology implementation using enum-based specifications.

    This technology provides movement enhancement:
    - After you activate a system, units get +1 movement range

    The implementation uses the centralized specification registry to ensure
    consistency with the enum-based technology framework.
    """

    def __init__(self) -> None:
        """
        Initialize Gravity Drive technology.

        Raises:
            ValueError: If no specification is found for Gravity Drive
        """
        super().__init__(Technology.GRAVITY_DRIVE, "Gravity Drive")
        self._registry = TechnologySpecificationRegistry()
        self._specification: TechnologySpecification = self._load_specification()

    def _load_specification(self) -> "TechnologySpecification":
        """
        Load the specification for Gravity Drive from the registry.

        Returns:
            TechnologySpecification: The loaded specification

        Raises:
            ValueError: If no specification is found
        """
        specification = self._registry.get_specification(Technology.GRAVITY_DRIVE)
        if specification is None:
            raise ValueError(
                f"No specification found for {Technology.GRAVITY_DRIVE.name}"
            )
        return specification

    @property
    def color(self) -> Optional[TechnologyColor]:
        """Technology color from specification."""
        return self._specification.color

    @property
    def prerequisites(self) -> list[TechnologyColor]:
        """Required prerequisite colors from specification."""
        return list(self._specification.prerequisites)

    @property
    def faction_restriction(self) -> Optional[Faction]:
        """Faction restriction from specification."""
        return self._specification.faction_restriction

    def get_abilities(self) -> list[Ability]:
        """
        Get all abilities from enum-based specification.

        Returns:
            list[Ability]: List of abilities with proper source attribution
        """
        abilities = []
        for ability_spec in self._specification.abilities:
            ability = create_ability_from_specification(ability_spec)
            ability.source = "Gravity Drive"  # type: ignore[attr-defined]
            abilities.append(ability)
        return abilities
