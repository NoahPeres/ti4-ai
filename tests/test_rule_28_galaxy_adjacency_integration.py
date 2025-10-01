"""Integration tests for Rule 28 deals with galaxy adjacency system.

Tests the integration between Rule 28 component transactions and the existing
galaxy adjacency system, including wormhole adjacency rules and dynamic
adjacency checking during transactions.

Requirements: 2.1, 2.2, 2.3, 2.4, 2.5
"""

from unittest.mock import Mock

from ti4.core.galaxy import Galaxy
from ti4.core.game_state import GameState
from ti4.core.hex_coordinate import HexCoordinate
from ti4.core.rule_28_deals import ComponentValidator, TransactionStatus
from ti4.core.system import System
from ti4.core.transactions import TransactionOffer
from ti4.core.unit import Unit


class TestRule28GalaxyAdjacencyIntegration:
    """Integration tests for Rule 28 deals with galaxy adjacency system."""

    def test_validate_neighbor_requirement_with_real_galaxy_same_system(self) -> None:
        """Test neighbor validation when players have units in the same system.

        Requirements: 2.1, 2.2
        """
        # Create a real galaxy with systems
        galaxy = Galaxy()

        # Create system with coordinates
        system_id = "test_system"
        coordinate = HexCoordinate(0, 0)
        galaxy.place_system(coordinate, system_id)

        system = System(system_id)
        galaxy.register_system(system)

        # Add units for both players in the same system
        player1_unit = Unit("fighter", "player1")
        player2_unit = Unit("fighter", "player2")
        system.place_unit_in_space(player1_unit)
        system.place_unit_in_space(player2_unit)

        # Create mock game state
        mock_game_state = Mock(spec=GameState)

        # Create validator with real galaxy
        validator = ComponentValidator(galaxy=galaxy, game_state=mock_game_state)

        # Test: Players should be neighbors (same system)
        result = validator.validate_neighbor_requirement("player1", "player2")
        assert result is True

    def test_validate_neighbor_requirement_with_real_galaxy_adjacent_systems(
        self,
    ) -> None:
        """Test neighbor validation when players have units in adjacent systems.

        Requirements: 2.1, 2.2
        """
        # Create a real galaxy with adjacent systems
        galaxy = Galaxy()

        # Create two adjacent systems
        system1_id = "system1"
        system2_id = "system2"
        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)  # Adjacent to (0,0)

        galaxy.place_system(coord1, system1_id)
        galaxy.place_system(coord2, system2_id)

        system1 = System(system1_id)
        system2 = System(system2_id)
        galaxy.register_system(system1)
        galaxy.register_system(system2)

        # Add units for players in different adjacent systems
        player1_unit = Unit("fighter", "player1")
        player2_unit = Unit("fighter", "player2")
        system1.place_unit_in_space(player1_unit)
        system2.place_unit_in_space(player2_unit)

        # Create mock game state
        mock_game_state = Mock(spec=GameState)

        # Create validator with real galaxy
        validator = ComponentValidator(galaxy=galaxy, game_state=mock_game_state)

        # Test: Players should be neighbors (adjacent systems)
        result = validator.validate_neighbor_requirement("player1", "player2")
        assert result is True

    def test_validate_neighbor_requirement_with_real_galaxy_non_adjacent_systems(
        self,
    ) -> None:
        """Test neighbor validation when players have units in non-adjacent systems.

        Requirements: 2.1, 2.2
        """
        # Create a real galaxy with non-adjacent systems
        galaxy = Galaxy()

        # Create two non-adjacent systems
        system1_id = "system1"
        system2_id = "system2"
        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(2, 0)  # Not adjacent to (0,0)

        galaxy.place_system(coord1, system1_id)
        galaxy.place_system(coord2, system2_id)

        system1 = System(system1_id)
        system2 = System(system2_id)
        galaxy.register_system(system1)
        galaxy.register_system(system2)

        # Add units for players in different non-adjacent systems
        player1_unit = Unit("fighter", "player1")
        player2_unit = Unit("fighter", "player2")
        system1.place_unit_in_space(player1_unit)
        system2.place_unit_in_space(player2_unit)

        # Create mock game state
        mock_game_state = Mock(spec=GameState)

        # Create validator with real galaxy
        validator = ComponentValidator(galaxy=galaxy, game_state=mock_game_state)

        # Test: Players should NOT be neighbors (non-adjacent systems)
        result = validator.validate_neighbor_requirement("player1", "player2")
        assert result is False

    def test_validate_neighbor_requirement_with_wormhole_adjacency(self) -> None:
        """Test neighbor validation when players are connected via wormholes.

        Requirements: 2.1, 2.2, 2.4
        """
        # Create a real galaxy with wormhole-connected systems
        galaxy = Galaxy()

        # Create two systems with matching wormholes (not physically adjacent)
        system1_id = "alpha_system_1"
        system2_id = "alpha_system_2"
        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(3, 0)  # Far apart physically

        galaxy.place_system(coord1, system1_id)
        galaxy.place_system(coord2, system2_id)

        # Create systems with alpha wormholes
        from ti4.core.constants import WormholeType
        from ti4.core.system import System

        system1 = System(system1_id)
        system2 = System(system2_id)

        # Add alpha wormholes to both systems
        system1.add_wormhole(WormholeType.ALPHA)
        system2.add_wormhole(WormholeType.ALPHA)

        galaxy.register_system(system1)
        galaxy.register_system(system2)

        # Add units for players in different wormhole-connected systems
        player1_unit = Unit("fighter", "player1")
        player2_unit = Unit("fighter", "player2")
        system1.place_unit_in_space(player1_unit)
        system2.place_unit_in_space(player2_unit)

        # Create mock game state
        mock_game_state = Mock(spec=GameState)

        # Create validator with real galaxy
        validator = ComponentValidator(galaxy=galaxy, game_state=mock_game_state)

        # Test: Players should be neighbors (wormhole connection)
        result = validator.validate_neighbor_requirement("player1", "player2")
        assert result is True

    def test_dynamic_adjacency_checking_during_transaction(self) -> None:
        """Test that adjacency is checked dynamically during transaction validation.

        Requirements: 2.3, 2.4
        """
        # Create a real galaxy with systems
        galaxy = Galaxy()

        # Create two adjacent systems
        system1_id = "system1"
        system2_id = "system2"
        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)  # Adjacent to (0,0)

        galaxy.place_system(coord1, system1_id)
        galaxy.place_system(coord2, system2_id)

        system1 = System(system1_id)
        system2 = System(system2_id)
        galaxy.register_system(system1)
        galaxy.register_system(system2)

        # Add units for players in adjacent systems
        player1_unit = Unit("fighter", "player1")
        player2_unit = Unit("fighter", "player2")
        system1.place_unit_in_space(player1_unit)
        system2.place_unit_in_space(player2_unit)

        # Create mock game state with players
        mock_game_state = Mock(spec=GameState)
        mock_game_state.players = []  # Empty players list for this test

        # Create validator with real galaxy
        validator = ComponentValidator(galaxy=galaxy, game_state=mock_game_state)

        # Create a transaction to validate
        from datetime import datetime

        from ti4.core.rule_28_deals import ComponentTransaction

        transaction = ComponentTransaction(
            transaction_id="test_transaction",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=2),
            request=TransactionOffer(commodities=1),
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        # Test: Transaction validation should check adjacency dynamically
        result = validator.validate_transaction(transaction)
        # Should fail due to resource issues, but NOT due to adjacency
        assert result.is_valid is False
        assert not any("not neighbors" in error for error in result.error_messages)

        # Now move player2's unit to a non-adjacent system
        system2.remove_unit_from_space(player2_unit)

        system3_id = "system3"
        coord3 = HexCoordinate(3, 0)  # Not adjacent to system1
        galaxy.place_system(coord3, system3_id)

        system3 = System(system3_id)
        galaxy.register_system(system3)
        system3.place_unit_in_space(player2_unit)

        # Test: Transaction validation should now fail due to non-adjacency
        result = validator.validate_transaction(transaction)
        assert result.is_valid is False
        assert any("not neighbors" in error for error in result.error_messages)

    def test_player_position_tracking_for_adjacency(self) -> None:
        """Test that player positions are properly tracked for adjacency determination.

        Requirements: 2.2, 2.3
        """
        # Create a real galaxy with systems
        galaxy = Galaxy()

        # Create three systems: A, B (adjacent to A), C (not adjacent to A or B)
        system_a_id = "system_a"
        system_b_id = "system_b"
        system_c_id = "system_c"
        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)  # Adjacent to A
        coord_c = HexCoordinate(3, 0)  # Not adjacent to A or B

        galaxy.place_system(coord_a, system_a_id)
        galaxy.place_system(coord_b, system_b_id)
        galaxy.place_system(coord_c, system_c_id)

        system_a = System(system_a_id)
        system_b = System(system_b_id)
        system_c = System(system_c_id)
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)
        galaxy.register_system(system_c)

        # Initially, place player1 in system A and player2 in system C (not neighbors)
        player1_unit = Unit("fighter", "player1")
        player2_unit = Unit("fighter", "player2")
        system_a.place_unit_in_space(player1_unit)
        system_c.place_unit_in_space(player2_unit)

        # Create mock game state
        mock_game_state = Mock(spec=GameState)

        # Create validator with real galaxy
        validator = ComponentValidator(galaxy=galaxy, game_state=mock_game_state)

        # Test: Players should NOT be neighbors initially
        result = validator.validate_neighbor_requirement("player1", "player2")
        assert result is False

        # Move player2 from system C to system B (now adjacent to player1 in system A)
        system_c.remove_unit_from_space(player2_unit)
        system_b.place_unit_in_space(player2_unit)

        # Test: Players should now be neighbors
        result = validator.validate_neighbor_requirement("player1", "player2")
        assert result is True

        # Move player1 to also be in system B (same system)
        player1_unit_2 = Unit("destroyer", "player1")
        system_b.place_unit_in_space(player1_unit_2)

        # Test: Players should still be neighbors (same system + adjacent system)
        result = validator.validate_neighbor_requirement("player1", "player2")
        assert result is True
