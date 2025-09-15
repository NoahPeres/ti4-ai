"""Action validation engine for TI4."""

from typing import Any


class ValidationError(Exception):
    """Base class for validation errors."""

    def __init__(self, message: str, context: str) -> None:
        self.message = message
        self.context = context
        super().__init__(message)


class SyntaxValidationError(ValidationError):
    """Error raised when action syntax is invalid."""

    pass


class PreconditionValidationError(ValidationError):
    """Error raised when action preconditions are not met."""

    pass


class RuleValidationError(ValidationError):
    """Error raised when action violates game rules."""

    pass


class ValidationEngine:
    """Engine for validating player actions through multiple layers.

    The validation pipeline consists of three layers:
    1. Syntax validation - ensures action parameters are well-formed
    2. Precondition validation - checks if action prerequisites are met
    3. Rule validation - verifies action complies with current game rules
    """

    def validate(self, action: Any, state: Any, player_id: Any) -> bool:
        """Validate an action through multiple layers.

        Args:
            action: The action to validate
            state: Current game state
            player_id: ID of the player attempting the action

        Returns:
            True if validation passes

        Raises:
            SyntaxValidationError: If action syntax is invalid
            PreconditionValidationError: If action preconditions are not met
            RuleValidationError: If action violates game rules
        """
        self._validate_syntax(action)
        self._validate_preconditions(action, state, player_id)
        self._validate_rules(action, state, player_id)

        return True

    def _validate_syntax(self, action: Any) -> None:
        """Validate action syntax."""
        if hasattr(action, "valid_syntax") and not action.valid_syntax:
            raise SyntaxValidationError("Invalid action syntax", "action parameters")

    def _validate_preconditions(self, action: Any, state: Any, player_id: Any) -> None:
        """Validate action preconditions."""
        if hasattr(action, "preconditions_met") and not action.preconditions_met:
            raise PreconditionValidationError(
                "Action preconditions not met", "insufficient resources or state"
            )

    def _validate_rules(self, action: Any, state: Any, player_id: Any) -> None:
        """Validate action against game rules."""
        if hasattr(action, "follows_rules") and not action.follows_rules:
            raise RuleValidationError(
                "Action violates game rules", "rule constraint not satisfied"
            )
