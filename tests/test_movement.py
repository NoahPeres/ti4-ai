"""Tests for movement validation and execution."""

from src.ti4.core.constants import Technology, UnitType
from src.ti4.core.galaxy import Galaxy
from src.ti4.core.hex_coordinate import HexCoordinate
from src.ti4.core.movement import MovementExecutor, MovementOperation, MovementValidator
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class TestMovementValidator:
    def test_movement_validator_creation(self) -> None:
        """Test that MovementValidator can be created."""
        galaxy = Galaxy()
        validator = MovementValidator(galaxy)
        assert validator is not None

    def test_validate_basic_movement(self) -> None:
        """Test that basic movement validation works."""
        galaxy = Galaxy()
        validator = MovementValidator(galaxy)

        # Create systems
        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)  # Adjacent to A
        system_a = System("system_a")
        system_b = System("system_b")

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # Create unit in system A
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system_a.place_unit_in_space(unit)

        # Test movement from A to B
        movement = MovementOperation(
            unit=unit,
            from_system_id="system_a",
            to_system_id="system_b",
            player_id="player1",
        )
        assert validator.validate_movement(movement) is True

    def test_validate_invalid_movement_non_adjacent(self) -> None:
        """Test that movement to non-adjacent systems is invalid."""
        galaxy = Galaxy()
        validator = MovementValidator(galaxy)

        # Create non-adjacent systems
        coord_a = HexCoordinate(0, 0)
        coord_c = HexCoordinate(2, 0)  # Not adjacent to A
        system_a = System("system_a")
        system_c = System("system_c")

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_c, "system_c")
        galaxy.register_system(system_a)
        galaxy.register_system(system_c)

        # Create unit in system A
        unit = Unit(unit_type=UnitType.CARRIER, owner="player1")
        system_a.place_unit_in_space(unit)

        # Test invalid movement from A to C
        movement = MovementOperation(
            unit=unit,
            from_system_id="system_a",
            to_system_id="system_c",
            player_id="player1",
        )
        assert validator.validate_movement(movement) is False

    def test_validate_movement_invalid_system_ids(self) -> None:
        """Test that movement with invalid system IDs is rejected."""
        galaxy = Galaxy()
        validator = MovementValidator(galaxy)

        # Create system A only
        coord_a = HexCoordinate(0, 0)
        system_a = System("system_a")
        galaxy.place_system(coord_a, "system_a")
        galaxy.register_system(system_a)

        # Create unit in system A
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system_a.place_unit_in_space(unit)

        # Test invalid movement with invalid system IDs
        movement = MovementOperation(
            unit=unit,
            from_system_id="invalid_system",
            to_system_id="system_b",
            player_id="player1",
        )
        assert validator.validate_movement(movement) is False

    def test_validate_movement_with_technologies(self) -> None:
        """Test that movement validation considers technology upgrades."""
        galaxy = Galaxy()
        validator = MovementValidator(galaxy)

        # Create systems that are 2 hexes apart with intermediate system
        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)  # Intermediate system
        coord_c = HexCoordinate(2, 0)  # 2 hexes away
        system_a = System("system_a")
        system_b = System("system_b")
        system_c = System("system_c")

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.place_system(coord_c, "system_c")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)
        galaxy.register_system(system_c)

        # Create unit with Gravity Drive (movement 2)
        from src.ti4.core.constants import Technology
        unit = Unit(unit_type=UnitType.CARRIER, owner="player1")  # Movement 1
        unit.add_technology(Technology.GRAVITY_DRIVE)  # Increases movement to 2
        system_a.place_unit_in_space(unit)

        # Test movement should be valid with technology
        movement = MovementOperation(
            unit=unit,
            from_system_id="system_a",
            to_system_id="system_c",
            player_id="player1",
            player_technologies={Technology.GRAVITY_DRIVE},
        )
        assert validator.validate_movement(movement) is True


class TestMovementExecution:
    def test_execute_movement(self) -> None:
        """Test that movement execution works correctly."""
        galaxy = Galaxy()

        # Create systems
        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)
        system_a = System("system_a")
        system_b = System("system_b")

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # Create systems dict for executor
        systems = {"system_a": system_a, "system_b": system_b}
        executor = MovementExecutor(galaxy, systems)

        # Create unit in system A
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system_a.place_unit_in_space(unit)

        # Execute movement
        movement = MovementOperation(
            unit=unit,
            from_system_id="system_a",
            to_system_id="system_b",
            player_id="player1",
        )
        result = executor.execute_movement(movement)

        # Verify movement was successful
        assert result is True
        assert unit not in system_a.get_units_in_space()
        assert unit in system_b.get_units_in_space()

    def test_movement_with_gravity_drive(self) -> None:
        """Test movement execution with gravity drive technology."""
        galaxy = Galaxy()

        # Create systems
        coord_a = HexCoordinate(0, 0)
        coord_c = HexCoordinate(0, 2)  # Distance 2 from A
        system_a = System("system_a")
        system_c = System("system_c")

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_c, "system_c")
        galaxy.register_system(system_a)
        galaxy.register_system(system_c)

        # Create systems dict for executor
        systems = {"system_a": system_a, "system_c": system_c}
        executor = MovementExecutor(galaxy, systems)

        # Create unit with Gravity Drive
        unit = Unit(unit_type=UnitType.DESTROYER, owner="player1")
        unit.add_technology(Technology.GRAVITY_DRIVE)
        system_a.place_unit_in_space(unit)

        # Execute long-range movement
        movement = MovementOperation(
            unit=unit,
            from_system_id="system_a",
            to_system_id="system_c",
            player_id="player1",
            player_technologies={Technology.GRAVITY_DRIVE},
        )
        result = executor.execute_movement(movement)

        # Verify movement was successful
        assert result is True
        assert unit not in system_a.get_units_in_space()
        assert unit in system_c.get_units_in_space()

    def test_unit_movement_range(self) -> None:
        """Test that units respect their movement range."""
        # Test basic cruiser movement (range 2)
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")

        # Cruiser should have movement 2, carrier should have movement 1
        assert cruiser.get_movement() == 2
        assert carrier.get_movement() == 1

    def test_ground_force_transport_from_planet(self) -> None:
        """Test transporting ground forces from planet to planet."""
        galaxy = Galaxy()

        # Create systems
        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)
        system_a = System("system_a")
        system_b = System("system_b")

        from src.ti4.core.planet import Planet

        planet_a = Planet(name="Planet A", resources=2, influence=1)
        planet_b = Planet(name="Planet B", resources=1, influence=2)
        system_a.add_planet(planet_a)
        system_b.add_planet(planet_b)

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # Create systems dict for executor
        systems = {"system_a": system_a, "system_b": system_b}
        executor = MovementExecutor(galaxy, systems)

        # Create carrier and infantry
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")  # Capacity 4
        infantry1 = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        infantry2 = Unit(unit_type=UnitType.INFANTRY, owner="player1")

        # Place carrier in space of system A
        system_a.place_unit_in_space(carrier)

        # Place infantry on planet in system A
        system_a.place_unit_on_planet(infantry1, "Planet A")
        system_a.place_unit_on_planet(infantry2, "Planet A")

        # Load infantry onto carrier (transport capacity)
        carrier.load_transport_unit(infantry1)
        carrier.load_transport_unit(infantry2)

        # Move carrier with infantry to system B
        movement = MovementOperation(
            unit=carrier,
            from_system_id="system_a",
            to_system_id="system_b",
            player_id="player1",
            from_location="space",
            to_location="space",
        )
        result = executor.execute_movement(movement)

        # Verify movement was successful
        assert result is True
        assert carrier in system_b.get_units_in_space()

        # Unload infantry on planet B
        carrier.unload_unit(infantry1)
        carrier.unload_unit(infantry2)
        system_b.place_unit_on_planet(infantry1, "Planet B")
        system_b.place_unit_on_planet(infantry2, "Planet B")

        # Verify infantry are on planet B
        assert infantry1 in system_b.get_units_on_planet("Planet B")
        assert infantry2 in system_b.get_units_on_planet("Planet B")

    def test_invalid_transport_exceeds_capacity(self) -> None:
        """Test that transport fails when exceeding capacity."""
        galaxy = Galaxy()

        # Create systems
        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)
        system_a = System("system_a")
        system_b = System("system_b")

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # Create systems dict for executor
        systems = {"system_a": system_a, "system_b": system_b}
        MovementExecutor(galaxy, systems)

        # Create system
        coord_a = HexCoordinate(0, 0)
        system_a = System("system_a")
        galaxy.place_system(coord_a, "system_a")
        galaxy.register_system(system_a)

        # Create carrier (capacity 4) and too many ground forces
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")
        destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player1")
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")

        system_a.place_unit_in_space(carrier)
        system_a.place_unit_in_space(destroyer)

        # Try to load infantry onto destroyer (no capacity)
        from src.ti4.core.exceptions import FleetCapacityError

        try:
            destroyer.load_transport_unit(infantry)
            assert False, "Should not be able to load infantry on destroyer"
        except FleetCapacityError:
            pass  # Expected to fail with specific exception

    def test_invalid_direct_planet_to_planet_movement(self) -> None:
        """Test that direct planet-to-planet movement fails."""
        galaxy = Galaxy()

        # Create systems
        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)
        system_a = System("system_a")
        system_b = System("system_b")

        from src.ti4.core.planet import Planet

        planet_a = Planet(name="Planet A", resources=2, influence=1)
        planet_b = Planet(name="Planet B", resources=1, influence=2)
        system_a.add_planet(planet_a)
        system_b.add_planet(planet_b)

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # Create systems dict for executor
        systems = {"system_a": system_a, "system_b": system_b}
        executor = MovementExecutor(galaxy, systems)

        # Create infantry on planet A
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        system_a.place_unit_on_planet(infantry, "Planet A")

        # Try direct movement from planet to planet (should fail)
        movement = MovementOperation(
            unit=infantry,
            from_system_id="system_a",
            to_system_id="system_b",
            player_id="player1",
            from_location="Planet A",
            to_location="Planet B",
        )
        result = executor.execute_movement(movement)

        # Should fail - ground forces need transport
        assert result is False

    def test_correct_tactical_action_movement_sequence(self) -> None:
        """Test a correct sequence of tactical action movements."""
        galaxy = Galaxy()

        # Create systems
        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)
        system_a = System("system_a")
        system_b = System("system_b")

        from src.ti4.core.planet import Planet

        planet_a = Planet(name="Planet A", resources=2, influence=1)
        system_a.add_planet(planet_a)

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # Create systems dict for executor
        systems = {"system_a": system_a, "system_b": system_b}
        executor = MovementExecutor(galaxy, systems)

        # Create units
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")  # Has capacity 4

        # Initial placement
        system_a.place_unit_on_planet(infantry, "Planet A")
        system_a.place_unit_in_space(carrier)

        # Step 1: Load infantry onto carrier
        carrier.load_transport_unit(infantry)

        # Step 2: Move carrier to system B
        movement = MovementOperation(
            unit=carrier,
            from_system_id="system_a",
            to_system_id="system_b",
            player_id="player1",
        )
        result = executor.execute_movement(movement)
        assert result is True

        # Step 3: Unload infantry in system B space (for invasion)
        carrier.unload_unit(infantry)
        system_b.place_unit_in_space(infantry)

        # Verify final positions
        assert carrier in system_b.get_units_in_space()
        assert infantry in system_b.get_units_in_space()
