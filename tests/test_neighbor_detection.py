"""Tests for neighbor detection mechanics based on LRR Rule 60."""

from src.ti4.core.galaxy import Galaxy
from src.ti4.core.hex_coordinate import HexCoordinate
from src.ti4.core.player import Player
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class TestNeighborDetection:
    """Test neighbor detection rules from LRR 60."""

    def test_players_with_units_in_same_system_are_neighbors(self):
        """
        Test LRR 60.0: Two players are neighbors if they both have a unit
        or control a planet in the same system.

        Specifically: Players with units in the same system should be neighbors.
        """
        galaxy = Galaxy()

        # Create a system
        coord = HexCoordinate(0, 0)
        galaxy.place_system(coord, "system1")

        system = System("system1")
        galaxy.register_system(system)

        # Create two players
        player1 = Player("player1", "Red")
        player2 = Player("player2", "Blue")

        # Create units for both players in the same system
        unit1 = Unit("fighter", player1.id)
        unit2 = Unit("fighter", player2.id)

        # Place units in the same system
        system.place_unit_in_space(unit1)
        system.place_unit_in_space(unit2)

        # Players should be neighbors because they both have units in the same system
        assert galaxy.are_players_neighbors(player1.id, player2.id) is True

    def test_players_with_units_in_adjacent_systems_are_neighbors(self):
        """
        Test LRR 60.0: Two players are neighbors if they both have a unit
        or control a planet in systems that are adjacent to each other.

        Specifically: Players with units in adjacent systems should be neighbors.
        """
        galaxy = Galaxy()

        # Create two adjacent systems
        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)  # Adjacent to coord1

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        system1 = System("system1")
        system2 = System("system2")

        galaxy.register_system(system1)
        galaxy.register_system(system2)

        # Create two players
        player1 = Player("player1", "Red")
        player2 = Player("player2", "Blue")

        # Create units for players in adjacent systems
        unit1 = Unit("fighter", player1.id)
        unit2 = Unit("fighter", player2.id)

        # Place units in adjacent systems
        system1.place_unit_in_space(unit1)
        system2.place_unit_in_space(unit2)

        # Players should be neighbors because they have units in adjacent systems
        assert galaxy.are_players_neighbors(player1.id, player2.id) is True

    def test_players_with_units_in_non_adjacent_systems_are_not_neighbors(self):
        """
        Test LRR 60.0: Players should not be neighbors if their units/planets
        are in systems that are not adjacent.
        """
        galaxy = Galaxy()

        # Create two non-adjacent systems
        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(3, 0)  # Distance 3, not adjacent

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        system1 = System("system1")
        system2 = System("system2")

        galaxy.register_system(system1)
        galaxy.register_system(system2)

        # Create two players
        player1 = Player("player1", "Red")
        player2 = Player("player2", "Blue")

        # Create units for players in non-adjacent systems
        unit1 = Unit("fighter", player1.id)
        unit2 = Unit("fighter", player2.id)

        # Place units in non-adjacent systems
        system1.place_unit_in_space(unit1)
        system2.place_unit_in_space(unit2)

        # Players should NOT be neighbors
        assert galaxy.are_players_neighbors(player1.id, player2.id) is False

    def test_players_with_units_connected_via_wormhole_are_neighbors(self):
        """
        Test LRR 60.0: Players should be neighbors if their systems are
        connected via wormholes (extending adjacency).
        """
        galaxy = Galaxy()

        # Create two systems that are far apart but connected via wormhole
        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(5, 0)  # Distance 5, not physically adjacent

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        system1 = System("system1")
        system2 = System("system2")

        # Add matching wormholes to both systems
        system1.add_wormhole("alpha")
        system2.add_wormhole("alpha")

        galaxy.register_system(system1)
        galaxy.register_system(system2)

        # Create two players
        player1 = Player("player1", "Red")
        player2 = Player("player2", "Blue")

        # Create units for players in wormhole-connected systems
        unit1 = Unit("fighter", player1.id)
        unit2 = Unit("fighter", player2.id)

        # Place units in wormhole-connected systems
        system1.place_unit_in_space(unit1)
        system2.place_unit_in_space(unit2)

        # Players should be neighbors due to wormhole connection
        assert galaxy.are_players_neighbors(player1.id, player2.id) is True

    def test_players_with_no_units_are_not_neighbors(self):
        """
        Test edge case: Players with no units should not be neighbors.
        """
        galaxy = Galaxy()

        # Create two players
        player1 = Player("player1", "Red")
        player2 = Player("player2", "Blue")

        # Players with no units should not be neighbors
        assert galaxy.are_players_neighbors(player1.id, player2.id) is False
