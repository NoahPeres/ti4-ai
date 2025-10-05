"""
Simple integration tests for Rule 9: ANOMALIES

This module contains basic integration tests that validate the core
anomaly system functionality that has been implemented.

LRR References:
- Rule 9: ANOMALIES (core anomaly system)
"""

import pytest

from src.ti4.core.anomaly_manager import AnomalyManager
from src.ti4.core.constants import AnomalyType
from src.ti4.core.planet import Planet
from src.ti4.core.system import System


class TestAnomalyIntegrationBasic:
    """Test basic anomaly system integration"""

    def setup_method(self):
        """Set up test fixtures for each test"""
        self.anomaly_manager = AnomalyManager()

    def test_anomaly_system_creation_and_effects(self):
        """Test creating anomaly systems and getting their effects"""
        # Create different types of anomaly systems
        asteroid_system = self.anomaly_manager.create_anomaly_system(
            "asteroid_system", [AnomalyType.ASTEROID_FIELD]
        )
        nebula_system = self.anomaly_manager.create_anomaly_system(
            "nebula_system", [AnomalyType.NEBULA]
        )
        gravity_rift_system = self.anomaly_manager.create_anomaly_system(
            "gravity_rift_system", [AnomalyType.GRAVITY_RIFT]
        )
        supernova_system = self.anomaly_manager.create_anomaly_system(
            "supernova_system", [AnomalyType.SUPERNOVA]
        )

        # Test asteroid field effects
        asteroid_effects = self.anomaly_manager.get_anomaly_effects_summary(
            asteroid_system
        )
        assert asteroid_effects["blocks_movement"] is True
        assert asteroid_effects["requires_active_system"] is False
        assert asteroid_effects["move_value_modifier"] == 0
        assert asteroid_effects["combat_bonus"] == 0
        assert AnomalyType.ASTEROID_FIELD in asteroid_effects["anomaly_types"]

        # Test nebula effects
        nebula_effects = self.anomaly_manager.get_anomaly_effects_summary(nebula_system)
        assert (
            nebula_effects["blocks_movement"] is False
        )  # Nebula blocks conditionally, not absolutely
        assert nebula_effects["requires_active_system"] is True
        assert nebula_effects["move_value_modifier"] == -1
        assert nebula_effects["combat_bonus"] == 1
        assert AnomalyType.NEBULA in nebula_effects["anomaly_types"]

        # Test gravity rift effects
        gravity_effects = self.anomaly_manager.get_anomaly_effects_summary(
            gravity_rift_system
        )
        assert gravity_effects["blocks_movement"] is False
        assert gravity_effects["requires_active_system"] is False
        assert gravity_effects["move_value_modifier"] == 1
        assert gravity_effects["combat_bonus"] == 0
        assert AnomalyType.GRAVITY_RIFT in gravity_effects["anomaly_types"]

        # Test supernova effects
        supernova_effects = self.anomaly_manager.get_anomaly_effects_summary(
            supernova_system
        )
        assert supernova_effects["blocks_movement"] is True
        assert supernova_effects["requires_active_system"] is False
        assert supernova_effects["move_value_modifier"] == 0
        assert supernova_effects["combat_bonus"] == 0
        assert AnomalyType.SUPERNOVA in supernova_effects["anomaly_types"]

    def test_normal_system_has_no_anomaly_effects(self):
        """Test that normal systems have no anomaly effects"""
        normal_system = System("normal_system")

        effects = self.anomaly_manager.get_anomaly_effects_summary(normal_system)
        assert effects["blocks_movement"] is False
        assert effects["requires_active_system"] is False
        assert effects["move_value_modifier"] == 0
        assert effects["combat_bonus"] == 0
        assert len(effects["anomaly_types"]) == 0

    def test_multiple_anomaly_types_on_same_system(self):
        """Test systems with multiple anomaly types"""
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

        # Should have nebula conditional blocking behavior
        assert (
            effects["blocks_movement"] is False
        )  # No absolute blockers (asteroid/supernova)
        assert effects["requires_active_system"] is True
        assert effects["combat_bonus"] == 1  # Nebula combat bonus

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
        self.anomaly_manager.add_anomaly_to_system(
            test_system, AnomalyType.GRAVITY_RIFT
        )
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

    def test_anomaly_systems_with_planets(self):
        """Test that anomaly systems can contain planets"""
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

        # Effects should still work
        effects = self.anomaly_manager.get_anomaly_effects_summary(anomaly_system)
        assert (
            effects["blocks_movement"] is False
        )  # Nebula blocks conditionally, not absolutely
        assert effects["combat_bonus"] == 1

    def test_movement_blocking_detection(self):
        """Test that movement blocking is properly detected"""
        # Create different anomaly systems
        asteroid_system = self.anomaly_manager.create_anomaly_system(
            "asteroid", [AnomalyType.ASTEROID_FIELD]
        )
        nebula_system = self.anomaly_manager.create_anomaly_system(
            "nebula", [AnomalyType.NEBULA]
        )
        gravity_rift_system = self.anomaly_manager.create_anomaly_system(
            "gravity_rift", [AnomalyType.GRAVITY_RIFT]
        )
        supernova_system = self.anomaly_manager.create_anomaly_system(
            "supernova", [AnomalyType.SUPERNOVA]
        )
        normal_system = System("normal")

        # Test systems that block movement
        assert self.anomaly_manager.is_system_blocking_movement(asteroid_system) is True
        assert (
            self.anomaly_manager.is_system_blocking_movement(supernova_system) is True
        )
        assert (
            self.anomaly_manager.is_system_blocking_movement(nebula_system) is False
        )  # Nebula blocks conditionally

        # Test systems that don't block movement
        assert (
            self.anomaly_manager.is_system_blocking_movement(gravity_rift_system)
            is False
        )
        assert self.anomaly_manager.is_system_blocking_movement(normal_system) is False

    def test_move_value_modifiers(self):
        """Test that move value modifiers are calculated correctly"""
        # Create different anomaly systems
        gravity_rift_system = self.anomaly_manager.create_anomaly_system(
            "gravity_rift", [AnomalyType.GRAVITY_RIFT]
        )
        nebula_system = self.anomaly_manager.create_anomaly_system(
            "nebula", [AnomalyType.NEBULA]
        )
        normal_system = System("normal")

        # Test gravity rift modifier
        gravity_modifier = self.anomaly_manager.get_system_move_value_modifier(
            gravity_rift_system
        )
        assert gravity_modifier == 1  # Gravity rift gives +1 move value

        # Test nebula modifier
        nebula_modifier = self.anomaly_manager.get_system_move_value_modifier(
            nebula_system
        )
        assert (
            nebula_modifier == -1
        )  # Nebula reduces move value to 1 (represented as -1 modifier)

        # Test normal system modifier
        normal_modifier = self.anomaly_manager.get_system_move_value_modifier(
            normal_system
        )
        assert normal_modifier == 0  # No modifier for normal systems

    def test_performance_with_many_systems(self):
        """Test that the system performs well with many anomaly systems"""
        # Create many anomaly systems
        systems = []

        for i in range(100):
            anomaly_type = list(AnomalyType)[i % len(AnomalyType)]
            system = self.anomaly_manager.create_anomaly_system(
                f"system_{i}", [anomaly_type]
            )
            systems.append(system)

        assert len(systems) == 100

        for system in systems:
            effects = self.anomaly_manager.get_anomaly_effects_summary(system)
            assert effects is not None

    def test_error_handling_with_invalid_inputs(self):
        """Test error handling with invalid inputs"""
        from src.ti4.core.exceptions import (
            AnomalyStateConsistencyError,
            InvalidAnomalyTypeError,
        )

        # Test with None system
        with pytest.raises(AnomalyStateConsistencyError):
            self.anomaly_manager.get_anomaly_effects_summary(None)

        # Test with empty system ID
        with pytest.raises(AnomalyStateConsistencyError):
            self.anomaly_manager.create_anomaly_system("", [AnomalyType.NEBULA])

        # Test with invalid anomaly type (this should be caught by the system)
        with pytest.raises(InvalidAnomalyTypeError):
            system = System("test")
            system.add_anomaly_type("invalid_type")  # This should fail

    def test_system_state_consistency(self):
        """Test that system state remains consistent after operations"""
        # Create system and perform multiple operations
        system = self.anomaly_manager.create_anomaly_system(
            "consistency_test", [AnomalyType.NEBULA]
        )

        # Add planets
        planet = Planet("test_planet", resources=2, influence=1)
        system.planets = [planet]

        # Add another anomaly type
        self.anomaly_manager.add_anomaly_to_system(system, AnomalyType.GRAVITY_RIFT)

        # Remove original anomaly type
        self.anomaly_manager.remove_anomaly_from_system(system, AnomalyType.NEBULA)

        # Verify final state is consistent
        assert system.is_anomaly()  # Still anomaly due to gravity rift
        assert system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)
        assert not system.has_anomaly_type(AnomalyType.NEBULA)
        assert len(system.planets) == 1  # Planets preserved
        assert system.planets[0].name == "test_planet"

        # Effects should reflect current state
        effects = self.anomaly_manager.get_anomaly_effects_summary(system)
        assert AnomalyType.GRAVITY_RIFT in effects["anomaly_types"]
        assert AnomalyType.NEBULA not in effects["anomaly_types"]
        assert effects["blocks_movement"] is False  # Gravity rift doesn't block
        assert effects["move_value_modifier"] == 1  # Gravity rift bonus
