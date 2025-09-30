"""
Tests for Dark Energy Tap integration with abilities system.

This module tests the integration between Dark Energy Tap technology
and the AbilityManager system, including ability registration, triggering,
and enum mapping.
"""

from unittest.mock import Mock

from ti4.core.abilities import AbilityManager, TimingWindow
from ti4.core.constants import AbilityEffectType, AbilityTrigger, Technology
from ti4.core.game_state import GameState
from ti4.core.technology_cards.concrete.dark_energy_tap import DarkEnergyTap


class TestDarkEnergyTapAbilitiesIntegration:
    """Test Dark Energy Tap integration with abilities system."""

    def setup_method(self):
        """Setup test fixtures."""
        self.game_state = GameState()
        self.ability_manager = AbilityManager(self.game_state)
        self.dark_energy_tap = DarkEnergyTap()

    def test_dark_energy_tap_registers_abilities_with_manager(self):
        """Test Dark Energy Tap registers its abilities with AbilityManager."""
        # RED: Test ability registration
        initial_count = len(self.ability_manager.abilities)

        # Register Dark Energy Tap abilities
        self.dark_energy_tap.register_with_systems(self.ability_manager, None)

        # Should have registered 2 abilities
        assert len(self.ability_manager.abilities) == initial_count + 2

    def test_ability_trigger_enum_mapping_to_timing_window(self):
        """Test AbilityTrigger enums map correctly to TimingWindow enums."""
        # RED: Test enum mapping
        from ti4.core.technology_cards.abilities_integration import (
            map_trigger_to_timing,
        )

        # Test specific mappings for Dark Energy Tap
        assert (
            map_trigger_to_timing(AbilityTrigger.AFTER_TACTICAL_ACTION)
            == TimingWindow.AFTER
        )
        assert (
            map_trigger_to_timing(AbilityTrigger.WHEN_RETREAT_DECLARED)
            == TimingWindow.WHEN
        )

    def test_ability_effect_enum_mapping_to_game_effects(self):
        """Test AbilityEffectType enums map to actual game effects."""
        # RED: Test effect mapping
        from ti4.core.technology_cards.abilities_integration import (
            map_effect_to_handler,
        )

        # Test specific mappings for Dark Energy Tap
        frontier_handler = map_effect_to_handler(
            AbilityEffectType.EXPLORE_FRONTIER_TOKEN
        )
        retreat_handler = map_effect_to_handler(
            AbilityEffectType.ALLOW_RETREAT_TO_EMPTY_ADJACENT
        )

        assert frontier_handler is not None
        assert retreat_handler is not None
        assert callable(frontier_handler)
        assert callable(retreat_handler)

    def test_dark_energy_tap_frontier_exploration_triggers_correctly(self):
        """Test Dark Energy Tap frontier exploration ability triggers through AbilityManager."""
        # RED: Test ability triggering
        self.dark_energy_tap.register_with_systems(self.ability_manager, None)

        # Create context for tactical action in frontier system
        context = {
            "player": Mock(),
            "system_id": "test_system",
            "has_ships": True,
            "has_frontier_token": True,
        }

        # Trigger the event
        result = self.ability_manager.trigger_event(
            "tactical_action_in_frontier_system", context
        )

        # Should have resolved the frontier exploration ability
        assert result.success
        assert len(result.resolved_abilities) >= 1

        # Find the frontier exploration ability
        frontier_ability = None
        for ability in result.resolved_abilities:
            if "frontier" in ability.name.lower():
                frontier_ability = ability
                break

        assert frontier_ability is not None

    def test_dark_energy_tap_retreat_enhancement_triggers_correctly(self):
        """Test Dark Energy Tap retreat enhancement ability triggers through AbilityManager."""
        # RED: Test ability triggering
        self.dark_energy_tap.register_with_systems(self.ability_manager, None)

        # Create context for retreat declaration
        context = {"player": Mock(), "combat_id": "test_combat"}

        # Trigger the event
        result = self.ability_manager.trigger_event("retreat_declared", context)

        # Should have resolved the retreat enhancement ability
        assert result.success
        assert len(result.resolved_abilities) >= 1

        # Find the retreat enhancement ability
        retreat_ability = None
        for ability in result.resolved_abilities:
            if "retreat" in ability.name.lower():
                retreat_ability = ability
                break

        assert retreat_ability is not None

    def test_ability_resolution_through_manager(self):
        """Test abilities resolve correctly through AbilityManager."""
        # RED: Test ability resolution
        self.dark_energy_tap.register_with_systems(self.ability_manager, None)

        # Get the registered abilities
        registered_abilities = [
            ability
            for ability in self.ability_manager.abilities
            if "Dark Energy Tap" in getattr(ability, "source", "")
        ]

        # Should have 2 registered abilities
        assert len(registered_abilities) >= 2

    def test_enum_based_ability_creation(self):
        """Test abilities are created using enum-based specifications."""
        # RED: Test enum-based creation
        from ti4.core.technology_cards.abilities_integration import (
            create_ability_from_specification,
        )
        from ti4.core.technology_cards.specifications import (
            TechnologySpecificationRegistry,
        )

        registry = TechnologySpecificationRegistry()
        spec = registry.get_specification(Technology.DARK_ENERGY_TAP)

        # Create abilities from specification
        abilities = []
        for ability_spec in spec.abilities:
            ability = create_ability_from_specification(ability_spec)
            abilities.append(ability)

        # Should have created 2 abilities
        assert len(abilities) == 2

        # Check that abilities have correct properties
        ability_names = [ability.name for ability in abilities]
        assert any("frontier" in name.lower() for name in ability_names)
        assert any("retreat" in name.lower() for name in ability_names)

    def test_ability_frequency_and_timing_enforcement(self):
        """Test ability frequency and timing are enforced correctly."""
        # RED: Test frequency enforcement
        self.dark_energy_tap.register_with_systems(self.ability_manager, None)

        # Create context for frontier exploration
        context = {
            "player": Mock(),
            "system_id": "test_system",
            "has_ships": True,
            "has_frontier_token": True,
            "occurrence_id": 1,
        }

        # Trigger the event twice with same occurrence_id
        result1 = self.ability_manager.trigger_event(
            "tactical_action_in_frontier_system", context
        )
        result2 = self.ability_manager.trigger_event(
            "tactical_action_in_frontier_system", context
        )

        # First should succeed, second should not trigger (ONCE_PER_TRIGGER)
        assert result1.success
        # For ONCE_PER_TRIGGER, same occurrence_id should not trigger again
        assert len(result2.resolved_abilities) == 0

    def test_ability_conditions_validation(self):
        """Test ability conditions are validated correctly."""
        # RED: Test condition validation
        self.dark_energy_tap.register_with_systems(self.ability_manager, None)

        # Create context without required conditions
        context_no_ships = {
            "player": Mock(),
            "system_id": "test_system",
            "has_ships": False,  # Missing required condition
            "has_frontier_token": True,
        }

        # Should not trigger without required conditions
        result = self.ability_manager.trigger_event(
            "tactical_action_in_frontier_system", context_no_ships
        )

        # Should not resolve frontier exploration ability due to missing condition
        frontier_abilities = [
            ability
            for ability in result.resolved_abilities
            if "frontier" in ability.name.lower()
        ]
        assert len(frontier_abilities) == 0

    def test_multiple_technology_abilities_coexist(self):
        """Test multiple technology abilities can coexist in AbilityManager."""
        # RED: Test multiple technologies
        self.dark_energy_tap.register_with_systems(self.ability_manager, None)

        # Create a mock second technology with abilities
        class MockTechnology:
            def register_with_systems(self, ability_manager, unit_stats_provider):
                from ti4.core.abilities import Ability, AbilityEffect

                test_ability = Ability(
                    name="Test Ability",
                    timing=TimingWindow.ACTION,
                    trigger="test_trigger",
                    effect=AbilityEffect(type="test_effect", value=True),
                )
                ability_manager.add_ability(test_ability)

        mock_tech = MockTechnology()
        mock_tech.register_with_systems(self.ability_manager, None)

        # Should have abilities from both technologies
        assert (
            len(self.ability_manager.abilities) >= 3
        )  # 2 from Dark Energy Tap + 1 from mock

    def test_ability_manager_integration_error_handling(self):
        """Test error handling in ability manager integration."""
        # RED: Test error handling

        # Test with invalid ability manager
        try:
            self.dark_energy_tap.register_with_systems(None, None)
            assert False, "Should have raised an error"
        except (AttributeError, TypeError):
            pass  # Expected error

        # Test with mock that raises errors
        class ErrorAbilityManager:
            def add_ability(self, ability):
                raise RuntimeError("Test error")

        error_manager = ErrorAbilityManager()

        # Should handle registration errors gracefully
        try:
            self.dark_energy_tap.register_with_systems(error_manager, None)
            assert False, "Should have raised an error"
        except RuntimeError:
            pass  # Expected error
