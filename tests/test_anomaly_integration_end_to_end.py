"""
Integration tests for Rule 9: ANOMALIES - End-to-end scenarios

This module contains comprehensive integration tests that validate the entire
anomaly system working together with existing TI4 systems including movement,
combat, and system management.

LRR References:
- Rule 9: ANOMALIES (core anomaly system)
- Rule 11: ASTEROID FIELD (movement blocking)
- Rule 41: GRAVITY RIFT (movement bonuses and destruction)
- Rule 59: NEBULA (movement restrictions and combat bonuses)
- Rule 86: SUPERNOVA (movement blocking)
- Rule 58: MOVEMENT (integration with anomaly rules)
- Rule 78: SPACE COMBAT (integration with nebula bonuses)
"""

import pytest
from unittest.mock import Mock, patch

from src.ti4.core.anomaly_manager import AnomalyManager
from src.ti4.core.constants import AnomalyType
from src.ti4.core.system import System
from src.ti4.core.unit import Unit, UnitType


class TestAnomalySystemIntegration:
    """Test complete anomaly system integration with existing TI4 systems"""

    def setup_method(self):
        """Set up test fixtures for each test"""
        self.anomaly_manager = AnomalyManager()
        
        # Create test systems
        self.normal_system = System("normal_system")
        self.asteroid_system = self.anomaly_manager.create_anomaly_system(
            "asteroid_system", [AnomalyType.ASTEROID_FIELD]
        )
        self.nebula_system = self.anomaly_manager.create_anomaly_system(
            "nebula_system", [AnomalyType.NEBULA]
        )
        self.gravity_rift_system = self.anomaly_manager.create_anomaly_system(
            "gravity_rift_system", [AnomalyType.GRAVITY_RIFT]
        )
        self.supernova_system = self.anomaly_manager.create_anomaly_system(
            "supernova_system", [AnomalyType.SUPERNOVA]
        )

    def test_anomaly_system_creation_and_identification(self):
        """Test that anomaly systems are properly created and identified"""
        # Test asteroid field system
        assert self.asteroid_system.is_anomaly()
        assert self.asteroid_system.has_anomaly_type(AnomalyType.ASTEROID_FIELD)
        
        # Test nebula system
        assert self.nebula_system.is_anomaly()
        assert self.nebula_system.has_anomaly_type(AnomalyType.NEBULA)
        
        # Test gravity rift system
        assert self.gravity_rift_system.is_anomaly()
        assert self.gravity_rift_system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)
        
        # Test supernova system
        assert self.supernova_system.is_anomaly()
        assert self.supernova_system.has_anomaly_type(AnomalyType.SUPERNOVA)
        
        # Test normal system
        assert not self.normal_system.is_anomaly()

    def test_anomaly_effects_summary_integration(self):
        """Test that anomaly effects are properly summarized"""
        # Test asteroid field effects
        asteroid_effects = self.anomaly_manager.get_anomaly_effects_summary(self.asteroid_system)
        assert asteroid_effects["blocks_movement"] is True
        assert asteroid_effects["requires_active_system"] is False
        assert AnomalyType.ASTEROID_FIELD in asteroid_effects["anomaly_types"]
        
        # Test nebula effects
        nebula_effects = self.anomaly_manager.get_anomaly_effects_summary(self.nebula_system)
        assert nebula_effects["blocks_movement"] is True  # Nebula blocks movement when not active
        assert nebula_effects["requires_active_system"] is True
        assert AnomalyType.NEBULA in nebula_effects["anomaly_types"]
        
        # Test gravity rift effects
        gravity_effects = self.anomaly_manager.get_anomaly_effects_summary(self.gravity_rift_system)
        assert gravity_effects["blocks_movement"] is False  # Gravity rift doesn't block movement
        assert gravity_effects["requires_active_system"] is False
        assert AnomalyType.GRAVITY_RIFT in gravity_effects["anomaly_types"]
        
        # Test normal system effects
        normal_effects = self.anomaly_manager.get_anomaly_effects_summary(self.normal_system)
        assert normal_effects["blocks_movement"] is False
        assert normal_effects["requires_active_system"] is False
        assert len(normal_effects["anomaly_types"]) == 0

    def test_movement_blocking_detection(self):
        """Test that movement blocking is properly detected"""
        # Test systems that block movement
        assert self.anomaly_manager.is_system_blocking_movement(self.asteroid_system) is True
        assert self.anomaly_manager.is_system_blocking_movement(self.supernova_system) is True
        assert self.anomaly_manager.is_system_blocking_movement(self.nebula_system) is True
        
        # Test systems that don't block movement
        assert self.anomaly_manager.is_system_blocking_movement(self.gravity_rift_system) is False
        assert self.anomaly_manager.is_system_blocking_movement(self.normal_system) is False

    def test_move_value_modifiers(self):
        """Test that move value modifiers are calculated correctly"""
        # Test gravity rift modifier
        gravity_modifier = self.anomaly_manager.get_system_move_value_modifier(self.gravity_rift_system)
        assert gravity_modifier == 1  # Gravity rift gives +1 move value
        
        # Test nebula modifier
        nebula_modifier = self.anomaly_manager.get_system_move_value_modifier(self.nebula_system)
        assert nebula_modifier == -1  # Nebula reduces move value to 1 (represented as -1 modifier)
        
        # Test normal system modifier
        normal_modifier = self.anomaly_manager.get_system_move_value_modifier(self.normal_system)
        assert normal_modifier == 0  # No modifier for normal systems

    def test_multiple_anomaly_types_on_same_system(self):
        """Test systems with multiple anomaly types"""
        # Create system with multiple anomaly types
        multi_anomaly_system = self.anomaly_manager.create_anomaly_system(
            "multi_anomaly", [AnomalyType.NEBULA, AnomalyType.GRAVITY_RIFT]
        )
        
        # Verify both anomaly types are present
        assert multi_anomaly_system.has_anomaly_type(AnomalyType.NEBULA)
        assert multi_anomaly_system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)
        
        # Test effects summary includes both types
        effects = self.anomaly_manager.get_anomaly_effects_summary(multi_anomaly_system)
        assert AnomalyType.NEBULA in effects["anomaly_types"]
        assert AnomalyType.GRAVITY_RIFT in effects["anomaly_types"]
        
        # Should have nebula blocking behavior (most restrictive)
        assert effects["blocks_movement"] is True
        assert effects["requires_active_system"] is True

    def test_dynamic_anomaly_assignment(self):
        """Test adding and removing anomaly types dynamically"""
        # Start with normal system
        test_system = System("dynamic_test")
        assert not test_system.is_anomaly()
        
        # Add anomaly type
        self.anomaly_manager.add_anomaly_to_system(test_system, AnomalyType.NEBULA)
        assert test_system.is_anomaly()
        assert test_system.has_anomaly_type(AnomalyType.NEBULA)
        
        # Add second anomaly type
        self.anomaly_manager.add_anomaly_to_system(test_system, AnomalyType.GRAVITY_RIFT)
        assert test_system.has_anomaly_type(AnomalyType.NEBULA)
        assert test_system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)
        
        # Remove one anomaly type
        self.anomaly_manager.remove_anomaly_from_system(test_system, AnomalyType.NEBULA)
        assert not test_system.has_anomaly_type(AnomalyType.NEBULA)
        assert test_system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)
        assert test_system.is_anomaly()  # Still anomaly due to gravity rift
        
        # Clear all anomalies
        self.anomaly_manager.clear_all_anomalies_from_system(test_system)
        assert not test_system.is_anomaly()
        assert len(test_system.get_anomaly_types()) == 0


class TestAnomalyCombatIntegration:
    """Test anomaly integration with combat system"""

    def setup_method(self):
        """Set up test fixtures for combat tests"""
        self.anomaly_manager = AnomalyManager()
        self.nebula_system = self.anomaly_manager.create_anomaly_system(
            "nebula_system", [AnomalyType.NEBULA]
        )

    def test_nebula_combat_effects_in_summary(self):
        """Test that nebula combat effects are included in effects summary"""
        effects = self.anomaly_manager.get_anomaly_effects_summary(self.nebula_system)
        
        # Should have combat bonus for nebula
        assert effects["combat_bonus"] == 1
        assert AnomalyType.NEBULA in effects["anomaly_types"]

    def test_multiple_anomaly_combat_effects_stacking(self):
        """Test combat effects when system has multiple anomaly types"""
        # Create system with multiple anomaly types
        multi_anomaly_system = self.anomaly_manager.create_anomaly_system(
            "multi_anomaly", [AnomalyType.NEBULA, AnomalyType.GRAVITY_RIFT]
        )
        
        # Get all combat effects
        effects = self.anomaly_manager.get_anomaly_effects_summary(multi_anomaly_system)
        
        # Should have nebula combat bonus
        assert effects["combat_bonus"] == 1
        # Should have both anomaly types
        assert AnomalyType.NEBULA in effects["anomaly_types"]
        assert AnomalyType.GRAVITY_RIFT in effects["anomaly_types"]


class TestAnomalySystemCompatibility:
    """Test backward compatibility and system integration"""

    def setup_method(self):
        """Set up test fixtures for compatibility tests"""
        self.anomaly_manager = AnomalyManager()

    def test_existing_system_tile_compatibility(self):
        """Test that anomaly systems work with existing SystemTile interface"""
        from src.ti4.core.system_tile import SystemTile, TileType
        
        # Create anomaly system tile
        anomaly_tile = SystemTile(
            tile_id="test_anomaly",
            tile_type=TileType.ANOMALY,
            systems=[]
        )
        
        # Should be identified as anomaly
        assert anomaly_tile.is_anomaly()
        
        # Create anomaly system and add to tile
        anomaly_system = self.anomaly_manager.create_anomaly_system(
            "test_system", [AnomalyType.NEBULA]
        )
        anomaly_tile.systems.append(anomaly_system)
        
        # Verify integration
        assert len(anomaly_tile.systems) == 1
        assert anomaly_tile.systems[0].is_anomaly()

    def test_anomaly_system_with_planets_compatibility(self):
        """Test that anomaly systems can contain planets"""
        from src.ti4.core.planet import Planet
        
        # Create anomaly system with planets
        anomaly_system = self.anomaly_manager.create_anomaly_system(
            "anomaly_with_planets", [AnomalyType.NEBULA]
        )
        
        # Add planets to the system
        planet1 = Planet("planet1", resources=2, influence=1)
        planet2 = Planet("planet2", resources=1, influence=3)
        
        anomaly_system.planets = [planet1, planet2]
        
        # System should still be anomaly and have planets
        assert anomaly_system.is_anomaly()
        assert len(anomaly_system.planets) == 2
        assert anomaly_system.has_anomaly_type(AnomalyType.NEBULA)

    def test_dynamic_anomaly_assignment_compatibility(self):
        """Test adding/removing anomaly types from existing systems"""
        # Start with normal system
        normal_system = System("test_system")
        assert not normal_system.is_anomaly()
        
        # Convert to anomaly system
        anomaly_system = self.anomaly_manager.convert_system_to_anomaly_type(
            normal_system, AnomalyType.GRAVITY_RIFT
        )
        
        assert anomaly_system.is_anomaly()
        assert anomaly_system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)
        
        # Add second anomaly type
        self.anomaly_manager.add_anomaly_to_system(anomaly_system, AnomalyType.NEBULA)
        
        assert anomaly_system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)
        assert anomaly_system.has_anomaly_type(AnomalyType.NEBULA)
        
        # Remove one anomaly type
        self.anomaly_manager.remove_anomaly_from_system(anomaly_system, AnomalyType.GRAVITY_RIFT)
        
        assert not anomaly_system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)
        assert anomaly_system.has_anomaly_type(AnomalyType.NEBULA)
        assert anomaly_system.is_anomaly()  # Still anomaly due to nebula


class TestAnomalyPerformanceAndValidation:
    """Test performance characteristics and validation of anomaly system"""

    def setup_method(self):
        """Set up test fixtures for performance tests"""
        self.anomaly_manager = AnomalyManager()

    def test_large_scale_anomaly_operations_performance(self):
        """Test performance with many anomaly systems"""
        import time
        
        # Create many anomaly systems
        anomaly_systems = []
        start_time = time.time()
        
        for i in range(1000):
            system = self.anomaly_manager.create_anomaly_system(
                f"system_{i}", [AnomalyType.NEBULA]
            )
            anomaly_systems.append(system)
        
        creation_time = time.time() - start_time
        
        # Should create 1000 systems in reasonable time (< 1 second)
        assert creation_time < 1.0
        
        # Test querying performance
        start_time = time.time()
        
        for system in anomaly_systems:
            effects = self.anomaly_manager.get_anomaly_effects_summary(system)
            assert effects is not None
        
        query_time = time.time() - start_time
        
        # Should query 1000 systems in reasonable time (< 0.5 seconds)
        assert query_time < 0.5

    def test_anomaly_validation_edge_cases(self):
        """Test validation of edge cases and error conditions"""
        # Test invalid anomaly type
        with pytest.raises(ValueError):
            self.anomaly_manager.create_anomaly_system(
                "invalid_system", ["invalid_anomaly_type"]
            )
        
        # Test empty anomaly types list
        system = self.anomaly_manager.create_anomaly_system(
            "empty_system", []
        )
        assert not system.is_anomaly()
        
        # Test None system ID
        with pytest.raises(ValueError):
            self.anomaly_manager.create_anomaly_system(None, [AnomalyType.NEBULA])
        
        # Test duplicate anomaly types
        system = self.anomaly_manager.create_anomaly_system(
            "duplicate_system", [AnomalyType.NEBULA, AnomalyType.NEBULA]
        )
        # Should deduplicate automatically
        assert len(system.get_anomaly_types()) == 1

    def test_memory_usage_with_complex_anomaly_systems(self):
        """Test memory efficiency with complex anomaly configurations"""
        import sys
        
        # Create complex anomaly system
        complex_system = self.anomaly_manager.create_anomaly_system(
            "complex_system", 
            [AnomalyType.NEBULA, AnomalyType.GRAVITY_RIFT, AnomalyType.ASTEROID_FIELD]
        )
        
        # Get initial memory usage
        initial_size = sys.getsizeof(complex_system)
        
        # Add many operations
        for _ in range(100):
            effects = self.anomaly_manager.get_anomaly_effects_summary(complex_system)
            modifiers = self.anomaly_manager.get_combat_modifiers(complex_system, True)
        
        # Memory usage should not grow significantly
        final_size = sys.getsizeof(complex_system)
        growth_ratio = final_size / initial_size
        
        # Should not grow by more than 50%
        assert growth_ratio < 1.5


class TestAnomalyErrorHandlingIntegration:
    """Test comprehensive error handling across the anomaly system"""

    def setup_method(self):
        """Set up test fixtures for error handling tests"""
        self.anomaly_manager = AnomalyManager()

    def test_movement_error_propagation(self):
        """Test that movement errors are properly propagated with context"""
        asteroid_system = self.anomaly_manager.create_anomaly_system(
            "asteroid_system", [AnomalyType.ASTEROID_FIELD]
        )
        
        cruiser = Unit(UnitType.CRUISER, player_id="player1")
        
        # Attempt movement into asteroid field
        with pytest.raises(AnomalyMovementError) as exc_info:
            self.anomaly_manager.validate_movement_into_system(
                cruiser, asteroid_system, is_active_system=False
            )
        
        error = exc_info.value
        assert "asteroid field" in str(error).lower()
        assert "blocks movement" in str(error).lower()
        assert asteroid_system.system_id in str(error)

    def test_combat_integration_error_handling(self):
        """Test error handling in combat integration scenarios"""
        # Test with invalid system
        with pytest.raises(ValueError):
            self.anomaly_manager.get_combat_modifiers(None, is_defender=True)
        
        # Test with corrupted anomaly system
        corrupted_system = System("corrupted")
        corrupted_system.anomaly_types = ["invalid_type"]  # Corrupt the data
        
        with pytest.raises(ValueError):
            self.anomaly_manager.get_anomaly_effects_summary(corrupted_system)

    def test_system_state_consistency_validation(self):
        """Test validation of system state consistency"""
        # Create system and then corrupt its state
        system = self.anomaly_manager.create_anomaly_system(
            "test_system", [AnomalyType.NEBULA]
        )
        
        # Corrupt the anomaly types
        system.anomaly_types = None
        
        # Should detect inconsistency
        with pytest.raises(ValueError):
            self.anomaly_manager.validate_system_state(system)
        
        # Test with empty but valid state
        system.anomaly_types = []
        result = self.anomaly_manager.validate_system_state(system)
        assert result.valid
        assert not result.is_anomaly