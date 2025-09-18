"""Tests for System class wormhole validation and edge cases."""

import pytest

from src.ti4.core.system import System


class TestSystemWormholeValidation:
    """Test System class wormhole methods for validation and edge cases."""

    def test_add_valid_wormhole_types(self) -> None:
        """Test adding all valid wormhole types."""
        system = System("test_system")
        valid_types = ["alpha", "beta", "gamma", "delta"]

        for wormhole_type in valid_types:
            system.add_wormhole(wormhole_type)
            assert system.has_wormhole(wormhole_type), (
                f"Should have {wormhole_type} wormhole"
            )

        assert len(system.get_wormhole_types()) == 4, "Should have all 4 wormhole types"

    def test_add_invalid_wormhole_type_raises_error(self) -> None:
        """Test that adding invalid wormhole types raises ValueError."""
        system = System("test_system")

        invalid_types = ["epsilon", "zeta", "invalid", "123"]

        for invalid_type in invalid_types:
            with pytest.raises(
                ValueError, match=f"Invalid wormhole type: {invalid_type}"
            ):
                system.add_wormhole(invalid_type)

    def test_add_empty_wormhole_type_raises_error(self) -> None:
        """Test that adding empty wormhole type raises ValueError."""
        system = System("test_system")

        with pytest.raises(ValueError, match="Wormhole type cannot be empty"):
            system.add_wormhole("")

    def test_add_duplicate_wormhole_type_ignored(self) -> None:
        """Test that adding duplicate wormhole types doesn't create duplicates."""
        system = System("test_system")

        # Add alpha wormhole multiple times
        system.add_wormhole("alpha")
        system.add_wormhole("alpha")
        system.add_wormhole("alpha")

        wormhole_types = system.get_wormhole_types()
        assert wormhole_types.count("alpha") == 1, "Should only have one alpha wormhole"
        assert len(wormhole_types) == 1, "Should only have one wormhole total"

    def test_has_wormhole_returns_false_for_nonexistent(self) -> None:
        """Test that has_wormhole returns False for non-existent wormhole types."""
        system = System("test_system")

        assert not system.has_wormhole("alpha"), (
            "Should not have alpha wormhole initially"
        )
        assert not system.has_wormhole("beta"), (
            "Should not have beta wormhole initially"
        )
        assert not system.has_wormhole("invalid"), (
            "Should not have invalid wormhole type"
        )

    def test_get_wormhole_types_returns_copy(self) -> None:
        """Test that get_wormhole_types returns a copy to prevent external modification."""
        system = System("test_system")
        system.add_wormhole("alpha")
        system.add_wormhole("beta")

        wormhole_types = system.get_wormhole_types()
        original_length = len(wormhole_types)

        # Modify the returned list
        wormhole_types.append("gamma")
        wormhole_types.remove("alpha")

        # Original system should be unchanged
        assert len(system.get_wormhole_types()) == original_length, (
            "Original system should be unchanged"
        )
        assert system.has_wormhole("alpha"), "System should still have alpha wormhole"
        assert not system.has_wormhole("gamma"), "System should not have gamma wormhole"

    def test_remove_wormhole_success(self) -> None:
        """Test successful wormhole removal."""
        system = System("test_system")
        system.add_wormhole("alpha")
        system.add_wormhole("beta")

        # Remove alpha wormhole
        result = system.remove_wormhole("alpha")

        assert result is True, "Should return True when wormhole is removed"
        assert not system.has_wormhole("alpha"), (
            "Should not have alpha wormhole after removal"
        )
        assert system.has_wormhole("beta"), "Should still have beta wormhole"

    def test_remove_nonexistent_wormhole(self) -> None:
        """Test removing non-existent wormhole returns False."""
        system = System("test_system")
        system.add_wormhole("alpha")

        # Try to remove non-existent wormhole
        result = system.remove_wormhole("beta")

        assert result is False, "Should return False when wormhole doesn't exist"
        assert system.has_wormhole("alpha"), "Should still have alpha wormhole"

    def test_wormhole_operations_integration(self) -> None:
        """Test integration of all wormhole operations."""
        system = System("test_system")

        # Start with empty system
        assert len(system.get_wormhole_types()) == 0, "Should start with no wormholes"

        # Add multiple wormholes
        system.add_wormhole("alpha")
        system.add_wormhole("gamma")
        assert len(system.get_wormhole_types()) == 2, "Should have 2 wormholes"

        # Check specific wormholes
        assert system.has_wormhole("alpha"), "Should have alpha wormhole"
        assert system.has_wormhole("gamma"), "Should have gamma wormhole"
        assert not system.has_wormhole("beta"), "Should not have beta wormhole"

        # Remove one wormhole
        system.remove_wormhole("alpha")
        assert len(system.get_wormhole_types()) == 1, (
            "Should have 1 wormhole after removal"
        )
        assert not system.has_wormhole("alpha"), (
            "Should not have alpha wormhole after removal"
        )
        assert system.has_wormhole("gamma"), "Should still have gamma wormhole"
