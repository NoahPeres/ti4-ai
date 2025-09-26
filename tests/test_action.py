"""Tests for Action framework."""

from typing import Any

import pytest

from ti4.actions.action import Action, PlayerDecision


def test_player_decision_is_abstract() -> None:
    """Test that PlayerDecision cannot be instantiated directly."""
    # Should not be able to create PlayerDecision directly
    with pytest.raises(TypeError):
        PlayerDecision()


def test_action_is_abstract() -> None:
    """Test that Action cannot be instantiated directly."""
    # Should not be able to create Action directly
    with pytest.raises(TypeError):
        Action()


def test_concrete_action_implementation() -> None:
    """Test that concrete actions can implement the interface."""

    class TestTacticalAction(Action):
        def is_legal(self, state: Any, player_id: str) -> bool:
            return True

        def execute(self, state: Any, player_id: str) -> Any:
            return state

        def get_description(self) -> str:
            return "tactical action: activate system"

    action = TestTacticalAction()

    # Should be able to call all methods
    assert action.is_legal(None, "player1") is True
    assert action.execute("state", "player1") == "state"
    assert action.get_description() == "tactical action: activate system"


def test_concrete_player_decision_implementation() -> None:
    """Test that concrete player decisions can implement the interface."""

    class TestTransaction(PlayerDecision):
        def is_legal(self, state: Any, player_id: str) -> bool:
            return True

        def execute(self, state: Any, player_id: str) -> Any:
            return state

        def get_description(self) -> str:
            return "transaction: trade commodities"

    decision = TestTransaction()

    # Should be able to call all methods
    assert decision.is_legal(None, "player1") is True
    assert decision.execute("state", "player1") == "state"
    assert decision.get_description() == "transaction: trade commodities"


def test_action_result_creation() -> None:
    """Test that ActionResult can be created with success and new state."""
    from ti4.actions.action import ActionResult

    result = ActionResult(
        success=True, new_state="new_state", message="Action succeeded"
    )

    assert result.success is True
    assert result.new_state == "new_state"
    assert result.message == "Action succeeded"


def test_action_inherits_from_player_decision() -> None:
    """Test that Action is a subclass of PlayerDecision."""
    assert issubclass(Action, PlayerDecision)
