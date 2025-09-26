"""Tests for PhaseTransitionError."""

from ti4.core.game_phase import GamePhase


class TestPhaseTransitionError:
    """Test PhaseTransitionError creation and functionality."""

    def test_phase_transition_error_creation(self) -> None:
        """Test PhaseTransitionError creation with phase information."""
        # RED: This will fail because PhaseTransitionError doesn't exist yet
        from ti4.core.exceptions import PhaseTransitionError

        from_phase = GamePhase.STRATEGY
        to_phase = GamePhase.AGENDA

        error = PhaseTransitionError(from_phase, to_phase)

        expected_message = f"Invalid transition from {from_phase} to {to_phase}"
        assert str(error) == expected_message
        assert error.from_phase == from_phase
        assert error.to_phase == to_phase
        assert hasattr(error, "timestamp")

    def test_phase_transition_error_with_context(self) -> None:
        """Test PhaseTransitionError creation with additional context."""
        # RED: This will fail because PhaseTransitionError doesn't exist yet
        from ti4.core.exceptions import PhaseTransitionError

        from_phase = GamePhase.ACTION
        to_phase = GamePhase.SETUP
        context = {"game_id": "test_game", "player_count": 4}

        error = PhaseTransitionError(from_phase, to_phase, context=context)

        expected_message = f"Invalid transition from {from_phase} to {to_phase}"
        assert str(error) == expected_message
        assert error.from_phase == from_phase
        assert error.to_phase == to_phase
        assert error.context == context
        assert hasattr(error, "timestamp")
