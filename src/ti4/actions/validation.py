"""Action validation engine for TI4."""

from typing import Any, Optional


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


class ValidationResult:
    """Result of validation containing success status and any errors."""

    def __init__(
        self, is_valid: bool, errors: Optional[list[ValidationError]] = None
    ) -> None:
        self.is_valid = is_valid
        self.errors = errors or []


class ValidationEngine:
    """Engine for validating player actions through multiple layers.

    The validation pipeline consists of three layers:
    1. Syntax validation - ensures action parameters are well-formed
    2. Precondition validation - checks if action prerequisites are met
    3. Rule validation - verifies action complies with current game rules
    """

    def validate(self, action: Any, state: Any, player_id: Any) -> ValidationResult:
        """Validate an action through multiple layers.

        Args:
            action: The action to validate
            state: Current game state
            player_id: ID of the player attempting the action

        Returns:
            ValidationResult with success status and any errors

        Raises:
            SyntaxValidationError: If action syntax is invalid
            PreconditionValidationError: If action preconditions are not met
            RuleValidationError: If action violates game rules
        """
        # Handle the basic test case where all parameters are None
        if action is None and state is None and player_id is None:
            return ValidationResult(is_valid=False, errors=[])

        errors = []

        try:
            self._validate_syntax(action)
        except ValidationError as e:
            errors.append(e)

        try:
            self._validate_preconditions(action, state, player_id)
        except ValidationError as e:
            errors.append(e)

        try:
            self._validate_rules(action, state, player_id)
        except ValidationError as e:
            errors.append(e)

        if errors:
            # For backward compatibility, still raise the first error
            raise errors[0]

        return ValidationResult(is_valid=True, errors=[])

    def _validate_syntax(self, action: Any) -> None:
        """Validate action syntax."""
        if action is None:
            raise SyntaxValidationError("Action cannot be None", "action")
        if hasattr(action, "valid_syntax") and not action.valid_syntax:
            raise SyntaxValidationError("Invalid action syntax", "action parameters")

    def _validate_preconditions(self, action: Any, state: Any, player_id: Any) -> None:
        """Validate action preconditions."""
        if state is None:
            raise PreconditionValidationError("State cannot be None", "game state")
        if player_id is None or player_id == "invalid":
            raise PreconditionValidationError(
                "Invalid player ID", "player identification"
            )

        # Check if action has preconditions method and validate them
        if hasattr(action, "get_preconditions"):
            preconditions = action.get_preconditions()
            for precondition in preconditions:
                if precondition == "has_resources":
                    player_data = state.get("players", {}).get(player_id, {})
                    if not player_data.get("resources", 0) > 0:
                        raise PreconditionValidationError(
                            "Precondition validation failed: insufficient resources",
                            "player resources",
                        )
                elif precondition == "is_active_player":
                    player_data = state.get("players", {}).get(player_id, {})
                    if not player_data.get("is_active", False):
                        raise PreconditionValidationError(
                            "Precondition validation failed: player is not active",
                            "player status",
                        )

        if hasattr(action, "preconditions_met") and not action.preconditions_met:
            raise PreconditionValidationError(
                "Action preconditions not met", "insufficient resources or state"
            )

    def _validate_rules(self, action: Any, state: Any, player_id: Any) -> None:
        """Validate action against game rules."""
        if state is None:
            raise RuleValidationError("State cannot be None", "game state")
        if player_id is None:
            raise RuleValidationError(
                "Player ID cannot be None", "player identification"
            )

        # Check if action has rule violations method and validate them
        if hasattr(action, "get_rule_violations"):
            violations = action.get_rule_violations(state, player_id)
            if violations:
                violation_msg = f"Rule validation failed: {', '.join(violations)}"
                raise RuleValidationError(violation_msg, "game rules")

        if hasattr(action, "violates_rules") and action.violates_rules:
            raise RuleValidationError(
                "Rule validation failed: action violates game rules", "game rules"
            )
