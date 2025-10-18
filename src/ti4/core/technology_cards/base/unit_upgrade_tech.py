"""
Unit upgrade technology card base implementation.

This module provides the base class for unit upgrade technology cards.
"""

from typing import TYPE_CHECKING, Any

from ti4.core.constants import UnitStatModification, UnitType
from ti4.core.technology import TechnologyColor

from ..unit_stats_integration import UnitStatModificationMapper
from .technology_card import BaseTechnologyCard

if TYPE_CHECKING:
    from ti4.core.constants import Technology
    from ti4.core.unit_stats import UnitStats


class UnitUpgradeTechnologyCard(BaseTechnologyCard):
    """
    Base implementation for unit upgrade technology cards.

    This class provides the foundation for technology cards that
    upgrade unit statistics and capabilities.
    """

    def __init__(
        self, technology_enum: "Technology", name: str, upgraded_unit_type: UnitType
    ) -> None:
        """
        Initialize the unit upgrade technology card.

        Args:
            technology_enum: The Technology enum value for this card
            name: Display name of the technology
            upgraded_unit_type: The unit type this technology upgrades
        """
        super().__init__(technology_enum, name)
        self._upgraded_unit_type = upgraded_unit_type

    @property
    def color(self) -> TechnologyColor | None:
        """Technology color (None for unit upgrades)."""
        # Unit upgrades have no color per TI4 rules
        return None

    @property
    def upgraded_unit_type(self) -> UnitType:
        """The unit type this technology upgrades."""
        return self._upgraded_unit_type

    def get_unit_stat_modifications(
        self,
    ) -> dict[UnitStatModification, int | bool]:
        """
        Get the stat modifications this upgrade provides using enums.

        Default implementation returns empty dict. Subclasses should override
        to provide the actual stat modifications using UnitStatModification enums.

        Returns:
            Dictionary mapping UnitStatModification enums to values
        """
        return {}

    def get_legacy_unit_stat_modifications(self) -> "UnitStats":
        """
        Get the stat modifications as UnitStats object for UnitStatsProvider.

        This method converts enum-based modifications to UnitStats object
        expected by the existing UnitStatsProvider.

        Returns:
            UnitStats object with the specified modifications
        """
        enum_modifications = self.get_unit_stat_modifications()
        if not enum_modifications:
            from ti4.core.unit_stats import UnitStats

            return UnitStats()

        # Convert enum-based modifications to UnitStats object
        return UnitStatModificationMapper.map_modifications_to_unit_stats(
            enum_modifications
        )

    def register_with_systems(
        self, ability_manager: Any, unit_stats_provider: Any
    ) -> None:
        """
        Register this technology with game systems.

        Overrides base implementation to also register unit stat modifications.

        Args:
            ability_manager: The ability manager to register abilities with
            unit_stats_provider: The unit stats provider for unit modifications
        """
        # Register abilities with ability manager
        super().register_with_systems(ability_manager, unit_stats_provider)

        # Register unit stat modifications
        enum_modifications = self.get_unit_stat_modifications()
        if enum_modifications and unit_stats_provider:
            stat_modifications = self.get_legacy_unit_stat_modifications()
            unit_stats_provider.register_technology_modifier(
                self.technology_enum, self.upgraded_unit_type, stat_modifications
            )
