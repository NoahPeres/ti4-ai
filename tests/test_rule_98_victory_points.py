"""Tests for Rule 98 Victory Points - comprehensive victory condition testing."""

import pytest

from src.ti4.core.game_phase import GamePhase
from src.ti4.core.game_state import GameState
from src.ti4.core.objective import Objective
from src.ti4.core.player import Player


class TestRule98VictoryPoints:
    """Test Rule 98 Victory Points implementation."""

    def test_simultaneous_victory_tie_breaking_by_initiative_order(self) -> None:
        """Test Rule 98.7: Initiative order determines winner when multiple players reach 10 points simultaneously.

        Note: Sequential scoring simulates "simultaneous" victory as winner checks are evaluated
        post-scoring in this engine, modeling end-of-round evaluation semantics.
        """
        # Create players in specific initiative order
        player1 = Player(id="player1", faction="sol")
        player2 = Player(id="player2", faction="hacan")
        player3 = Player(id="player3", faction="xxcha")

        # Players are in initiative order: player1, player2, player3
        game_state = GameState(players=[player1, player2, player3])

        # Set up scenario where multiple players could reach 10 points simultaneously
        # Give each player 8 points initially
        state1 = game_state.award_victory_points("player1", 8)
        state2 = state1.award_victory_points("player2", 8)
        state3 = state2.award_victory_points("player3", 8)

        # Create objectives that would give 2 points each
        objective_a = Objective(
            id="obj_a",
            name="Objective A",
            description="Test objective A",
            points=2,
            is_public=True,
            scoring_phase=GamePhase.STATUS,
        )
        objective_b = Objective(
            id="obj_b",
            name="Objective B",
            description="Test objective B",
            points=2,
            is_public=True,
            scoring_phase=GamePhase.STATUS,
        )
        objective_c = Objective(
            id="obj_c",
            name="Objective C",
            description="Test objective C",
            points=2,
            is_public=True,
            scoring_phase=GamePhase.STATUS,
        )

        # Simulate simultaneous scoring that would give all players 10 points
        # In a real game, this could happen during status phase when multiple players
        # score objectives that push them to 10 points
        final_state = state3.score_objective("player2", objective_b, GamePhase.STATUS)
        final_state = final_state.score_objective(
            "player3", objective_c, GamePhase.STATUS
        )
        final_state = final_state.score_objective(
            "player1", objective_a, GamePhase.STATUS
        )

        # All players should have 10 points
        assert final_state.get_victory_points("player1") == 10
        assert final_state.get_victory_points("player2") == 10
        assert final_state.get_victory_points("player3") == 10

        # The winner should be determined by initiative order (earliest player wins)
        # According to Rule 98.7, player1 should win as they are earliest in initiative order
        assert final_state.has_winner()
        assert final_state.get_winner() == "player1"

    def test_fourteen_point_victory_variant(self) -> None:
        """Test Rule 98.2a: 14-point victory variant when using 14-space victory track."""
        player = Player(id="player1", faction="sol")

        # Create game state with 14-point victory variant enabled
        game_state = GameState(players=[player], victory_points_to_win=14)

        # Player with 10 points should not win in 14-point variant
        state_10_points = game_state.award_victory_points("player1", 10)
        assert not state_10_points.has_winner()
        assert state_10_points.get_winner() is None

        # Player with 13 points should not win
        state_13_points = game_state.award_victory_points("player1", 13)
        assert not state_13_points.has_winner()

        # Player with 14 points should win
        state_14_points = game_state.award_victory_points("player1", 14)
        assert state_14_points.has_winner()
        assert state_14_points.get_winner() == "player1"

    def test_victory_point_maximum_enforcement_objective_scoring(self) -> None:
        """Test that VP maximum is enforced when scoring objectives, not just direct awards."""
        player = Player(id="player1", faction="sol")
        game_state = GameState(players=[player])

        # Create a 2-point objective
        objective = Objective(
            id="test_objective",
            name="Test Objective",
            description="A test objective worth 2 points",
            points=2,
            is_public=True,
            scoring_phase=GamePhase.ACTION,
        )

        # Award 9 points first (should be allowed)
        state_9 = game_state.award_victory_points("player1", 9)
        assert state_9.get_victory_points("player1") == 9

        # Scoring a 2-point objective should fail (would exceed 10 point maximum)
        with pytest.raises(ValueError, match="cannot exceed maximum victory points"):
            state_9.score_objective("player1", objective, GamePhase.ACTION)

    def test_victory_point_maximum_enforcement(self) -> None:
        """Test Rule 98.4a: Player cannot have more than 10 victory points (or variant maximum)."""
        player = Player(id="player1", faction="sol")
        game_state = GameState(players=[player])

        # Award 10 points (should be allowed)
        state_10 = game_state.award_victory_points("player1", 10)
        assert state_10.get_victory_points("player1") == 10

        # Attempting to award more points should be prevented or capped
        # This should either raise an error or cap at maximum
        with pytest.raises(ValueError, match="cannot exceed maximum victory points"):
            state_10.award_victory_points("player1", 1)

    def test_most_fewest_victory_points_tie_resolution(self) -> None:
        """Test Rule 98.5: Effects apply to all tied players for most/fewest victory points."""
        player1 = Player(id="player1", faction="sol")
        player2 = Player(id="player2", faction="hacan")
        player3 = Player(id="player3", faction="xxcha")

        game_state = GameState(players=[player1, player2, player3])

        # Set up tie scenario: player1 and player2 have 5 points, player3 has 3
        state1 = game_state.award_victory_points("player1", 5)
        state2 = state1.award_victory_points("player2", 5)
        state3 = state2.award_victory_points("player3", 3)

        # Test getting players with most victory points (should return both tied players)
        most_vp_players = state3.get_players_with_most_victory_points()
        assert most_vp_players == [
            "player1",
            "player2",
        ]  # initiative fallback = players list

        # Test getting players with fewest victory points (should return player3)
        fewest_vp_players = state3.get_players_with_fewest_victory_points()
        assert fewest_vp_players == ["player3"]

        # Test scenario where all players are tied
        equal_state = game_state.award_victory_points("player1", 4)
        equal_state = equal_state.award_victory_points("player2", 4)
        equal_state = equal_state.award_victory_points("player3", 4)

        most_equal = equal_state.get_players_with_most_victory_points()
        fewest_equal = equal_state.get_players_with_fewest_victory_points()

        assert most_equal == ["player1", "player2", "player3"]
        assert fewest_equal == ["player1", "player2", "player3"]
