"""
Tests for comprehensive anomaly error handling and edge cases.

This module tests custom exception types, validation logic, and edge cases
for the anomaly system implementation.

LRR References:
- Rule 9.2a: Anomalies with planets
- Rule 9.4-9.5: Dynamic and multiple anomalies
"""

import pytest

from src.ti4.core.constants import AnomalyType
from src.ti4.core.planet import Planet
from src.ti4.core.system import System


class TestAnomalyCustomExceptions:
    """Test custom exception types for anomaly-related errors."""

    def test_anomaly_movement_error_exists(self) -> None:
        """Test that AnomalyMovementError exception exists."""
        # This test will fail initially (RED phase)
        from src.ti4.core.exceptions import AnomalyMovementError

        # Should be able to create and raise the exception
        with pytest.raises(AnomalyMovementError):
            raise AnomalyMovementError("Test movement blocked")

    def test_invalid_anomaly_type_error_exists(self) -> None:
        """Test that InvalidAnomalyTypeError exception exists."""
        from src.ti4.core.exceptions import InvalidAnomalyTypeError

        # Should be able to create and raise the exception
        with pytest.raises(InvalidAnomalyTypeError):
            raise InvalidAnomalyTypeError("Invalid anomaly type: test")

    def test_gravity_rift_destruction_error_exists(self) -> None:
        """Test that GravityRiftDestructionError exception exists."""
        from src.ti4.core.exceptions import GravityRiftDestructionError

        # Should be able to create and raise the exception
        with pytest.raises(GravityRiftDestructionError):
            raise GravityRiftDestructionError("Unit destroyed by gravity rift")

    def test_anomaly_state_consistency_error_exists(self) -> None:
        """Test that AnomalyStateConsistencyError exception exists."""
        from src.ti4.core.exceptions import AnomalyStateConsistencyError

        # Should be able to create and raise the exception
        with pytest.raises(AnomalyStateConsistencyError):
            raise AnomalyStateConsistencyError("System state inconsistent")


class TestAnomalyTypeValidation:
    """Test validation for anomaly type assignments."""

    def test_empty_string_anomaly_type_raises_error(self) -> None:
        """Test that empty string anomaly type raises InvalidAnomalyTypeError."""
        from src.ti4.core.exceptions import InvalidAnomalyTypeError

        system = System("test_system")

        with pytest.raises(
            InvalidAnomalyTypeError, match="Anomaly type cannot be empty"
        ):
            system.add_anomaly_type("")

    def test_whitespace_only_anomaly_type_raises_error(self) -> None:
        """Test that whitespace-only anomaly type raises InvalidAnomalyTypeError."""
        from src.ti4.core.exceptions import InvalidAnomalyTypeError

        system = System("test_system")

        with pytest.raises(
            InvalidAnomalyTypeError, match="Anomaly type cannot be empty"
        ):
            system.add_anomaly_type("   ")

    def test_numeric_anomaly_type_raises_error(self) -> None:
        """Test that numeric anomaly type raises InvalidAnomalyTypeError."""
        from src.ti4.core.exceptions import InvalidAnomalyTypeError

        system = System("test_system")

        with pytest.raises(InvalidAnomalyTypeError, match="Invalid anomaly type"):
            system.add_anomaly_type("123")

    def test_special_character_anomaly_type_raises_error(self) -> None:
        """Test that special character anomaly type raises InvalidAnomalyTypeError."""
        from src.ti4.core.exceptions import InvalidAnomalyTypeError

        system = System("test_system")

        with pytest.raises(InvalidAnomalyTypeError, match="Invalid anomaly type"):
            system.add_anomaly_type("@#$%")


class TestSystemStateConsistency:
    """Test validation for system state consistency."""

    def test_empty_system_id_raises_error(self) -> None:
        """Test that empty system ID raises AnomalyStateConsistencyError."""
        from src.ti4.core.exceptions import AnomalyStateConsistencyError

        with pytest.raises(
            AnomalyStateConsistencyError, match="System ID cannot be empty"
        ):
            System("")

    def test_none_system_id_raises_error(self) -> None:
        """Test that None system ID raises AnomalyStateConsistencyError."""
        from src.ti4.core.exceptions import AnomalyStateConsistencyError

        with pytest.raises(
            AnomalyStateConsistencyError, match="System ID cannot be None"
        ):
            System(None)  # type: ignore

    def test_system_with_corrupted_anomaly_list_raises_error(self) -> None:
        """Test that system with corrupted anomaly list raises error on access."""
        from src.ti4.core.exceptions import AnomalyStateConsistencyError

        system = System("test_system")
        system.add_anomaly_type(AnomalyType.NEBULA)

        # Simulate corruption by directly modifying internal state
        system.anomaly_types.append(None)  # type: ignore

        with pytest.raises(
            AnomalyStateConsistencyError, match="Corrupted anomaly types"
        ):
            system.get_anomaly_types()


class TestMultipleAnomalyTypesEdgeCases:
    """Test edge cases with systems having multiple anomaly types."""

    def test_duplicate_anomaly_types_handled_correctly(self) -> None:
        """Test that adding duplicate anomaly types doesn't create duplicates."""
        system = System("test_system")

        # Add same anomaly type multiple times
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.NEBULA)

        # Should only have one instance
        anomaly_types = system.get_anomaly_types()
        assert len(anomaly_types) == 1
        assert AnomalyType.NEBULA in anomaly_types

    def test_all_four_anomaly_types_on_same_system(self) -> None:
        """Test system with all four anomaly types (extreme edge case)."""
        system = System("extreme_anomaly_system")

        # Add all four anomaly types
        system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.SUPERNOVA)
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # Should have all four types
        anomaly_types = system.get_anomaly_types()
        assert len(anomaly_types) == 4
        assert AnomalyType.ASTEROID_FIELD in anomaly_types
        assert AnomalyType.NEBULA in anomaly_types
        assert AnomalyType.SUPERNOVA in anomaly_types
        assert AnomalyType.GRAVITY_RIFT in anomaly_types

    def test_anomaly_type_removal_from_multiple_types(self) -> None:
        """Test removing specific anomaly type from system with multiple types."""
        system = System("multi_anomaly_system")

        # Add multiple anomaly types
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)
        system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)

        # Remove one type
        system.remove_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # Should have remaining types
        anomaly_types = system.get_anomaly_types()
        assert len(anomaly_types) == 2
        assert AnomalyType.NEBULA in anomaly_types
        assert AnomalyType.ASTEROID_FIELD in anomaly_types
        assert AnomalyType.GRAVITY_RIFT not in anomaly_types

    def test_conflicting_anomaly_effects_handled_correctly(self) -> None:
        """Test that conflicting anomaly effects are handled correctly."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        system = System("conflicting_system")
        # Add both movement-blocking and movement-enhancing anomalies
        system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)  # Blocks movement
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)  # Enhances movement

        manager = AnomalyManager()
        effects = manager.get_anomaly_effects_summary(system)

        # Movement blocking should take precedence
        assert effects["blocks_movement"] is True


class TestAnomaliesWithPlanetsEdgeCases:
    """Test edge cases for anomalies with planets (Rule 9.2a)."""

    def test_anomaly_system_with_multiple_planets(self) -> None:
        """Test anomaly system with multiple planets maintains all properties."""
        system = System("multi_planet_anomaly")

        # Add multiple planets
        planet1 = Planet("Planet Alpha", resources=3, influence=2)
        planet2 = Planet("Planet Beta", resources=1, influence=4)
        planet3 = Planet("Planet Gamma", resources=2, influence=1)

        system.add_planet(planet1)
        system.add_planet(planet2)
        system.add_planet(planet3)

        # Add anomaly type
        system.add_anomaly_type(AnomalyType.NEBULA)

        # Should maintain all planets and anomaly status
        assert system.is_anomaly()
        assert len(system.planets) == 3
        assert system.get_planet_by_name("Planet Alpha") is not None
        assert system.get_planet_by_name("Planet Beta") is not None
        assert system.get_planet_by_name("Planet Gamma") is not None

    def test_planet_added_to_existing_anomaly_system(self) -> None:
        """Test adding planet to existing anomaly system."""
        system = System("existing_anomaly")
        system.add_anomaly_type(AnomalyType.SUPERNOVA)

        # Add planet after anomaly
        planet = Planet("New Planet", resources=2, influence=3)
        system.add_planet(planet)

        # Should maintain both anomaly and planet
        assert system.is_anomaly()
        assert system.has_anomaly_type(AnomalyType.SUPERNOVA)
        assert len(system.planets) == 1
        assert system.planets[0].name == "New Planet"

    def test_anomaly_removed_from_system_with_planets(self) -> None:
        """Test removing anomaly from system with planets preserves planets."""
        system = System("anomaly_with_planets")

        # Add planet and anomaly
        planet = Planet("Test Planet", resources=2, influence=1)
        system.add_planet(planet)
        system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)

        # Remove anomaly
        system.remove_anomaly_type(AnomalyType.ASTEROID_FIELD)

        # Should preserve planet but lose anomaly status
        assert not system.is_anomaly()
        assert len(system.planets) == 1
        assert system.planets[0].name == "Test Planet"


class TestDynamicAnomalyAssignmentEdgeCases:
    """Test edge cases for dynamic anomaly assignment (Rule 9.4-9.5)."""

    def test_rapid_anomaly_type_changes(self) -> None:
        """Test rapid addition and removal of anomaly types."""
        system = System("dynamic_system")

        # Rapidly add and remove different anomaly types
        for _ in range(10):
            system.add_anomaly_type(AnomalyType.NEBULA)
            system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)
            system.remove_anomaly_type(AnomalyType.NEBULA)
            system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)
            system.remove_anomaly_type(AnomalyType.GRAVITY_RIFT)
            system.remove_anomaly_type(AnomalyType.ASTEROID_FIELD)

        # Should end up with no anomalies
        assert not system.is_anomaly()
        assert len(system.get_anomaly_types()) == 0

    def test_anomaly_manager_with_invalid_system_state(self) -> None:
        """Test AnomalyManager handling of invalid system state."""
        from src.ti4.core.anomaly_manager import AnomalyManager
        from src.ti4.core.exceptions import AnomalyStateConsistencyError

        manager = AnomalyManager()

        # Create system with invalid state
        system = System("invalid_system")
        system.system_id = ""  # Make system invalid

        with pytest.raises(AnomalyStateConsistencyError):
            manager.get_anomaly_effects_summary(system)

    def test_concurrent_anomaly_modifications(self) -> None:
        """Test concurrent modifications to anomaly types (thread safety edge case)."""
        import threading
        import time

        system = System("concurrent_system")
        errors = []

        def add_anomalies():
            try:
                for _i in range(100):
                    system.add_anomaly_type(AnomalyType.NEBULA)
                    time.sleep(
                        0.001
                    )  # Small delay to increase chance of race conditions
            except Exception as e:
                errors.append(e)

        def remove_anomalies():
            try:
                for _i in range(100):
                    system.remove_anomaly_type(AnomalyType.NEBULA)
                    time.sleep(
                        0.001
                    )  # Small delay to increase chance of race conditions
            except Exception as e:
                errors.append(e)

        # Run concurrent operations
        thread1 = threading.Thread(target=add_anomalies)
        thread2 = threading.Thread(target=remove_anomalies)

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        # Should not have any errors (system should handle concurrent access gracefully)
        assert len(errors) == 0
        # Final state should be consistent
        assert isinstance(system.get_anomaly_types(), list)


class TestAnomalyManagerErrorHandling:
    """Test comprehensive error handling in AnomalyManager."""

    def test_create_anomaly_system_with_invalid_id(self) -> None:
        """Test creating anomaly system with invalid system ID."""
        from src.ti4.core.anomaly_manager import AnomalyManager
        from src.ti4.core.exceptions import AnomalyStateConsistencyError

        manager = AnomalyManager()

        with pytest.raises(
            AnomalyStateConsistencyError, match="System ID cannot be empty"
        ):
            manager.create_anomaly_system("", [AnomalyType.NEBULA])

    def test_add_anomaly_to_system_with_invalid_type(self) -> None:
        """Test adding invalid anomaly type through manager."""
        from src.ti4.core.anomaly_manager import AnomalyManager
        from src.ti4.core.exceptions import InvalidAnomalyTypeError

        manager = AnomalyManager()
        system = System("test_system")

        with pytest.raises(InvalidAnomalyTypeError):
            manager.add_anomaly_to_system(system, "invalid_type")  # type: ignore

    def test_manager_operations_with_corrupted_system(self) -> None:
        """Test manager operations with corrupted system state."""
        from src.ti4.core.anomaly_manager import AnomalyManager
        from src.ti4.core.exceptions import AnomalyStateConsistencyError

        manager = AnomalyManager()
        system = System("test_system")

        # Corrupt the system by setting invalid system_id
        system.system_id = None  # type: ignore

        with pytest.raises(AnomalyStateConsistencyError):
            manager.get_anomaly_effects_summary(system)


class TestMovementRuleErrorHandling:
    """Test error handling in movement rules with anomalies."""

    def test_movement_context_with_invalid_galaxy(self) -> None:
        """Test movement validation with invalid galaxy state."""
        from src.ti4.core.constants import UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule, MovementContext
        from src.ti4.core.unit import Unit

        # Create movement context with empty galaxy
        galaxy = Galaxy()
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        context = MovementContext(
            unit=unit,
            from_coordinate=HexCoordinate(0, 0),
            to_coordinate=HexCoordinate(1, 0),
            player_technologies=set(),
            galaxy=galaxy,
        )

        anomaly_rule = AnomalyRule()

        # Should handle missing systems gracefully
        # This should not raise an exception, but return a safe default
        result = anomaly_rule.can_move(context)
        assert isinstance(result, bool)

    def test_gravity_rift_destruction_with_invalid_roll(self) -> None:
        """Test gravity rift destruction with invalid dice roll values."""
        from src.ti4.core.constants import UnitType
        from src.ti4.core.movement_rules import AnomalyRule
        from src.ti4.core.unit import Unit

        anomaly_rule = AnomalyRule()
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")

        # Test invalid roll values
        with pytest.raises(ValueError, match="Invalid dice roll value"):
            anomaly_rule.check_gravity_rift_destruction(unit, 0)

        with pytest.raises(ValueError, match="Invalid dice roll value"):
            anomaly_rule.check_gravity_rift_destruction(unit, 11)

        with pytest.raises(ValueError, match="Invalid dice roll value"):
            anomaly_rule.check_gravity_rift_destruction(unit, -1)


class TestSystemInfoDisplayErrorHandling:
    """Test error handling in system information display."""

    def test_system_info_display_with_invalid_state(self) -> None:
        """Test system info display with invalid system state."""
        from src.ti4.core.exceptions import AnomalyStateConsistencyError

        system = System("test_system")
        system.system_id = ""  # Make system invalid

        with pytest.raises(
            AnomalyStateConsistencyError, match="System ID cannot be empty"
        ):
            system.get_system_info_display()

    def test_system_info_display_with_corrupted_planets(self) -> None:
        """Test system info display with corrupted planet data."""
        system = System("test_system")
        system.add_anomaly_type(AnomalyType.NEBULA)

        # Add corrupted planet data
        system.planets.append(None)  # type: ignore

        # Should handle corrupted data gracefully
        info = system.get_system_info_display()
        assert isinstance(info, dict)
        assert "planets" in info
        # Should filter out None planets
        assert all(planet is not None for planet in info["planets"])

    def test_system_info_display_with_anomaly_manager_failure(self) -> None:
        """Test system info display when AnomalyManager fails."""
        system = System("test_system")
        system.add_anomaly_type(AnomalyType.NEBULA)

        # Mock AnomalyManager to fail by corrupting system state temporarily
        original_anomaly_types = system.anomaly_types
        system.anomaly_types = [None]  # type: ignore

        # Should handle AnomalyManager failure gracefully
        info = system.get_system_info_display()
        assert isinstance(info, dict)
        assert "effects_summary" in info

        # Restore original state
        system.anomaly_types = original_anomaly_types
