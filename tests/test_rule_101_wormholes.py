"""Tests for Rule 101: WORMHOLES implementation based on LRR."""

import pytest

from src.ti4.core.galaxy import Galaxy
from src.ti4.core.hex_coordinate import HexCoordinate
from src.ti4.core.system import System


class TestRule101Wormholes:
    """Test Rule 101: WORMHOLES - Systems that contain identical wormholes are adjacent."""

    # Test data constants
    WORMHOLE_TYPES = ["alpha", "beta", "gamma", "delta"]

    def _create_galaxy_with_wormhole_systems(
        self, wormhole_configs: list[tuple[str, str, HexCoordinate]]
    ) -> Galaxy:
        """
        Helper method to create a galaxy with multiple wormhole systems.

        Args:
            wormhole_configs: List of (system_id, wormhole_type, coordinate) tuples

        Returns:
            Configured Galaxy instance
        """
        galaxy = Galaxy()

        for system_id, wormhole_type, coord in wormhole_configs:
            galaxy.place_system(coord, system_id)
            system = System(system_id)
            system.add_wormhole(wormhole_type)
            galaxy.register_system(system)

        return galaxy

    def _create_system_with_wormholes(
        self, system_id: str, wormhole_types: list[str]
    ) -> System:
        """
        Helper method to create a system with multiple wormhole types.

        Args:
            system_id: Unique identifier for the system
            wormhole_types: List of wormhole types to add

        Returns:
            Configured System instance
        """
        system = System(system_id)
        for wormhole_type in wormhole_types:
            system.add_wormhole(wormhole_type)
        return system

    def test_alpha_wormhole_systems_are_adjacent(self):
        """Test LRR 101.1: Alpha wormhole systems are adjacent to each other."""
        wormhole_configs = [
            ("alpha_system_1", "alpha", HexCoordinate(0, 0)),
            ("alpha_system_2", "alpha", HexCoordinate(3, 0)),
            ("alpha_system_3", "alpha", HexCoordinate(0, 3)),
        ]

        galaxy = self._create_galaxy_with_wormhole_systems(wormhole_configs)

        # All alpha wormhole systems should be adjacent to each other
        system_ids = ["alpha_system_1", "alpha_system_2", "alpha_system_3"]
        for i, system_a in enumerate(system_ids):
            for system_b in system_ids[i + 1 :]:
                assert galaxy.are_systems_adjacent(system_a, system_b), (
                    f"{system_a} should be adjacent to {system_b} via alpha wormhole"
                )

    def test_beta_wormhole_systems_are_adjacent(self):
        """Test LRR 101.2: Beta wormhole systems are adjacent to each other."""
        wormhole_configs = [
            ("beta_system_1", "beta", HexCoordinate(0, 0)),
            ("beta_system_2", "beta", HexCoordinate(5, 0)),
        ]

        galaxy = self._create_galaxy_with_wormhole_systems(wormhole_configs)

        assert galaxy.are_systems_adjacent("beta_system_1", "beta_system_2"), (
            "Beta wormhole systems should be adjacent"
        )

    def test_gamma_wormhole_systems_are_adjacent(self):
        """Test LRR 101.3: Gamma wormhole systems are adjacent to each other."""
        wormhole_configs = [
            ("gamma_system_1", "gamma", HexCoordinate(0, 0)),
            ("gamma_system_2", "gamma", HexCoordinate(4, 0)),
        ]

        galaxy = self._create_galaxy_with_wormhole_systems(wormhole_configs)

        assert galaxy.are_systems_adjacent("gamma_system_1", "gamma_system_2"), (
            "Gamma wormhole systems should be adjacent"
        )

    def test_delta_wormhole_systems_are_adjacent(self):
        """Test LRR 101.4: Delta wormhole systems are adjacent to each other."""
        wormhole_configs = [
            ("delta_system_1", "delta", HexCoordinate(0, 0)),
            ("delta_system_2", "delta", HexCoordinate(2, 0)),
        ]

        galaxy = self._create_galaxy_with_wormhole_systems(wormhole_configs)

        assert galaxy.are_systems_adjacent("delta_system_1", "delta_system_2"), (
            "Delta wormhole systems should be adjacent"
        )

    @pytest.mark.parametrize("wormhole_type", WORMHOLE_TYPES)
    def test_same_wormhole_type_adjacency(self, wormhole_type: str) -> None:
        """Parameterized test for same wormhole type adjacency."""
        wormhole_configs = [
            (f"{wormhole_type}_system_1", wormhole_type, HexCoordinate(0, 0)),
            (f"{wormhole_type}_system_2", wormhole_type, HexCoordinate(6, 0)),
        ]

        galaxy = self._create_galaxy_with_wormhole_systems(wormhole_configs)

        assert galaxy.are_systems_adjacent(
            f"{wormhole_type}_system_1", f"{wormhole_type}_system_2"
        ), f"Systems with {wormhole_type} wormholes should be adjacent"

    def test_different_wormhole_types_are_not_adjacent(self):
        """Test LRR 101.5: Different wormhole types are not adjacent to each other."""
        coords = [
            HexCoordinate(0, 0),
            HexCoordinate(3, 0),
            HexCoordinate(0, 3),
            HexCoordinate(3, 3),
        ]
        wormhole_configs = [
            (f"{wtype}_system", wtype, coord)
            for wtype, coord in zip(self.WORMHOLE_TYPES, coords)
        ]

        galaxy = self._create_galaxy_with_wormhole_systems(wormhole_configs)

        # Test all combinations of different wormhole types
        system_ids = [f"{wtype}_system" for wtype in self.WORMHOLE_TYPES]
        for i, system_a in enumerate(system_ids):
            for system_b in system_ids[i + 1 :]:
                assert not galaxy.are_systems_adjacent(system_a, system_b), (
                    f"{system_a} should NOT be adjacent to {system_b} (different wormhole types)"
                )

    def test_multiple_wormhole_types_create_multiple_adjacencies(self):
        """Test LRR 101: Systems with multiple wormhole types are adjacent to systems with any matching type."""
        galaxy = Galaxy()

        # Create multi-wormhole system
        multi_coord = HexCoordinate(0, 0)
        galaxy.place_system(multi_coord, "multi_wormhole_system")
        multi_system = self._create_system_with_wormholes(
            "multi_wormhole_system", ["alpha", "beta"]
        )
        galaxy.register_system(multi_system)

        # Create single-wormhole systems
        single_configs = [
            ("alpha_only_system", "alpha", HexCoordinate(3, 0)),
            ("beta_only_system", "beta", HexCoordinate(0, 3)),
            ("gamma_only_system", "gamma", HexCoordinate(3, 3)),
        ]

        for system_id, wormhole_type, coord in single_configs:
            galaxy.place_system(coord, system_id)
            system = self._create_system_with_wormholes(system_id, [wormhole_type])
            galaxy.register_system(system)

        # Multi-wormhole system should be adjacent to systems with matching types
        assert galaxy.are_systems_adjacent(
            "multi_wormhole_system", "alpha_only_system"
        ), "Multi-wormhole system should be adjacent to alpha system"
        assert galaxy.are_systems_adjacent(
            "multi_wormhole_system", "beta_only_system"
        ), "Multi-wormhole system should be adjacent to beta system"

        # Multi-wormhole system should NOT be adjacent to systems with non-matching types
        assert not galaxy.are_systems_adjacent(
            "multi_wormhole_system", "gamma_only_system"
        ), "Multi-wormhole system should NOT be adjacent to gamma system"

    def test_wormhole_adjacency_is_symmetric(self):
        """Test that wormhole adjacency is symmetric (A adjacent to B implies B adjacent to A)."""
        wormhole_configs = [
            ("system_a", "alpha", HexCoordinate(0, 0)),
            ("system_b", "alpha", HexCoordinate(5, 0)),
        ]

        galaxy = self._create_galaxy_with_wormhole_systems(wormhole_configs)

        # Adjacency should be symmetric
        assert galaxy.are_systems_adjacent("system_a", "system_b"), (
            "System A should be adjacent to System B"
        )
        assert galaxy.are_systems_adjacent("system_b", "system_a"), (
            "System B should be adjacent to System A (symmetry)"
        )

    def test_system_with_no_wormhole_not_adjacent_to_wormhole_systems(self):
        """Test that systems without wormholes are not adjacent to wormhole systems via wormholes."""
        galaxy = Galaxy()

        # Create systems far apart to avoid physical adjacency
        coords = [HexCoordinate(0, 0), HexCoordinate(5, 0)]
        system_ids = ["no_wormhole_system", "alpha_wormhole_system"]

        # System without wormhole
        galaxy.place_system(coords[0], system_ids[0])
        no_wormhole_system = System(system_ids[0])
        galaxy.register_system(no_wormhole_system)

        # System with wormhole
        galaxy.place_system(coords[1], system_ids[1])
        wormhole_system = self._create_system_with_wormholes(system_ids[1], ["alpha"])
        galaxy.register_system(wormhole_system)

        # Should not be adjacent via wormholes
        assert not galaxy.are_systems_adjacent(
            "no_wormhole_system", "alpha_wormhole_system"
        ), "System without wormhole should NOT be adjacent to wormhole system"
