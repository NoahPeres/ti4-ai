"""
Dark Energy Tap technology implementation.

This module implements the Dark Energy Tap technology card from Prophecy of Kings,
which enables frontier exploration and enhanced retreat capabilities.

CONFIRMED SPECIFICATIONS - DO NOT MODIFY WITHOUT USER APPROVAL:
- Color: Blue technology
- Prerequisites: None (Level 0 technology)
- Expansion: Prophecy of Kings
- Available to all factions
"""

from typing import Optional

from ti4.core.abilities import Ability, AbilityEffect, TimingWindow
from ti4.core.constants import AbilityTrigger, Faction, Technology
from ti4.core.technology import TechnologyColor
from ti4.core.technology_cards.base.passive_tech import PassiveTechnologyCard


class DarkEnergyTap(PassiveTechnologyCard):
    """
    Dark Energy Tap technology implementation.

    This technology provides two abilities:
    1. Frontier Exploration: After tactical action in frontier system, explore frontier token
    2. Retreat Enhancement: When retreat declared, allow retreat to empty adjacent systems

    LRR References:
    - Rule 35.4: Frontier exploration mechanics
    - Retreat rules for enhanced retreat capabilities
    """

    def __init__(self) -> None:
        """Initialize Dark Energy Tap technology."""
        super().__init__(Technology.DARK_ENERGY_TAP, "Dark Energy Tap")

    @property
    def color(self) -> Optional[TechnologyColor]:
        """Technology color (Blue)."""
        return TechnologyColor.BLUE

    @property
    def prerequisites(self) -> list[TechnologyColor]:
        """Required prerequisite colors from specification."""
        from ..specifications import TechnologySpecificationRegistry

        registry = TechnologySpecificationRegistry()
        spec = registry.get_specification(Technology.DARK_ENERGY_TAP)
        return list(spec.prerequisites) if spec else []

    @property
    def faction_restriction(self) -> Optional[Faction]:
        """Faction restriction (available to all)."""
        return None

    def get_abilities(self) -> list[Ability]:
        """Get all abilities provided by Dark Energy Tap."""
        return [
            self._create_frontier_exploration_ability(),
            self._create_retreat_enhancement_ability(),
        ]

    def _create_frontier_exploration_ability(self) -> Ability:
        """Create the frontier exploration ability."""
        from ti4.core.constants import AbilityCondition
        from ti4.core.technology_cards.abilities_integration import EnhancedAbility

        ability = EnhancedAbility(
            name="Frontier Exploration",
            timing=TimingWindow.AFTER,
            trigger=AbilityTrigger.AFTER_TACTICAL_ACTION.value,
            effect=AbilityEffect(
                type="explore_frontier_token",
                value=True,
                conditions=[
                    {"type": "has_ships_in_system", "value": True},
                    {"type": "system_contains_frontier", "value": True},
                ],
            ),
            mandatory=True,
            conditions=[
                AbilityCondition.HAS_SHIPS_IN_SYSTEM,
                AbilityCondition.SYSTEM_CONTAINS_FRONTIER,
            ],
        )
        # Add source identifier for tracking
        ability.source = "Dark Energy Tap"  # type: ignore[attr-defined]
        return ability

    def _create_retreat_enhancement_ability(self) -> Ability:
        """Create the retreat enhancement ability."""
        from ti4.core.constants import AbilityTrigger
        from ti4.core.technology_cards.abilities_integration import EnhancedAbility

        ability = EnhancedAbility(
            name="Enhanced Retreat",
            timing=TimingWindow.WHEN,
            trigger=AbilityTrigger.WHEN_RETREAT_DECLARED.value,
            effect=AbilityEffect(
                type="allow_retreat_to_empty_adjacent",
                value=True,
            ),
            mandatory=False,
            conditions=[],  # No conditions for retreat enhancement
        )
        # Add source identifier for tracking
        ability.source = "Dark Energy Tap"  # type: ignore[attr-defined]
        return ability
