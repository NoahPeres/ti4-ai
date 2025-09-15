"""Tests for ValidationEngine class."""

import pytest

from src.ti4.actions.validation import (
    PreconditionValidationError,
    RuleValidationError,
    SyntaxValidationError,
    ValidationEngine,
    ValidationError,
)


def test_validation_engine_creation():
    """Test that ValidationEngine can be created."""
    engine = ValidationEngine()
    assert engine is not None


def test_validation_engine_has_validate_method():
    """Test that ValidationEngine has a validate method."""
    engine = ValidationEngine()

    # Should have a validate method that takes action, state, and player_id
    result = engine.validate(action=None, state=None, player_id=None)
    assert result is not None


def test_validation_error_creation():
    """Test that ValidationError can be created with message and context."""
    error = ValidationError("Test error message", "test context")
    assert error.message == "Test error message"
    assert error.context == "test context"


def test_syntax_validation_error_creation():
    """Test that SyntaxValidationError can be created."""
    error = SyntaxValidationError("Invalid syntax", "action parameter")
    assert error.message == "Invalid syntax"
    assert error.context == "action parameter"
    assert isinstance(error, ValidationError)


def test_precondition_validation_error_creation():
    """Test that PreconditionValidationError can be created."""
    error = PreconditionValidationError(
        "Precondition not met", "insufficient resources"
    )
    assert error.message == "Precondition not met"
    assert error.context == "insufficient resources"
    assert isinstance(error, ValidationError)


def test_rule_validation_error_creation():
    """Test that RuleValidationError can be created."""
    error = RuleValidationError("Rule violation", "cannot move through enemy fleet")
    assert error.message == "Rule violation"
    assert error.context == "cannot move through enemy fleet"
    assert isinstance(error, ValidationError)


def test_validation_engine_multi_layer_validation():
    """Test that ValidationEngine performs multi-layered validation."""
    engine = ValidationEngine()

    # Create a mock action that should fail syntax validation
    class MockAction:
        def __init__(self, valid_syntax=True):
            self.valid_syntax = valid_syntax

    action = MockAction(valid_syntax=False)

    # Should raise SyntaxValidationError for invalid syntax
    with pytest.raises(SyntaxValidationError):
        engine.validate(action, state=None, player_id="player1")


def test_validation_engine_precondition_validation():
    """Test that ValidationEngine performs precondition validation."""
    engine = ValidationEngine()

    # Create a mock action that passes syntax but fails precondition
    class MockAction:
        def __init__(self, valid_syntax=True, preconditions_met=True):
            self.valid_syntax = valid_syntax
            self.preconditions_met = preconditions_met

    action = MockAction(valid_syntax=True, preconditions_met=False)

    # Should raise PreconditionValidationError
    with pytest.raises(PreconditionValidationError):
        engine.validate(action, state=None, player_id="player1")


def test_validation_engine_rule_validation():
    """Test that ValidationEngine performs rule validation."""
    engine = ValidationEngine()

    # Create a mock action that passes syntax and preconditions but fails rules
    class MockAction:
        def __init__(
            self, valid_syntax=True, preconditions_met=True, follows_rules=True
        ):
            self.valid_syntax = valid_syntax
            self.preconditions_met = preconditions_met
            self.follows_rules = follows_rules

    action = MockAction(valid_syntax=True, preconditions_met=True, follows_rules=False)

    # Should raise RuleValidationError
    with pytest.raises(RuleValidationError):
        engine.validate(action, state=None, player_id="player1")


def test_validation_engine_successful_validation():
    """Test that ValidationEngine returns True when all validation layers pass."""
    engine = ValidationEngine()

    # Create a mock action that passes all validation layers
    class MockAction:
        def __init__(
            self, valid_syntax=True, preconditions_met=True, follows_rules=True
        ):
            self.valid_syntax = valid_syntax
            self.preconditions_met = preconditions_met
            self.follows_rules = follows_rules

    action = MockAction(valid_syntax=True, preconditions_met=True, follows_rules=True)

    # Should return True when all validations pass
    result = engine.validate(action, state=None, player_id="player1")
    assert result is True


def test_validation_error_handling_and_reporting():
    """Test that validation errors contain detailed messages and context."""
    engine = ValidationEngine()

    # Test syntax validation error reporting
    class MockAction:
        def __init__(self, valid_syntax=False):
            self.valid_syntax = valid_syntax

    action = MockAction(valid_syntax=False)

    try:
        engine.validate(action, state=None, player_id="player1")
        assert False, "Should have raised SyntaxValidationError"
    except SyntaxValidationError as e:
        assert e.message == "Invalid action syntax"
        assert e.context == "action parameters"
        assert str(e) == "Invalid action syntax"


def test_validation_engine_integration_with_action_framework():
    """Test that ValidationEngine integrates with the existing Action framework."""
    from src.ti4.actions.action import Action

    engine = ValidationEngine()

    # Create a concrete action that implements the Action interface
    class TestAction(Action):
        def __init__(
            self, valid_syntax=True, preconditions_met=True, follows_rules=True
        ):
            self.valid_syntax = valid_syntax
            self.preconditions_met = preconditions_met
            self.follows_rules = follows_rules

        def is_legal(self, state, player_id) -> bool:
            # Use the validation engine to determine legality
            try:
                engine.validate(self, state, player_id)
                return True
            except ValidationError:
                return False

        def execute(self, state, player_id):
            return state

        def get_description(self) -> str:
            return "test action"

    # Test valid action
    valid_action = TestAction(
        valid_syntax=True, preconditions_met=True, follows_rules=True
    )
    assert valid_action.is_legal(None, "player1") is True

    # Test invalid action (syntax error)
    invalid_action = TestAction(valid_syntax=False)
    assert invalid_action.is_legal(None, "player1") is False
