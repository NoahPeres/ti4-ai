"""
Tests for dynamic anomaly assignment system (Task 6).

This module tests the ability to dynamically add and remove anomaly types
from existing systems while maintaining system properties and supporting
multiple anomaly types with effect stacking.

LRR References:
- Rule 9.4: Ability-created anomalies
- Rule 9.5: Multiple anomaly types on same system
"""

import pytest

from src.ti4.core.constants import AnomalyType
from src.ti4.core.exceptions import InvalidAnomalyTypeError
from src.ti4.core.planet import Planet
from src.ti4.core.system import System


class TestDynamicAnomalyAssignment:
    """Test dynamic addition and removal of anomaly types from systems."""

    def test_add_anomaly_to_empty_system(self) -> None:
        """Test adding anomaly type to an empty system."""
        system = System("test_system")

        # Initially no anomalies
        assert not system.is_anomaly()
        assert system.get_anomaly_types() == []

        # Add anomaly type
        system.add_anomaly_type(AnomalyType.NEBULA)

        # Should now be an anomaly
        assert system.is_anomaly()
        assert AnomalyType.NEBULA in system.get_anomaly_types()
        assert len(system.get_anomaly_types()) == 1

    def test_add_multiple_anomaly_types_sequentially(self) -> None:
        """Test adding multiple anomaly types one by one."""
        system = System("multi_anomaly_system")

        # Add first anomaly
        system.add_anomaly_type(AnomalyType.NEBULA)
        assert system.has_anomaly_type(AnomalyType.NEBULA)
        assert len(system.get_anomaly_types()) == 1

        # Add second anomaly
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)
        assert system.has_anomaly_type(AnomalyType.NEBULA)
        assert system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)
        assert len(system.get_anomaly_types()) == 2

        # Add third anomaly
        system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)
        assert system.has_anomaly_type(AnomalyType.NEBULA)
        assert system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)
        assert system.has_anomaly_type(AnomalyType.ASTEROID_FIELD)
        assert len(system.get_anomaly_types()) == 3

    def test_remove_anomaly_from_multi_anomaly_system(self) -> None:
        """Test removing specific anomaly types from system with multiple anomalies."""
        system = System("multi_anomaly_system")

        # Add multiple anomalies
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)
        system.add_anomaly_type(AnomalyType.SUPERNOVA)

        # Remove one anomaly
        system.remove_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # Should still have other anomalies
        assert system.is_anomaly()
        assert system.has_anomaly_type(AnomalyType.NEBULA)
        assert not system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)
        assert system.has_anomaly_type(AnomalyType.SUPERNOVA)
        assert len(system.get_anomaly_types()) == 2

    def test_remove_all_anomalies_makes_system_normal(self) -> None:
        """Test that removing all anomalies makes system no longer an anomaly."""
        system = System("test_system")

        # Add anomalies
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)
        assert system.is_anomaly()

        # Remove all anomalies
        system.remove_anomaly_type(AnomalyType.NEBULA)
        system.remove_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # Should no longer be an anomaly
        assert not system.is_anomaly()
        assert system.get_anomaly_types() == []

    def test_add_duplicate_anomaly_type_has_no_effect(self) -> None:
        """Test that adding the same anomaly type twice has no effect."""
        system = System("test_system")

        # Add anomaly type
        system.add_anomaly_type(AnomalyType.NEBULA)
        initial_count = len(system.get_anomaly_types())

        # Add same anomaly type again
        system.add_anomaly_type(AnomalyType.NEBULA)

        # Should still have only one instance
        assert len(system.get_anomaly_types()) == initial_count
        assert system.get_anomaly_types().count(AnomalyType.NEBULA) == 1


class TestSystemPropertyPreservation:
    """Test that system properties are preserved when adding/removing anomalies."""

    def test_planets_preserved_when_adding_anomalies(self) -> None:
        """Test that planets are preserved when adding anomaly types."""
        system = System("planet_system")

        # Add planets
        planet1 = Planet("Planet A", resources=2, influence=1)
        planet2 = Planet("Planet B", resources=1, influence=3)
        system.add_planet(planet1)
        system.add_planet(planet2)

        initial_planet_count = len(system.planets)
        initial_planet_names = [p.name for p in system.planets]

        # Add anomaly type
        system.add_anomaly_type(AnomalyType.NEBULA)

        # Planets should be preserved
        assert len(system.planets) == initial_planet_count
        assert [p.name for p in system.planets] == initial_planet_names
        assert system.is_anomaly()

    def test_planets_preserved_when_removing_anomalies(self) -> None:
        """Test that planets are preserved when removing anomaly types."""
        system = System("anomaly_planet_system")

        # Add planets and anomalies
        planet = Planet("Test Planet", resources=2, influence=1)
        system.add_planet(planet)
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # Remove one anomaly
        system.remove_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # Planet should be preserved
        assert len(system.planets) == 1
        assert system.planets[0].name == "Test Planet"
        assert system.is_anomaly()  # Still has nebula

    def test_wormholes_preserved_when_adding_anomalies(self) -> None:
        """Test that wormholes are preserved when adding anomaly types."""
        system = System("wormhole_system")

        # Add wormholes
        system.add_wormhole("alpha")
        system.add_wormhole("beta")

        initial_wormholes = system.get_wormhole_types()

        # Add anomaly type
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # Wormholes should be preserved
        assert system.get_wormhole_types() == initial_wormholes
        assert system.has_wormhole("alpha")
        assert system.has_wormhole("beta")
        assert system.is_anomaly()

    def test_wormholes_preserved_when_removing_anomalies(self) -> None:
        """Test that wormholes are preserved when removing anomaly types."""
        system = System("anomaly_wormhole_system")

        # Add wormholes and anomalies
        system.add_wormhole("gamma")
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.SUPERNOVA)

        # Remove anomaly
        system.remove_anomaly_type(AnomalyType.SUPERNOVA)

        # Wormhole should be preserved
        assert system.has_wormhole("gamma")
        assert system.is_anomaly()  # Still has nebula

    def test_complex_system_properties_preserved(self) -> None:
        """Test that complex systems with multiple properties are preserved."""
        system = System("complex_system")

        # Add multiple types of properties
        planet1 = Planet("Planet A", resources=2, influence=1)
        planet2 = Planet("Planet B", resources=1, influence=3)
        system.add_planet(planet1)
        system.add_planet(planet2)
        system.add_wormhole("alpha")
        system.add_wormhole("delta")

        # Add multiple anomalies
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # Verify all properties preserved
        assert len(system.planets) == 2
        assert system.planets[0].name == "Planet A"
        assert system.planets[1].name == "Planet B"
        assert system.has_wormhole("alpha")
        assert system.has_wormhole("delta")
        assert system.has_anomaly_type(AnomalyType.NEBULA)
        assert system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)
        assert system.is_anomaly()

        # Remove one anomaly
        system.remove_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # All other properties should still be preserved
        assert len(system.planets) == 2
        assert system.has_wormhole("alpha")
        assert system.has_wormhole("delta")
        assert system.has_anomaly_type(AnomalyType.NEBULA)
        assert not system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)


class TestAnomalyEffectStacking:
    """Test that multiple anomaly types stack their effects properly."""

    def test_multiple_blocking_anomalies_still_block(self) -> None:
        """Test that systems with multiple blocking anomalies still block movement."""
        system = System("multi_blocking_system")

        # Add multiple blocking anomalies
        system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)
        system.add_anomaly_type(AnomalyType.SUPERNOVA)

        # Should still be blocking (both types block movement)
        assert system.has_anomaly_type(AnomalyType.ASTEROID_FIELD)
        assert system.has_anomaly_type(AnomalyType.SUPERNOVA)
        assert system.is_anomaly()

    def test_nebula_with_other_anomalies_preserves_nebula_rules(self) -> None:
        """Test that nebula rules are preserved when combined with other anomalies."""
        system = System("nebula_combo_system")

        # Add nebula with other anomaly types
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # Should have both anomaly types
        assert system.has_anomaly_type(AnomalyType.NEBULA)
        assert system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)
        assert len(system.get_anomaly_types()) == 2

    def test_gravity_rift_with_other_anomalies_preserves_rift_effects(self) -> None:
        """Test that gravity rift effects are preserved when combined with other anomalies."""
        system = System("rift_combo_system")

        # Add gravity rift with other anomaly types
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)
        system.add_anomaly_type(AnomalyType.NEBULA)

        # Should have both anomaly types
        assert system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)
        assert system.has_anomaly_type(AnomalyType.NEBULA)
        assert len(system.get_anomaly_types()) == 2

    def test_all_four_anomaly_types_can_coexist(self) -> None:
        """Test that all four anomaly types can exist on the same system."""
        system = System("all_anomalies_system")

        # Add all four anomaly types
        system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.SUPERNOVA)
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # Should have all four types
        assert system.has_anomaly_type(AnomalyType.ASTEROID_FIELD)
        assert system.has_anomaly_type(AnomalyType.NEBULA)
        assert system.has_anomaly_type(AnomalyType.SUPERNOVA)
        assert system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)
        assert len(system.get_anomaly_types()) == 4
        assert system.is_anomaly()


class TestDynamicAnomalyEdgeCases:
    """Test edge cases for dynamic anomaly assignment."""

    def test_remove_nonexistent_anomaly_type_safe(self) -> None:
        """Test that removing non-existent anomaly type is safe."""
        system = System("test_system")

        # Add one anomaly
        system.add_anomaly_type(AnomalyType.NEBULA)

        # Try to remove different anomaly type
        system.remove_anomaly_type(AnomalyType.GRAVITY_RIFT)  # Should not raise error

        # Original anomaly should still be there
        assert system.has_anomaly_type(AnomalyType.NEBULA)
        assert not system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)

    def test_remove_from_empty_system_safe(self) -> None:
        """Test that removing anomaly from empty system is safe."""
        system = System("empty_system")

        # Try to remove anomaly from empty system
        system.remove_anomaly_type(AnomalyType.ASTEROID_FIELD)  # Should not raise error

        # System should remain empty
        assert not system.is_anomaly()
        assert system.get_anomaly_types() == []

    def test_string_and_enum_anomaly_types_equivalent(self) -> None:
        """Test that string and enum anomaly types are treated equivalently."""
        system = System("test_system")

        # Add using enum
        system.add_anomaly_type(AnomalyType.NEBULA)

        # Check using string
        assert system.has_anomaly_type("nebula")

        # Remove using string
        system.remove_anomaly_type("nebula")

        # Check using enum
        assert not system.has_anomaly_type(AnomalyType.NEBULA)

    def test_invalid_anomaly_type_raises_error(self) -> None:
        """Test that invalid anomaly types raise appropriate errors."""
        system = System("test_system")

        with pytest.raises(InvalidAnomalyTypeError, match="Invalid anomaly type"):
            system.add_anomaly_type("invalid_anomaly")

        with pytest.raises(InvalidAnomalyTypeError, match="Invalid anomaly type"):
            system.remove_anomaly_type("invalid_anomaly")

        with pytest.raises(InvalidAnomalyTypeError, match="Invalid anomaly type"):
            system.has_anomaly_type("invalid_anomaly")

    def test_none_anomaly_type_raises_error(self) -> None:
        """Test that None anomaly type raises appropriate errors."""
        system = System("test_system")

        with pytest.raises(
            InvalidAnomalyTypeError, match="Anomaly type cannot be None"
        ):
            system.add_anomaly_type(None)  # type: ignore

        with pytest.raises(
            InvalidAnomalyTypeError, match="Anomaly type cannot be None"
        ):
            system.remove_anomaly_type(None)  # type: ignore

        with pytest.raises(
            InvalidAnomalyTypeError, match="Anomaly type cannot be None"
        ):
            system.has_anomaly_type(None)  # type: ignore


class TestAnomalySystemQueries:
    """Test querying systems for anomaly information after dynamic changes."""

    def test_get_anomaly_types_returns_current_state(self) -> None:
        """Test that get_anomaly_types reflects current system state."""
        system = System("dynamic_system")

        # Initially empty
        assert system.get_anomaly_types() == []

        # Add anomaly
        system.add_anomaly_type(AnomalyType.NEBULA)
        anomaly_types = system.get_anomaly_types()
        assert AnomalyType.NEBULA in anomaly_types
        assert len(anomaly_types) == 1

        # Add another
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)
        anomaly_types = system.get_anomaly_types()
        assert AnomalyType.NEBULA in anomaly_types
        assert AnomalyType.GRAVITY_RIFT in anomaly_types
        assert len(anomaly_types) == 2

        # Remove one
        system.remove_anomaly_type(AnomalyType.NEBULA)
        anomaly_types = system.get_anomaly_types()
        assert AnomalyType.NEBULA not in anomaly_types
        assert AnomalyType.GRAVITY_RIFT in anomaly_types
        assert len(anomaly_types) == 1

    def test_is_anomaly_reflects_current_state(self) -> None:
        """Test that is_anomaly reflects current system state."""
        system = System("dynamic_system")

        # Initially not anomaly
        assert not system.is_anomaly()

        # Add anomaly
        system.add_anomaly_type(AnomalyType.SUPERNOVA)
        assert system.is_anomaly()

        # Add another
        system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)
        assert system.is_anomaly()

        # Remove one (still has another)
        system.remove_anomaly_type(AnomalyType.SUPERNOVA)
        assert system.is_anomaly()

        # Remove last one
        system.remove_anomaly_type(AnomalyType.ASTEROID_FIELD)
        assert not system.is_anomaly()

    def test_has_anomaly_type_reflects_current_state(self) -> None:
        """Test that has_anomaly_type reflects current system state."""
        system = System("dynamic_system")

        # Initially no anomalies
        assert not system.has_anomaly_type(AnomalyType.NEBULA)

        # Add anomaly
        system.add_anomaly_type(AnomalyType.NEBULA)
        assert system.has_anomaly_type(AnomalyType.NEBULA)
        assert not system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # Add another
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)
        assert system.has_anomaly_type(AnomalyType.NEBULA)
        assert system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # Remove one
        system.remove_anomaly_type(AnomalyType.NEBULA)
        assert not system.has_anomaly_type(AnomalyType.NEBULA)
        assert system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)
