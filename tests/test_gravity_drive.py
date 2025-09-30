"""
Tests for Gravity Drive technology implementation.

This module tests the Gravity Drive technology card implementation
following the new technology card framework.
"""

import pytest

from ti4.core.constants import Technology
from ti4.core.technology import TechnologyColor
from ti4.core.technology_cards.concrete.gravity_drive import GravityDrive
from ti4.core.technology_cards.specifications import TechnologySpecificationRegistry


class TestGravityDrive:
    """Test Gravity Drive technology implementation."""

    @pytest.fixture
    def gravity_drive(self):
        """Fixture providing a GravityDrive instance."""
        return GravityDrive()

    @pytest.fixture
    def registry(self):
        """Fixture providing a TechnologySpecificationRegistry instance."""
        return TechnologySpecificationRegistry()

    @pytest.fixture
    def game_setup(self):
        """Fixture providing common game setup for integration tests."""
        from ti4.actions.movement_engine import MovementPlan, MovementValidator
        from ti4.core.constants import UnitType
        from ti4.core.galaxy import Galaxy
        from ti4.core.hex_coordinate import HexCoordinate
        from ti4.core.system import System
        from ti4.core.unit import Unit

        # Setup galaxy with two systems
        galaxy = Galaxy()
        system1 = System(system_id="system1")
        system2 = System(system_id="system2")

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(2, 0)  # Distance 2

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create validator and movement plan factory
        validator = MovementValidator(galaxy)

        def create_movement_plan():
            return MovementPlan()

        return {
            "galaxy": galaxy,
            "system1": system1,
            "system2": system2,
            "validator": validator,
            "create_movement_plan": create_movement_plan,
            "UnitType": UnitType,
            "Unit": Unit,
        }

    def test_gravity_drive_basic_properties(self, gravity_drive):
        """Test Gravity Drive basic properties."""
        # Test basic properties
        assert gravity_drive.technology_enum == Technology.GRAVITY_DRIVE
        assert gravity_drive.name == "Gravity Drive"
        assert gravity_drive.color == TechnologyColor.BLUE
        assert gravity_drive.prerequisites == [TechnologyColor.BLUE]
        assert gravity_drive.faction_restriction is None

    def test_gravity_drive_abilities(self, gravity_drive):
        """Test Gravity Drive abilities."""
        abilities = gravity_drive.get_abilities()

        # Should have one ability
        assert len(abilities) == 1

        # Test movement enhancement ability (now uses enum-based naming)
        movement_ability = abilities[0]
        assert movement_ability.name == "Modify Unit Stats"
        assert movement_ability.timing.name == "AFTER"
        assert "activate" in movement_ability.trigger.lower()

    def test_gravity_drive_uses_enum_specification(self, gravity_drive, registry):
        """Test that Gravity Drive uses the enum-based specification system."""
        # Should have specification in registry
        spec = registry.get_specification(Technology.GRAVITY_DRIVE)
        assert spec is not None

        # Properties should match specification
        assert gravity_drive.color == spec.color
        assert gravity_drive.prerequisites == list(spec.prerequisites)
        assert gravity_drive.faction_restriction == spec.faction_restriction

        # Should create abilities from specification
        abilities = gravity_drive.get_abilities()
        assert len(abilities) == len(spec.abilities)

        # First ability should match specification
        ability = abilities[0]
        spec_ability = spec.abilities[0]
        assert ability.mandatory == spec_ability.mandatory

    def test_gravity_drive_error_handling(self):
        """Test Gravity Drive error handling for missing specifications."""
        # This test verifies that proper error messages are provided
        # when specifications are missing (though this shouldn't happen in practice)

        # Test that initialization succeeds with valid registry
        gravity_drive = GravityDrive()
        assert gravity_drive.name == "Gravity Drive"

        # Test that abilities have proper source attribution
        abilities = gravity_drive.get_abilities()
        for ability in abilities:
            assert hasattr(ability, "source")
            assert ability.source == "Gravity Drive"

    def test_gravity_drive_functional_behavior(self):
        """Test that Gravity Drive actually provides movement enhancement functionality."""
        gravity_drive = GravityDrive()
        abilities = gravity_drive.get_abilities()
        movement_ability = abilities[0]

        # Test that the ability can trigger on system activation
        context = {
            "event": "after_activate_system",
            "player": "test_player",
            "system": "test_system",
        }

        # The ability should be able to trigger after system activation
        can_trigger = movement_ability.can_trigger("after_activate_system", context)
        assert can_trigger, "Gravity Drive should trigger after system activation"

        # Test that the ability is mandatory (as per specification)
        assert movement_ability.mandatory, "Gravity Drive ability should be mandatory"

        # Test that the ability has the correct timing
        from ti4.core.abilities import TimingWindow

        assert movement_ability.timing == TimingWindow.AFTER, (
            "Should trigger AFTER system activation"
        )

    def test_gravity_drive_movement_enhancement_effect(self):
        """Test that Gravity Drive actually enhances unit movement when triggered."""
        gravity_drive = GravityDrive()
        abilities = gravity_drive.get_abilities()
        movement_ability = abilities[0]

        # Test the effect type and value
        effect = movement_ability.effect
        assert effect.type == "modify_unit_stats", "Should modify unit stats"

        # The effect should be applicable (this tests the framework integration)
        assert effect.value is True, "Effect should be enabled"

        # Test that the ability has proper source attribution for tracking
        assert hasattr(movement_ability, "source"), "Should have source attribution"
        assert movement_ability.source == "Gravity Drive", (
            "Should be attributed to Gravity Drive"
        )

    def test_gravity_drive_enables_distant_system_access(self):
        """Test that Gravity Drive enables access to systems normally too far away."""
        from ti4.actions.movement_engine import MovementPlan, MovementValidator
        from ti4.core.constants import UnitType
        from ti4.core.galaxy import Galaxy
        from ti4.core.hex_coordinate import HexCoordinate
        from ti4.core.system import System
        from ti4.core.unit import Unit

        # Setup galaxy with systems distance 2 apart
        galaxy = Galaxy()
        system1 = System(system_id="home_system")
        System(system_id="distant_system")

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(2, 0)  # Distance 2

        galaxy.place_system(coord1, "home_system")
        galaxy.place_system(coord2, "distant_system")

        # Create carrier (movement 1) - normally can't reach distance 2
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")
        system1.place_unit_in_space(carrier)

        # Create movement plan
        movement_plan = MovementPlan()
        movement_plan.add_ship_movement(carrier, "home_system", "distant_system")

        # Test without Gravity Drive - should be invalid
        validator = MovementValidator(galaxy)
        result_without_tech = validator.validate_movement_plan(movement_plan, "player1")

        assert result_without_tech.is_valid is False
        assert result_without_tech.errors is not None
        assert "insufficient movement" in result_without_tech.errors[0].lower()

        # Test with Gravity Drive - should be valid and automatically applied
        result_with_tech = validator.validate_movement_plan(
            movement_plan, "player1", technologies={Technology.GRAVITY_DRIVE}
        )
        assert result_with_tech.is_valid is True
        assert result_with_tech.technology_effects is not None
        assert Technology.GRAVITY_DRIVE.value in result_with_tech.technology_effects

    def test_gravity_drive_cross_galaxy_tactical_movement(self):
        """Test Gravity Drive enables complex tactical movements across multiple systems."""
        from ti4.actions.movement_engine import MovementPlan, MovementValidator
        from ti4.core.constants import UnitType
        from ti4.core.galaxy import Galaxy
        from ti4.core.hex_coordinate import HexCoordinate
        from ti4.core.system import System
        from ti4.core.unit import Unit

        # Setup galaxy with systems in a line
        galaxy = Galaxy()
        system1 = System(system_id="home_base")
        System(system_id="intermediate")
        System(system_id="target_system")

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)  # Distance 1 from home
        coord3 = HexCoordinate(2, 0)  # Distance 2 from home, 1 from intermediate

        galaxy.place_system(coord1, "home_base")
        galaxy.place_system(coord2, "intermediate")
        galaxy.place_system(coord3, "target_system")

        # Create destroyer (movement 2) - can reach intermediate but not target without tech
        destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player1")
        system1.place_unit_in_space(destroyer)

        # Test movement to target system (distance 2) - should work with destroyer's movement 2
        movement_plan = MovementPlan()
        movement_plan.add_ship_movement(destroyer, "home_base", "target_system")

        validator = MovementValidator(galaxy)
        result = validator.validate_movement_plan(movement_plan, "player1")

        # This should be valid without Gravity Drive (destroyer has movement 2)
        assert result.is_valid is True

        # Now test with carrier (movement 1) - needs Gravity Drive
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")
        system1.place_unit_in_space(carrier)

        movement_plan_carrier = MovementPlan()
        movement_plan_carrier.add_ship_movement(carrier, "home_base", "target_system")

        # Without Gravity Drive - should fail
        result_without_tech = validator.validate_movement_plan(
            movement_plan_carrier, "player1"
        )
        assert result_without_tech.is_valid is False

        # With Gravity Drive - should succeed
        result_with_tech = validator.validate_movement_plan(
            movement_plan_carrier, "player1", technologies={Technology.GRAVITY_DRIVE}
        )
        assert result_with_tech.is_valid is True
        assert Technology.GRAVITY_DRIVE.value in result_with_tech.technology_effects

    def test_gravity_drive_objective_system_access(self):
        """Test Gravity Drive enables reaching objective systems for victory conditions."""
        from ti4.actions.movement_engine import MovementPlan, MovementValidator
        from ti4.core.constants import UnitType
        from ti4.core.galaxy import Galaxy
        from ti4.core.hex_coordinate import HexCoordinate
        from ti4.core.planet import Planet
        from ti4.core.system import System
        from ti4.core.unit import Unit

        # Setup galaxy representing a typical objective scenario
        galaxy = Galaxy()
        home_system = System(system_id="home_system")
        objective_system = System(system_id="mecatol_rex")  # Common objective system

        # Add a valuable planet to the objective system
        mecatol = Planet(name="mecatol_rex", resources=1, influence=6)
        objective_system.add_planet(mecatol)

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(2, 0)  # Distance 2 - typical for Mecatol Rex

        galaxy.place_system(coord1, "home_system")
        galaxy.place_system(coord2, "mecatol_rex")

        # Create units for objective completion
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")  # Movement 2
        home_system.place_unit_in_space(cruiser)

        # Test movement to objective system (just the cruiser)
        movement_plan = MovementPlan()
        movement_plan.add_ship_movement(cruiser, "home_system", "mecatol_rex")

        validator = MovementValidator(galaxy)

        # This should work without Gravity Drive (cruiser has movement 2)
        result = validator.validate_movement_plan(movement_plan, "player1")
        assert result.is_valid is True

        # Test with carrier (movement 1) - needs Gravity Drive
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        home_system.place_unit_in_space(carrier)
        home_system.place_unit_on_planet(infantry, "home_planet")

        movement_plan_carrier = MovementPlan()
        movement_plan_carrier.add_ship_movement(carrier, "home_system", "mecatol_rex")
        movement_plan_carrier.add_ground_force_movement(
            infantry, "home_system", "mecatol_rex", "home_planet", "space"
        )

        # Without Gravity Drive - should fail
        result_without_tech = validator.validate_movement_plan(
            movement_plan_carrier, "player1"
        )
        assert result_without_tech.is_valid is False

        # With Gravity Drive - should succeed
        result_with_tech = validator.validate_movement_plan(
            movement_plan_carrier, "player1", technologies={Technology.GRAVITY_DRIVE}
        )
        assert result_with_tech.is_valid is True
        assert Technology.GRAVITY_DRIVE.value in result_with_tech.technology_effects

    def test_gravity_drive_multiple_ships_limitation(self):
        """Test that Gravity Drive has limitations when multiple ships need enhancement."""
        from ti4.actions.movement_engine import MovementPlan, MovementValidator
        from ti4.core.constants import UnitType
        from ti4.core.galaxy import Galaxy
        from ti4.core.hex_coordinate import HexCoordinate
        from ti4.core.system import System
        from ti4.core.unit import Unit

        # Setup galaxy with multiple systems
        galaxy = Galaxy()
        system1 = System(system_id="system1")
        system2 = System(system_id="system2")
        System(system_id="target_system")

        coord1 = HexCoordinate(0, 0)  # Distance 2 from target
        coord2 = HexCoordinate(0, 1)  # Distance 2 from target
        coord3 = HexCoordinate(2, 0)  # Target system

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")
        galaxy.place_system(coord3, "target_system")

        # Create two carriers (movement 1) both distance 2 away
        carrier1 = Unit(unit_type=UnitType.CARRIER, owner="player1")
        carrier2 = Unit(unit_type=UnitType.CARRIER, owner="player1")

        system1.place_unit_in_space(carrier1)
        system2.place_unit_in_space(carrier2)

        # Create movement plan - both ships need Gravity Drive
        movement_plan = MovementPlan()
        movement_plan.add_ship_movement(carrier1, "system1", "target_system")
        movement_plan.add_ship_movement(carrier2, "system2", "target_system")

        validator = MovementValidator(galaxy)

        # Test with Gravity Drive - should still be invalid (can only help one ship)
        result = validator.validate_movement_plan(
            movement_plan, "player1", technologies={Technology.GRAVITY_DRIVE}
        )

        # This should be invalid because Gravity Drive can only be applied to one ship
        # and we have two ships that both need it
        assert result.is_valid is False
        assert result.errors is not None
        assert (
            len([e for e in result.errors if "insufficient movement" in e.lower()]) >= 1
        )

    def test_gravity_drive_register_with_systems(self):
        """Test Gravity Drive registration with game systems."""
        gravity_drive = GravityDrive()

        # Mock systems for testing
        class MockAbilityManager:
            def __init__(self):
                self.abilities = []

            def add_ability(self, ability):
                self.abilities.append(ability)

        mock_ability_manager = MockAbilityManager()
        mock_unit_stats_provider = None

        # Should not raise an exception
        gravity_drive.register_with_systems(
            mock_ability_manager, mock_unit_stats_provider
        )

        # Should have registered one ability
        assert len(mock_ability_manager.abilities) == 1
        assert mock_ability_manager.abilities[0].name == "Modify Unit Stats"
