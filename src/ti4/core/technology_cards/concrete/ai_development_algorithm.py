"""
AI Development Algorithm technology implementation.

This module implements the AI Development Algorithm technology card from Prophecy of Kings,
which demonstrates exhaustible abilities that are NOT ACTION abilities.

CONFIRMED SPECIFICATIONS - DO NOT MODIFY WITHOUT USER APPROVAL:
- Color: Yellow technology
- Prerequisites: None (Level 0 technology)
- Expansion: Prophecy of Kings
- Available to all factions
- Has two exhaustible abilities (neither are ACTION abilities)
"""

from ti4.core.abilities import Ability, AbilityEffect, TimingWindow
from ti4.core.constants import Faction, Technology
from ti4.core.technology import TechnologyColor
from ti4.core.technology_cards.base.exhaustible_tech import ExhaustibleTechnologyCard


class AIDevelopmentAlgorithm(ExhaustibleTechnologyCard):
    """
    AI Development Algorithm technology implementation.

    This technology provides two exhaustible abilities:
    1. Research Enhancement: When you research a unit upgrade technology,
       exhaust to ignore any 1 prerequisite
    2. Production Cost Reduction: When 1 or more of your units use PRODUCTION,
       exhaust to reduce the combined cost by the number of unit upgrade technologies you own

    This demonstrates that ExhaustibleTechnologyCard supports more than just ACTION abilities.

    LRR References:
    - Rule 90: Technology mechanics
    - Production rules for cost reduction
    - Research rules for prerequisite ignoring
    """

    def __init__(self) -> None:
        """Initialize AI Development Algorithm technology."""
        super().__init__(
            Technology.AI_DEVELOPMENT_ALGORITHM, "AI Development Algorithm"
        )

    @property
    def color(self) -> TechnologyColor | None:
        """Technology color (Yellow)."""
        return TechnologyColor.YELLOW

    @property
    def prerequisites(self) -> list[TechnologyColor]:
        """Required prerequisite colors (none - Level 0)."""
        return []

    @property
    def faction_restriction(self) -> Faction | None:
        """Faction restriction (available to all)."""
        return None

    def get_exhaustible_abilities(self) -> list[Ability]:
        """Get all abilities that can exhaust this card."""
        return [
            self._create_research_enhancement_ability(),
            self._create_production_cost_reduction_ability(),
        ]

    def _create_research_enhancement_ability(self) -> Ability:
        """Create the research enhancement ability."""
        return Ability(
            name="Research Enhancement",
            timing=TimingWindow.WHEN,
            trigger="research_unit_upgrade_technology",
            effect=AbilityEffect(
                type="ignore_prerequisite",
                value=1,
                conditions=[
                    {"type": "researching_unit_upgrade", "value": True},
                ],
            ),
            mandatory=False,  # Optional ability
        )

    def _create_production_cost_reduction_ability(self) -> Ability:
        """Create the production cost reduction ability."""
        return Ability(
            name="Production Cost Reduction",
            timing=TimingWindow.WHEN,
            trigger="units_use_production",
            effect=AbilityEffect(
                type="reduce_production_cost",
                value="unit_upgrade_count",  # Reduce by number of unit upgrades owned
                conditions=[
                    {"type": "units_using_production", "value": True},
                ],
            ),
            mandatory=False,  # Optional ability
        )

    def get_abilities(self) -> list[Ability]:
        """Get all abilities provided by AI Development Algorithm."""
        return self.get_exhaustible_abilities()
