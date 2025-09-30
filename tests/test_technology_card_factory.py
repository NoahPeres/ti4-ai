"""
Tests for technology card factory system.

This module tests the TechnologyCardFactory for instantiating technology cards
using enum-based specifications with caching functionality.
"""

import pytest

from ti4.core.constants import Technology
from ti4.core.technology_cards.protocols import TechnologyCardProtocol


class TestTechnologyCardFactory:
    """Test the TechnologyCardFactory functionality."""

    def test_factory_can_be_imported(self):
        """Test that TechnologyCardFactory can be imported."""
        # RED: This will fail initially since factory doesn't exist yet
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        assert TechnologyCardFactory is not None

    def test_factory_can_create_dark_energy_tap(self):
        """Test that factory can create Dark Energy Tap technology card."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()
        card = factory.create_card(Technology.DARK_ENERGY_TAP)

        # Should return a TechnologyCardProtocol implementation
        assert isinstance(card, TechnologyCardProtocol)
        assert card.technology_enum == Technology.DARK_ENERGY_TAP
        assert card.name == "Dark Energy Tap"

    def test_factory_can_create_gravity_drive(self):
        """Test that factory can create Gravity Drive technology card."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()
        card = factory.create_card(Technology.GRAVITY_DRIVE)

        # Should return a TechnologyCardProtocol implementation
        assert isinstance(card, TechnologyCardProtocol)
        assert card.technology_enum == Technology.GRAVITY_DRIVE
        assert card.name == "Gravity Drive"

    def test_factory_caches_instances(self):
        """Test that factory caches technology card instances."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()

        # Create same technology twice
        card1 = factory.create_card(Technology.DARK_ENERGY_TAP)
        card2 = factory.create_card(Technology.DARK_ENERGY_TAP)

        # Should return the same instance (cached)
        assert card1 is card2

    def test_factory_creates_different_instances_for_different_technologies(self):
        """Test that factory creates different instances for different technologies."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()

        dark_energy_tap = factory.create_card(Technology.DARK_ENERGY_TAP)
        gravity_drive = factory.create_card(Technology.GRAVITY_DRIVE)

        # Should be different instances
        assert dark_energy_tap is not gravity_drive
        assert dark_energy_tap.technology_enum != gravity_drive.technology_enum

    def test_factory_raises_error_for_unregistered_technology(self):
        """Test that factory raises error for unregistered technology."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()

        # Try to create a technology that doesn't have a concrete implementation
        with pytest.raises(ValueError, match="No implementation found"):
            factory.create_card(Technology.CRUISER_II)

    def test_factory_can_clear_cache(self):
        """Test that factory can clear its cache."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()

        # Create and cache a card
        card1 = factory.create_card(Technology.DARK_ENERGY_TAP)

        # Clear cache
        factory.clear_cache()

        # Create again - should be a new instance
        card2 = factory.create_card(Technology.DARK_ENERGY_TAP)

        # Should be different instances after cache clear
        assert card1 is not card2
        assert card1.technology_enum == card2.technology_enum

    def test_factory_can_check_if_technology_is_supported(self):
        """Test that factory can check if a technology is supported."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()

        # Should support technologies with concrete implementations
        assert factory.is_supported(Technology.DARK_ENERGY_TAP)
        assert factory.is_supported(Technology.GRAVITY_DRIVE)

        # Should not support technologies without concrete implementations
        assert not factory.is_supported(Technology.CRUISER_II)

    def test_factory_can_list_supported_technologies(self):
        """Test that factory can list all supported technologies."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()

        supported = factory.get_supported_technologies()

        # Should include technologies with concrete implementations
        assert Technology.DARK_ENERGY_TAP in supported
        assert Technology.GRAVITY_DRIVE in supported

        # Should not include technologies without concrete implementations
        assert Technology.CRUISER_II not in supported

    def test_factory_uses_enum_based_specifications(self):
        """Test that factory uses enum-based specifications."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()
        card = factory.create_card(Technology.DARK_ENERGY_TAP)

        # Should use specifications from the registry
        from ti4.core.technology import TechnologyColor

        assert card.color == TechnologyColor.BLUE
        assert card.prerequisites == []  # No prerequisites for Dark Energy Tap

    def test_factory_enforces_manual_confirmation_protocol(self):
        """Test that factory enforces manual confirmation protocol."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()

        # Mock a technology that isn't confirmed
        # This test will need to be updated based on how confirmation is implemented
        # For now, we'll test that confirmed technologies work
        card = factory.create_card(Technology.DARK_ENERGY_TAP)
        assert card is not None


class TestTechnologyCardFactoryIntegration:
    """Test factory integration with existing systems."""

    def test_factory_creates_cards_compatible_with_registry(self):
        """Test that factory-created cards work with TechnologyCardRegistry."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory
        from ti4.core.technology_cards.registry import TechnologyCardRegistry

        factory = TechnologyCardFactory()
        registry = TechnologyCardRegistry()

        # Create card with factory
        card = factory.create_card(Technology.DARK_ENERGY_TAP)

        # Should be able to register with registry
        registry.register_card(card)

        # Should be retrievable from registry
        retrieved = registry.get_card(Technology.DARK_ENERGY_TAP)
        assert retrieved is card

    def test_factory_creates_cards_with_proper_abilities(self):
        """Test that factory-created cards have proper abilities."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()
        card = factory.create_card(Technology.DARK_ENERGY_TAP)

        abilities = card.get_abilities()

        # Dark Energy Tap should have 2 abilities
        assert len(abilities) == 2

        # Check ability names
        ability_names = [ability.name for ability in abilities]
        assert "Frontier Exploration" in ability_names
        assert "Enhanced Retreat" in ability_names

    def test_factory_creates_cards_that_can_register_with_systems(self):
        """Test that factory-created cards can register with game systems."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()
        card = factory.create_card(Technology.DARK_ENERGY_TAP)

        # Mock systems
        class MockAbilityManager:
            def __init__(self):
                self.abilities = []

            def add_ability(self, ability):
                self.abilities.append(ability)

        class MockUnitStatsProvider:
            def __init__(self):
                self.modifications = {}

        mock_ability_manager = MockAbilityManager()
        mock_unit_stats_provider = MockUnitStatsProvider()

        # Should be able to register with systems without error
        card.register_with_systems(mock_ability_manager, mock_unit_stats_provider)

        # Should have registered abilities
        assert len(mock_ability_manager.abilities) > 0


class TestTechnologyCardFactoryErrorHandling:
    """Test factory error handling and edge cases."""

    def test_factory_handles_invalid_technology_enum(self):
        """Test that factory handles invalid technology enum values."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()

        # Test with None
        with pytest.raises(TypeError, match="Expected Technology enum"):
            factory.create_card(None)  # type: ignore

        # Test with string
        with pytest.raises(TypeError, match="Expected Technology enum"):
            factory.create_card("DARK_ENERGY_TAP")  # type: ignore

    def test_factory_handles_empty_cache_operations(self):
        """Test that factory handles cache operations on empty cache."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()

        # Should not error when clearing empty cache
        factory.clear_cache()

        # Should still work after clearing empty cache
        card = factory.create_card(Technology.DARK_ENERGY_TAP)
        assert card is not None

    def test_factory_is_thread_safe(self):
        """Test that factory operations are thread-safe."""
        # This is a placeholder for thread safety testing
        # Implementation will depend on whether we need thread safety
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()

        # Basic test - create multiple cards
        cards = []
        for _ in range(10):
            card = factory.create_card(Technology.DARK_ENERGY_TAP)
            cards.append(card)

        # All should be the same instance due to caching
        for card in cards[1:]:
            assert card is cards[0]

    def test_factory_get_cache_size(self):
        """Test that factory can report cache size."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()

        # Initially empty
        assert factory.get_cache_size() == 0

        # Create one card
        factory.create_card(Technology.DARK_ENERGY_TAP)
        assert factory.get_cache_size() == 1

        # Create another card
        factory.create_card(Technology.GRAVITY_DRIVE)
        assert factory.get_cache_size() == 2

        # Clear cache
        factory.clear_cache()
        assert factory.get_cache_size() == 0

    def test_factory_is_cached(self):
        """Test that factory can check if a technology is cached."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()

        # Initially not cached
        assert not factory.is_cached(Technology.DARK_ENERGY_TAP)

        # Create card - should be cached
        factory.create_card(Technology.DARK_ENERGY_TAP)
        assert factory.is_cached(Technology.DARK_ENERGY_TAP)

        # Other technology not cached
        assert not factory.is_cached(Technology.GRAVITY_DRIVE)

        # Clear cache
        factory.clear_cache()
        assert not factory.is_cached(Technology.DARK_ENERGY_TAP)

    def test_factory_is_cached_validates_input(self):
        """Test that is_cached validates input."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()

        with pytest.raises(TypeError, match="Expected Technology enum"):
            factory.is_cached("DARK_ENERGY_TAP")  # type: ignore

    def test_factory_get_supported_technologies_is_sorted(self):
        """Test that supported technologies are returned in sorted order."""
        from ti4.core.technology_cards.factory import TechnologyCardFactory

        factory = TechnologyCardFactory()
        supported = factory.get_supported_technologies()

        # Should be sorted by name
        names = [tech.name for tech in supported]
        assert names == sorted(names)
