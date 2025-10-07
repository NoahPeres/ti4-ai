"""Test agenda phase voting integration with ResourceManager.

This module tests the integration of ResourceManager influence calculations
with the existing agenda phase voting system, implementing Rule 47.3 trade goods
restrictions for voting.

Requirements tested:
- 9.1: Integrate ResourceManager influence calculations with existing agenda phase voting
- 9.2: Implement trade goods restriction for voting (Rule 47.3)
- 9.3: Add planet exhaustion tracking for voting operations
- 9.4: Ensure compatibility with existing VotingSystem
- 9.5: Write integration tests for agenda phase voting with influence spending
"""

from src.ti4.core.agenda_phase import VotingSystem
from src.ti4.core.constants import Faction
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.resource_management import ResourceManager


class TestAgendaPhaseVotingIntegration:
    """Test integration of ResourceManager with agenda phase voting."""

    def test_voting_system_uses_resource_manager_for_influence_calculation(
        self,
    ) -> None:
        """Test that VotingSystem can use ResourceManager for influence calculations.

        Requirements: 9.1, 9.4
        """
        # Arrange
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        # Add planets with influence
        planet1 = Planet("Mecatol Rex", resources=1, influence=6)
        planet2 = Planet("Jord", resources=4, influence=4)
        planet1.set_control("player1")
        planet2.set_control("player1")
        game_state = game_state.add_player_planet("player1", planet1)
        game_state = game_state.add_player_planet("player1", planet2)

        # Add trade goods to player
        player.gain_trade_goods(3)

        resource_manager = ResourceManager(game_state)
        voting_system = VotingSystem()

        # Act
        available_influence = voting_system.calculate_available_influence_for_voting(
            "player1", resource_manager
        )

        # Assert
        # Should only count planet influence, not trade goods (Rule 47.3)
        assert available_influence == 10  # 6 + 4 from planets only

    def test_trade_goods_excluded_from_voting_influence(self) -> None:
        """Test that trade goods cannot be used for influence during voting.

        Requirements: 9.2
        """
        # Arrange
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        # Add planet with influence
        planet = Planet("Mecatol Rex", resources=1, influence=6)
        planet.set_control("player1")
        game_state = game_state.add_player_planet("player1", planet)

        # Add trade goods to player
        player.gain_trade_goods(5)

        resource_manager = ResourceManager(game_state)
        voting_system = VotingSystem()

        # Act
        # For voting, trade goods should be excluded (Rule 47.3)
        voting_influence = resource_manager.calculate_available_influence(
            "player1", for_voting=True
        )
        non_voting_influence = resource_manager.calculate_available_influence(
            "player1", for_voting=False
        )

        # Assert
        assert voting_influence == 6  # Only planet influence
        assert non_voting_influence == 11  # Planet + trade goods

        # Try to vote with more influence than planets provide
        # Should fail because trade goods can't be used for voting
        result = voting_system.cast_votes_with_resource_manager(
            player_id="player1",
            influence_amount=8,  # More than planet influence alone
            outcome="For",
            resource_manager=resource_manager,
        )

        # Should fail due to insufficient influence (trade goods excluded)
        assert not result.success
        assert "trade goods cannot be used for voting" in result.error_message

    def test_planet_exhaustion_tracked_during_voting(self) -> None:
        """Test that planet exhaustion is properly tracked during voting operations.

        Requirements: 9.3
        """
        # Arrange
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        # Add planets with influence
        planet1 = Planet("Mecatol Rex", resources=1, influence=6)
        planet2 = Planet("Jord", resources=4, influence=4)
        planet1.set_control("player1")
        planet2.set_control("player1")
        game_state = game_state.add_player_planet("player1", planet1)
        game_state = game_state.add_player_planet("player1", planet2)

        resource_manager = ResourceManager(game_state)
        voting_system = VotingSystem()

        # Verify planets start ready
        assert not planet1.is_exhausted()
        assert not planet2.is_exhausted()

        # Act
        result = voting_system.cast_votes_with_influence_spending(
            player_id="player1",
            influence_amount=8,  # Should exhaust both planets (6 + 4 = 10, but only need 8)
            outcome="For",
            resource_manager=resource_manager,
        )

        # Assert
        assert result.success
        assert result.votes_cast == 8

        # Verify planets are exhausted after voting
        assert planet1.is_exhausted()  # Should be exhausted
        # Note: The ResourceManager exhausts planets fully, so both should be exhausted

    def test_voting_system_compatibility_with_existing_methods(self) -> None:
        """Test that enhanced VotingSystem remains compatible with existing methods.

        Requirements: 9.4
        """
        # Arrange
        voting_system = VotingSystem()

        # Create planets the old way
        planet1 = Planet("Mecatol Rex", resources=1, influence=6)
        planet2 = Planet("Jord", resources=4, influence=4)
        planet1.set_control("player1")
        planet2.set_control("player1")

        # Act - Use existing cast_votes method
        result = voting_system.cast_votes(
            player_id="player1", planets=[planet1, planet2], outcome="For"
        )

        # Assert - Should still work
        assert result.success
        assert result.votes_cast == 10

        # Verify new methods are also available
        assert hasattr(voting_system, "cast_votes_with_resource_manager")
        assert hasattr(voting_system, "calculate_available_influence_for_voting")
        assert hasattr(voting_system, "cast_votes_with_influence_spending")

    def test_complete_voting_workflow_with_resource_manager(self) -> None:
        """Test complete voting workflow using ResourceManager integration.

        Requirements: 9.1, 9.2, 9.3, 9.4, 9.5
        """
        # Arrange
        game_state = GameState()
        player1 = Player("player1", Faction.SOL)
        player2 = Player("player2", Faction.HACAN)
        game_state = game_state.add_player(player1)
        game_state = game_state.add_player(player2)

        # Add planets for player1
        planet1 = Planet("Mecatol Rex", resources=1, influence=6)
        planet2 = Planet("Jord", resources=4, influence=4)
        planet1.set_control("player1")
        planet2.set_control("player1")
        game_state = game_state.add_player_planet("player1", planet1)
        game_state = game_state.add_player_planet("player1", planet2)

        # Add planets for player2
        planet3 = Planet("Arc Prime", resources=4, influence=0)
        planet4 = Planet("Wren Terra", resources=2, influence=1)
        planet3.set_control("player2")
        planet4.set_control("player2")
        game_state = game_state.add_player_planet("player2", planet3)
        game_state = game_state.add_player_planet("player2", planet4)

        # Add trade goods (should not affect voting)
        player1.gain_trade_goods(5)
        player2.gain_trade_goods(3)

        resource_manager = ResourceManager(game_state)
        voting_system = VotingSystem()

        # Act
        # Player1 votes "For" with 8 influence (should use both planets)
        result1 = voting_system.cast_votes_with_resource_manager(
            player_id="player1",
            influence_amount=8,
            outcome="For",
            resource_manager=resource_manager,
        )

        # Player2 votes "Against" with 1 influence (Wren Terra)
        result2 = voting_system.cast_votes_with_resource_manager(
            player_id="player2",
            influence_amount=1,
            outcome="Against",
            resource_manager=resource_manager,
        )

        # Assert
        assert result1.success
        assert result1.votes_cast == 8
        assert result2.success
        assert result2.votes_cast == 1

        # Check vote tally
        tally = voting_system.get_vote_tally()
        assert tally["For"] == 8
        assert tally["Against"] == 1

        # Verify planets are exhausted correctly
        # Note: ResourceManager exhausts planets fully, so both of player1's planets should be exhausted
        assert planet1.is_exhausted()  # Used for voting
        assert planet2.is_exhausted()  # Used for voting
        assert not planet3.is_exhausted()  # Not used (no influence)
        assert planet4.is_exhausted()  # Used for voting


class TestVotingSystemEnhancements:
    """Test enhancements to VotingSystem for ResourceManager integration."""

    def test_voting_system_has_resource_manager_integration_methods(self) -> None:
        """Test that VotingSystem has methods for ResourceManager integration.

        RED: This test should fail as the methods don't exist yet.

        Requirements: 9.1, 9.4
        """
        # Arrange
        voting_system = VotingSystem()

        # Act & Assert
        # These methods should exist but don't yet
        assert hasattr(voting_system, "cast_votes_with_resource_manager")
        assert hasattr(voting_system, "calculate_available_influence_for_voting")
        assert hasattr(voting_system, "cast_votes_with_influence_spending")

    def test_voting_system_validates_trade_goods_restriction(self) -> None:
        """Test that VotingSystem validates trade goods restriction for voting.

        Requirements: 9.2
        """
        # Arrange
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        # Add planet with low influence
        planet = Planet("Low Influence", resources=3, influence=2)
        planet.set_control("player1")
        game_state = game_state.add_player_planet("player1", planet)

        # Add trade goods
        player.gain_trade_goods(5)

        resource_manager = ResourceManager(game_state)
        voting_system = VotingSystem()

        # Act
        # Try to vote with more influence than planets provide
        # Should fail because trade goods can't be used for voting
        result = voting_system.cast_votes_with_resource_manager(
            player_id="player1",
            influence_amount=5,  # More than planet influence (2)
            outcome="For",
            resource_manager=resource_manager,
        )

        # Assert
        assert not result.success
        assert "trade goods cannot be used for voting" in result.error_message
