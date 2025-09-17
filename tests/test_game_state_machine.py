"""Tests for GameStateMachine."""

import pytest

from src.ti4.core.game_phase import GamePhase
from src.ti4.core.game_state_machine import GameStateMachine


class TestGameStateMachine:
    """Test cases for GameStateMachine."""

    def test_initial_phase_is_setup(self):
        """Test that state machine starts in SETUP phase."""
        state_machine = GameStateMachine()
        assert state_machine.current_phase == GamePhase.SETUP

    def test_can_transition_to_valid_phase(self):
        """Test that can_transition_to returns True for valid transitions."""
        state_machine = GameStateMachine()
        # From SETUP, should be able to go to STRATEGY
        assert state_machine.can_transition_to(GamePhase.STRATEGY)

    def test_can_transition_to_invalid_phase(self):
        """Test that can_transition_to returns False for invalid transitions."""
        state_machine = GameStateMachine()
        # From SETUP, should NOT be able to go directly to ACTION
        assert not state_machine.can_transition_to(GamePhase.ACTION)

    def test_transition_to_valid_phase(self):
        """Test that transition_to changes phase for valid transitions."""
        state_machine = GameStateMachine()
        state_machine.transition_to(GamePhase.STRATEGY)
        assert state_machine.current_phase == GamePhase.STRATEGY

    def test_transition_to_invalid_phase_raises_error(self):
        """Test that transition_to raises error for invalid transitions."""
        state_machine = GameStateMachine()
        with pytest.raises(
            ValueError,
            match="Invalid transition from GamePhase.SETUP to GamePhase.ACTION",
        ):
            state_machine.transition_to(GamePhase.ACTION)

    def test_get_valid_transitions(self):
        """Test that get_valid_transitions returns correct transitions."""
        state_machine = GameStateMachine()
        valid_transitions = state_machine.get_valid_transitions()
        assert valid_transitions == {GamePhase.STRATEGY}

    def test_full_phase_cycle(self):
        """Test a complete phase transition cycle."""
        state_machine = GameStateMachine()

        # SETUP -> STRATEGY
        state_machine.transition_to(GamePhase.STRATEGY)
        assert state_machine.current_phase == GamePhase.STRATEGY
        assert state_machine.get_valid_transitions() == {GamePhase.ACTION}

        # STRATEGY -> ACTION
        state_machine.transition_to(GamePhase.ACTION)
        assert state_machine.current_phase == GamePhase.ACTION
        assert state_machine.get_valid_transitions() == {GamePhase.STATUS}

        # ACTION -> STATUS
        state_machine.transition_to(GamePhase.STATUS)
        assert state_machine.current_phase == GamePhase.STATUS
        assert state_machine.get_valid_transitions() == {GamePhase.AGENDA}

        # STATUS -> AGENDA
        state_machine.transition_to(GamePhase.AGENDA)
        assert state_machine.current_phase == GamePhase.AGENDA
        assert state_machine.get_valid_transitions() == {GamePhase.STRATEGY}

        # AGENDA -> STRATEGY (next round)
        state_machine.transition_to(GamePhase.STRATEGY)
        assert state_machine.current_phase == GamePhase.STRATEGY

    def test_transition_map_completeness(self):
        """Test that all phases have defined transitions."""
        GameStateMachine()

        # Test each phase has valid transitions defined
        for phase in GamePhase:
            # Create a new state machine in the desired phase
            test_machine = GameStateMachine()
            test_machine._current_phase = phase

            # Each phase should have at least one valid transition
            valid_transitions = test_machine.get_valid_transitions()
            assert len(valid_transitions) > 0, f"Phase {phase} has no valid transitions"
