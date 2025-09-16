"""Tests for unit movement system."""

from src.ti4.core.galaxy import Galaxy
from src.ti4.core.hex_coordinate import HexCoordinate
from src.ti4.core.movement import MovementExecutor, MovementOperation, MovementValidator
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class TestMovementValidator:
    def test_movement_validator_creation(self):
        """Test that MovementValidator can be created."""
        galaxy = Galaxy()
        validator = MovementValidator(galaxy)
        assert validator is not None

    def test_validate_basic_movement(self):
        """Test basic movement validation between adjacent systems."""
        galaxy = Galaxy()

        # Create two adjacent systems
        system1 = System(system_id="system1")
        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)  # Adjacent

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create a unit in system1
        unit = Unit(unit_type="cruiser", owner="player1")
        system1.place_unit_in_space(unit)

        # Create movement operation
        movement = MovementOperation(
            unit=unit,
            from_system_id="system1",
            to_system_id="system2",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)
        assert validator.is_valid_movement(movement) is True

    def test_validate_invalid_movement_non_adjacent(self):
        """Test that movement between non-adjacent systems is invalid."""
        galaxy = Galaxy()

        # Create two non-adjacent systems
        system1 = System(system_id="system1")
        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(2, 0)  # Distance 2, not adjacent

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create a unit in system1 (carrier has movement 1)
        unit = Unit(unit_type="carrier", owner="player1")
        system1.place_unit_in_space(unit)

        # Create movement operation
        movement = MovementOperation(
            unit=unit,
            from_system_id="system1",
            to_system_id="system2",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)
        assert validator.is_valid_movement(movement) is False

    def test_validate_movement_invalid_system_ids(self):
        """Test movement validation with invalid system IDs."""
        galaxy = Galaxy()
        coord1 = HexCoordinate(0, 0)
        galaxy.place_system(coord1, "system1")

        unit = Unit(unit_type="cruiser", owner="player1")

        # Test with invalid from_system_id
        movement = MovementOperation(
            unit=unit,
            from_system_id="invalid_system",
            to_system_id="system1",
            player_id="player1",
        )
        validator = MovementValidator(galaxy)
        assert validator.is_valid_movement(movement) is False

        # Test with invalid to_system_id
        movement = MovementOperation(
            unit=unit,
            from_system_id="system1",
            to_system_id="invalid_system",
            player_id="player1",
        )
        assert validator.is_valid_movement(movement) is False

    def test_validate_movement_with_technologies(self):
        """Test movement validation with player technologies."""
        galaxy = Galaxy()
        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)
        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        unit = Unit(unit_type="cruiser", owner="player1")

        # Test movement with gravity drive technology
        movement = MovementOperation(
            unit=unit,
            from_system_id="system1",
            to_system_id="system2",
            player_id="player1",
            player_technologies={"gravity_drive"},
        )
        validator = MovementValidator(galaxy)
        assert validator.is_valid_movement(movement) is True


class TestMovementExecution:
    def test_execute_movement(self):
        """Test executing a valid movement action."""
        galaxy = Galaxy()

        # Create two adjacent systems
        system1 = System(system_id="system1")
        system2 = System(system_id="system2")
        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)  # Adjacent

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create a unit in system1
        unit = Unit(unit_type="cruiser", owner="player1")
        system1.place_unit_in_space(unit)

        # Create movement operation
        movement = MovementOperation(
            unit=unit,
            from_system_id="system1",
            to_system_id="system2",
            player_id="player1",
        )

        # Create movement executor and execute
        executor = MovementExecutor(galaxy, {"system1": system1, "system2": system2})
        executor.execute_movement(movement)

        # Unit should be moved from system1 to system2
        assert unit not in system1.space_units
        assert unit in system2.space_units

    def test_movement_with_gravity_drive(self):
        """Test movement with gravity drive technology."""
        galaxy = Galaxy()

        # Create systems that are distance 2 apart
        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(2, 0)  # Distance 2

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create a unit with movement 1 (carrier)
        unit = Unit(unit_type="carrier", owner="player1")  # Movement 1

        # Without gravity drive, this should be invalid (distance 2 > movement 1)
        movement_without_tech = MovementOperation(
            unit=unit,
            from_system_id="system1",
            to_system_id="system2",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)
        assert validator.is_valid_movement(movement_without_tech) is False

        # With gravity drive technology, this should be valid
        movement_with_tech = MovementOperation(
            unit=unit,
            from_system_id="system1",
            to_system_id="system2",
            player_id="player1",
            player_technologies={"gravity_drive"},
        )

        # Should be valid with gravity drive (assuming it adds +1 movement)
        assert validator.is_valid_movement(movement_with_tech) is True

    def test_unit_movement_range(self):
        """Test that different units have different movement ranges."""
        # Test different unit types
        cruiser = Unit(unit_type="cruiser", owner="player1")
        destroyer = Unit(unit_type="destroyer", owner="player1")
        carrier = Unit(unit_type="carrier", owner="player1")

        # Verify movement values from unit stats
        assert cruiser.get_movement() == 2
        assert destroyer.get_movement() == 2
        assert carrier.get_movement() == 1

    def test_ground_force_transport_from_planet(self):
        """Test transporting ground forces from a planet."""
        from src.ti4.core.movement import (
            TransportExecutor,
            TransportOperation,
            TransportValidator,
        )
        from src.ti4.core.planet import Planet

        galaxy = Galaxy()

        # Create systems with planets
        system1 = System(system_id="system1")
        system2 = System(system_id="system2")
        planet1 = Planet(name="planet1", resources=2, influence=1)
        system1.add_planet(planet1)

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)  # Adjacent

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create units
        carrier = Unit(unit_type="carrier", owner="player1")  # Capacity 4
        infantry1 = Unit(unit_type="infantry", owner="player1")
        infantry2 = Unit(unit_type="infantry", owner="player1")

        # Place carrier in space, infantry on planet
        system1.place_unit_in_space(carrier)
        system1.place_unit_on_planet(infantry1, "planet1")
        system1.place_unit_on_planet(infantry2, "planet1")

        # Create transport operation
        transport = TransportOperation(
            transport_ship=carrier,
            ground_forces=[infantry1, infantry2],
            from_system_id="system1",
            to_system_id="system2",
            from_location="planet1",
            to_location="space",
            player_id="player1",
        )

        # Validate and execute transport
        validator = TransportValidator(galaxy)
        assert validator.is_valid_transport(transport) is True

        executor = TransportExecutor({"system1": system1, "system2": system2})
        executor.execute_transport(transport)

        # Verify results
        assert carrier in system2.space_units  # Carrier moved
        assert infantry1 in system2.space_units  # Infantry transported
        assert infantry2 in system2.space_units
        assert infantry1 not in planet1.units  # No longer on planet
        assert infantry2 not in planet1.units

    def test_invalid_transport_exceeds_capacity(self):
        """Test that transport fails when exceeding ship capacity."""
        from src.ti4.core.movement import TransportOperation, TransportValidator

        galaxy = Galaxy()
        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)
        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create units - destroyer has 0 capacity
        destroyer = Unit(unit_type="destroyer", owner="player1")
        infantry = Unit(unit_type="infantry", owner="player1")

        transport = TransportOperation(
            transport_ship=destroyer,
            ground_forces=[infantry],  # 1 infantry, but destroyer has 0 capacity
            from_system_id="system1",
            to_system_id="system2",
            player_id="player1",
        )

        validator = TransportValidator(galaxy)
        assert validator.is_valid_transport(transport) is False

    def test_invalid_direct_planet_to_planet_movement(self):
        """Test that direct planet-to-planet movement is invalid according to TI4 rules."""
        from src.ti4.core.planet import Planet

        galaxy = Galaxy()
        system1 = System(system_id="system1")
        planet1 = Planet(name="planet1", resources=2, influence=1)
        planet2 = Planet(name="planet2", resources=1, influence=2)
        system1.add_planet(planet1)
        system1.add_planet(planet2)

        coord1 = HexCoordinate(0, 0)
        galaxy.place_system(coord1, "system1")

        # Create infantry on planet1
        infantry = Unit(unit_type="infantry", owner="player1")
        system1.place_unit_on_planet(infantry, "planet1")

        # Attempt to move infantry directly from planet1 to planet2 (same system)
        # This should be INVALID - ground forces must move to space first
        movement = MovementOperation(
            unit=infantry,
            from_system_id="system1",
            to_system_id="system1",  # Same system
            from_location="planet1",
            to_location="planet2",  # Direct planet-to-planet
            player_id="player1",
        )

        validator = MovementValidator(galaxy)
        # This should be invalid according to TI4 rules
        assert validator.is_valid_movement(movement) is False

    def test_correct_tactical_action_movement_sequence(self):
        """Test the correct two-step tactical action movement process."""
        from src.ti4.core.planet import Planet

        galaxy = Galaxy()
        system1 = System(system_id="system1")
        planet1 = Planet(name="planet1", resources=2, influence=1)
        planet2 = Planet(name="planet2", resources=1, influence=2)
        system1.add_planet(planet1)
        system1.add_planet(planet2)

        coord1 = HexCoordinate(0, 0)
        galaxy.place_system(coord1, "system1")

        # Create infantry on planet1 and a carrier in space
        infantry = Unit(unit_type="infantry", owner="player1")
        carrier = Unit(unit_type="carrier", owner="player1")  # Has capacity 4
        system1.place_unit_on_planet(infantry, "planet1")
        system1.place_unit_in_space(carrier)

        # Step 1: Movement Step - Infantry moves from planet1 to space area
        # (This would be part of a larger tactical action movement)
        movement_to_space = MovementOperation(
            unit=infantry,
            from_system_id="system1",
            to_system_id="system1",
            from_location="planet1",
            to_location="space",  # Must go to space first
            player_id="player1",
        )

        validator = MovementValidator(galaxy)
        executor = MovementExecutor(galaxy, {"system1": system1})

        # This should be valid (infantry can move to space if capacity exists)
        assert validator.is_valid_movement(movement_to_space) is True
        executor.execute_movement(movement_to_space)

        # Verify infantry is now in space
        assert infantry not in planet1.units
        assert infantry in system1.space_units

        # Step 2: Commit Ground Forces Step - Infantry moves from space to planet2
        # (This would be a separate step in the tactical action)
        commit_to_planet = MovementOperation(
            unit=infantry,
            from_system_id="system1",
            to_system_id="system1",
            from_location="space",
            to_location="planet2",  # Now can go to different planet
            player_id="player1",
        )

        # This should be valid (infantry is in space and can be committed)
        assert validator.is_valid_movement(commit_to_planet) is True
        executor.execute_movement(commit_to_planet)

        # Verify infantry is now on planet2
        assert infantry not in system1.space_units
        assert infantry in planet2.units
