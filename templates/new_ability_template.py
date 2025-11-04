"""
Template for implementing new technology abilities.

This template provides a standardized approach for implementing technology
abilities that follows the development guidelines and best practices.

USAGE:
1. Copy this template to the appropriate location
2. Get user confirmation for all specifications
3. Replace placeholder values with confirmed specifications
4. Implement the specific ability logic
5. Write comprehensive tests

IMPORTANT: Never implement without user confirmation of specifications!
"""

from ti4.core.constants import (
    AbilityCondition,
    AbilityEffectType,
    AbilityTrigger,
    Expansion,
    Technology,
)
from ti4.core.technology import TechnologyColor
from ti4.core.technology_cards.base.passive_tech import PassiveTechnologyCard
from ti4.core.technology_cards.specifications import (
    AbilitySpecification,
    TechnologySpecification,
)

# Alternative imports based on technology type:
# from ti4.core.technology_cards.base.exhaustible_tech import ExhaustibleTechnologyCard
# from ti4.core.technology_cards.base.unit_upgrade_tech import UnitUpgradeTechnologyCard


class NewTechnologyTemplate(PassiveTechnologyCard):
    """
    Template implementation for [TECHNOLOGY_NAME].

    CONFIRMED SPECIFICATIONS - DO NOT MODIFY WITHOUT USER APPROVAL:
    - Name: [USER_CONFIRMED_NAME]
    - Color: [USER_CONFIRMED_COLOR]
    - Prerequisites: [USER_CONFIRMED_PREREQUISITES]
    - Type: [USER_CONFIRMED_TYPE]
    - Expansion: [USER_CONFIRMED_EXPANSION]
    - Abilities: [USER_CONFIRMED_ABILITIES]
    - Confirmed by user on [DATE]

    LRR References:
    - Rule [XX]: [RELEVANT_RULE_DESCRIPTION]
    """

    def __init__(self) -> None:
        """Initialize [TECHNOLOGY_NAME] with confirmed specifications."""

        # STEP 1: Define technology specification
        # NOTE: Template requires user to add Technology enum first
        # Replace with user-confirmed values
        tech_spec = TechnologySpecification(
            technology=Technology.YOUR_TECHNOLOGY_ENUM,  # Add to Technology enum first
            name="[USER_CONFIRMED_NAME]",
            color=TechnologyColor.BLUE,  # Replace with confirmed color
            prerequisites=(),  # Tuple of TechnologyColor values
            faction_restriction=None,  # Or specific Faction enum
            expansion=Expansion.BASE,  # Use Expansion enum
            abilities=tuple(self._create_abilities()),  # Returns tuple
        )

        # Initialize base class with the Technology enum and name, then store the full spec
        super().__init__(tech_spec.technology, tech_spec.name)
        self._specification = tech_spec

    def _create_abilities(self) -> tuple[AbilitySpecification, ...]:
        """
        Create ability specifications for this technology.

        Returns:
            Tuple of AbilitySpecification objects
        """
        abilities_list = []

        # STEP 2: Define each ability with confirmed specifications
        # Example ability - replace with user-confirmed specifications
        ability = AbilitySpecification(
            trigger=AbilityTrigger.AFTER_TACTICAL_ACTION,  # Use enum!
            effect=AbilityEffectType.EXPLORE_FRONTIER_TOKEN,  # Use enum!
            conditions=(  # Use tuple of enum values!
                AbilityCondition.SYSTEM_CONTAINS_FRONTIER,
            ),
            mandatory=False,  # Confirm with user
            passive=True,  # Confirm with user (True for passive effects, False for active)
        )
        abilities_list.append(ability)

        # Add additional abilities as confirmed by user
        # ability2 = AbilitySpecification(...)
        # abilities_list.append(ability2)

        return tuple(abilities_list)

    def can_use_ability(
        self, ability_index: int = 0, context: dict | None = None
    ) -> bool:
        """
        Check if the specified ability can be used.

        Args:
            ability_index: Index of the ability to check (default: 0)
            context: Game context for validation

        Returns:
            True if ability can be used, False otherwise
        """
        # STEP 3: Implement ability-specific validation logic
        # This should integrate with the game state and validate conditions

        if context is None:
            context = {}

        # Get the ability specification
        if ability_index >= len(self._specification.abilities):
            return False

        ability = self._specification.abilities[ability_index]

        # Validate conditions using the framework
        from ti4.core.technology_cards.abilities_integration import (
            validate_ability_conditions,
        )

        try:
            return validate_ability_conditions(ability.conditions, context)
        except NotImplementedError:
            # Log the unimplemented condition for development
            print(f"Warning: Unimplemented condition in {self._specification.name}")
            return False

    def use_ability(self, ability_index: int = 0, context: dict | None = None) -> bool:
        """
        Use the specified ability.

        Args:
            ability_index: Index of the ability to use (default: 0)
            context: Game context for the ability

        Returns:
            True if ability was used successfully, False otherwise
        """
        # STEP 4: Implement ability execution logic

        if not self.can_use_ability(ability_index, context):
            return False

        if context is None:
            context = {}

        ability = self._specification.abilities[ability_index]

        # Implement the specific effect based on the ability type
        if ability.effect == AbilityEffectType.EXPLORE_FRONTIER_TOKEN:
            return self._handle_frontier_exploration(context)
        elif ability.effect == AbilityEffectType.MODIFY_UNIT_STATS:
            return self._handle_unit_stat_modification(context)
        # Add other effect handlers as needed
        else:
            # This should not happen if all effects are properly implemented
            raise NotImplementedError(
                f"Effect handler for {ability.effect} not implemented"
            )

    def _handle_frontier_exploration(self, context: dict) -> bool:
        """
        Handle frontier token exploration effect.

        Args:
            context: Game context

        Returns:
            True if effect was applied successfully
        """
        # STEP 5: Implement specific effect logic
        # This would integrate with the exploration system

        # Example implementation - replace with actual game integration
        frontier_tokens = context.get("frontier_tokens", [])
        if frontier_tokens:
            # Process frontier exploration
            # This would call into the exploration system
            return True

        return False

    def _handle_unit_stat_modification(self, context: dict) -> bool:
        """
        Handle unit stat modification effect.

        Args:
            context: Game context

        Returns:
            True if effect was applied successfully
        """
        # STEP 6: Implement unit stat modification logic
        # This would integrate with the unit stats system

        # Example implementation - replace with actual game integration
        units = context.get("units", [])
        if units:
            # Apply stat modifications
            # This would call into the unit stats system
            return True

        return False


# STEP 7: Create factory function for easy instantiation
def create_new_technology() -> NewTechnologyTemplate:
    """
    Create a new instance of [TECHNOLOGY_NAME].

    Returns:
        Configured NewTechnologyTemplate instance
    """
    return NewTechnologyTemplate()


# STEP 8: Add to technology registry (if needed)
# This would typically be done in the registry module
"""
Example registry entry:

TECHNOLOGY_REGISTRY = {
    # ... existing technologies
    Technology.NEW_TECHNOLOGY: create_new_technology,
}
"""
