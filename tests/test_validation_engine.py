"""Tests for ValidationEngine class."""

from typing import Any

import pytest

from ti4.actions.action import Action
from ti4.actions.validation import (
    PreconditionValidationError,
    RuleValidationError,
    SyntaxValidationError,
    ValidationEngine,
    ValidationError,
)


def test_validation_engine_creation() -> None:
    """Test that ValidationEngine can be created."""
    engine = ValidationEngine()
    assert engine is not None


def test_validation_engine_has_validate_method() -> None:
    """Test that ValidationEngine has a validate method."""
    engine = ValidationEngine()

    # Should have a validate method that takes action, state, and player_id
    result = engine.validate(action=None, state=None, player_id=None)
    assert result is not None


def test_validation_error_creation() -> None:
    """Test that ValidationError can be created with message and context."""
    error = ValidationError("Test error message", "test context")
    assert error.message == "Test error message"
    assert error.context == "test context"


def test_syntax_validation_error_creation() -> None:
    """Test that SyntaxValidationError can be created."""
    error = SyntaxValidationError("Invalid syntax", "action parameter")
    assert error.message == "Invalid syntax"
    assert error.context == "action parameter"
    assert isinstance(error, ValidationError)


def test_precondition_validation_error_creation() -> None:
    """Test that PreconditionValidationError can be created."""
    error = PreconditionValidationError(
        "Precondition not met", "insufficient resources"
    )
    assert error.message == "Precondition not met"
    assert error.context == "insufficient resources"
    assert isinstance(error, ValidationError)


def test_rule_validation_error_creation() -> None:
    """Test that RuleValidationError can be created."""
    error = RuleValidationError("Rule violation", "game rule 42")
    assert error.message == "Rule violation"
    assert error.context == "game rule 42"
    assert isinstance(error, ValidationError)


def test_validation_engine_multi_layer_validation() -> None:
    """Test that ValidationEngine performs multi-layer validation."""
    engine = ValidationEngine()

    # Mock action that should fail validation
    class MockAction(Action):
        def __init__(self) -> None:
            super().__init__()

        def is_legal(self, state: Any, player_id: Any) -> bool:
            return True

        def execute(self, state: Any, player_id: Any) -> Any:
            return state

        def get_description(self) -> str:
            return "Mock action"

    action = MockAction()

    # Test with invalid parameters - should raise ValidationError
    with pytest.raises(ValidationError):
        engine.validate(action=action, state=None, player_id="invalid")

    # Test with missing state - should raise ValidationError
    with pytest.raises(ValidationError):
        engine.validate(action=action, state=None, player_id="player1")

    # Test with missing action - should raise ValidationError
    with pytest.raises(ValidationError):
        engine.validate(action=None, state={}, player_id="player1")


def test_validation_engine_precondition_validation() -> None:
    """Test that ValidationEngine validates preconditions."""
    engine = ValidationEngine()

    # Mock action with preconditions
    class MockActionWithPreconditions(Action):
        def __init__(self) -> None:
            super().__init__()

        def is_legal(self, state: Any, player_id: Any) -> bool:
            return True

        def execute(self, state: Any, player_id: Any) -> Any:
            return state

        def get_description(self) -> str:
            return "Mock action with preconditions"

        def get_preconditions(self) -> list[str]:
            return ["has_resources", "is_active_player"]

    action = MockActionWithPreconditions()
    state = {
        "players": {
            "player1": {"resources": 0, "is_active": False}  # Fails preconditions
        }
    }

    # Should raise PreconditionValidationError
    with pytest.raises(PreconditionValidationError):
        engine.validate(action=action, state=state, player_id="player1")

    # Test with valid preconditions
    valid_state = {
        "players": {
            "player1": {"resources": 10, "is_active": True}  # Meets preconditions
        }
    }

    # Should not raise an exception
    result = engine.validate(action=action, state=valid_state, player_id="player1")
    assert result is not None


def test_validation_engine_rule_validation() -> None:
    """Test that ValidationEngine validates game rules."""
    engine = ValidationEngine()

    # Mock action that violates rules
    class MockActionWithRuleViolation(Action):
        def __init__(self) -> None:
            super().__init__()

        def is_legal(self, state: Any, player_id: Any) -> bool:
            return True

        def execute(self, state: Any, player_id: Any) -> Any:
            return state

        def get_description(self) -> str:
            return "Mock action with rule violations"

        def get_rule_violations(self, state: Any, player_id: str) -> list[str]:
            return ["invalid_phase", "insufficient_resources"]

    action = MockActionWithRuleViolation()
    state = {"current_phase": "strategy"}

    # Should raise RuleValidationError
    with pytest.raises(RuleValidationError):
        engine.validate(action=action, state=state, player_id="player1")

    # Mock action that follows rules
    class MockActionWithoutRuleViolation(Action):
        def __init__(self) -> None:
            super().__init__()

        def is_legal(self, state: Any, player_id: Any) -> bool:
            return True

        def execute(self, state: Any, player_id: Any) -> Any:
            return state

        def get_description(self) -> str:
            return "Mock action without rule violations"

        def get_rule_violations(self, state: Any, player_id: str) -> list[str]:
            return []

    valid_action = MockActionWithoutRuleViolation()

    # Should not raise an exception
    result = engine.validate(action=valid_action, state=state, player_id="player1")
    assert result is not None


def test_validation_engine_successful_validation() -> None:
    """Test that ValidationEngine allows valid actions."""
    engine = ValidationEngine()

    # Mock valid action
    class MockValidAction(Action):
        def __init__(self) -> None:
            super().__init__()

        def is_legal(self, state: Any, player_id: Any) -> bool:
            return True

        def execute(self, state: Any, player_id: Any) -> Any:
            return state

        def get_description(self) -> str:
            return "Mock valid action"

        def get_preconditions(self) -> list[str]:
            return ["has_resources"]

        def get_rule_violations(self, state: Any, player_id: str) -> list[str]:
            return []

    action = MockValidAction()
    state = {
        "players": {"player1": {"resources": 10, "is_active": True}},
        "current_phase": "action",
    }

    # Should validate successfully
    result = engine.validate(action=action, state=state, player_id="player1")
    assert result is not None
    assert result.is_valid is True
    assert len(result.errors) == 0


def test_validation_error_handling_and_reporting() -> None:
    """Test that ValidationEngine properly handles and reports errors."""
    engine = ValidationEngine()

    # Mock action that has multiple validation issues
    class MockProblematicAction(Action):
        def __init__(self) -> None:
            super().__init__()

        def is_legal(self, state: Any, player_id: Any) -> bool:
            return True

        def execute(self, state: Any, player_id: Any) -> Any:
            return state

        def get_description(self) -> str:
            return "Mock problematic action"

        def get_preconditions(self) -> list[str]:
            return ["has_resources", "is_active_player"]

        def get_rule_violations(self, state: Any, player_id: str) -> list[str]:
            return ["invalid_phase"]

    action = MockProblematicAction()
    state = {
        "players": {"player1": {"resources": 0}},  # Insufficient resources
        "current_phase": "strategy",  # Wrong phase
    }

    # Should collect multiple validation errors
    with pytest.raises(ValidationError) as exc_info:
        engine.validate(action=action, state=state, player_id="player1")

    # The exception should contain information about the validation failure
    assert "validation" in str(exc_info.value).lower()


def test_validation_engine_integration_with_action_framework() -> None:
    """Test that ValidationEngine integrates properly with the action framework."""
    engine = ValidationEngine()

    # Test with a more realistic action scenario
    class MockTacticalAction(Action):
        def __init__(self, system_id: str) -> None:
            super().__init__()
            self.system_id = system_id

        def is_legal(self, state: Any, player_id: Any) -> bool:
            """Check if this action is legal."""
            return state.get("current_phase") == "tactical"

        def execute(self, state: Any, player_id: Any) -> Any:
            # Simulate moving ships to a system
            return state

        def get_description(self) -> str:
            """Get description of this action."""
            return f"Tactical action on system {self.system_id}"

        def get_preconditions(self) -> list[str]:
            return ["has_ships_to_move", "system_is_adjacent"]

        def get_rule_violations(self, state: Any, player_id: str) -> list[str]:
            violations = []
            if state.get("current_phase") != "tactical":
                violations.append("Tactical actions only allowed in tactical phase")
            return violations

    # Test valid tactical action
    valid_action = MockTacticalAction("system_42")
    valid_state = {
        "current_phase": "tactical",
        "players": {
            "player1": {
                "ships": {"system_41": ["destroyer", "cruiser"]},
                "is_active": True,
            }
        },
        "map": {
            "system_41": {"adjacent_systems": ["system_42"]},
            "system_42": {"ships": {}},
        },
    }

    # Should validate successfully
    result = engine.validate(
        action=valid_action, state=valid_state, player_id="player1"
    )
    assert result is not None

    # Test invalid tactical action (wrong phase)
    invalid_state = valid_state.copy()
    invalid_state["current_phase"] = "strategy"

    with pytest.raises(RuleValidationError):
        engine.validate(action=valid_action, state=invalid_state, player_id="player1")
