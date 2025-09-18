"""Tests for wormhole adjacency mechanics based on LRR Rule 6.1."""

from src.ti4.core.galaxy import Galaxy
from src.ti4.core.hex_coordinate import HexCoordinate
from src.ti4.core.system import System


class TestWormholeAdjacency:
    """Test wormhole adjacency rules from LRR 6.1."""

    def test_alpha_wormhole_systems_are_adjacent_regardless_of_distance(self) -> None:
        """
        Test LRR 6.1: A system that has a wormhole is treated as being adjacent
        to a system that has a matching wormhole.

        Specifically: Two systems with alpha wormholes should be adjacent
        even if they are far apart on the galaxy map.
        """
        galaxy = Galaxy()

        # Create two systems far apart (distance > 1)
        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(5, 0)  # Distance 5, definitely not physically adjacent

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create system objects with alpha wormholes
        system1 = System("system1")
        system2 = System("system2")

        # Add alpha wormholes to both systems
        system1.add_wormhole("alpha")
        system2.add_wormhole("alpha")

        # Register systems with galaxy so it can access them
        galaxy.register_system(system1)
        galaxy.register_system(system2)

        # Verify they are not physically adjacent (sanity check)
        assert coord1.distance_to(coord2) > 1

        # Systems with matching alpha wormholes should be adjacent per LRR 6.1
        assert galaxy.are_systems_adjacent("system1", "system2") is True

    def test_different_wormhole_types_are_not_adjacent(self) -> None:
        """
        Test LRR 6.1: Systems with different wormhole types should not be adjacent.
        Only matching wormholes create adjacency.
        """
        galaxy = Galaxy()

        # Create two systems
        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(3, 0)

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create systems with different wormhole types
        system1 = System("system1")
        system2 = System("system2")

        system1.add_wormhole("alpha")
        system2.add_wormhole("beta")  # Different wormhole type

        galaxy.register_system(system1)
        galaxy.register_system(system2)

        # Systems with different wormhole types should NOT be adjacent
        assert galaxy.are_systems_adjacent("system1", "system2") is False

    def test_system_without_wormhole_not_adjacent_to_wormhole_system(self) -> None:
        """
        Test LRR 6.1: A system without wormholes should not be adjacent
        to a system with wormholes (unless physically adjacent).
        """
        galaxy = Galaxy()

        # Create two systems far apart
        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(4, 0)

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # One system has wormhole, other doesn't
        system1 = System("system1")
        system2 = System("system2")  # No wormhole added

        system1.add_wormhole("alpha")

        galaxy.register_system(system1)
        galaxy.register_system(system2)

        # Should not be adjacent via wormholes
        assert galaxy.are_systems_adjacent("system1", "system2") is False
