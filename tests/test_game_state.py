"""Tests for GameState class."""

from src.ti4.core.game_state import GameState


def test_game_state_creation() -> None:
    """Test that GameState can be created."""
    state = GameState()
    assert state is not None


def test_game_state_equality() -> None:
    """Test that GameState instances with same data are equal."""
    game_id = "test-game-id"
    state1 = GameState(game_id=game_id)
    state2 = GameState(game_id=game_id)

    assert state1 == state2


def test_game_state_hashing() -> None:
    """Test that GameState instances can be hashed consistently."""
    game_id = "test-game-id"
    state1 = GameState(game_id=game_id)
    state2 = GameState(game_id=game_id)

    # Same states should have same hash
    assert hash(state1) == hash(state2)

    # Should be able to use as dict key
    state_dict = {state1: "test"}
    assert state_dict[state2] == "test"


def test_game_state_validation() -> None:
    """Test basic validation methods for state consistency."""
    state = GameState()

    # Should have a validation method
    assert hasattr(state, "is_valid")
    assert callable(state.is_valid)

    # Basic state should be valid
    assert state.is_valid() is True
