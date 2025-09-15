"""Tests for GamePhase management."""

from src.ti4.core.game_phase import GamePhase, is_valid_transition


def test_game_phase_enum_exists():
    """Test that GamePhase enum has basic phases."""
    # Should have at least a setup phase
    assert hasattr(GamePhase, "SETUP")
    assert GamePhase.SETUP is not None


def test_phase_transition_logic():
    """Test that phase transition logic exists."""
    # Should have a function to validate transitions
<<<<<<< HEAD
    from src.ti4.core.game_phase import is_valid_transition

=======
>>>>>>> 1346505907443084e976e966a542dd04bf2e4157
    # Should be able to transition from SETUP to some other phase
    assert is_valid_transition(GamePhase.SETUP, GamePhase.SETUP) is False
