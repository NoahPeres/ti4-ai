"""
Tests for anomaly integration with movement system (Task 7).

Tests comprehensive movement validation through anomaly systems with
detailed error messages and movement cost calculations.

LRR References:
- Rule 58: Movement integration with all anomaly types
- Requirements: 8.1, 8.2, 8.3, 8.4
"""

from src.ti4.core.constants import AnomalyType, UnitType
from src.ti4.core.galaxy import Galaxy
from src.ti4.core.hex_coordinate import HexCoordinate
from src.ti4.core.movement import MovementOperation, MovementValidator
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class TestAnomalyMovementPathValidation:
    """Test movement path validation through multiple anomalies (Requirement 8.1)."""

    def test_movement_path_validation_checks_all_systems_in_path(self) -> None:
        """Test that anomaly restrictions are checked for all systems in the path."""
        # Create galaxy with multiple systems in path
        galaxy = Galaxy()

        # Set up coordinates for a 3-system path
        start_coord = HexCoordinate(0, 0)
        middle_coord = HexCoordinate(1, 0)
        end_coord = HexCoordinate(2, 0)

        # Create systems
        start_system = System("start_system")
        middle_system = System("middle_system")
        end_system = System("end_system")

        # Add asteroid field to middle system (should block movement)
        middle_system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)

        # Register systems in galaxy
        galaxy.place_system(start_coord, "start_system")
        galaxy.register_system(start_system)
        galaxy.place_system(middle_coord, "middle_system")
        galaxy.register_system(middle_system)
        galaxy.place_system(end_coord, "end_system")
        galaxy.register_system(end_system)

        # Create movement operation
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        movement = MovementOperation(
            unit=unit,
            from_system_id="start_system",
            to_system_id="end_system",
            player_id="player1",
        )

        # Create validator
        validator = MovementValidator(galaxy)

        # Movement should be invalid due to asteroid field in path
        assert not validator.validate_movement_path_through_anomalies(movement)

    def test_movement_path_validation_with_multiple_anomaly_types(self) -> None:
        """Test path validation with multiple different anomaly types."""
        # This test should fail initially - method doesn't exist yet
        galaxy = Galaxy()

        # Set up 4-system path with different anomalies
        coords = [HexCoordinate(i, 0) for i in range(4)]
        systems = [System(f"system_{i}") for i in range(4)]

        # Add different anomaly types
        systems[1].add_anomaly_type(AnomalyType.NEBULA)  # Should block if not active
        systems[2].add_anomaly_type(AnomalyType.GRAVITY_RIFT)  # Should allow with bonus

        # Register systems
        for i, (coord, system) in enumerate(zip(coords, systems, strict=False)):
            galaxy.place_system(coord, f"system_{i}")
            galaxy.register_system(system)

        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        movement = MovementOperation(
            unit=unit,
            from_system_id="system_0",
            to_system_id="system_3",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)

        # Should fail due to nebula not being active system
        assert not validator.validate_movement_path_through_anomalies(movement)


class TestAnomalyMovementErrorMessages:
    """Test detailed error messages for anomaly movement failures (Requirement 8.4)."""

    def test_asteroid_field_error_message_specifies_blocking_anomaly(self) -> None:
        """Test that error messages specify which anomaly caused the failure."""
        galaxy = Galaxy()

        start_coord = HexCoordinate(0, 0)
        end_coord = HexCoordinate(1, 0)

        start_system = System("start_system")
        end_system = System("asteroid_system")
        end_system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)

        galaxy.place_system(start_coord, "start_system")
        galaxy.register_system(start_system)
        galaxy.place_system(end_coord, "asteroid_system")
        galaxy.register_system(end_system)

        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        movement = MovementOperation(
            unit=unit,
            from_system_id="start_system",
            to_system_id="asteroid_system",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)

        # Should return detailed error message
        result = validator.get_movement_validation_error(movement)
        assert result is not None
        assert "asteroid field" in result.lower()
        assert "asteroid_system" in result

    def test_nebula_error_message_explains_active_system_requirement(self) -> None:
        """Test that nebula error messages explain active system requirement."""
        galaxy = Galaxy()

        start_coord = HexCoordinate(0, 0)
        end_coord = HexCoordinate(1, 0)

        start_system = System("start_system")
        end_system = System("nebula_system")
        end_system.add_anomaly_type(AnomalyType.NEBULA)

        galaxy.place_system(start_coord, "start_system")
        galaxy.register_system(start_system)
        galaxy.place_system(end_coord, "nebula_system")
        galaxy.register_system(end_system)

        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        movement = MovementOperation(
            unit=unit,
            from_system_id="start_system",
            to_system_id="nebula_system",
            player_id="player1",
            active_system_id="different_system",  # Set different active system to trigger error
        )

        validator = MovementValidator(galaxy)

        # Should return detailed error message about active system requirement
        result = validator.get_movement_validation_error(movement)
        assert result is not None
        assert "nebula" in result.lower()
        assert "active system" in result.lower()


class TestAnomalyMovementCostCalculation:
    """Test movement cost calculation with anomaly effects (Requirement 8.3)."""

    def test_gravity_rift_bonus_applied_to_movement_cost(self) -> None:
        """Test that gravity rift bonuses are applied to movement calculations."""
        galaxy = Galaxy()

        start_coord = HexCoordinate(0, 0)
        end_coord = HexCoordinate(2, 0)  # Distance 2

        start_system = System("gravity_rift_system")
        start_system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)
        end_system = System("end_system")

        galaxy.place_system(start_coord, "gravity_rift_system")
        galaxy.register_system(start_system)
        galaxy.place_system(end_coord, "end_system")
        galaxy.register_system(end_system)

        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")  # Base move 2
        movement = MovementOperation(
            unit=unit,
            from_system_id="gravity_rift_system",
            to_system_id="end_system",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)

        # Should calculate effective movement range with gravity rift bonus
        effective_range = validator.calculate_effective_movement_range(movement)
        assert effective_range == 3  # Base 2 + gravity rift bonus 1

    def test_nebula_penalty_applied_to_movement_cost(self) -> None:
        """Test that nebula move value penalties are applied."""
        galaxy = Galaxy()

        start_coord = HexCoordinate(0, 0)
        end_coord = HexCoordinate(1, 0)

        start_system = System("nebula_system")
        start_system.add_anomaly_type(AnomalyType.NEBULA)
        end_system = System("end_system")

        galaxy.place_system(start_coord, "nebula_system")
        galaxy.register_system(start_system)
        galaxy.place_system(end_coord, "end_system")
        galaxy.register_system(end_system)

        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")  # Base move 2
        movement = MovementOperation(
            unit=unit,
            from_system_id="nebula_system",
            to_system_id="end_system",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)

        # Should calculate effective movement range with nebula penalty
        effective_range = validator.calculate_effective_movement_range(movement)
        assert effective_range == 1  # Nebula sets move value to 1


class TestComprehensiveAnomalyPathValidation:
    """Test comprehensive path validation through multiple anomalies (Requirement 8.2)."""

    def test_complex_path_with_multiple_anomaly_effects(self) -> None:
        """Test movement through path with multiple anomaly effects."""
        galaxy = Galaxy()

        # Create 5-system path with various anomalies
        coords = [HexCoordinate(i, 0) for i in range(5)]
        systems = [System(f"system_{i}") for i in range(5)]

        # System 0: Start (normal)
        # System 1: Gravity rift (bonus)
        # System 2: Nebula (requires active)
        # System 3: Gravity rift (bonus)
        # System 4: End (normal)

        systems[1].add_anomaly_type(AnomalyType.GRAVITY_RIFT)
        systems[2].add_anomaly_type(AnomalyType.NEBULA)
        systems[3].add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # Register systems
        for i, (coord, system) in enumerate(zip(coords, systems, strict=False)):
            galaxy.place_system(coord, f"system_{i}")
            galaxy.register_system(system)

        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        movement = MovementOperation(
            unit=unit,
            from_system_id="system_0",
            to_system_id="system_4",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)

        # Test 1: Should fail when nebula is not active
        result = validator.validate_movement_with_anomaly_effects(movement)
        assert not result.is_valid
        assert "nebula" in result.error_message.lower()

        # Test 2: Should succeed when nebula is active system
        movement_with_active = MovementOperation(
            unit=unit,
            from_system_id="system_0",
            to_system_id="system_4",
            player_id="player1",
            active_system_id="system_2",  # Nebula is active
        )

        result = validator.validate_movement_with_anomaly_effects(movement_with_active)
        assert result.is_valid

        # Test 3: Should calculate correct effective range with bonuses
        effective_range = validator.calculate_effective_movement_range(
            movement_with_active
        )
        assert effective_range == 4  # Base 2 + 2 gravity rift bonuses

    def test_movement_blocked_by_multiple_blocking_anomalies(self) -> None:
        """Test that movement is properly blocked by multiple blocking anomalies."""
        galaxy = Galaxy()

        coords = [HexCoordinate(i, 0) for i in range(4)]
        systems = [System(f"system_{i}") for i in range(4)]

        # Add blocking anomalies
        systems[1].add_anomaly_type(AnomalyType.ASTEROID_FIELD)
        systems[2].add_anomaly_type(AnomalyType.SUPERNOVA)

        # Register systems
        for i, (coord, system) in enumerate(zip(coords, systems, strict=False)):
            galaxy.place_system(coord, f"system_{i}")
            galaxy.register_system(system)

        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        movement = MovementOperation(
            unit=unit,
            from_system_id="system_0",
            to_system_id="system_3",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)

        # Should be blocked by first blocking anomaly encountered
        result = validator.validate_movement_with_anomaly_effects(movement)
        assert not result.is_valid
        assert "asteroid field" in result.error_message.lower()
        assert "system_1" in result.error_message
