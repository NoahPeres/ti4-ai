"""
Technology card framework integration system.

This module provides the complete integration of the technology card framework
with existing game systems, ensuring that Dark Energy Tap and Gravity Drive
are properly registered and available throughout the game.
"""

from typing import Optional

from ti4.core.abilities import AbilityManager
from ti4.core.constants import Technology
from ti4.core.unit_stats import UnitStatsProvider

from .factory import TechnologyCardFactory
from .protocols import TechnologyCardProtocol
from .registry import TechnologyCardRegistry


class TechnologyFrameworkIntegration:
    """
    Complete integration system for the technology card framework.

    This class coordinates the registration of technology cards with all
    relevant game systems, ensuring seamless integration between the new
    framework and existing systems.
    """

    def __init__(
        self,
        ability_manager: Optional[AbilityManager] = None,
        unit_stats_provider: Optional[UnitStatsProvider] = None,
    ) -> None:
        """
        Initialize the technology framework integration.

        Args:
            ability_manager: The ability manager to register abilities with
            unit_stats_provider: The unit stats provider for unit modifications
        """
        self.factory = TechnologyCardFactory()
        self.registry = TechnologyCardRegistry()
        self.ability_manager = ability_manager  # Optional, may be None
        self.unit_stats_provider = unit_stats_provider or UnitStatsProvider()

        # Automatically register all supported technology cards
        self._register_all_technology_cards()

    def _register_all_technology_cards(self) -> None:
        """Register all supported technology cards with game systems."""
        supported_technologies = self.factory.get_supported_technologies()

        for technology in supported_technologies:
            self._register_technology_card(technology)

    def _register_technology_card(self, technology: Technology) -> None:
        """
        Register a single technology card with all relevant systems.

        Args:
            technology: The technology to register
        """
        # Create the technology card instance
        card = self.factory.create_card(technology)

        # Register with the technology card registry
        if not self.registry.is_registered(technology):
            self.registry.register_card(card)

        # Register abilities with the ability manager (if available)
        if self.ability_manager is not None:
            abilities = card.get_abilities()
            for ability in abilities:
                # Add technology source information
                ability.source = card.name  # type: ignore[attr-defined]
                # Register with ability manager
                self.ability_manager.add_ability(ability)

        # Register unit stat modifications for unit-upgrade cards
        from .protocols import UnitUpgradeTechnologyProtocol

        if isinstance(card, UnitUpgradeTechnologyProtocol):
            enum_mods = card.get_unit_stat_modifications()
            if enum_mods:
                stats = card.get_legacy_unit_stat_modifications()
                self.unit_stats_provider.register_technology_modifier(
                    technology, card.upgraded_unit_type, stats
                )

    def get_technology_card(
        self, technology: Technology
    ) -> Optional[TechnologyCardProtocol]:
        """
        Get a technology card instance.

        Args:
            technology: The technology to get

        Returns:
            The technology card instance, or None if not supported
        """
        if self.factory.is_supported(technology):
            return self.factory.create_card(technology)
        return None

    def is_technology_supported(self, technology: Technology) -> bool:
        """
        Check if a technology is supported by the framework.

        Args:
            technology: The technology to check

        Returns:
            True if the technology is supported
        """
        return self.factory.is_supported(technology)

    def get_supported_technologies(self) -> list[Technology]:
        """
        Get all technologies supported by the framework.

        Returns:
            List of supported technologies
        """
        return self.factory.get_supported_technologies()

    def validate_integration(self) -> dict[str, bool]:
        """
        Validate that the integration is working correctly.

        Returns:
            Dictionary of validation results
        """
        results = {}

        # Check that factory is working
        results["factory_operational"] = (
            len(self.factory.get_supported_technologies()) > 0
        )

        # Check that registry has cards
        results["registry_populated"] = len(self.registry.get_all_cards()) > 0

        # Check that Dark Energy Tap is available
        results["dark_energy_tap_available"] = self.is_technology_supported(
            Technology.DARK_ENERGY_TAP
        )

        # Check that Gravity Drive is available
        results["gravity_drive_available"] = self.is_technology_supported(
            Technology.GRAVITY_DRIVE
        )

        # Check that cards have abilities
        if results["dark_energy_tap_available"]:
            det_card = self.get_technology_card(Technology.DARK_ENERGY_TAP)
            results["dark_energy_tap_has_abilities"] = (
                len(det_card.get_abilities()) > 0 if det_card else False
            )

        if results["gravity_drive_available"]:
            gd_card = self.get_technology_card(Technology.GRAVITY_DRIVE)
            results["gravity_drive_has_abilities"] = (
                len(gd_card.get_abilities()) > 0 if gd_card else False
            )

        return results


# Global integration instance for easy access
_global_integration: Optional[TechnologyFrameworkIntegration] = None


def get_technology_framework_integration() -> TechnologyFrameworkIntegration:
    """
    Get the global technology framework integration instance.

    Returns:
        The global integration instance
    """
    global _global_integration
    if _global_integration is None:
        _global_integration = TechnologyFrameworkIntegration()
    return _global_integration


def initialize_technology_framework(
    ability_manager: Optional[AbilityManager] = None,
    unit_stats_provider: Optional[UnitStatsProvider] = None,
) -> TechnologyFrameworkIntegration:
    """
    Initialize the technology framework with specific managers.

    Args:
        ability_manager: The ability manager to use
        unit_stats_provider: The unit stats provider to use

    Returns:
        The initialized integration instance
    """
    global _global_integration
    _global_integration = TechnologyFrameworkIntegration(
        ability_manager=ability_manager,
        unit_stats_provider=unit_stats_provider,
    )
    return _global_integration
