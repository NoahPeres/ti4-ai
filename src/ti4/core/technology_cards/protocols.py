"""
Technology card protocols and interfaces.

This module defines the core protocols that all technology card implementations
must follow to ensure consistency and proper integration with game systems.
"""

from typing import Any, Protocol, runtime_checkable

from ti4.core.abilities import Ability
from ti4.core.constants import Faction, Technology, UnitStatModification, UnitType
from ti4.core.technology import TechnologyColor


@runtime_checkable
class TechnologyCardProtocol(Protocol):
    """
    Protocol that all technology cards must implement.

    This protocol defines the core interface for technology cards,
    ensuring consistent behavior across all implementations.
    """

    @property
    def technology_enum(self) -> Technology:
        """The Technology enum value for this card."""
        ...

    @property
    def name(self) -> str:
        """Display name of the technology."""
        ...

    @property
    def color(self) -> TechnologyColor | None:
        """Technology color (None for unit upgrades)."""
        ...

    @property
    def prerequisites(self) -> list[TechnologyColor]:
        """Required prerequisite colors."""
        ...

    @property
    def faction_restriction(self) -> Faction | None:
        """Faction restriction (None if available to all)."""
        ...

    def get_abilities(self) -> list[Ability]:
        """Get all abilities provided by this technology."""
        ...

    def register_with_systems(
        self, ability_manager: Any, unit_stats_provider: Any
    ) -> None:
        """Register this technology with game systems."""
        ...


@runtime_checkable
class ExhaustibleTechnologyProtocol(Protocol):
    """
    Protocol for technologies that can be exhausted.

    This protocol defines the interface for technology cards that have
    exhaustion mechanics (can be flipped face-down after use).
    """

    def is_exhausted(self) -> bool:
        """Check if this technology is exhausted."""
        ...

    def exhaust(self) -> None:
        """Exhaust this technology."""
        ...

    def ready(self) -> None:
        """Ready this technology."""
        ...

    def get_exhaustible_abilities(self) -> list[Ability]:
        """Get all abilities that can exhaust this card."""
        ...

    def get_action_ability(self) -> Ability | None:
        """Get the ACTION ability that exhausts this card (if any)."""
        ...


@runtime_checkable
class UnitUpgradeTechnologyProtocol(Protocol):
    """
    Protocol for unit upgrade technologies.

    This protocol defines the interface for technology cards that
    upgrade unit statistics and capabilities.
    """

    @property
    def upgraded_unit_type(self) -> UnitType:
        """The unit type this technology upgrades."""
        ...

    def get_unit_stat_modifications(
        self,
    ) -> dict[UnitStatModification, int | bool]:
        """Get the stat modifications this upgrade provides."""
        ...

    def get_legacy_unit_stat_modifications(self) -> Any:
        """Get the stat modifications as UnitStats object for UnitStatsProvider."""
        ...
