"""
Tests for Dark Energy Tap technology implementation.

This module tests the Dark Energy Tap technology card implementation,
including its frontier exploration and retreat enhancement abilities.
"""

from ti4.core.abilities import TimingWindow
from ti4.core.constants import Technology
from ti4.core.technology import TechnologyColor
from ti4.core.technology_cards.concrete.dark_energy_tap import DarkEnergyTap


class TestDarkEnergyTap:
    """Test Dark Energy Tap technology implementation."""

    def test_dark_energy_tap_basic_properties(self):
        """Test Dark Energy Tap basic properties match confirmed specifications."""
        # RED: Test basic properties
        dark_energy_tap = DarkEnergyTap()

        assert dark_energy_tap.technology_enum == Technology.DARK_ENERGY_TAP
        assert dark_energy_tap.name == "Dark Energy Tap"
        assert dark_energy_tap.color == TechnologyColor.BLUE
        assert dark_energy_tap.prerequisites == []  # No prerequisites
        assert dark_energy_tap.faction_restriction is None

    def test_dark_energy_tap_has_frontier_exploration_ability(self):
        """Test Dark Energy Tap has frontier exploration ability."""
        # RED: Test frontier exploration ability exists
        dark_energy_tap = DarkEnergyTap()
        abilities = dark_energy_tap.get_abilities()

        # Should have exactly 2 abilities
        assert len(abilities) == 2

        # Find the frontier exploration ability
        frontier_ability = None
        for ability in abilities:
            if "frontier" in ability.name.lower():
                frontier_ability = ability
                break

        assert frontier_ability is not None
        assert frontier_ability.timing == TimingWindow.AFTER
        assert frontier_ability.trigger == "tactical_action_in_frontier_system"
        assert frontier_ability.mandatory is True

    def test_dark_energy_tap_has_retreat_enhancement_ability(self):
        """Test Dark Energy Tap has retreat enhancement ability."""
        # RED: Test retreat enhancement ability exists
        dark_energy_tap = DarkEnergyTap()
        abilities = dark_energy_tap.get_abilities()

        # Find the retreat enhancement ability
        retreat_ability = None
        for ability in abilities:
            if "retreat" in ability.name.lower():
                retreat_ability = ability
                break

        assert retreat_ability is not None
        assert retreat_ability.timing == TimingWindow.WHEN
        assert retreat_ability.trigger == "when_retreat_declared"
        assert retreat_ability.mandatory is False

    def test_dark_energy_tap_implements_protocol(self):
        """Test Dark Energy Tap implements TechnologyCardProtocol."""
        # RED: Test protocol compliance

        dark_energy_tap = DarkEnergyTap()

        # Should implement all protocol methods
        assert hasattr(dark_energy_tap, "technology_enum")
        assert hasattr(dark_energy_tap, "name")
        assert hasattr(dark_energy_tap, "color")
        assert hasattr(dark_energy_tap, "prerequisites")
        assert hasattr(dark_energy_tap, "faction_restriction")
        assert hasattr(dark_energy_tap, "get_abilities")
        assert hasattr(dark_energy_tap, "register_with_systems")

    def test_dark_energy_tap_register_with_systems(self):
        """Test Dark Energy Tap registers abilities with game systems."""
        # RED: Test system registration
        dark_energy_tap = DarkEnergyTap()

        # Mock ability manager
        class MockAbilityManager:
            def __init__(self):
                self.abilities = []

            def add_ability(self, ability):
                self.abilities.append(ability)

        mock_ability_manager = MockAbilityManager()
        mock_unit_stats_provider = None  # Not needed for this test

        dark_energy_tap.register_with_systems(
            mock_ability_manager, mock_unit_stats_provider
        )

        # Should have registered 2 abilities
        assert len(mock_ability_manager.abilities) == 2

    def test_dark_energy_tap_frontier_exploration_ability_details(self):
        """Test Dark Energy Tap frontier exploration ability has correct details."""
        # RED: Test detailed ability properties
        dark_energy_tap = DarkEnergyTap()
        abilities = dark_energy_tap.get_abilities()

        frontier_ability = None
        for ability in abilities:
            if "frontier" in ability.name.lower():
                frontier_ability = ability
                break

        assert frontier_ability is not None
        assert frontier_ability.name == "Frontier Exploration"
        assert getattr(frontier_ability, "source", None) == "Dark Energy Tap"
        assert frontier_ability.effect.type == "explore_frontier_token"
        assert frontier_ability.effect.value is True

        # Check conditions
        conditions = frontier_ability.effect.conditions
        assert len(conditions) == 2
        assert {"type": "has_ships_in_system", "value": True} in conditions
        assert {"type": "system_contains_frontier", "value": True} in conditions

    def test_dark_energy_tap_retreat_enhancement_ability_details(self):
        """Test Dark Energy Tap retreat enhancement ability has correct details."""
        # RED: Test detailed ability properties
        dark_energy_tap = DarkEnergyTap()
        abilities = dark_energy_tap.get_abilities()

        retreat_ability = None
        for ability in abilities:
            if "retreat" in ability.name.lower():
                retreat_ability = ability
                break

        assert retreat_ability is not None
        assert retreat_ability.name == "Enhanced Retreat"
        assert getattr(retreat_ability, "source", None) == "Dark Energy Tap"
        assert retreat_ability.effect.type == "allow_retreat_to_empty_adjacent"
        assert retreat_ability.effect.value is True

        # Should have no conditions for retreat enhancement
        assert retreat_ability.effect.conditions is None

    def test_dark_energy_tap_specification_consistency(self):
        """Test Dark Energy Tap matches its specification in the registry."""
        # RED: Test specification consistency
        from ti4.core.technology_cards.specifications import (
            TechnologySpecificationRegistry,
        )

        registry = TechnologySpecificationRegistry()
        spec = registry.get_specification(Technology.DARK_ENERGY_TAP)

        assert spec is not None
        assert spec.name == "Dark Energy Tap"
        assert spec.color == TechnologyColor.BLUE
        assert spec.prerequisites == ()
        assert spec.faction_restriction is None

        # Test implementation matches specification
        dark_energy_tap = DarkEnergyTap()
        assert dark_energy_tap.name == spec.name
        assert dark_energy_tap.color == spec.color
        assert dark_energy_tap.prerequisites == list(spec.prerequisites)
        assert dark_energy_tap.faction_restriction == spec.faction_restriction

    def test_dark_energy_tap_abilities_match_specification(self):
        """Test Dark Energy Tap abilities match the specification."""
        # RED: Test ability specification consistency
        from ti4.core.technology_cards.specifications import (
            TechnologySpecificationRegistry,
        )

        registry = TechnologySpecificationRegistry()
        spec = registry.get_specification(Technology.DARK_ENERGY_TAP)

        dark_energy_tap = DarkEnergyTap()
        abilities = dark_energy_tap.get_abilities()

        # Should have same number of abilities as specification
        assert len(abilities) == len(spec.abilities)

        # Check that abilities match specification patterns
        ability_names = [ability.name for ability in abilities]
        assert "Frontier Exploration" in ability_names
        assert "Enhanced Retreat" in ability_names

    def test_dark_energy_tap_error_handling(self):
        """Test Dark Energy Tap handles edge cases properly."""
        # RED: Test error handling
        dark_energy_tap = DarkEnergyTap()

        # Should not raise errors when getting properties multiple times
        assert dark_energy_tap.technology_enum == Technology.DARK_ENERGY_TAP
        assert dark_energy_tap.technology_enum == Technology.DARK_ENERGY_TAP

        # Should not raise errors when getting abilities multiple times
        abilities1 = dark_energy_tap.get_abilities()
        abilities2 = dark_energy_tap.get_abilities()
        assert len(abilities1) == len(abilities2)

        # Abilities should be consistent across calls
        for i, ability in enumerate(abilities1):
            assert ability.name == abilities2[i].name
            assert ability.timing == abilities2[i].timing
            assert ability.trigger == abilities2[i].trigger
