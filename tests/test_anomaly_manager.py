"""
Tests for AnomalyManager class - high-level anomaly management interface.

This module tests the AnomalyManager class which provides a high-level
interface for managing anomaly systems and coordinating anomaly operations.

LRR References:
- Rule 9.4: Ability-created anomalies
- Rule 9.5: Multiple anomaly types on same system
"""

import pytest

from src.ti4.core.constants import AnomalyType
from src.ti4.core.planet import Planet
from src.ti4.core.system import System


class TestAnomalyManager:
    """Test AnomalyManager high-level interface."""

    def test_anomaly_manager_import(self) -> None:
        """Test that AnomalyManager can be imported."""
        # This test will fail initially (RED phase)
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        assert manager is not None

    def test_create_anomaly_system_single_type(self) -> None:
        """Test creating an anomaly system with a single anomaly type."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        system = manager.create_anomaly_system("test_system", [AnomalyType.NEBULA])

        assert system.system_id == "test_system"
        assert system.is_anomaly()
        assert system.has_anomaly_type(AnomalyType.NEBULA)
        assert len(system.get_anomaly_types()) == 1

    def test_create_anomaly_system_multiple_types(self) -> None:
        """Test creating an anomaly system with multiple anomaly types."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        anomaly_types = [
            AnomalyType.NEBULA,
            AnomalyType.GRAVITY_RIFT,
            AnomalyType.ASTEROID_FIELD,
        ]
        system = manager.create_anomaly_system("multi_anomaly", anomaly_types)

        assert system.system_id == "multi_anomaly"
        assert system.is_anomaly()
        for anomaly_type in anomaly_types:
            assert system.has_anomaly_type(anomaly_type)
        assert len(system.get_anomaly_types()) == 3

    def test_create_anomaly_system_empty_types_list(self) -> None:
        """Test creating system with empty anomaly types list creates normal system."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        system = manager.create_anomaly_system("normal_system", [])

        assert system.system_id == "normal_system"
        assert not system.is_anomaly()
        assert system.get_anomaly_types() == []

    def test_get_anomaly_effects_summary_single_anomaly(self) -> None:
        """Test getting anomaly effects summary for system with single anomaly."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        system = System("nebula_system")
        system.add_anomaly_type(AnomalyType.NEBULA)

        effects = manager.get_anomaly_effects_summary(system)

        assert isinstance(effects, dict)
        assert "anomaly_types" in effects
        assert AnomalyType.NEBULA in effects["anomaly_types"]
        assert "blocks_movement" in effects
        assert "requires_active_system" in effects
        assert "move_value_modifier" in effects
        assert "combat_bonus" in effects

    def test_get_anomaly_effects_summary_multiple_anomalies(self) -> None:
        """Test getting anomaly effects summary for system with multiple anomalies."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        system = System("multi_anomaly_system")
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        effects = manager.get_anomaly_effects_summary(system)

        assert isinstance(effects, dict)
        assert len(effects["anomaly_types"]) == 2
        assert AnomalyType.NEBULA in effects["anomaly_types"]
        assert AnomalyType.GRAVITY_RIFT in effects["anomaly_types"]

    def test_get_anomaly_effects_summary_normal_system(self) -> None:
        """Test getting anomaly effects summary for normal system."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        system = System("normal_system")

        effects = manager.get_anomaly_effects_summary(system)

        assert isinstance(effects, dict)
        assert effects["anomaly_types"] == []
        assert not effects["blocks_movement"]
        assert not effects["requires_active_system"]
        assert effects["move_value_modifier"] == 0
        assert effects["combat_bonus"] == 0

    def test_add_anomaly_to_existing_system(self) -> None:
        """Test adding anomaly type to existing system through manager."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        system = System("existing_system")

        # Add planet to system first
        planet = Planet("Test Planet", resources=2, influence=1)
        system.add_planet(planet)

        # Add anomaly through manager
        manager.add_anomaly_to_system(system, AnomalyType.NEBULA)

        # System should now be an anomaly but preserve planet
        assert system.is_anomaly()
        assert system.has_anomaly_type(AnomalyType.NEBULA)
        assert len(system.planets) == 1
        assert system.planets[0].name == "Test Planet"

    def test_remove_anomaly_from_system(self) -> None:
        """Test removing anomaly type from system through manager."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        system = System("anomaly_system")
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # Remove one anomaly through manager
        manager.remove_anomaly_from_system(system, AnomalyType.GRAVITY_RIFT)

        # Should still have nebula but not gravity rift
        assert system.is_anomaly()
        assert system.has_anomaly_type(AnomalyType.NEBULA)
        assert not system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)

    def test_clear_all_anomalies_from_system(self) -> None:
        """Test clearing all anomalies from system through manager."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        system = System("anomaly_system")
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)
        system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)

        # Add planet to verify it's preserved
        planet = Planet("Test Planet", resources=2, influence=1)
        system.add_planet(planet)

        # Clear all anomalies
        manager.clear_all_anomalies_from_system(system)

        # Should no longer be anomaly but preserve planet
        assert not system.is_anomaly()
        assert system.get_anomaly_types() == []
        assert len(system.planets) == 1
        assert system.planets[0].name == "Test Planet"

    def test_convert_system_to_anomaly_type(self) -> None:
        """Test converting normal system to specific anomaly type."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        system = System("normal_system")

        # Add some properties first
        planet = Planet("Test Planet", resources=2, influence=1)
        system.add_planet(planet)
        system.add_wormhole("alpha")

        # Convert to anomaly
        manager.convert_system_to_anomaly_type(system, AnomalyType.SUPERNOVA)

        # Should be anomaly but preserve other properties
        assert system.is_anomaly()
        assert system.has_anomaly_type(AnomalyType.SUPERNOVA)
        assert len(system.planets) == 1
        assert system.has_wormhole("alpha")

    def test_is_system_blocking_movement(self) -> None:
        """Test checking if system blocks movement through manager."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()

        # Normal system should not block
        normal_system = System("normal_system")
        assert not manager.is_system_blocking_movement(normal_system)

        # Asteroid field should block
        asteroid_system = System("asteroid_system")
        asteroid_system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)
        assert manager.is_system_blocking_movement(asteroid_system)

        # Supernova should block
        supernova_system = System("supernova_system")
        supernova_system.add_anomaly_type(AnomalyType.SUPERNOVA)
        assert manager.is_system_blocking_movement(supernova_system)

        # Nebula should block (when not active)
        nebula_system = System("nebula_system")
        nebula_system.add_anomaly_type(AnomalyType.NEBULA)
        assert manager.is_system_blocking_movement(nebula_system)

        # Gravity rift should not block
        rift_system = System("rift_system")
        rift_system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)
        assert not manager.is_system_blocking_movement(rift_system)

    def test_get_system_move_value_modifier(self) -> None:
        """Test getting move value modifier for system through manager."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()

        # Normal system should have no modifier
        normal_system = System("normal_system")
        assert manager.get_system_move_value_modifier(normal_system) == 0

        # Nebula should reduce move value to 1 (modifier depends on base move value)
        nebula_system = System("nebula_system")
        nebula_system.add_anomaly_type(AnomalyType.NEBULA)
        # For nebula, the modifier is context-dependent, but we can test that it's recognized
        modifier = manager.get_system_move_value_modifier(nebula_system)
        assert isinstance(modifier, int)

        # Gravity rift provides bonus when exiting (context-dependent)
        rift_system = System("rift_system")
        rift_system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)
        modifier = manager.get_system_move_value_modifier(rift_system)
        assert isinstance(modifier, int)


class TestAnomalyManagerErrorHandling:
    """Test error handling in AnomalyManager."""

    def test_invalid_anomaly_type_raises_error(self) -> None:
        """Test that invalid anomaly types raise appropriate errors."""
        from src.ti4.core.anomaly_manager import AnomalyManager
        from src.ti4.core.exceptions import InvalidAnomalyTypeError

        manager = AnomalyManager()
        system = System("test_system")

        with pytest.raises(InvalidAnomalyTypeError):
            manager.add_anomaly_to_system(system, "invalid_anomaly")  # type: ignore

    def test_none_system_raises_error(self) -> None:
        """Test that None system raises appropriate errors."""
        from src.ti4.core.anomaly_manager import AnomalyManager
        from src.ti4.core.exceptions import AnomalyStateConsistencyError

        manager = AnomalyManager()

        with pytest.raises(AnomalyStateConsistencyError):
            manager.add_anomaly_to_system(None, AnomalyType.NEBULA)  # type: ignore

        with pytest.raises(AnomalyStateConsistencyError):
            manager.get_anomaly_effects_summary(None)  # type: ignore

    def test_none_anomaly_type_raises_error(self) -> None:
        """Test that None anomaly type raises appropriate errors."""
        from src.ti4.core.anomaly_manager import AnomalyManager
        from src.ti4.core.exceptions import InvalidAnomalyTypeError

        manager = AnomalyManager()
        system = System("test_system")

        with pytest.raises(InvalidAnomalyTypeError):
            manager.add_anomaly_to_system(system, None)  # type: ignore

        with pytest.raises(InvalidAnomalyTypeError):
            manager.convert_system_to_anomaly_type(system, None)  # type: ignore
