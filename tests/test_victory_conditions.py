"""Tests for victory point tracking and objective system."""

from src.ti4.core.game_state import GameState
from src.ti4.core.player import Player


class TestVictoryPointTracking:
    """Test victory point assignment and tracking."""

    def test_player_starts_with_zero_victory_points(self):
        """Test that players start with zero victory points."""
        player = Player(id="player1", faction="sol")
        game_state = GameState(players=[player])

        assert game_state.get_victory_points("player1") == 0

    def test_award_victory_points_to_player(self):
        """Test that victory points can be awarded to a player."""
        player = Player(id="player1", faction="sol")
        game_state = GameState(players=[player])

        new_state = game_state.award_victory_points("player1", 2)
        assert new_state.get_victory_points("player1") == 2

    def test_check_victory_condition(self):
        """Test that victory condition is checked correctly."""
        player = Player(id="player1", faction="sol")
        game_state = GameState(players=[player])

        # Player with less than 10 points should not have won
        state_with_points = game_state.award_victory_points("player1", 8)
        assert not state_with_points.has_winner()

        # Player with 10 or more points should have won
        winning_state = game_state.award_victory_points("player1", 10)
        assert winning_state.has_winner()
        assert winning_state.get_winner() == "player1"


class TestObjectiveSystem:
    """Test objective card structure and completion detection."""

    def test_create_objective_card(self):
        """Test that objective cards can be created with proper structure."""
        from src.ti4.core.objective import Objective
        from src.ti4.core.game_phase import GamePhase

        # This should fail initially - we need to implement Objective class
        objective = Objective(
            id="control_planets",
            name="Control 6 planets",
            description="Control 6 planets outside your home system",
            points=1,
            is_public=True,
            scoring_phase=GamePhase.STATUS
        )
        assert objective.id == "control_planets"
        assert objective.points == 1
        assert objective.is_public is True

    def test_objective_completion_detection(self):
        """Test that objective completion can be detected."""
        from src.ti4.core.objective import Objective
        from src.ti4.core.game_phase import GamePhase

        player = Player(id="player1", faction="sol")
        game_state = GameState(players=[player])

        objective = Objective(
            id="control_planets",
            name="Control 6 planets",
            description="Control 6 planets outside your home system",
            points=1,
            is_public=True,
            scoring_phase=GamePhase.STATUS
        )

        # This should fail initially - we need to implement completion detection
        assert not game_state.is_objective_completed("player1", objective)

        # After meeting the condition, it should be completed
        # For now, we'll simulate this with a simple method
        state_with_completion = game_state.complete_objective("player1", objective)
        assert state_with_completion.is_objective_completed("player1", objective)

    def test_completing_objective_awards_victory_points(self):
        """Test that completing an objective awards the correct victory points."""
        from src.ti4.core.objective import Objective
        from src.ti4.core.game_phase import GamePhase

        player = Player(id="player1", faction="sol")
        game_state = GameState(players=[player])

        objective = Objective(
            id="control_planets",
            name="Control 6 planets",
            description="Control 6 planets outside your home system",
            points=2,
            is_public=True,
            scoring_phase=GamePhase.STATUS
        )

        # Initially no points
        assert game_state.get_victory_points("player1") == 0

        # Complete objective and award points
        state_with_completion = game_state.complete_objective("player1", objective)
        final_state = state_with_completion.award_victory_points(
            "player1", objective.points
        )

        # Should have the objective completed and points awarded
        assert final_state.is_objective_completed("player1", objective)
        assert final_state.get_victory_points("player1") == 2


class TestPublicObjectives:
    """Test basic public objective implementation."""

    def test_control_planets_objective_completion(self):
        """Test that control planets objective can be completed."""
        from src.ti4.core.public_objectives import ControlPlanetsObjective

        player = Player(id="player1", faction="sol")
        game_state = GameState(players=[player])

        objective = ControlPlanetsObjective()
        assert not objective.is_completed_by(game_state, "player1")

    def test_spend_resources_objective_completion(self):
        """Test that spend resources objective can be completed."""
        from src.ti4.core.public_objectives import SpendResourcesObjective

        player = Player(id="player1", faction="sol")
        game_state = GameState(players=[player])

        objective = SpendResourcesObjective()
        assert not objective.is_completed_by(game_state, "player1")

    def test_objective_scoring_and_validation(self):
        """Test that objectives can be scored and validated for timing."""
        from src.ti4.core.public_objectives import ControlPlanetsObjective

        player = Player(id="player1", faction="sol")
        game_state = GameState(players=[player])

        objective = ControlPlanetsObjective()

        # Test that we can get the objective data
        obj_data = objective.get_objective()
        assert obj_data.points == 1
        assert obj_data.is_public is True

        # Test that multiple completions are prevented
        state_with_completion = game_state.complete_objective("player1", obj_data)
        assert state_with_completion.is_objective_completed("player1", obj_data)

        # Completing the same objective again should not change anything
        state_with_duplicate = state_with_completion.complete_objective(
            "player1", obj_data
        )
        assert state_with_duplicate.is_objective_completed("player1", obj_data)

        # The completed objectives list should still only contain one entry
        player_objectives = state_with_duplicate.completed_objectives.get("player1", [])
        assert player_objectives.count(obj_data.id) == 1
