"""
Tests for technology card protocols and interfaces.

This module tests the base technology card protocol and interfaces
for the technology card framework.
"""

from typing import Any, Optional

import pytest

from ti4.core.abilities import Ability
from ti4.core.constants import Faction, Technology, UnitType
from ti4.core.technology import TechnologyColor


class MockAbilityManager:
    """Mock ability manager for testing."""

    def __init__(self):
        self.abilities = []

    def add_ability(self, ability: Ability) -> None:
        """Add an ability to the manager."""
        self.abilities.append(ability)


class MockUnitStatsProvider:
    """Mock unit stats provider for testing."""

    def __init__(self):
        self.registered_modifications: dict[Technology, dict[str, Any]] = {}

    def register_technology_modifier(
        self, technology: Technology, unit_type: UnitType, modifications: dict[str, Any]
    ) -> None:
        """Register technology modifications."""
        self.registered_modifications[technology] = {
            "unit_type": unit_type,
            "modifications": modifications,
        }


class TestTechnologyCardProtocol:
    """Test the base TechnologyCardProtocol interface."""

    def test_technology_card_protocol_exists(self):
        """Test that TechnologyCardProtocol can be imported."""
        from ti4.core.technology_cards import TechnologyCardProtocol

        # Protocol should exist and be importable
        assert TechnologyCardProtocol is not None

    def test_technology_card_protocol_has_required_properties(self):
        """Test that TechnologyCardProtocol defines all required properties."""

        # Create a mock implementation to test protocol compliance
        class MockTechnologyCard:
            @property
            def technology_enum(self) -> Technology:
                return Technology.GRAVITY_DRIVE

            @property
            def name(self) -> str:
                return "Test Technology"

            @property
            def color(self) -> Optional[TechnologyColor]:
                return TechnologyColor.BLUE

            @property
            def prerequisites(self) -> list[TechnologyColor]:
                return [TechnologyColor.BLUE]

            @property
            def faction_restriction(self) -> Optional[Faction]:
                return None

            def get_abilities(self) -> list[Ability]:
                return []

            def register_with_systems(
                self, ability_manager, unit_stats_provider
            ) -> None:
                pass

        # Should be able to create instance that follows protocol
        mock_card = MockTechnologyCard()

        # Test all required properties exist
        assert mock_card.technology_enum == Technology.GRAVITY_DRIVE
        assert mock_card.name == "Test Technology"
        assert mock_card.color == TechnologyColor.BLUE
        assert mock_card.prerequisites == [TechnologyColor.BLUE]
        assert mock_card.faction_restriction is None
        assert mock_card.get_abilities() == []


class TestExhaustibleTechnologyProtocol:
    """Test the ExhaustibleTechnologyProtocol interface."""

    def test_exhaustible_technology_protocol_exists(self):
        """Test that ExhaustibleTechnologyProtocol can be imported."""
        from ti4.core.technology_cards import ExhaustibleTechnologyProtocol

        # Protocol should exist and be importable
        assert ExhaustibleTechnologyProtocol is not None

    def test_exhaustible_technology_protocol_has_required_methods(self):
        """Test that ExhaustibleTechnologyProtocol defines all required methods."""
        from ti4.core.abilities import Ability

        # Create a mock implementation to test protocol compliance
        class MockExhaustibleTechnology:
            def __init__(self):
                self._exhausted = False

            def is_exhausted(self) -> bool:
                return self._exhausted

            def exhaust(self) -> None:
                self._exhausted = True

            def ready(self) -> None:
                self._exhausted = False

            def get_action_ability(self) -> Optional[Ability]:
                return None

        # Should be able to create instance that follows protocol
        mock_card = MockExhaustibleTechnology()

        # Test all required methods exist and work
        assert not mock_card.is_exhausted()
        mock_card.exhaust()
        assert mock_card.is_exhausted()
        mock_card.ready()
        assert not mock_card.is_exhausted()
        assert mock_card.get_action_ability() is None


class TestUnitUpgradeTechnologyProtocol:
    """Test the UnitUpgradeTechnologyProtocol interface."""

    def test_unit_upgrade_technology_protocol_exists(self):
        """Test that UnitUpgradeTechnologyProtocol can be imported."""
        from ti4.core.technology_cards import UnitUpgradeTechnologyProtocol

        # Protocol should exist and be importable
        assert UnitUpgradeTechnologyProtocol is not None

    def test_unit_upgrade_technology_protocol_has_required_properties(self):
        """Test that UnitUpgradeTechnologyProtocol defines all required properties."""
        from typing import Any

        # Create a mock implementation to test protocol compliance
        class MockUnitUpgradeTechnology:
            @property
            def upgraded_unit_type(self) -> UnitType:
                return UnitType.CRUISER

            def get_unit_stat_modifications(self) -> dict[str, Any]:
                return {"combat_value": 6, "movement": 2}

        # Should be able to create instance that follows protocol
        mock_card = MockUnitUpgradeTechnology()

        # Test all required properties exist
        assert mock_card.upgraded_unit_type == UnitType.CRUISER
        assert mock_card.get_unit_stat_modifications() == {
            "combat_value": 6,
            "movement": 2,
        }


class TestProtocolCompliance:
    """Test protocol compliance checking functionality."""

    def test_can_check_protocol_compliance(self):
        """Test that we can check if a class implements a protocol."""

        # This test will fail initially since we haven't implemented the protocols yet
        # But it defines what we want to achieve

        class ValidTechnologyCard:
            @property
            def technology_enum(self) -> Technology:
                return Technology.GRAVITY_DRIVE

            @property
            def name(self) -> str:
                return "Valid Technology"

            @property
            def color(self) -> Optional[TechnologyColor]:
                return TechnologyColor.BLUE

            @property
            def prerequisites(self) -> list[TechnologyColor]:
                return []

            @property
            def faction_restriction(self) -> Optional[Faction]:
                return None

            def get_abilities(self) -> list[Ability]:
                return []

            def register_with_systems(
                self, ability_manager, unit_stats_provider
            ) -> None:
                pass

        # Should be able to create a valid implementation
        valid_card = ValidTechnologyCard()

        # Basic protocol compliance check (structural typing)
        assert hasattr(valid_card, "technology_enum")
        assert hasattr(valid_card, "name")
        assert hasattr(valid_card, "color")
        assert hasattr(valid_card, "prerequisites")
        assert hasattr(valid_card, "faction_restriction")
        assert hasattr(valid_card, "get_abilities")
        assert hasattr(valid_card, "register_with_systems")


class TestBaseTechnologyCardImplementations:
    """Test the base technology card implementations."""

    def test_exhaustible_technology_card_base_class(self):
        """Test the ExhaustibleTechnologyCard base class."""
        from ti4.core.abilities import Ability
        from ti4.core.constants import Faction, Technology
        from ti4.core.technology import TechnologyColor
        from ti4.core.technology_cards import ExhaustibleTechnologyCard

        # Create a concrete implementation for testing
        class TestExhaustibleTech(ExhaustibleTechnologyCard):
            @property
            def color(self) -> Optional[TechnologyColor]:
                return TechnologyColor.BLUE

            @property
            def prerequisites(self) -> list[TechnologyColor]:
                return [TechnologyColor.BLUE]

            @property
            def faction_restriction(self) -> Optional[Faction]:
                return None

            def get_abilities(self) -> list[Ability]:
                return []

        # Test exhaustion mechanics
        tech = TestExhaustibleTech(Technology.GRAVITY_DRIVE, "Test Tech")

        assert not tech.is_exhausted()
        tech.exhaust()
        assert tech.is_exhausted()
        tech.ready()
        assert not tech.is_exhausted()

        # Test double exhaustion raises error
        tech.exhaust()
        with pytest.raises(ValueError, match="already exhausted"):
            tech.exhaust()

        # Test get_action_ability returns None by default
        assert tech.get_action_ability() is None

    def test_unit_upgrade_technology_card_base_class(self):
        """Test the UnitUpgradeTechnologyCard base class."""
        from ti4.core.abilities import Ability
        from ti4.core.constants import Faction, Technology, UnitType
        from ti4.core.technology_cards import UnitUpgradeTechnologyCard

        # Create a concrete implementation for testing
        class TestUnitUpgradeTech(UnitUpgradeTechnologyCard):
            @property
            def prerequisites(self) -> list[TechnologyColor]:
                return [TechnologyColor.BLUE, TechnologyColor.GREEN]

            @property
            def faction_restriction(self) -> Optional[Faction]:
                return None

            def get_abilities(self) -> list[Ability]:
                return []

            def get_unit_stat_modifications(self):
                from ti4.core.constants import UnitStatModification

                return {
                    UnitStatModification.COMBAT_VALUE: 6,
                    UnitStatModification.MOVEMENT: 2,
                }

        # Test unit upgrade functionality
        tech = TestUnitUpgradeTech(
            Technology.CRUISER_II, "Cruiser II", UnitType.CRUISER
        )

        assert tech.upgraded_unit_type == UnitType.CRUISER
        assert tech.color is None  # Unit upgrades have no color
        from ti4.core.constants import UnitStatModification

        expected_mods = {
            UnitStatModification.COMBAT_VALUE: 6,
            UnitStatModification.MOVEMENT: 2,
        }
        assert tech.get_unit_stat_modifications() == expected_mods

        # Test register_with_systems method
        mock_ability_manager = MockAbilityManager()
        mock_unit_stats_provider = MockUnitStatsProvider()

        tech.register_with_systems(mock_ability_manager, mock_unit_stats_provider)

        # Should register unit stat modifications
        assert mock_unit_stats_provider.registered_modifications
        assert (
            Technology.CRUISER_II in mock_unit_stats_provider.registered_modifications
        )
        # Check that modifications were registered
        registered = mock_unit_stats_provider.registered_modifications[
            Technology.CRUISER_II
        ]
        assert registered["unit_type"] == UnitType.CRUISER

        # The modifications should now be a UnitStats object
        from ti4.core.unit_stats import UnitStats

        modifications = registered["modifications"]
        assert isinstance(modifications, UnitStats)
        assert modifications.combat_value == 6
        assert modifications.movement == 2

        # Test edge case: no stat modifications
        class TestUnitUpgradeTechNoMods(UnitUpgradeTechnologyCard):
            @property
            def prerequisites(self) -> list[TechnologyColor]:
                return []

            @property
            def faction_restriction(self) -> Optional[Faction]:
                return None

            def get_abilities(self) -> list[Ability]:
                return []

            # Override to return empty dict (default behavior)
            def get_unit_stat_modifications(self):
                return {}

        tech_no_mods = TestUnitUpgradeTechNoMods(
            Technology.FIGHTER_II, "Fighter II", UnitType.FIGHTER
        )
        mock_unit_stats_provider_2 = MockUnitStatsProvider()

        tech_no_mods.register_with_systems(
            mock_ability_manager, mock_unit_stats_provider_2
        )

        # Should not register anything since no modifications
        assert (
            Technology.FIGHTER_II
            not in mock_unit_stats_provider_2.registered_modifications
        )

        # Test edge case: None unit_stats_provider
        tech.register_with_systems(mock_ability_manager, None)
        # Should not crash

    def test_technology_card_registry(self):
        """Test the TechnologyCardRegistry functionality."""
        from ti4.core.abilities import Ability
        from ti4.core.constants import Faction, Technology
        from ti4.core.technology import TechnologyColor
        from ti4.core.technology_cards import (
            PassiveTechnologyCard,
            TechnologyCardRegistry,
        )

        # Create a test technology card
        class TestTech(PassiveTechnologyCard):
            @property
            def color(self) -> Optional[TechnologyColor]:
                return TechnologyColor.BLUE

            @property
            def prerequisites(self) -> list[TechnologyColor]:
                return []

            @property
            def faction_restriction(self) -> Optional[Faction]:
                return None

            def get_abilities(self) -> list[Ability]:
                return []

        registry = TechnologyCardRegistry()
        test_tech = TestTech(Technology.GRAVITY_DRIVE, "Test Tech")

        # Test registration
        assert not registry.is_registered(Technology.GRAVITY_DRIVE)
        registry.register_card(test_tech)
        assert registry.is_registered(Technology.GRAVITY_DRIVE)

        # Test retrieval
        retrieved_tech = registry.get_card(Technology.GRAVITY_DRIVE)
        assert retrieved_tech is test_tech

        # Test duplicate registration raises error
        with pytest.raises(ValueError, match="already registered"):
            registry.register_card(test_tech)

        # Test unregistration
        assert registry.unregister_card(Technology.GRAVITY_DRIVE)
        assert not registry.is_registered(Technology.GRAVITY_DRIVE)
        assert registry.get_card(Technology.GRAVITY_DRIVE) is None

        # Test unregistering non-existent technology returns False
        assert not registry.unregister_card(Technology.GRAVITY_DRIVE)

        # Test get_all_cards functionality
        test_tech2 = TestTech(Technology.DARK_ENERGY_TAP, "Test Tech 2")
        registry.register_card(test_tech)
        registry.register_card(test_tech2)

        all_cards = registry.get_all_cards()
        assert len(all_cards) == 2
        assert test_tech in all_cards
        assert test_tech2 in all_cards

        # Test clear functionality
        registry.clear()
        assert len(registry.get_all_cards()) == 0
        assert not registry.is_registered(Technology.GRAVITY_DRIVE)
        assert not registry.is_registered(Technology.DARK_ENERGY_TAP)

    def test_passive_technology_card_base_class(self):
        """Test the PassiveTechnologyCard base class."""
        from ti4.core.abilities import Ability
        from ti4.core.constants import Faction, Technology
        from ti4.core.technology import TechnologyColor
        from ti4.core.technology_cards import PassiveTechnologyCard

        # Create a concrete implementation for testing
        class TestPassiveTech(PassiveTechnologyCard):
            @property
            def color(self) -> Optional[TechnologyColor]:
                return TechnologyColor.GREEN

            @property
            def prerequisites(self) -> list[TechnologyColor]:
                return [TechnologyColor.GREEN]

            @property
            def faction_restriction(self) -> Optional[Faction]:
                return None

            def get_abilities(self) -> list[Ability]:
                return []

        # Test passive technology functionality
        tech = TestPassiveTech(Technology.GRAVITY_DRIVE, "Test Passive Tech")

        assert tech.technology_enum == Technology.GRAVITY_DRIVE
        assert tech.name == "Test Passive Tech"
        assert tech.color == TechnologyColor.GREEN
        assert tech.prerequisites == [TechnologyColor.GREEN]
        assert tech.faction_restriction is None
        assert tech.get_abilities() == []

        # Test register_with_systems method
        mock_ability_manager = MockAbilityManager()
        mock_unit_stats_provider = MockUnitStatsProvider()

        tech.register_with_systems(mock_ability_manager, mock_unit_stats_provider)

        # Should not register any abilities since get_abilities returns empty list
        assert len(mock_ability_manager.abilities) == 0
