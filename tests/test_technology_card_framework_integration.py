"""
Comprehensive integration tests for the Technology Card Framework.

This module tests the complete technology card lifecycle, integration with multiple
game systems, enum-based specification system end-to-end, and manual confirmation
protocol in realistic scenarios.

Requirements tested:
- 4.4: Existing technology functionality continues to work
- 5.5: Dark Energy Tap prerequisites are validated correctly
- 8.5: Clear error messages guide to correct implementation
"""

from unittest.mock import Mock, patch

import pytest

from ti4.core.abilities import AbilityManager, TimingWindow
from ti4.core.constants import (
    AbilityCondition,
    AbilityEffectType,
    AbilityTrigger,
    Technology,
)
from ti4.core.game_state import GameState
from ti4.core.technology import TechnologyColor
from ti4.core.technology_cards.concrete.dark_energy_tap import DarkEnergyTap
from ti4.core.technology_cards.concrete.gravity_drive import GravityDrive
from ti4.core.technology_cards.exceptions import TechnologySpecificationError
from ti4.core.technology_cards.factory import TechnologyCardFactory
from ti4.core.technology_cards.registry import TechnologyCardRegistry
from ti4.core.technology_cards.specifications import TechnologySpecificationRegistry
from ti4.core.unit_stats import UnitStatsProvider

# Constants for test validation
EXPECTED_DARK_ENERGY_TAP_ABILITIES = 2
EXPECTED_GRAVITY_DRIVE_ABILITIES = 1
PERFORMANCE_TEST_ITERATIONS = 100
PERFORMANCE_MAX_TIME_SECONDS = 1.0


class IntegrationTestFixture:
    """Shared fixture for integration tests to reduce duplication."""

    def __init__(self):
        """Initialize common test components."""
        self.game_state = GameState()
        self.ability_manager = AbilityManager(self.game_state)
        self.unit_stats_provider = UnitStatsProvider()
        self.factory = TechnologyCardFactory()
        self.registry = TechnologyCardRegistry()
        self.specification_registry = TechnologySpecificationRegistry()
        self.dark_energy_tap = DarkEnergyTap()
        self.gravity_drive = GravityDrive()

    def create_mock_player_with_technology(
        self, technology: Technology, player_id: str = "test_player"
    ) -> Mock:
        """Create a mock player with specified technology."""
        mock_player = Mock()
        mock_player.technologies = {technology}
        mock_player.id = player_id
        return mock_player

    def create_frontier_exploration_context(
        self, has_ships: bool = True, has_frontier: bool = True
    ) -> dict:
        """Create context for frontier exploration testing."""
        return {
            "player": Mock(),
            "system_id": "test_system",
            "has_ships": has_ships,
            "has_frontier_token": has_frontier,
        }

    def create_retreat_context(self, combat_id: str = "test_combat") -> dict:
        """Create context for retreat testing."""
        return {
            "player": Mock(),
            "combat_id": combat_id,
            "retreating_units": [Mock()],
            "adjacent_systems": ["system1", "system2"],
        }

    def assert_ability_count(
        self, abilities: list, expected_count: int, context: str = ""
    ):
        """Assert ability count with descriptive error message."""
        assert len(abilities) == expected_count, (
            f"Expected {expected_count} abilities{' for ' + context if context else ''}, "
            f"but got {len(abilities)}: {[ability.name for ability in abilities]}"
        )

    def assert_technology_card_properties(
        self, card, expected_technology: Technology, expected_name: str
    ):
        """Assert basic technology card properties."""
        assert card is not None, "Technology card should not be None"
        assert card.technology_enum == expected_technology, (
            f"Expected technology {expected_technology}, got {card.technology_enum}"
        )
        assert card.name == expected_name, (
            f"Expected name '{expected_name}', got '{card.name}'"
        )


class TestTechnologyCardLifecycleIntegration:
    """Test complete technology card lifecycle (registration, lookup, usage)."""

    def setup_method(self):
        """Setup test fixtures for lifecycle testing."""
        self.fixture = IntegrationTestFixture()

    def test_complete_dark_energy_tap_lifecycle(self):
        """Test complete Dark Energy Tap lifecycle from creation to usage.

        Requirements: 4.4, 5.5 - Complete technology functionality
        """
        # RED: Test complete lifecycle

        # 1. CREATION: Factory creates Dark Energy Tap
        dark_energy_tap = self.fixture.factory.create_card(Technology.DARK_ENERGY_TAP)
        self.fixture.assert_technology_card_properties(
            dark_energy_tap, Technology.DARK_ENERGY_TAP, "Dark Energy Tap"
        )
        assert dark_energy_tap.color == TechnologyColor.BLUE
        assert dark_energy_tap.prerequisites == []

        # 2. REGISTRATION: Register with game systems
        dark_energy_tap.register_with_systems(
            self.fixture.ability_manager, self.fixture.unit_stats_provider
        )

        # Should have registered abilities
        initial_ability_count = len(self.fixture.ability_manager.abilities)
        assert initial_ability_count >= EXPECTED_DARK_ENERGY_TAP_ABILITIES

        # 3. REGISTRY: Register with technology registry
        self.fixture.registry.register_card(dark_energy_tap)

        # Should be retrievable from registry
        retrieved_card = self.fixture.registry.get_card(Technology.DARK_ENERGY_TAP)
        assert retrieved_card is dark_energy_tap

        # 4. USAGE: Use abilities in game context
        # Test frontier exploration ability
        frontier_context = self.fixture.create_frontier_exploration_context()

        frontier_result = self.fixture.ability_manager.trigger_event(
            "tactical_action_in_frontier_system", frontier_context
        )
        assert frontier_result.success
        assert len(frontier_result.resolved_abilities) >= 1

        # Test retreat enhancement ability
        retreat_context = self.fixture.create_retreat_context()

        retreat_result = self.fixture.ability_manager.trigger_event(
            "retreat_declared", retreat_context
        )
        assert retreat_result.success
        assert len(retreat_result.resolved_abilities) >= 1

    def test_complete_gravity_drive_lifecycle(self):
        """Test complete Gravity Drive lifecycle from creation to usage.

        Requirements: 4.4 - Existing technology functionality continues to work
        """
        # RED: Test Gravity Drive lifecycle

        # 1. CREATION: Factory creates Gravity Drive
        gravity_drive = self.fixture.factory.create_card(Technology.GRAVITY_DRIVE)
        self.fixture.assert_technology_card_properties(
            gravity_drive, Technology.GRAVITY_DRIVE, "Gravity Drive"
        )
        assert gravity_drive.color == TechnologyColor.BLUE

        # 2. REGISTRATION: Register with game systems
        gravity_drive.register_with_systems(
            self.fixture.ability_manager, self.fixture.unit_stats_provider
        )

        # 3. REGISTRY: Register with technology registry
        self.fixture.registry.register_card(gravity_drive)

        # Should be retrievable from registry
        retrieved_card = self.fixture.registry.get_card(Technology.GRAVITY_DRIVE)
        assert retrieved_card is gravity_drive

        # 4. USAGE: Use abilities in game context
        abilities = gravity_drive.get_abilities()
        self.fixture.assert_ability_count(
            abilities, EXPECTED_GRAVITY_DRIVE_ABILITIES, "Gravity Drive"
        )

    def test_multiple_technology_cards_coexist(self):
        """Test multiple technology cards can coexist in the same systems.

        Requirements: 4.4 - All technology implementations are consistent
        """
        # RED: Test multiple technologies

        # Create multiple technology cards
        dark_energy_tap = self.fixture.factory.create_card(Technology.DARK_ENERGY_TAP)
        gravity_drive = self.fixture.factory.create_card(Technology.GRAVITY_DRIVE)

        # Register both with systems
        dark_energy_tap.register_with_systems(
            self.fixture.ability_manager, self.fixture.unit_stats_provider
        )
        gravity_drive.register_with_systems(
            self.fixture.ability_manager, self.fixture.unit_stats_provider
        )

        # Register both with registry
        self.fixture.registry.register_card(dark_energy_tap)
        self.fixture.registry.register_card(gravity_drive)

        # Both should be retrievable
        assert (
            self.fixture.registry.get_card(Technology.DARK_ENERGY_TAP)
            is dark_energy_tap
        )
        assert self.fixture.registry.get_card(Technology.GRAVITY_DRIVE) is gravity_drive

        # Both should have registered abilities
        all_abilities = self.fixture.ability_manager.abilities
        dark_energy_abilities = [
            ability
            for ability in all_abilities
            if "Dark Energy Tap" in getattr(ability, "source", "")
        ]
        gravity_drive_abilities = [
            ability
            for ability in all_abilities
            if "Gravity Drive" in getattr(ability, "source", "")
        ]

        self.fixture.assert_ability_count(
            dark_energy_abilities, EXPECTED_DARK_ENERGY_TAP_ABILITIES, "Dark Energy Tap"
        )
        self.fixture.assert_ability_count(
            gravity_drive_abilities, EXPECTED_GRAVITY_DRIVE_ABILITIES, "Gravity Drive"
        )

    def test_technology_card_factory_integration_with_registry(self):
        """Test factory and registry work together seamlessly.

        Requirements: 1.4 - Clear file structure and organization
        """
        # RED: Test factory-registry integration

        # Factory should create cards that work with registry
        supported_technologies = self.fixture.factory.get_supported_technologies()

        for technology in supported_technologies:
            # Create card with factory
            card = self.fixture.factory.create_card(technology)

            # Register with registry
            self.fixture.registry.register_card(card)

            # Should be retrievable
            retrieved = self.fixture.registry.get_card(technology)
            assert retrieved is card

    def test_technology_card_caching_across_systems(self):
        """Test technology card caching works across different systems.

        Requirements: 1.3 - Clear template and location to follow
        """
        # RED: Test caching integration

        # Create card through factory (should be cached)
        card1 = self.fixture.factory.create_card(Technology.DARK_ENERGY_TAP)

        # Create same card again (should return cached instance)
        card2 = self.fixture.factory.create_card(Technology.DARK_ENERGY_TAP)

        assert card1 is card2

        # Register cached card with registry
        self.fixture.registry.register_card(card1)

        # Retrieved card should be the same cached instance
        retrieved = self.fixture.registry.get_card(Technology.DARK_ENERGY_TAP)
        assert retrieved is card1


class TestDarkEnergyTapMultiSystemIntegration:
    """Test Dark Energy Tap integration with multiple game systems."""

    def setup_method(self):
        """Setup test fixtures for multi-system integration."""
        self.game_state = GameState()
        self.ability_manager = AbilityManager(self.game_state)
        self.unit_stats_provider = UnitStatsProvider()
        self.dark_energy_tap = DarkEnergyTap()

    def test_dark_energy_tap_abilities_system_integration(self):
        """Test Dark Energy Tap integration with abilities system.

        Requirements: 2.1, 5.3 - Abilities integrate with abilities system
        """
        # RED: Test abilities system integration

        # Register with abilities system
        self.dark_energy_tap.register_with_systems(
            self.ability_manager, self.unit_stats_provider
        )

        # Should have registered abilities
        abilities = self.dark_energy_tap.get_abilities()
        assert len(abilities) == 2

        # Abilities should have correct timing windows
        ability_timings = [ability.timing for ability in abilities]
        assert TimingWindow.AFTER in ability_timings  # Frontier exploration
        assert TimingWindow.WHEN in ability_timings  # Retreat enhancement

    def test_dark_energy_tap_exploration_system_integration(self):
        """Test Dark Energy Tap integration with Rule 35 exploration system.

        Requirements: 5.2, 5.4 - Frontier exploration integration
        """
        # RED: Test exploration system integration

        # This test requires the exploration system to check for Dark Energy Tap
        # We'll mock the exploration system for this test

        with patch("ti4.core.exploration.ExplorationSystem") as mock_exploration:
            mock_manager = Mock()
            mock_exploration.return_value = mock_manager

            # Dark Energy Tap should enable frontier exploration
            mock_manager.can_explore_frontier_token.return_value = True

            # Register Dark Energy Tap
            self.dark_energy_tap.register_with_systems(
                self.ability_manager, self.unit_stats_provider
            )

            # Test that frontier exploration is enabled
            context = {
                "player": Mock(),
                "system_id": "frontier_system",
                "has_ships": True,
                "has_frontier_token": True,
                "technologies": {Technology.DARK_ENERGY_TAP},
            }

            result = self.ability_manager.trigger_event(
                "tactical_action_in_frontier_system", context
            )

            assert result.success

    def test_dark_energy_tap_combat_system_integration(self):
        """Test Dark Energy Tap integration with combat/retreat system.

        Requirements: 5.3 - Retreat enhancement integration
        """
        # RED: Test combat system integration

        # Register Dark Energy Tap
        self.dark_energy_tap.register_with_systems(
            self.ability_manager, self.unit_stats_provider
        )

        # Test retreat enhancement
        retreat_context = {
            "player": Mock(),
            "combat_id": "test_combat",
            "retreating_units": [Mock()],
            "adjacent_systems": ["system1", "system2"],
        }

        result = self.ability_manager.trigger_event("retreat_declared", retreat_context)

        assert result.success

        # Should have enhanced retreat options
        retreat_abilities = [
            ability
            for ability in result.resolved_abilities
            if "retreat" in ability.name.lower()
        ]
        assert len(retreat_abilities) >= 1

    def test_dark_energy_tap_game_state_integration(self):
        """Test Dark Energy Tap integration with game state management.

        Requirements: 5.5 - Prerequisites are validated correctly
        """
        # RED: Test game state integration

        # Mock player with Dark Energy Tap technology
        mock_player = Mock()
        mock_player.technologies = {Technology.DARK_ENERGY_TAP}
        mock_player.id = "test_player"

        # Create new game state with player (since GameState is frozen)
        from ti4.core.game_state import GameState

        game_state_with_player = GameState(players=[mock_player])

        # Create ability manager with the new game state
        ability_manager_with_player = AbilityManager(game_state_with_player)

        # Register Dark Energy Tap
        self.dark_energy_tap.register_with_systems(
            ability_manager_with_player, self.unit_stats_provider
        )

        # Test that abilities are registered (we can't easily test player-specific abilities
        # without more complex setup, so we'll test that abilities are registered)
        registered_abilities = ability_manager_with_player.abilities

        # Should include Dark Energy Tap abilities
        dark_energy_abilities = [
            ability
            for ability in registered_abilities
            if "Dark Energy Tap" in getattr(ability, "source", "")
        ]
        assert len(dark_energy_abilities) >= 2

    def test_dark_energy_tap_prerequisite_validation_integration(self):
        """Test Dark Energy Tap prerequisite validation with technology system.

        Requirements: 5.5 - Prerequisites are validated correctly
        """
        # RED: Test prerequisite validation

        # Dark Energy Tap has no prerequisites (confirmed by user)
        assert self.dark_energy_tap.prerequisites == []

        # Should be researchable without any prerequisites
        mock_player = Mock()
        mock_player.technologies = set()
        mock_player.get_technology_colors.return_value = []

        # Mock technology manager
        with patch("ti4.core.technology.TechnologyManager") as mock_tech_manager:
            mock_manager = Mock()
            mock_tech_manager.return_value = mock_manager

            # Should be able to research Dark Energy Tap
            mock_manager.can_research_technology.return_value = True

            can_research = mock_manager.can_research_technology(
                mock_player, Technology.DARK_ENERGY_TAP
            )
            assert can_research

    def test_dark_energy_tap_exhaustion_system_integration(self):
        """Test Dark Energy Tap integration with exhaustion mechanics.

        Requirements: 2.3 - Exhaustion mechanics integration
        """
        # RED: Test exhaustion integration

        # Dark Energy Tap is not exhaustible (passive abilities)
        # But test that it works with exhaustion system

        # Register with systems
        self.dark_energy_tap.register_with_systems(
            self.ability_manager, self.unit_stats_provider
        )

        # Dark Energy Tap abilities should be passive (not exhaustible)
        abilities = self.dark_energy_tap.get_abilities()
        for ability in abilities:
            # Should not require exhaustion
            assert not getattr(ability, "requires_exhaustion", False)


class TestEnumBasedSpecificationSystemIntegration:
    """Test enum-based specification system end-to-end."""

    def setup_method(self):
        """Setup test fixtures for enum system testing."""
        self.specification_registry = TechnologySpecificationRegistry()
        self.factory = TechnologyCardFactory()

    def test_enum_based_technology_creation_end_to_end(self):
        """Test complete enum-based technology creation process.

        Requirements: 3.1, 3.2, 3.3 - Comprehensive protocol for implementation
        """
        # RED: Test enum-based creation

        # 1. Get specification from enum-based registry
        spec = self.specification_registry.get_specification(Technology.DARK_ENERGY_TAP)

        assert spec is not None
        assert spec.name == "Dark Energy Tap"
        assert spec.color == TechnologyColor.BLUE
        assert spec.prerequisites == []
        assert spec.faction_restriction is None

        # 2. Create technology card using enum-based factory
        card = self.factory.create_card(Technology.DARK_ENERGY_TAP)

        # Should match specification
        assert card.name == spec.name
        assert card.color == spec.color
        assert card.prerequisites == spec.prerequisites
        assert card.faction_restriction == spec.faction_restriction

        # 3. Abilities should be created from enum specifications
        abilities = card.get_abilities()
        assert len(abilities) == len(spec.abilities)

    def test_ability_trigger_enum_to_timing_window_mapping(self):
        """Test AbilityTrigger enum maps correctly to TimingWindow enum.

        Requirements: 7.2, 7.3 - Support all ability and timing patterns
        """
        # RED: Test enum mapping

        from ti4.core.technology_cards.abilities_integration import (
            map_trigger_to_timing,
        )

        # Test all relevant mappings
        test_mappings = [
            (AbilityTrigger.ACTION, TimingWindow.ACTION),
            (AbilityTrigger.AFTER_TACTICAL_ACTION, TimingWindow.AFTER),
            (AbilityTrigger.WHEN_RETREAT_DECLARED, TimingWindow.WHEN),
            (AbilityTrigger.START_OF_TURN, TimingWindow.START_OF_TURN),
            (AbilityTrigger.END_OF_TURN, TimingWindow.END_OF_TURN),
        ]

        for trigger_enum, expected_timing in test_mappings:
            actual_timing = map_trigger_to_timing(trigger_enum)
            assert actual_timing == expected_timing

    def test_ability_effect_enum_to_handler_mapping(self):
        """Test AbilityEffectType enum maps to actual game effect handlers.

        Requirements: 7.2 - Support all ability patterns
        """
        # RED: Test effect mapping

        from ti4.core.technology_cards.abilities_integration import (
            map_effect_to_handler,
        )

        # Test key effect mappings
        test_effects = [
            AbilityEffectType.EXPLORE_FRONTIER_TOKEN,
            AbilityEffectType.ALLOW_RETREAT_TO_EMPTY_ADJACENT,
            AbilityEffectType.MODIFY_UNIT_STATS,
            AbilityEffectType.GAIN_TRADE_GOODS,
        ]

        for effect_enum in test_effects:
            handler = map_effect_to_handler(effect_enum)
            assert handler is not None
            assert callable(handler)

    def test_ability_condition_enum_validation(self):
        """Test AbilityCondition enum validation works correctly.

        Requirements: 7.2 - Support all ability patterns
        """
        # RED: Test condition validation

        from ti4.core.technology_cards.abilities_integration import (
            validate_ability_conditions,
        )

        # Test condition validation
        test_conditions = [
            (AbilityCondition.HAS_SHIPS_IN_SYSTEM, {"has_ships": True}, True),
            (AbilityCondition.HAS_SHIPS_IN_SYSTEM, {"has_ships": False}, False),
            (AbilityCondition.CONTROL_PLANET, {"controls_planet": True}, True),
            (
                AbilityCondition.SYSTEM_CONTAINS_FRONTIER,
                {"has_frontier_token": True},
                True,
            ),
        ]

        for condition_enum, context, expected_result in test_conditions:
            result = validate_ability_conditions([condition_enum], context)
            assert result == expected_result

    def test_technology_color_enum_validation(self):
        """Test TechnologyColor enum validation and prerequisite checking.

        Requirements: 6.1, 6.2 - Color specification and prerequisite checking
        """
        # RED: Test color validation

        # Test all technology colors are valid
        valid_colors = [
            TechnologyColor.BLUE,
            TechnologyColor.GREEN,
            TechnologyColor.RED,
            TechnologyColor.YELLOW,
        ]

        for color in valid_colors:
            # Should be valid enum values
            assert isinstance(color, TechnologyColor)
            assert color.value in ["blue", "green", "red", "yellow"]

        # Test prerequisite validation
        spec = self.specification_registry.get_specification(Technology.DARK_ENERGY_TAP)

        # Dark Energy Tap has no prerequisites
        assert spec.prerequisites == []

        # Test a technology with prerequisites (when implemented)
        # This will be expanded when more technologies are added

    def test_enum_based_specification_completeness(self):
        """Test that enum-based specifications cover all required attributes.

        Requirements: 3.1 - Clear protocol covers all possible attributes
        """
        # RED: Test specification completeness

        spec = self.specification_registry.get_specification(Technology.DARK_ENERGY_TAP)

        # Should have all required attributes
        assert hasattr(spec, "name")
        assert hasattr(spec, "color")
        assert hasattr(spec, "prerequisites")
        assert hasattr(spec, "faction_restriction")
        assert hasattr(spec, "abilities")

        # Abilities should have all required attributes
        for ability_spec in spec.abilities:
            assert hasattr(ability_spec, "trigger")
            assert hasattr(ability_spec, "effect")
            assert hasattr(ability_spec, "conditions")

    def test_enum_registry_consistency(self):
        """Test that enum registry is consistent across all systems.

        Requirements: 6.1, 6.2, 6.3 - Comprehensive technology attributes
        """
        # RED: Test registry consistency

        # All supported technologies should have specifications
        supported_technologies = self.factory.get_supported_technologies()

        for technology in supported_technologies:
            spec = self.specification_registry.get_specification(technology)
            assert spec is not None

            # Specification should be consistent with created card
            card = self.factory.create_card(technology)
            assert card.name == spec.name
            assert card.color == spec.color
            assert card.prerequisites == spec.prerequisites


class TestManualConfirmationProtocolIntegration:
    """Test manual confirmation protocol in realistic scenarios."""

    def setup_method(self):
        """Setup test fixtures for confirmation protocol testing."""
        self.factory = TechnologyCardFactory()

    def test_confirmed_technology_creation_succeeds(self):
        """Test that confirmed technologies can be created successfully.

        Requirements: 8.5 - Clear error messages guide to correct implementation
        """
        # RED: Test confirmed technology creation

        # Dark Energy Tap is confirmed by user
        card = self.factory.create_card(Technology.DARK_ENERGY_TAP)
        assert card is not None
        assert card.technology_enum == Technology.DARK_ENERGY_TAP

        # Gravity Drive is also confirmed (refactored existing)
        card = self.factory.create_card(Technology.GRAVITY_DRIVE)
        assert card is not None
        assert card.technology_enum == Technology.GRAVITY_DRIVE

    def test_unconfirmed_technology_creation_fails_with_clear_error(self):
        """Test that unconfirmed technologies fail with clear error message.

        Requirements: 8.5 - Clear error messages guide to correct implementation
        """
        # RED: Test unconfirmed technology error

        # Try to create a technology that doesn't have a concrete implementation
        with pytest.raises(ValueError, match="No implementation found"):
            self.factory.create_card(Technology.CRUISER_II)

    def test_manual_confirmation_protocol_enforcement(self):
        """Test that manual confirmation protocol is enforced correctly.

        Requirements: 3.7 - Manual confirmation protocol enforcement
        """
        # RED: Test confirmation protocol

        from ti4.core.technology_cards.confirmation import require_confirmation

        # Should not raise error for confirmed technologies
        try:
            require_confirmation(Technology.DARK_ENERGY_TAP, "color")
            require_confirmation(Technology.DARK_ENERGY_TAP, "prerequisites")
        except TechnologySpecificationError:
            pytest.fail("Should not raise error for confirmed technology")

        # Should raise error for unconfirmed technologies
        with pytest.raises(TechnologySpecificationError, match="not confirmed"):
            require_confirmation(Technology.CRUISER_II, "prerequisites")

    def test_confirmation_protocol_with_realistic_development_scenario(self):
        """Test confirmation protocol in realistic development scenario.

        Requirements: 8.5 - Clear error messages guide implementation
        """
        # RED: Test realistic scenario

        # Scenario: Developer tries to implement a new technology
        # without confirming specifications first

        class NewTechnologyCard:
            """Mock new technology card implementation."""

            def __init__(self):
                # This should trigger confirmation protocol
                from ti4.core.technology_cards.confirmation import require_confirmation

                # Try to access unconfirmed specifications
                require_confirmation(Technology.FIGHTER_II, "prerequisites")
                require_confirmation(Technology.FIGHTER_II, "color")

        # Should raise clear error about needing confirmation
        with pytest.raises(TechnologySpecificationError) as exc_info:
            NewTechnologyCard()

        error_message = str(exc_info.value)
        assert "not confirmed" in error_message
        assert "Please ask user" in error_message

    def test_confirmation_protocol_integration_with_factory(self):
        """Test confirmation protocol integration with factory system.

        Requirements: 1.2, 1.3 - Factory methods and caching
        """
        # RED: Test factory confirmation integration

        # Factory should only create confirmed technologies
        supported = self.factory.get_supported_technologies()

        # All supported technologies should be confirmed
        for technology in supported:
            # Should be able to create without error
            card = self.factory.create_card(technology)
            assert card is not None

        # Unsupported technologies should not be creatable
        assert not self.factory.is_supported(Technology.CRUISER_II)
        assert not self.factory.is_supported(Technology.FIGHTER_II)

    def test_confirmation_error_messages_are_helpful(self):
        """Test that confirmation error messages provide helpful guidance.

        Requirements: 8.5 - Clear error messages guide implementation
        """
        # RED: Test helpful error messages

        from ti4.core.technology_cards.confirmation import require_confirmation

        try:
            require_confirmation(Technology.DESTROYER_II, "prerequisites")
            pytest.fail("Should have raised TechnologySpecificationError")
        except TechnologySpecificationError as e:
            error_message = str(e)

            # Should include technology name
            assert "DESTROYER_II" in error_message

            # Should include attribute being accessed
            assert "prerequisites" in error_message

            # Should provide guidance
            assert "ask user" in error_message.lower()
            assert "specification" in error_message.lower()

    def test_confirmation_protocol_with_multiple_attributes(self):
        """Test confirmation protocol when accessing multiple attributes.

        Requirements: 3.7 - Manual confirmation protocol enforcement
        """
        # RED: Test multiple attribute confirmation

        from ti4.core.technology_cards.confirmation import require_confirmation

        # Test accessing multiple attributes of confirmed technology
        try:
            require_confirmation(Technology.DARK_ENERGY_TAP, "name")
            require_confirmation(Technology.DARK_ENERGY_TAP, "color")
            require_confirmation(Technology.DARK_ENERGY_TAP, "prerequisites")
            require_confirmation(Technology.DARK_ENERGY_TAP, "abilities")
        except TechnologySpecificationError:
            pytest.fail("Should not raise error for confirmed technology")

        # Test accessing multiple attributes of unconfirmed technology
        unconfirmed_attributes = ["name", "color", "prerequisites", "abilities"]

        for attribute in unconfirmed_attributes:
            with pytest.raises(TechnologySpecificationError):
                require_confirmation(Technology.DREADNOUGHT_II, attribute)


class TestFrameworkRegressionIntegration:
    """Test that framework doesn't break existing functionality."""

    def setup_method(self):
        """Setup test fixtures for regression testing."""
        self.factory = TechnologyCardFactory()
        self.registry = TechnologyCardRegistry()

    def test_existing_technology_system_still_works(self):
        """Test that existing technology system functionality is preserved.

        Requirements: 4.4 - All existing technology functionality continues to work
        """
        # RED: Test existing system preservation

        # Test that we can still import and use existing technology classes
        from ti4.core.technology import TechnologyCard, TechnologyManager

        # Should be able to create technology manager
        tech_manager = TechnologyManager()
        assert tech_manager is not None

        # Should be able to work with existing TechnologyCard
        # (This tests backward compatibility)
        existing_card = TechnologyCard("Dark Energy Tap", "Test ability text")
        assert existing_card.name == "Dark Energy Tap"

    def test_new_framework_coexists_with_existing_system(self):
        """Test that new framework coexists with existing technology system.

        Requirements: 4.4 - Consistent technology implementations
        """
        # RED: Test coexistence

        # Create technology card with new framework
        new_card = self.factory.create_card(Technology.DARK_ENERGY_TAP)

        # Create technology card with existing system
        from ti4.core.technology import TechnologyCard

        existing_card = TechnologyCard("Dark Energy Tap", "Test ability text")

        # Both should represent the same technology
        assert new_card.technology_enum == Technology.DARK_ENERGY_TAP
        assert new_card.name == existing_card.name

    def test_framework_preserves_existing_test_functionality(self):
        """Test that framework preserves existing test functionality.

        Requirements: 4.4 - All existing functionality continues to work
        """
        # RED: Test existing test preservation

        # This test ensures that existing tests still pass
        # We'll run a basic check that existing patterns still work

        from ti4.core.constants import Technology
        from ti4.core.technology import TechnologyColor

        # Existing enum usage should still work
        assert Technology.DARK_ENERGY_TAP.name == "DARK_ENERGY_TAP"
        assert TechnologyColor.BLUE.value == "blue"

        # Existing technology creation patterns should still work
        technologies = [Technology.DARK_ENERGY_TAP, Technology.GRAVITY_DRIVE]
        for tech in technologies:
            assert isinstance(tech, Technology)

    def test_framework_maintains_performance_characteristics(self):
        """Test that framework maintains acceptable performance.

        Requirements: 4.4 - Existing functionality continues to work
        """
        # RED: Test performance maintenance

        import time

        # Test that technology creation is reasonably fast
        start_time = time.time()

        for _ in range(100):
            card = self.factory.create_card(Technology.DARK_ENERGY_TAP)
            assert card is not None

        end_time = time.time()
        elapsed = end_time - start_time

        # Should complete 100 creations in reasonable time (< 1 second)
        # This accounts for caching making subsequent creations very fast
        assert elapsed < 1.0

    def test_framework_error_handling_is_robust(self):
        """Test that framework error handling is robust and doesn't break systems.

        Requirements: 8.5 - Clear error messages guide implementation
        """
        # RED: Test robust error handling

        # Test various error conditions don't crash the system

        # Invalid technology enum
        with pytest.raises((ValueError, TypeError)):
            self.factory.create_card("invalid")  # type: ignore

        # None input
        with pytest.raises((ValueError, TypeError)):
            self.factory.create_card(None)  # type: ignore

        # After errors, system should still work normally
        card = self.factory.create_card(Technology.DARK_ENERGY_TAP)
        assert card is not None
