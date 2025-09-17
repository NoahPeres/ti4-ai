"""Tests for GameState class."""

import pytest

from src.ti4.core.game_state import GameState


def test_game_state_creation():
    """Test that GameState can be created."""
    state = GameState()
    assert state is not None


def test_game_state_immutability():
    """Test that GameState is immutable (frozen dataclass)."""
    state = GameState()

    # Should not be able to modify the state after creation
    with pytest.raises(AttributeError):
        state.new_field = "value"


def test_game_state_equality():
    """Test that GameState instances with same data are equal."""
    game_id = "test-game-id"
    state1 = GameState(game_id=game_id)
    state2 = GameState(game_id=game_id)

    assert state1 == state2


def test_game_state_hashing():
    """Test that GameState instances can be hashed consistently."""
    game_id = "test-game-id"
    state1 = GameState(game_id=game_id)
    state2 = GameState(game_id=game_id)

    # Same states should have same hash
    assert hash(state1) == hash(state2)

    # Should be able to use as dict key
    state_dict = {state1: "test"}
    assert state_dict[state2] == "test"


def test_game_state_validation():
    """Test basic validation methods for state consistency."""
    state = GameState()

    # Should have a validation method
    assert hasattr(state, "is_valid")
    assert callable(state.is_valid)

    # Basic state should be valid
    assert state.is_valid() is True
