"""Tests for TI4 Tactical Action implementation."""

from typing import Any, Optional

import pytest

from ti4.core.constants import UnitType
from ti4.core.galaxy import Galaxy
from ti4.core.hex_coordinate import HexCoordinate
from ti4.core.planet import Planet
from ti4.core.system import System
from ti4.core.unit import Unit


class TestTacticalAction:
    """Test the proper two-step tactical action structure."""

    def test_tactical_action_creation(self) -> None:
        """Test that TacticalAction can be created with active system."""
        from ti4.actions.movement_engine import TacticalAction

        # RED: This should fail because TacticalAction doesn't exist yet
        tactical_action = TacticalAction(
            active_system_id="system1", player_id="player1"
        )

        assert tactical_action.active_system_id == "system1"
        assert tactical_action.player_id == "player1"

        # Initialize steps for the new architecture
        tactical_action.initialize_steps()

        # Test new step-based architecture
        assert len(tactical_action.steps) >= 2
        step_names = [step.get_step_name() for step in tactical_action.steps]
        assert "Movement" in step_names
        assert "Commit Ground Forces" in step_names

    def test_extensible_step_architecture(self) -> None:
        """Test that the new step-based architecture is extensible."""
        from ti4.actions.movement_engine import TacticalAction, TacticalActionStep

        # Create a custom step for testing
        class TestStep(TacticalActionStep):
            def can_execute(self, game_state, context) -> None:
                return True

            def execute(self, game_state, context) -> None:
                return game_state

            def get_step_name(self) -> None:
                return "Test Step"

        tactical_action = TacticalAction("system1", "player1")
        tactical_action.initialize_steps()

        # Test adding custom steps
        initial_count = len(tactical_action.steps)
        tactical_action.add_step(TestStep())
        assert len(tactical_action.steps) == initial_count + 1

        # Test step execution control
        step_names = tactical_action.get_executable_steps(None)
        assert "Test Step" in step_names

        # Test step removal
        assert tactical_action.remove_step("Test Step") is True
        assert len(tactical_action.steps) == initial_count

    def test_movement_step_moves_units_to_space_area(self) -> None:
        """Test that Movement Step moves all units to the active system's space area."""
        from ti4.actions.movement_engine import MovementPlan, TacticalAction

        # Setup galaxy with two systems
        galaxy = Galaxy()
        system1 = System(system_id="system1")
        system2 = System(system_id="system2")

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)  # Adjacent

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create units in system1
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player1")
        system1.place_unit_in_space(cruiser)
        system1.place_unit_in_space(destroyer)

        # Create movement plan to move units to system2 (active system)
        movement_plan = MovementPlan()
        movement_plan.add_ship_movement(cruiser, "system1", "system2")
        movement_plan.add_ship_movement(destroyer, "system1", "system2")

        # Create tactical action
        tactical_action = TacticalAction(
            active_system_id="system2", player_id="player1"
        )

        # Execute movement step using new architecture
        tactical_action.initialize_steps()
        tactical_action.set_movement_plan(movement_plan)

        game_state = MockGameState(
            galaxy=galaxy, systems={"system1": system1, "system2": system2}
        )
        new_state = tactical_action.execute_step("Movement", game_state)

        # RED: This should fail because the classes don't exist yet
        # Units should be moved to system2's space area
        assert cruiser in new_state.systems["system2"].space_units
        assert destroyer in new_state.systems["system2"].space_units
        assert cruiser not in new_state.systems["system1"].space_units
        assert destroyer not in new_state.systems["system1"].space_units

    def test_ground_forces_cannot_move_directly_between_planets(self) -> None:
        """Test that ground forces cannot move directly from planet to planet."""
        from ti4.actions.movement_engine import (
            MovementPlan,
            MovementValidationError,
        )

        # Setup system with two planets
        galaxy = Galaxy()
        system1 = System(system_id="system1")
        planet1 = Planet(name="planet1", resources=2, influence=1)
        planet2 = Planet(name="planet2", resources=1, influence=2)
        system1.add_planet(planet1)
        system1.add_planet(planet2)

        coord1 = HexCoordinate(0, 0)
        galaxy.place_system(coord1, "system1")

        # Create infantry on planet1
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        system1.place_unit_on_planet(infantry, "planet1")

        # Attempt to create movement plan with direct planet-to-planet movement
        movement_plan = MovementPlan()

        # RED: This should fail because direct planet-to-planet movement is invalid
        with pytest.raises(
            MovementValidationError,
            match="Ground forces cannot move directly between planets",
        ):
            movement_plan.add_ground_force_movement(
                infantry,
                from_system="system1",
                to_system="system1",
                from_location="planet1",
                to_location="planet2",  # Direct planet-to-planet - INVALID
            )

    def test_joint_movement_validation(self) -> None:
        """Test that movement validation is performed jointly for entire plan."""
        from ti4.actions.movement_engine import MovementPlan, MovementValidator

        # Setup galaxy
        galaxy = Galaxy()
        system1 = System(system_id="system1")
        System(system_id="system2")

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)  # Adjacent

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create carrier and infantry
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")  # Capacity 4
        infantry1 = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        infantry2 = Unit(unit_type=UnitType.INFANTRY, owner="player1")

        system1.place_unit_in_space(carrier)
        system1.place_unit_on_planet(infantry1, "planet1")
        system1.place_unit_on_planet(infantry2, "planet1")

        # Create movement plan
        movement_plan = MovementPlan()
        movement_plan.add_ship_movement(carrier, "system1", "system2")
        movement_plan.add_ground_force_movement(
            infantry1, "system1", "system2", "planet1", "space"
        )
        movement_plan.add_ground_force_movement(
            infantry2, "system1", "system2", "planet1", "space"
        )

        # Validate entire plan jointly
        validator = MovementValidator(galaxy)

        # RED: This should fail because the validator doesn't exist yet
        validation_result = validator.validate_movement_plan(movement_plan, "player1")
        assert validation_result.is_valid is True
        assert validation_result.transport_assignments is not None

    def test_commit_ground_forces_step(self) -> None:
        """Test that Commit Ground Forces Step moves ground forces from space to planets."""
        from ti4.actions.movement_engine import (
            CommitGroundForcesPlan,
            TacticalAction,
        )

        # Setup system with planets
        galaxy = Galaxy()
        system1 = System(system_id="system1")
        planet1 = Planet(name="planet1", resources=2, influence=1)
        planet2 = Planet(name="planet2", resources=1, influence=2)
        system1.add_planet(planet1)
        system1.add_planet(planet2)

        coord1 = HexCoordinate(0, 0)
        galaxy.place_system(coord1, "system1")

        # Create ground forces in space area
        infantry1 = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        infantry2 = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        system1.place_unit_in_space(infantry1)
        system1.place_unit_in_space(infantry2)

        # Create commit plan
        commit_plan = CommitGroundForcesPlan()
        commit_plan.add_commitment(infantry1, "planet1")
        commit_plan.add_commitment(infantry2, "planet2")

        # Execute commit step using new architecture
        tactical_action = TacticalAction("system1", "player1")
        tactical_action.initialize_steps()
        tactical_action.set_commit_plan(commit_plan)

        game_state = MockGameState(galaxy=galaxy, systems={"system1": system1})
        tactical_action.execute_step("Commit Ground Forces", game_state)

        # RED: This should fail because CommitGroundForcesPlan doesn't exist yet
        # Ground forces should be moved from space to planets
        assert infantry1 in planet1.units
        assert infantry2 in planet2.units
        assert infantry1 not in system1.space_units
        assert infantry2 not in system1.space_units

    def test_complete_tactical_action_sequence(self) -> None:
        """Test a complete tactical action with both movement and commit steps."""
        from ti4.actions.movement_engine import (
            CommitGroundForcesPlan,
            MovementPlan,
            TacticalAction,
        )

        # Setup two systems
        galaxy = Galaxy()
        system1 = System(system_id="system1")
        system2 = System(system_id="system2")
        planet1 = Planet(name="planet1", resources=2, influence=1)
        planet2 = Planet(name="planet2", resources=1, influence=2)
        system1.add_planet(planet1)
        system2.add_planet(planet2)

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)  # Adjacent

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create units: carrier and infantry on planet1
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        system1.place_unit_in_space(carrier)
        system1.place_unit_on_planet(infantry, "planet1")

        # Create movement plan: move carrier and infantry to system2
        movement_plan = MovementPlan()
        movement_plan.add_ship_movement(carrier, "system1", "system2")
        movement_plan.add_ground_force_movement(
            infantry, "system1", "system2", "planet1", "space"
        )

        # Create commit plan: commit infantry to planet2 in system2
        commit_plan = CommitGroundForcesPlan()
        commit_plan.add_commitment(infantry, "planet2")

        # Execute complete tactical action using new architecture
        tactical_action = TacticalAction(
            active_system_id="system2", player_id="player1"
        )
        tactical_action.initialize_steps()
        tactical_action.set_movement_plan(movement_plan)
        tactical_action.set_commit_plan(commit_plan)

        game_state = MockGameState(
            galaxy=galaxy, systems={"system1": system1, "system2": system2}
        )

        # Step 1: Movement
        state_after_movement = tactical_action.execute_step("Movement", game_state)

        # Step 2: Commit Ground Forces
        tactical_action.execute_step("Commit Ground Forces", state_after_movement)

        # RED: This should fail because the commit step doesn't work yet
        # Verify final positions
        assert carrier in system2.space_units
        assert infantry in planet2.units
        assert carrier not in system1.space_units
        assert infantry not in planet1.units
        assert infantry not in system2.space_units  # Should be on planet, not in space

    def test_automatic_technology_effect_calculation(self) -> None:
        """Test that technology effects like Gravity Drive are automatically applied."""
        from ti4.actions.movement_engine import MovementPlan, MovementValidator

        # Setup galaxy with systems distance 2 apart
        galaxy = Galaxy()
        system1 = System(system_id="system1")
        System(system_id="system2")

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(2, 0)  # Distance 2

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create carrier (movement 1) - normally can't reach distance 2
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")
        system1.place_unit_in_space(carrier)

        # Create movement plan
        movement_plan = MovementPlan()
        movement_plan.add_ship_movement(carrier, "system1", "system2")

        # Test without Gravity Drive - should be invalid
        validator = MovementValidator(galaxy)
        result_without_tech = validator.validate_movement_plan(movement_plan, "player1")

        # RED: This should fail because we need to implement proper validation
        assert result_without_tech.is_valid is False
        assert result_without_tech.errors is not None
        assert "insufficient movement" in result_without_tech.errors[0].lower()

        # Test with Gravity Drive - should be valid and automatically applied
        result_with_tech = validator.validate_movement_plan(
            movement_plan, "player1", technologies={"gravity_drive"}
        )
        assert result_with_tech.is_valid is True
        assert result_with_tech.technology_effects is not None
        assert "gravity_drive" in result_with_tech.technology_effects

    def test_transport_capacity_validation(self) -> None:
        """Test that transport capacity is validated in joint movement planning."""
        from ti4.actions.movement_engine import MovementPlan, MovementValidator

        # Setup galaxy
        galaxy = Galaxy()
        system1 = System(system_id="system1")
        System(system_id="system2")
        planet1 = Planet(name="planet1", resources=2, influence=1)
        system1.add_planet(planet1)

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)  # Adjacent

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create destroyer (capacity 0) and 2 infantry
        destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player1")
        infantry1 = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        infantry2 = Unit(unit_type=UnitType.INFANTRY, owner="player1")

        system1.place_unit_in_space(destroyer)
        system1.place_unit_on_planet(infantry1, "planet1")
        system1.place_unit_on_planet(infantry2, "planet1")

        # Create movement plan - try to transport 2 infantry with destroyer (capacity 0)
        movement_plan = MovementPlan()
        movement_plan.add_ship_movement(destroyer, "system1", "system2")
        movement_plan.add_ground_force_movement(
            infantry1, "system1", "system2", "planet1", "space"
        )
        movement_plan.add_ground_force_movement(
            infantry2, "system1", "system2", "planet1", "space"
        )

        # Validate - should fail due to insufficient capacity
        validator = MovementValidator(galaxy)
        result = validator.validate_movement_plan(movement_plan, "player1")

        # This should fail because destroyer has 0 capacity but we're trying to transport 2 infantry
        assert result.is_valid is False
        assert result.errors is not None
        assert "insufficient transport capacity" in result.errors[0].lower()

    def test_joint_movement_validation_with_sufficient_capacity(self) -> None:
        """Test that joint movement validation passes with sufficient transport capacity."""
        from ti4.actions.movement_engine import MovementPlan, MovementValidator

        # Setup galaxy
        galaxy = Galaxy()
        system1 = System(system_id="system1")
        System(system_id="system2")
        planet1 = Planet(name="planet1", resources=2, influence=1)
        system1.add_planet(planet1)

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)  # Adjacent

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create carrier (capacity 4) and 2 infantry
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")
        infantry1 = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        infantry2 = Unit(unit_type=UnitType.INFANTRY, owner="player1")

        system1.place_unit_in_space(carrier)
        system1.place_unit_on_planet(infantry1, "planet1")
        system1.place_unit_on_planet(infantry2, "planet1")

        # Create movement plan - transport 2 infantry with carrier (capacity 4)
        movement_plan = MovementPlan()
        movement_plan.add_ship_movement(carrier, "system1", "system2")
        movement_plan.add_ground_force_movement(
            infantry1, "system1", "system2", "planet1", "space"
        )
        movement_plan.add_ground_force_movement(
            infantry2, "system1", "system2", "planet1", "space"
        )

        # Validate - should pass with sufficient capacity
        validator = MovementValidator(galaxy)
        result = validator.validate_movement_plan(movement_plan, "player1")

        # This should pass because carrier has capacity 4 and we're only transporting 2 infantry
        assert result.is_valid is True
        assert result.transport_assignments is not None

    def test_complete_ti4_tactical_action_validation(self) -> None:
        """Test that the complete TI4 tactical action structure is properly enforced."""
        from ti4.actions.movement_engine import (
            CommitGroundForcesPlan,
            MovementPlan,
            MovementValidator,
            TacticalAction,
        )

        # Setup galaxy with two systems
        galaxy = Galaxy()
        system1 = System(system_id="system1")
        system2 = System(system_id="system2")
        planet1 = Planet(name="planet1", resources=2, influence=1)
        planet2 = Planet(name="planet2", resources=1, influence=2)
        system1.add_planet(planet1)
        system2.add_planet(planet2)

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)  # Adjacent

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create units: carrier and infantry on planet1
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        system1.place_unit_in_space(carrier)
        system1.place_unit_on_planet(infantry, "planet1")

        # Step 1: Create and validate movement plan
        movement_plan = MovementPlan()
        movement_plan.add_ship_movement(carrier, "system1", "system2")
        movement_plan.add_ground_force_movement(
            infantry, "system1", "system2", "planet1", "space"
        )

        # Validate the movement plan jointly
        validator = MovementValidator(galaxy)
        validation_result = validator.validate_movement_plan(movement_plan, "player1")
        assert validation_result.is_valid is True

        # Step 2: Execute the tactical action
        tactical_action = TacticalAction(
            active_system_id="system2", player_id="player1"
        )
        game_state = MockGameState(
            galaxy=galaxy, systems={"system1": system1, "system2": system2}
        )

        # Execute movement step using new architecture
        tactical_action.initialize_steps()
        tactical_action.set_movement_plan(movement_plan)

        state_after_movement = tactical_action.execute_step("Movement", game_state)

        # Verify units are in system2's space area
        assert carrier in state_after_movement.systems["system2"].space_units
        assert infantry in state_after_movement.systems["system2"].space_units
        assert carrier not in state_after_movement.systems["system1"].space_units
        assert infantry not in planet1.units

        # Step 3: Create and execute commit ground forces plan
        commit_plan = CommitGroundForcesPlan()
        commit_plan.add_commitment(infantry, "planet2")

        # Execute commit step using new architecture
        tactical_action.set_commit_plan(commit_plan)
        final_state = tactical_action.execute_step(
            "Commit Ground Forces", state_after_movement
        )

        # Verify final positions
        assert (
            carrier in final_state.systems["system2"].space_units
        )  # Carrier stays in space
        assert infantry in planet2.units  # Infantry committed to planet2
        assert (
            infantry not in final_state.systems["system2"].space_units
        )  # Infantry no longer in space

    def test_multiple_systems_converging_movement(self) -> None:
        """Test that units can move from multiple systems into the active system."""
        from ti4.actions.movement_engine import MovementPlan, MovementValidator

        # Setup galaxy with three systems
        galaxy = Galaxy()
        system1 = System(system_id="system1")
        system2 = System(system_id="system2")
        System(system_id="system3")  # Active system

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 1)  # Adjacent to system3
        coord3 = HexCoordinate(1, 0)  # Active system, adjacent to both

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")
        galaxy.place_system(coord3, "system3")

        # Create units in different systems
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")  # Movement 2
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player1")  # Movement 2
        destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player1")  # Movement 2

        system1.place_unit_in_space(cruiser1)
        system2.place_unit_in_space(cruiser2)
        system2.place_unit_in_space(destroyer)

        # Create movement plan - all units converge on system3
        movement_plan = MovementPlan()
        movement_plan.add_ship_movement(cruiser1, "system1", "system3")
        movement_plan.add_ship_movement(cruiser2, "system2", "system3")
        movement_plan.add_ship_movement(destroyer, "system2", "system3")

        # Validate - should be valid (all movements are distance 1, units have movement 2)
        validator = MovementValidator(galaxy)
        result = validator.validate_movement_plan(movement_plan, "player1")

        assert result.is_valid is True
        assert result.errors is None

    def test_gravity_drive_selective_application(self) -> None:
        """Test that Gravity Drive is applied optimally to make movement legal."""
        from ti4.actions.movement_engine import MovementPlan, MovementValidator

        # Setup galaxy with systems at different distances
        galaxy = Galaxy()
        system1 = System(system_id="system1")
        system2 = System(system_id="system2")
        System(system_id="system3")  # Active system

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)  # Distance 1 from system3
        coord3 = HexCoordinate(2, 0)  # Active system

        galaxy.place_system(coord1, "system1")  # Distance 2 from system3
        galaxy.place_system(coord2, "system2")  # Distance 1 from system3
        galaxy.place_system(coord3, "system3")

        # Create carriers (movement 1) - need Gravity Drive for distance 2
        carrier1 = Unit(unit_type=UnitType.CARRIER, owner="player1")  # Distance 2 away
        carrier2 = Unit(unit_type=UnitType.CARRIER, owner="player1")  # Distance 1 away

        system1.place_unit_in_space(carrier1)
        system2.place_unit_in_space(carrier2)

        # Create movement plan
        movement_plan = MovementPlan()
        movement_plan.add_ship_movement(
            carrier1, "system1", "system3"
        )  # Needs Gravity Drive
        movement_plan.add_ship_movement(
            carrier2, "system2", "system3"
        )  # Doesn't need it

        # Test without Gravity Drive - should be invalid
        validator = MovementValidator(galaxy)
        result_without_tech = validator.validate_movement_plan(movement_plan, "player1")

        assert result_without_tech.is_valid is False
        assert result_without_tech.errors is not None
        assert "insufficient movement" in result_without_tech.errors[0].lower()

        # Test with Gravity Drive - should be valid and applied to carrier1
        result_with_tech = validator.validate_movement_plan(
            movement_plan, "player1", technologies={"gravity_drive"}
        )

        assert result_with_tech.is_valid is True
        assert result_with_tech.technology_effects is not None
        assert "gravity_drive" in result_with_tech.technology_effects

    def test_gravity_drive_insufficient_for_multiple_ships(self) -> None:
        """Test that Gravity Drive cannot make illegal moves with multiple ships needing it."""
        from ti4.actions.movement_engine import MovementPlan, MovementValidator

        # Setup galaxy
        galaxy = Galaxy()
        system1 = System(system_id="system1")
        system2 = System(system_id="system2")
        System(system_id="system3")  # Active system

        coord1 = HexCoordinate(0, 0)  # Distance 2 from system3
        coord2 = HexCoordinate(0, 1)  # Distance 2 from system3
        coord3 = HexCoordinate(2, 0)  # Active system

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")
        galaxy.place_system(coord3, "system3")

        # Create two carriers (movement 1) both distance 2 away
        carrier1 = Unit(unit_type=UnitType.CARRIER, owner="player1")
        carrier2 = Unit(unit_type=UnitType.CARRIER, owner="player1")

        system1.place_unit_in_space(carrier1)
        system2.place_unit_in_space(carrier2)

        # Create movement plan - both ships need Gravity Drive
        movement_plan = MovementPlan()
        movement_plan.add_ship_movement(carrier1, "system1", "system3")
        movement_plan.add_ship_movement(carrier2, "system2", "system3")

        # Test with Gravity Drive - should still be invalid (can only help one ship)
        validator = MovementValidator(galaxy)
        result = validator.validate_movement_plan(
            movement_plan, "player1", technologies={"gravity_drive"}
        )

        # This should be invalid because Gravity Drive can only be applied to one ship
        # and we have two ships that both need it
        assert result.is_valid is False
        assert result.errors is not None
        assert (
            len([e for e in result.errors if "insufficient movement" in e.lower()]) >= 1
        )

    def test_scalable_technology_system(self) -> None:
        """Test that the technology system is extensible for future technologies."""
        from ti4.actions.movement_engine import MovementValidator

        # This test demonstrates how new technologies could be added
        galaxy = Galaxy()
        system1 = System(system_id="system1")
        System(system_id="system2")

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(3, 0)  # Distance 3

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create a cruiser (movement 2)
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system1.place_unit_in_space(cruiser)

        # Test with multiple technologies (demonstrating extensibility)
        from ti4.actions.movement_engine import MovementPlan

        movement_plan = MovementPlan()
        movement_plan.add_ship_movement(cruiser, "system1", "system2")

        validator = MovementValidator(galaxy)

        # Test with future hypothetical technologies
        result = validator.validate_movement_plan(
            movement_plan,
            "player1",
            technologies={"gravity_drive", "future_tech_1", "future_tech_2"},
        )

        # Should work with gravity drive (2 + 1 = 3 movement)
        assert result.is_valid is True
        assert result.technology_effects is not None
        assert "gravity_drive" in result.technology_effects

    def test_complex_multi_system_scenario(self) -> None:
        """Test a complex scenario with multiple systems, technologies, and edge cases."""
        from ti4.actions.movement_engine import (
            MovementPlan,
            MovementValidator,
            TacticalAction,
        )

        # Setup a complex galaxy with 5 systems
        galaxy = Galaxy()
        systems = {}

        # Create systems in a pattern
        coords = [
            HexCoordinate(0, 0),  # system1
            HexCoordinate(1, 0),  # system2 - distance 1 from system1
            HexCoordinate(
                2, 0
            ),  # system3 - distance 2 from system1, distance 1 from system2
            HexCoordinate(0, 1),  # system4 - distance 1 from system1
            HexCoordinate(1, 1),  # system5 - distance 1 from system2, system4
        ]

        for i, coord in enumerate(coords, 1):
            system_id = f"system{i}"
            systems[system_id] = System(system_id=system_id)
            galaxy.place_system(coord, system_id)

        # Create diverse units in different systems
        # System 1: Carrier (movement 1) + Infantry
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")
        infantry1 = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        systems["system1"].place_unit_in_space(carrier)
        systems["system1"].place_unit_on_planet(infantry1, "planet1")

        # System 2: Cruiser (movement 2)
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        systems["system2"].place_unit_in_space(cruiser)

        # System 4: Destroyer (movement 2) + Infantry
        destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player1")
        infantry2 = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        systems["system4"].place_unit_in_space(destroyer)
        systems["system4"].place_unit_on_planet(infantry2, "planet4")

        # Create complex movement plan - all units converge on system5
        movement_plan = MovementPlan()

        # Carrier needs Gravity Drive to reach system5 (distance 2, movement 1)
        movement_plan.add_ship_movement(carrier, "system1", "system5")

        # Cruiser can reach system5 easily (distance 1, movement 2)
        movement_plan.add_ship_movement(cruiser, "system2", "system5")

        # Destroyer can reach system5 easily (distance 1, movement 2)
        movement_plan.add_ship_movement(destroyer, "system4", "system5")

        # Ground forces need transport
        movement_plan.add_ground_force_movement(
            infantry1, "system1", "system5", "planet1", "space"
        )
        movement_plan.add_ground_force_movement(
            infantry2, "system4", "system5", "planet4", "space"
        )

        # Test validation with Gravity Drive
        validator = MovementValidator(galaxy)
        result = validator.validate_movement_plan(
            movement_plan, "player1", technologies={"gravity_drive"}
        )

        # Should be valid - Gravity Drive helps carrier, other ships don't need help
        # Carrier has capacity 4, so can transport both infantry
        assert result.is_valid is True
        assert result.technology_effects is not None
        assert "gravity_drive" in result.technology_effects
        assert result.transport_assignments is not None

        # Test execution of the complete tactical action
        tactical_action = TacticalAction("system5", "player1")
        tactical_action.initialize_steps()
        tactical_action.set_movement_plan(movement_plan)

        game_state = MockGameState(galaxy=galaxy, systems=systems)
        final_state = tactical_action.execute_step("Movement", game_state)

        # Verify all units ended up in system5
        assert carrier in final_state.systems["system5"].space_units
        assert cruiser in final_state.systems["system5"].space_units
        assert destroyer in final_state.systems["system5"].space_units
        assert infantry1 in final_state.systems["system5"].space_units
        assert infantry2 in final_state.systems["system5"].space_units


class MockGameState:
    """Mock game state for testing."""

    def __init__(
        self, galaxy: Optional[Galaxy] = None, systems: Optional[dict[str, Any]] = None
    ) -> None:
        self.galaxy = galaxy
        self.systems = systems or {}
