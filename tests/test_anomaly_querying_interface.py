"""
Tests for anomaly querying and identification interface.

This module tests the anomaly querying and identification interface
as specified in Rule 9 requirements 10.1-10.4.

LRR References:
- Rule 9.1: Anomaly identification
- Rule 9.3: Art identification
"""

import pytest

from src.ti4.core.constants import AnomalyType
from src.ti4.core.planet import Planet
from src.ti4.core.system import System


class TestAnomalyIdentificationInterface:
    """Test anomaly identification interface (Requirements 10.1, 10.2)."""

    def test_query_system_for_anomaly_types_empty_system(self) -> None:
        """Test querying normal system returns empty list."""
        system = System("normal_system")

        anomaly_types = system.get_anomaly_types()

        assert isinstance(anomaly_types, list)
        assert len(anomaly_types) == 0
        assert anomaly_types == []

    def test_query_system_for_anomaly_types_single_anomaly(self) -> None:
        """Test querying system with single anomaly returns correct type."""
        system = System("nebula_system")
        system.add_anomaly_type(AnomalyType.NEBULA)

        anomaly_types = system.get_anomaly_types()

        assert isinstance(anomaly_types, list)
        assert len(anomaly_types) == 1
        assert AnomalyType.NEBULA in anomaly_types

    def test_query_system_for_anomaly_types_multiple_anomalies(self) -> None:
        """Test querying system with multiple anomalies returns all types."""
        system = System("multi_anomaly_system")
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)
        system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)

        anomaly_types = system.get_anomaly_types()

        assert isinstance(anomaly_types, list)
        assert len(anomaly_types) == 3
        assert AnomalyType.NEBULA in anomaly_types
        assert AnomalyType.GRAVITY_RIFT in anomaly_types
        assert AnomalyType.ASTEROID_FIELD in anomaly_types

    def test_query_system_returns_copy_not_reference(self) -> None:
        """Test that get_anomaly_types returns copy to prevent external modification."""
        system = System("test_system")
        system.add_anomaly_type(AnomalyType.NEBULA)

        anomaly_types = system.get_anomaly_types()
        anomaly_types.append(AnomalyType.SUPERNOVA)  # Modify returned list

        # Original system should be unchanged
        assert len(system.get_anomaly_types()) == 1
        assert AnomalyType.SUPERNOVA not in system.get_anomaly_types()

    def test_check_if_system_is_anomaly_normal_system(self) -> None:
        """Test that normal system returns False for is_anomaly."""
        system = System("normal_system")

        assert not system.is_anomaly()

    def test_check_if_system_is_anomaly_with_anomaly_type(self) -> None:
        """Test that system with anomaly type returns True for is_anomaly."""
        system = System("anomaly_system")
        system.add_anomaly_type(AnomalyType.NEBULA)

        assert system.is_anomaly()

    def test_check_if_system_is_anomaly_with_multiple_types(self) -> None:
        """Test that system with multiple anomaly types returns True for is_anomaly."""
        system = System("multi_anomaly_system")
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        assert system.is_anomaly()

    def test_check_if_system_is_anomaly_after_removal(self) -> None:
        """Test that system returns False after all anomaly types removed."""
        system = System("test_system")
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # Remove all anomaly types
        system.remove_anomaly_type(AnomalyType.NEBULA)
        system.remove_anomaly_type(AnomalyType.GRAVITY_RIFT)

        assert not system.is_anomaly()


class TestAnomalyEffectsQuerying:
    """Test anomaly effects querying interface (Requirement 10.3)."""

    def test_get_anomaly_effects_normal_system(self) -> None:
        """Test getting effects for normal system returns default values."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        system = System("normal_system")

        effects = manager.get_anomaly_effects_summary(system)

        assert isinstance(effects, dict)
        assert "anomaly_types" in effects
        assert "blocks_movement" in effects
        assert "requires_active_system" in effects
        assert "move_value_modifier" in effects
        assert "combat_bonus" in effects

        assert effects["anomaly_types"] == []
        assert effects["blocks_movement"] is False
        assert effects["requires_active_system"] is False
        assert effects["move_value_modifier"] == 0
        assert effects["combat_bonus"] == 0

    def test_get_anomaly_effects_asteroid_field(self) -> None:
        """Test getting effects for asteroid field system."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        system = System("asteroid_system")
        system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)

        effects = manager.get_anomaly_effects_summary(system)

        assert AnomalyType.ASTEROID_FIELD in effects["anomaly_types"]
        assert effects["blocks_movement"] is True
        assert effects["requires_active_system"] is False
        assert effects["move_value_modifier"] == 0
        assert effects["combat_bonus"] == 0

    def test_get_anomaly_effects_supernova(self) -> None:
        """Test getting effects for supernova system."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        system = System("supernova_system")
        system.add_anomaly_type(AnomalyType.SUPERNOVA)

        effects = manager.get_anomaly_effects_summary(system)

        assert AnomalyType.SUPERNOVA in effects["anomaly_types"]
        assert effects["blocks_movement"] is True
        assert effects["requires_active_system"] is False
        assert effects["move_value_modifier"] == 0
        assert effects["combat_bonus"] == 0

    def test_get_anomaly_effects_nebula(self) -> None:
        """Test getting effects for nebula system."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        system = System("nebula_system")
        system.add_anomaly_type(AnomalyType.NEBULA)

        effects = manager.get_anomaly_effects_summary(system)

        assert AnomalyType.NEBULA in effects["anomaly_types"]
        assert effects["blocks_movement"] is True
        assert effects["requires_active_system"] is True
        assert effects["move_value_modifier"] == -1  # Nebula reduces move value
        assert effects["combat_bonus"] == 1  # Nebula provides +1 combat bonus

    def test_get_anomaly_effects_gravity_rift(self) -> None:
        """Test getting effects for gravity rift system."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        system = System("rift_system")
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        effects = manager.get_anomaly_effects_summary(system)

        assert AnomalyType.GRAVITY_RIFT in effects["anomaly_types"]
        assert effects["blocks_movement"] is False
        assert effects["requires_active_system"] is False
        assert effects["move_value_modifier"] == 1  # Gravity rift provides +1 move value
        assert effects["combat_bonus"] == 0

    def test_get_anomaly_effects_multiple_anomalies(self) -> None:
        """Test getting effects for system with multiple anomaly types."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        system = System("multi_anomaly_system")
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        effects = manager.get_anomaly_effects_summary(system)

        assert len(effects["anomaly_types"]) == 2
        assert AnomalyType.NEBULA in effects["anomaly_types"]
        assert AnomalyType.GRAVITY_RIFT in effects["anomaly_types"]
        # Nebula effects should take precedence for movement blocking
        assert effects["blocks_movement"] is True
        assert effects["requires_active_system"] is True
        # Nebula move value modifier should take precedence
        assert effects["move_value_modifier"] == -1
        assert effects["combat_bonus"] == 1

    def test_get_anomaly_effects_with_planets(self) -> None:
        """Test that anomaly effects work correctly for systems with planets."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()
        system = System("nebula_with_planet")
        system.add_anomaly_type(AnomalyType.NEBULA)

        # Add planet to system
        planet = Planet("Test Planet", resources=2, influence=1)
        system.add_planet(planet)

        effects = manager.get_anomaly_effects_summary(system)

        # Anomaly effects should still apply even with planets
        assert AnomalyType.NEBULA in effects["anomaly_types"]
        assert effects["blocks_movement"] is True
        assert effects["combat_bonus"] == 1
        # System should still have the planet
        assert len(system.planets) == 1


class TestAnomalyDisplayInterface:
    """Test anomaly display interface (Requirement 10.4)."""

    def test_system_information_display_interface_exists(self) -> None:
        """Test that system has interface for displaying anomaly information."""
        # This test will initially fail (RED phase) - we need to implement this
        system = System("test_system")

        # Should have method to get formatted system information
        assert hasattr(system, "get_system_info_display")

    def test_system_information_display_normal_system(self) -> None:
        """Test display information for normal system."""
        system = System("normal_system")

        info = system.get_system_info_display()

        assert isinstance(info, dict)
        assert "system_id" in info
        assert "is_anomaly" in info
        assert "anomaly_status" in info
        assert info["system_id"] == "normal_system"
        assert info["is_anomaly"] is False
        assert info["anomaly_status"] == "Normal System"

    def test_system_information_display_single_anomaly(self) -> None:
        """Test display information for system with single anomaly."""
        system = System("nebula_system")
        system.add_anomaly_type(AnomalyType.NEBULA)

        info = system.get_system_info_display()

        assert info["system_id"] == "nebula_system"
        assert info["is_anomaly"] is True
        assert "Nebula" in info["anomaly_status"]

    def test_system_information_display_multiple_anomalies(self) -> None:
        """Test display information for system with multiple anomalies."""
        system = System("multi_anomaly_system")
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        info = system.get_system_info_display()

        assert info["system_id"] == "multi_anomaly_system"
        assert info["is_anomaly"] is True
        assert "Nebula" in info["anomaly_status"]
        assert "Gravity Rift" in info["anomaly_status"]

    def test_system_information_display_with_effects_summary(self) -> None:
        """Test that display information includes effects summary."""
        system = System("nebula_system")
        system.add_anomaly_type(AnomalyType.NEBULA)

        info = system.get_system_info_display()

        assert "effects_summary" in info
        effects = info["effects_summary"]
        assert "Movement blocked (requires active system)" in effects
        assert "Combat bonus: +1 for defenders" in effects
        assert "Move value reduced to 1" in effects

    def test_system_information_display_with_planets(self) -> None:
        """Test display information includes planet information."""
        system = System("nebula_with_planet")
        system.add_anomaly_type(AnomalyType.NEBULA)

        planet = Planet("Test Planet", resources=2, influence=1)
        system.add_planet(planet)

        info = system.get_system_info_display()

        assert "planets" in info
        assert len(info["planets"]) == 1
        assert info["planets"][0]["name"] == "Test Planet"


class TestAnomalyQueryingErrorHandling:
    """Test error handling for anomaly querying interface."""

    def test_get_anomaly_effects_summary_none_system(self) -> None:
        """Test that None system raises appropriate error."""
        from src.ti4.core.anomaly_manager import AnomalyManager

        manager = AnomalyManager()

        with pytest.raises(ValueError, match="System cannot be None"):
            manager.get_anomaly_effects_summary(None)  # type: ignore

    def test_system_display_info_handles_empty_system(self) -> None:
        """Test that display info works for system with no additional properties."""
        system = System("empty_system")

        info = system.get_system_info_display()

        assert info["system_id"] == "empty_system"
        assert info["is_anomaly"] is False
        assert info["planets"] == []
        assert info["anomaly_status"] == "Normal System"

    def test_system_display_info_validates_empty_system_id(self) -> None:
        """Test that display info validates system ID is not empty."""
        system = System("")  # Empty system ID

        with pytest.raises(ValueError, match="System ID cannot be empty"):
            system.get_system_info_display()
