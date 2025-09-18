"""Tests for Rule 61: OBJECTIVE CARDS - Phase-specific scoring and limits."""

import pytest

from src.ti4.core.game_phase import GamePhase
from src.ti4.core.game_state import GameState
from src.ti4.core.game_state_machine import GameStateMachine
from src.ti4.core.objective import Objective

from .test_rule_61_test_helpers import (
    ObjectiveTestHelpers,
    assert_objective_scored,
    assert_scoring_fails,
)


class TestPhaseSpecificObjectiveScoring:
    """Test phase-specific objective scoring mechanics (Rule 61.3, 61.5, 61.6, 61.7)."""

    def test_objective_has_scoring_phase_attribute(self) -> None:
        """Test that objectives specify which phase they can be scored in."""
        # Rule 61.3: Each objective card indicates the phase during which a player can score
        objectives = ObjectiveTestHelpers.create_standard_objectives()

        assert objectives["status_public"].scoring_phase == GamePhase.STATUS
        assert objectives["action_public"].scoring_phase == GamePhase.ACTION
        assert objectives["agenda_public"].scoring_phase == GamePhase.AGENDA

    def test_can_only_score_objective_in_correct_phase(self) -> None:
        """Test that objectives can only be scored during their designated phase."""
        # Rule 61.5: Players can score objectives following the timing indicated on the card
        game_state = GameState()

        status_objective = ObjectiveTestHelpers.create_public_objective(
            "status_obj", "Status Objective", GamePhase.STATUS
        )

        # Should be able to score status objective during status phase
        state1 = game_state.score_objective(
            "player1", status_objective, GamePhase.STATUS
        )
        assert_objective_scored(state1, "player1", status_objective, 1)

        # Should fail when trying to score status objective during action phase
        assert_scoring_fails(
            game_state,
            "player1",
            status_objective,
            GamePhase.ACTION,
            "Cannot score objective.*requiring status phase during action phase",
        )

        # Should fail when trying to score status objective during agenda phase
        assert_scoring_fails(
            game_state,
            "player1",
            status_objective,
            GamePhase.AGENDA,
            "Cannot score objective.*requiring status phase during agenda phase",
        )

    def test_status_phase_scoring_limits(self) -> None:
        """Test that players can score max one public + one secret objective per status phase."""
        # Rule 61.6: A player can score a maximum of one public objective and one secret objective during each status phase
        GameState()

        public_obj1 = ObjectiveTestHelpers.create_public_objective(
            "pub1", "Public 1", GamePhase.STATUS
        )
        public_obj2 = ObjectiveTestHelpers.create_public_objective(
            "pub2", "Public 2", GamePhase.STATUS
        )
        secret_obj1 = ObjectiveTestHelpers.create_secret_objective(
            "sec1", "Secret 1", GamePhase.STATUS
        )
        secret_obj2 = ObjectiveTestHelpers.create_secret_objective(
            "sec2", "Secret 2", GamePhase.STATUS
        )

        # Assign secret objectives to player first
        state_with_secrets = (
            ObjectiveTestHelpers.create_game_state_with_secret_objectives(
                "player1", [secret_obj1, secret_obj2]
            )
        )

        # Should be able to score one public objective
        state1 = state_with_secrets.score_objective(
            "player1", public_obj1, GamePhase.STATUS
        )

        # Should be able to score one secret objective in same phase
        state2 = state1.score_objective("player1", secret_obj1, GamePhase.STATUS)

        # Should fail when trying to score second public objective in same status phase
        assert_scoring_fails(
            state2,
            "player1",
            public_obj2,
            GamePhase.STATUS,
            "Already scored.*public objective.*status phase",
        )

        # Should fail when trying to score second secret objective in same status phase
        assert_scoring_fails(
            state2,
            "player1",
            secret_obj2,
            GamePhase.STATUS,
            "Already scored.*secret objective.*status phase",
        )

    def test_action_phase_unlimited_scoring(self) -> None:
        """Test that players can score unlimited objectives during action phase."""
        # Rule 61.7: A player can score any number of objectives during the action phase
        GameState()

        action_obj1 = ObjectiveTestHelpers.create_public_objective(
            "act1", "Action 1", GamePhase.ACTION
        )
        action_obj2 = ObjectiveTestHelpers.create_public_objective(
            "act2", "Action 2", GamePhase.ACTION
        )
        action_obj3 = ObjectiveTestHelpers.create_secret_objective(
            "act3", "Action 3", GamePhase.ACTION
        )

        # Assign secret objective to player first
        state_with_secret = (
            ObjectiveTestHelpers.create_game_state_with_secret_objectives(
                "player1", [action_obj3]
            )
        )

        # Should be able to score multiple objectives in action phase
        state1 = state_with_secret.score_objective(
            "player1", action_obj1, GamePhase.ACTION
        )
        state2 = state1.score_objective("player1", action_obj2, GamePhase.ACTION)
        state3 = state2.score_objective("player1", action_obj3, GamePhase.ACTION)

        assert_objective_scored(state3, "player1", action_obj1)
        assert_objective_scored(state3, "player1", action_obj2)
        assert_objective_scored(state3, "player1", action_obj3)

    def test_agenda_phase_unlimited_scoring(self) -> None:
        """Test that players can score unlimited objectives during agenda phase."""
        # Rule 61.7: A player can score any number of objectives during the agenda phase
        game_state = GameState()

        agenda_obj1 = Objective(
            "ag1", "Agenda 1", "First agenda", 1, False, GamePhase.AGENDA
        )
        agenda_obj2 = Objective(
            "ag2", "Agenda 2", "Second agenda", 1, False, GamePhase.AGENDA
        )

        # Assign secret objectives to player first
        state_with_secrets = game_state.assign_secret_objective("player1", agenda_obj1)
        state_with_secrets = state_with_secrets.assign_secret_objective(
            "player1", agenda_obj2
        )

        # Should be able to score multiple objectives in agenda phase
        state1 = state_with_secrets.score_objective(
            "player1", agenda_obj1, GamePhase.AGENDA
        )
        state2 = state1.score_objective("player1", agenda_obj2, GamePhase.AGENDA)

        assert state2.is_objective_completed("player1", agenda_obj1)
        assert state2.is_objective_completed("player1", agenda_obj2)

    def test_combat_objective_scoring_limit(self) -> None:
        """Test that only one objective can be scored during/after each combat."""
        # Rule 61.7: Players can only score one objective during or after each combat
        game_state = GameState()

        combat_obj1 = Objective(
            "cb1", "Combat 1", "First combat", 1, True, GamePhase.ACTION
        )
        combat_obj2 = Objective(
            "cb2", "Combat 2", "Second combat", 1, True, GamePhase.ACTION
        )

        # Should be able to score one objective during combat
        state1 = game_state.score_objective_during_combat(
            "player1", combat_obj1, "combat_1"
        )

        # Should fail when trying to score second objective in same combat
        with pytest.raises(ValueError, match="Already scored.*objective.*combat"):
            state1.score_objective_during_combat("player1", combat_obj2, "combat_1")

        # Should be able to score in different combat
        state2 = state1.score_objective_during_combat(
            "player1", combat_obj2, "combat_2"
        )
        assert state2.is_objective_completed("player1", combat_obj2)

    def test_objective_can_only_be_scored_once_per_game(self) -> None:
        """Test that each objective can only be scored once during the game."""
        # Rule 61.8: A player can score each objective only once during the game
        game_state = GameState()

        objective = Objective(
            "test", "Test", "Test objective", 1, True, GamePhase.ACTION
        )

        # Should be able to score objective first time
        state1 = game_state.score_objective("player1", objective, GamePhase.ACTION)
        assert state1.is_objective_completed("player1", objective)

        # Should fail when trying to score same objective again
        with pytest.raises(ValueError, match="Objective.*already scored.*player"):
            state1.score_objective("player1", objective, GamePhase.ACTION)


class TestObjectiveScoringMechanics:
    """Test objective scoring mechanics and validation."""

    def test_score_objective_awards_victory_points(self) -> None:
        """Test that scoring an objective awards the correct victory points."""
        game_state = GameState()

        objective = Objective(
            "test", "Test", "Test objective", 2, True, GamePhase.ACTION
        )

        # Player should start with 0 victory points
        assert game_state.get_victory_points("player1") == 0

        # Scoring objective should award points
        result_state = game_state.score_objective(
            "player1", objective, GamePhase.ACTION
        )
        assert result_state.get_victory_points("player1") == 2

    def test_multiple_players_can_score_same_public_objective(self) -> None:
        """Test that multiple players can score the same public objective."""
        game_state = GameState()

        public_objective = Objective(
            "pub", "Public", "Public objective", 1, True, GamePhase.ACTION
        )

        # Both players should be able to score the same public objective
        state1 = game_state.score_objective(
            "player1", public_objective, GamePhase.ACTION
        )
        state2 = state1.score_objective("player2", public_objective, GamePhase.ACTION)

        assert state2.is_objective_completed("player1", public_objective)
        assert state2.is_objective_completed("player2", public_objective)

    def test_secret_objectives_are_player_specific(self) -> None:
        """Test that secret objectives are specific to individual players."""
        # Rule 61.19: A player can only score their own secret objectives
        game_state = GameState()

        secret_objective = Objective(
            "sec", "Secret", "Secret objective", 1, False, GamePhase.ACTION
        )

        # Assign secret objective to player1
        state_with_secret = game_state.assign_secret_objective(
            "player1", secret_objective
        )

        # Player1 should be able to score their own secret objective
        new_state = state_with_secret.score_objective(
            "player1", secret_objective, GamePhase.ACTION
        )
        assert new_state.is_objective_completed("player1", secret_objective)
        assert new_state.get_victory_points("player1") == 1


class TestObjectivePhaseIntegration:
    """Test integration between objective system and game phase management."""

    def test_status_phase_objective_scoring_step(self) -> None:
        """Test that status phase includes objective scoring step."""
        # Rule 81.1: STEP 1-SCORE OBJECTIVES during status phase
        game_state = GameState()
        state_machine = GameStateMachine()

        # Move to status phase
        state_machine.transition_to(GamePhase.STRATEGY)
        state_machine.transition_to(GamePhase.ACTION)
        state_machine.transition_to(GamePhase.STATUS)

        # Should be able to execute status phase objective scoring
        objective = Objective(
            "test", "Test", "Test objective", 1, True, GamePhase.STATUS
        )
        result_state = game_state.execute_status_phase_step_1_score_objectives(
            "player1", [objective]
        )

        assert result_state.is_objective_completed("player1", objective)

    def test_phase_transition_resets_scoring_limits(self) -> None:
        """Test that phase transitions reset per-phase scoring limits."""
        game_state = GameState()

        public_obj1 = Objective(
            "pub1", "Public 1", "First public", 1, True, GamePhase.STATUS
        )
        public_obj2 = Objective(
            "pub2", "Public 2", "Second public", 1, True, GamePhase.STATUS
        )

        # Score one public objective in first status phase
        state1 = game_state.score_objective("player1", public_obj1, GamePhase.STATUS)

        # Simulate moving to next round (status phase again)
        state2 = state1.advance_to_next_status_phase()

        # Should be able to score another public objective in new status phase
        state3 = state2.score_objective("player1", public_obj2, GamePhase.STATUS)

        assert state3.is_objective_completed("player1", public_obj1)
        assert state3.is_objective_completed("player1", public_obj2)
