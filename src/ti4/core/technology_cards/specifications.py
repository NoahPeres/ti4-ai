"""
Technology specification system using enums.

This module provides a comprehensive enum-based specification system for all
technology cards, ensuring type safety and centralized data management.
"""

from dataclasses import dataclass

from ti4.core.constants import (
    AbilityCondition,
    AbilityEffectType,
    AbilityTrigger,
    Expansion,
    Faction,
    Technology,
)
from ti4.core.technology import TechnologyColor

# Constants for validation
UNIT_UPGRADE_TECHNOLOGIES = frozenset(
    {
        Technology.CRUISER_II,
        Technology.FIGHTER_II,
        Technology.SPEC_OPS_II,
        Technology.CARRIER_II,
        Technology.DREADNOUGHT_II,
        Technology.DESTROYER_II,
    }
)


@dataclass(frozen=True)
class AbilitySpecification:
    """
    Specification for a technology ability using only enum types.

    This dataclass defines all aspects of a technology ability using
    enum types to ensure type safety and consistency.
    """

    trigger: AbilityTrigger
    effect: AbilityEffectType
    conditions: tuple[AbilityCondition, ...]
    mandatory: bool
    passive: bool


@dataclass(frozen=True)
class TechnologySpecification:
    """
    Complete specification for a technology card using only enum types.

    This dataclass defines all aspects of a technology card using
    enum types to ensure type safety and centralized data management.
    """

    technology: Technology
    name: str
    color: TechnologyColor | None
    prerequisites: tuple[TechnologyColor, ...]
    faction_restriction: Faction | None
    expansion: Expansion
    abilities: tuple[AbilitySpecification, ...]


class TechnologySpecificationRegistry:
    """
    Registry for all technology specifications using enum-based data.

    This registry provides centralized access to all technology specifications
    and supports filtering and validation operations.
    """

    def __init__(self) -> None:
        """Initialize the registry with confirmed technology specifications."""
        self._specifications: dict[Technology, TechnologySpecification] = {}
        self._initialize_confirmed_specifications()

    def _initialize_confirmed_specifications(self) -> None:
        """Initialize registry with confirmed technology specifications."""
        # CONFIRMED SPECIFICATIONS - DO NOT MODIFY WITHOUT USER APPROVAL

        # Gravity Drive - CONFIRMED BY USER: Blue tech, 1 Blue prerequisite, movement enhancement
        self._specifications[Technology.GRAVITY_DRIVE] = TechnologySpecification(
            technology=Technology.GRAVITY_DRIVE,
            name="Gravity Drive",
            color=TechnologyColor.BLUE,
            prerequisites=(TechnologyColor.BLUE,),
            faction_restriction=None,
            expansion=Expansion.BASE,
            abilities=(
                AbilitySpecification(
                    trigger=AbilityTrigger.AFTER_ACTIVATE_SYSTEM,
                    effect=AbilityEffectType.MODIFY_UNIT_STATS,
                    conditions=(),
                    mandatory=True,
                    passive=False,
                ),
            ),
        )

        # Dark Energy Tap - CONFIRMED BY USER: Blue tech, no prerequisites, Prophecy of Kings
        self._specifications[Technology.DARK_ENERGY_TAP] = TechnologySpecification(
            technology=Technology.DARK_ENERGY_TAP,
            name="Dark Energy Tap",
            color=TechnologyColor.BLUE,
            prerequisites=(),  # CONFIRMED: No prerequisites (Level 0 technology)
            faction_restriction=None,
            expansion=Expansion.PROPHECY_OF_KINGS,
            abilities=(
                AbilitySpecification(
                    trigger=AbilityTrigger.AFTER_TACTICAL_ACTION,
                    effect=AbilityEffectType.EXPLORE_FRONTIER_TOKEN,
                    conditions=(
                        AbilityCondition.HAS_SHIPS_IN_SYSTEM,
                        AbilityCondition.SYSTEM_CONTAINS_FRONTIER,
                    ),
                    mandatory=True,
                    passive=False,
                ),
                AbilitySpecification(
                    trigger=AbilityTrigger.WHEN_RETREAT_DECLARED,
                    effect=AbilityEffectType.ALLOW_RETREAT_TO_EMPTY_ADJACENT,
                    conditions=(),
                    mandatory=False,
                    passive=True,
                ),
            ),
        )

    def get_specification(
        self, technology: Technology
    ) -> TechnologySpecification | None:
        """
        Get a technology specification by Technology enum.

        Args:
            technology: The Technology enum to get specification for

        Returns:
            TechnologySpecification if found, None otherwise

        Raises:
            TypeError: If technology is not a Technology enum
        """
        if not isinstance(technology, Technology):
            raise TypeError(f"Expected Technology enum, got {type(technology)}")
        return self._specifications.get(technology)

    def has_specification(self, technology: Technology) -> bool:
        """
        Check if a technology specification exists.

        Args:
            technology: The Technology enum to check

        Returns:
            True if specification exists, False otherwise

        Raises:
            TypeError: If technology is not a Technology enum
        """
        if not isinstance(technology, Technology):
            raise TypeError(f"Expected Technology enum, got {type(technology)}")
        return technology in self._specifications

    def get_all_specifications(self) -> list[TechnologySpecification]:
        """
        Get all technology specifications.

        Returns:
            List of all TechnologySpecification objects
        """
        return list(self._specifications.values())

    def get_specifications_by_color(
        self, color: TechnologyColor
    ) -> list[TechnologySpecification]:
        """
        Get all specifications for a specific color.

        Args:
            color: The TechnologyColor to filter by

        Returns:
            List of specifications matching the color

        Raises:
            TypeError: If color is not a TechnologyColor enum
        """
        if not isinstance(color, TechnologyColor):
            raise TypeError(f"Expected TechnologyColor enum, got {type(color)}")
        return [spec for spec in self._specifications.values() if spec.color == color]

    def get_specifications_by_expansion(
        self, expansion: Expansion
    ) -> list[TechnologySpecification]:
        """
        Get all specifications for a specific expansion.

        Args:
            expansion: The Expansion to filter by

        Returns:
            List of specifications matching the expansion

        Raises:
            TypeError: If expansion is not an Expansion enum
        """
        if not isinstance(expansion, Expansion):
            raise TypeError(f"Expected Expansion enum, got {type(expansion)}")
        return [
            spec
            for spec in self._specifications.values()
            if spec.expansion == expansion
        ]

    def get_specification_with_confirmation(
        self, technology: Technology
    ) -> TechnologySpecification:
        """
        Get a technology specification with manual confirmation enforcement.

        This method enforces the manual confirmation protocol by checking
        if the technology specification has been confirmed before returning it.

        Args:
            technology: The Technology enum to get specification for

        Returns:
            TechnologySpecification if confirmed

        Raises:
            TechnologySpecificationError: If technology is not confirmed
            TypeError: If technology is not a Technology enum
            ValueError: If technology specification is not found
        """
        from ti4.core.technology_cards.confirmation import require_confirmation

        require_confirmation(technology, "specification")
        spec = self.get_specification(technology)
        if spec is None:
            raise ValueError(f"No specification found for {technology}")
        return spec


def validate_specification(spec: TechnologySpecification) -> list[str]:
    """
    Validate a technology specification for consistency and completeness.

    Args:
        spec: The TechnologySpecification to validate

    Returns:
        List of validation error messages (empty if valid)

    Raises:
        TypeError: If spec is not a TechnologySpecification
    """
    if not isinstance(spec, TechnologySpecification):
        raise TypeError(f"Expected TechnologySpecification, got {type(spec)}")

    errors = []

    # Validate name
    if not spec.name or not spec.name.strip():
        errors.append("Technology name cannot be empty")

    # Validate unit upgrade color consistency using the constant
    if spec.technology in UNIT_UPGRADE_TECHNOLOGIES and spec.color is not None:
        errors.append(
            f"Unit upgrade technology {spec.technology} should not have a color"
        )

    # Validate non-unit-upgrade technologies have a color
    if spec.technology not in UNIT_UPGRADE_TECHNOLOGIES and spec.color is None:
        errors.append(
            f"Non-unit-upgrade technology {spec.technology} must have a color"
        )

    # Validate abilities
    for i, ability in enumerate(spec.abilities):
        if not isinstance(ability, AbilitySpecification):
            errors.append(f"Ability {i} is not an AbilitySpecification")

    return errors
