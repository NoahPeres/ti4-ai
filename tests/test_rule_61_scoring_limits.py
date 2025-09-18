"""
Comprehensive tests for Rule 61 objective scoring limits.

Tests the enforcement of:
- Status phase: max 1 public + 1 secret objective per player per phase
- Combat: max 1 objective per combat
- Phase transitions reset limits
"""

import pytest

from src.ti4.core.game_phase import GamePhase
from src.ti4.core.game_state import GameState
from src.ti4.core.objective import Objective


class TestStatusPhaseScoringLimits:
    """Test status phase scoring limits (Rule 61.6)."""

    def test_can_score_one_public_objective_per_status_phase(self):
        """Test that players can score exactly one public objective per status phase."""
        game_state = GameState()

        public_obj1 = Objective(
            "pub1", "Public 1", "First public", 1, True, GamePhase.STATUS
        )
        public_obj2 = Objective(
            "pub2", "Public 2", "Second public", 1, True, GamePhase.STATUS
        )

        # Score first public objective - should succeed
        state1 = game_state.score_objective("player1", public_obj1, GamePhase.STATUS)
        assert state1.is_objective_completed("player1", public_obj1)
        assert state1.get_victory_points("player1") == 1

        # Try to score second public objective in same status phase - should fail
        with pytest.raises(
            ValueError,
            match="Already scored a public objective during this status phase",
        ):
            state1.score_objective("player1", public_obj2, GamePhase.STATUS)

    def test_can_score_one_secret_objective_per_status_phase(self):
        """Test that players can score exactly one secret objective per status phase."""
        game_state = GameState()

        secret_obj1 = Objective(
            "sec1", "Secret 1", "First secret", 1, False, GamePhase.STATUS
        )
        secret_obj2 = Objective(
            "sec2", "Secret 2", "Second secret", 1, False, GamePhase.STATUS
        )

        # Assign secret objectives to player first
        state_with_secrets = game_state.assign_secret_objective("player1", secret_obj1)
        state_with_secrets = state_with_secrets.assign_secret_objective(
            "player1", secret_obj2
        )

        # Score first secret objective - should succeed
        state1 = state_with_secrets.score_objective(
            "player1", secret_obj1, GamePhase.STATUS
        )
        assert state1.is_objective_completed("player1", secret_obj1)
        assert state1.get_victory_points("player1") == 1

        # Try to score second secret objective in same status phase - should fail
        with pytest.raises(
            ValueError,
            match="Already scored a secret objective during this status phase",
        ):
            state1.score_objective("player1", secret_obj2, GamePhase.STATUS)

    def test_can_score_one_public_and_one_secret_per_status_phase(self):
        """Test that players can score one public AND one secret objective per status phase."""
        game_state = GameState()

        public_obj = Objective(
            "pub", "Public", "Public objective", 1, True, GamePhase.STATUS
        )
        secret_obj = Objective(
            "sec", "Secret", "Secret objective", 1, False, GamePhase.STATUS
        )

        # Assign secret objective to player first
        state_with_secret = game_state.assign_secret_objective("player1", secret_obj)

        # Score public objective first
        state1 = state_with_secret.score_objective(
            "player1", public_obj, GamePhase.STATUS
        )
        assert state1.get_victory_points("player1") == 1

        # Score secret objective - should succeed
        state2 = state1.score_objective("player1", secret_obj, GamePhase.STATUS)
        assert state2.get_victory_points("player1") == 2
        assert state2.is_objective_completed("player1", public_obj)
        assert state2.is_objective_completed("player1", secret_obj)

    def test_different_players_have_separate_scoring_limits(self):
        """Test that scoring limits are per-player."""
        game_state = GameState()

        public_obj1 = Objective(
            "pub1", "Public 1", "First public", 1, True, GamePhase.STATUS
        )
        public_obj2 = Objective(
            "pub2", "Public 2", "Second public", 1, True, GamePhase.STATUS
        )

        # Player 1 scores first public objective
        state1 = game_state.score_objective("player1", public_obj1, GamePhase.STATUS)

        # Player 2 should still be able to score a public objective
        state2 = state1.score_objective("player2", public_obj2, GamePhase.STATUS)

        assert state2.is_objective_completed("player1", public_obj1)
        assert state2.is_objective_completed("player2", public_obj2)
        assert state2.get_victory_points("player1") == 1
        assert state2.get_victory_points("player2") == 1

    def test_status_phase_limits_reset_between_phases(self):
        """Test that status phase scoring limits reset when advancing to next status phase."""
        game_state = GameState()

        public_obj1 = Objective(
            "pub1", "Public 1", "First public", 1, True, GamePhase.STATUS
        )
        public_obj2 = Objective(
            "pub2", "Public 2", "Second public", 1, True, GamePhase.STATUS
        )

        # Score first public objective
        state1 = game_state.score_objective("player1", public_obj1, GamePhase.STATUS)

        # Advance to next status phase (reset limits)
        state2 = state1.advance_to_next_status_phase()

        # Should now be able to score another public objective
        state3 = state2.score_objective("player1", public_obj2, GamePhase.STATUS)

        assert state3.is_objective_completed("player1", public_obj1)
        assert state3.is_objective_completed("player1", public_obj2)
        assert state3.get_victory_points("player1") == 2


class TestCombatScoringLimits:
    """Test combat objective scoring limits (Rule 61.7)."""

    def test_can_score_one_objective_per_combat(self):
        """Test that players can score only one objective per combat."""
        game_state = GameState()

        action_obj1 = Objective(
            "act1", "Action 1", "First action", 1, True, GamePhase.ACTION
        )
        action_obj2 = Objective(
            "act2", "Action 2", "Second action", 1, True, GamePhase.ACTION
        )

        combat_id = "combat_123"

        # Score first objective during combat - should succeed
        state1 = game_state.score_objective_during_combat(
            "player1", action_obj1, combat_id
        )
        assert state1.is_objective_completed("player1", action_obj1)
        assert state1.get_victory_points("player1") == 1

        # Try to score second objective in same combat - should fail
        with pytest.raises(
            ValueError, match="Already scored an objective during combat"
        ):
            state1.score_objective_during_combat("player1", action_obj2, combat_id)

    def test_different_combats_have_separate_limits(self):
        """Test that different combats have separate scoring limits."""
        game_state = GameState()

        action_obj1 = Objective(
            "act1", "Action 1", "First action", 1, True, GamePhase.ACTION
        )
        action_obj2 = Objective(
            "act2", "Action 2", "Second action", 1, True, GamePhase.ACTION
        )

        combat_id1 = "combat_123"
        combat_id2 = "combat_456"

        # Score objective in first combat
        state1 = game_state.score_objective_during_combat(
            "player1", action_obj1, combat_id1
        )

        # Score objective in second combat - should succeed
        state2 = state1.score_objective_during_combat(
            "player1", action_obj2, combat_id2
        )

        assert state2.is_objective_completed("player1", action_obj1)
        assert state2.is_objective_completed("player1", action_obj2)
        assert state2.get_victory_points("player1") == 2

    def test_combat_scoring_requires_action_phase_objective(self):
        """Test that combat scoring only works with action phase objectives."""
        game_state = GameState()

        status_obj = Objective(
            "stat", "Status", "Status objective", 1, True, GamePhase.STATUS
        )
        combat_id = "combat_123"

        # Try to score status phase objective during combat - should fail
        with pytest.raises(
            ValueError, match="Cannot score status phase objective during combat"
        ):
            game_state.score_objective_during_combat("player1", status_obj, combat_id)


class TestStatusPhaseStepExecution:
    """Test status phase step 1 execution (Rule 81.1)."""

    def test_execute_status_phase_step_1_multiple_objectives(self):
        """Test executing status phase step 1 with multiple objectives."""
        game_state = GameState()

        public_obj = Objective(
            "pub", "Public", "Public objective", 1, True, GamePhase.STATUS
        )
        secret_obj = Objective(
            "sec", "Secret", "Secret objective", 1, False, GamePhase.STATUS
        )

        # Assign secret objective to player first
        state_with_secret = game_state.assign_secret_objective("player1", secret_obj)

        # Execute status phase step 1 with both objectives
        objectives = [public_obj, secret_obj]
        final_state = state_with_secret.execute_status_phase_step_1_score_objectives(
            "player1", objectives
        )

        assert final_state.is_objective_completed("player1", public_obj)
        assert final_state.is_objective_completed("player1", secret_obj)
        assert final_state.get_victory_points("player1") == 2

    def test_execute_status_phase_step_1_respects_limits(self):
        """Test that status phase step 1 execution respects scoring limits."""
        game_state = GameState()

        public_obj1 = Objective(
            "pub1", "Public 1", "First public", 1, True, GamePhase.STATUS
        )
        public_obj2 = Objective(
            "pub2", "Public 2", "Second public", 1, True, GamePhase.STATUS
        )

        # Try to execute with two public objectives - should fail on second
        objectives = [public_obj1, public_obj2]

        with pytest.raises(
            ValueError,
            match="Already scored a public objective during this status phase",
        ):
            game_state.execute_status_phase_step_1_score_objectives(
                "player1", objectives
            )


class TestObjectiveScoringEdgeCases:
    """Test edge cases in objective scoring."""

    def test_cannot_score_same_objective_twice(self):
        """Test Rule 61.8: A player can score each objective only once during the game."""
        game_state = GameState()

        public_obj = Objective(
            "pub", "Public", "Public objective", 1, True, GamePhase.STATUS
        )

        # Score objective first time - should succeed
        state1 = game_state.score_objective("player1", public_obj, GamePhase.STATUS)
        assert state1.get_victory_points("player1") == 1

        # Advance to next status phase to reset limits
        state2 = state1.advance_to_next_status_phase()

        # Try to score same objective again - should fail
        with pytest.raises(ValueError, match="already scored by player"):
            state2.score_objective("player1", public_obj, GamePhase.STATUS)

    def test_multiple_players_can_score_same_public_objective(self):
        """Test that multiple players can score the same public objective."""
        game_state = GameState()

        public_obj = Objective(
            "pub", "Public", "Public objective", 1, True, GamePhase.STATUS
        )

        # Player 1 scores objective
        state1 = game_state.score_objective("player1", public_obj, GamePhase.STATUS)

        # Player 2 scores same objective - should succeed
        state2 = state1.score_objective("player2", public_obj, GamePhase.STATUS)

        assert state2.is_objective_completed("player1", public_obj)
        assert state2.is_objective_completed("player2", public_obj)
        assert state2.get_victory_points("player1") == 1
        assert state2.get_victory_points("player2") == 1

    def test_non_status_phase_objectives_ignore_status_limits(self):
        """Test that non-status phase objectives don't count against status phase limits."""
        game_state = GameState()

        action_obj = Objective(
            "act", "Action", "Action objective", 1, True, GamePhase.ACTION
        )
        status_obj = Objective(
            "stat", "Status", "Status objective", 1, True, GamePhase.STATUS
        )

        # Score action phase objective during action phase
        state1 = game_state.score_objective("player1", action_obj, GamePhase.ACTION)

        # Should still be able to score status phase objective during status phase
        state2 = state1.score_objective("player1", status_obj, GamePhase.STATUS)

        assert state2.is_objective_completed("player1", action_obj)
        assert state2.is_objective_completed("player1", status_obj)
        assert state2.get_victory_points("player1") == 2
