"""Error handling enhancements for status phase step handlers.

This module contains enhanced error handling implementations for all
status phase step handlers to support comprehensive error recovery,
graceful degradation, and state validation.

LRR References:
- Rule 81: Status Phase - Error handling requirements
- Requirements 11.1, 11.2, 11.3, 11.4, 11.5: Error handling specifications
"""

from typing import TYPE_CHECKING, Any

from .status_phase import (
    StepResult,
)

if TYPE_CHECKING:
    pass


def add_comprehensive_error_handling_to_step_handlers() -> None:
    """Add comprehensive error handling to all status phase step handlers.

    This function is now a no-op since error handling is built into the base classes.
    Kept for backward compatibility.
    """
    # No-op: Error handling is now built into the step handler base classes
    pass


def create_enhanced_step_result(
    success: bool, step_name: str, error_message: str = ""
) -> StepResult:
    """Create a step result with enhanced error information.

    Args:
        success: Whether the step succeeded
        step_name: The name of the step
        error_message: Optional error message for failures

    Returns:
        A StepResult with appropriate error information
    """
    return StepResult(success=success, step_name=step_name, error_message=error_message)


def validate_game_state(game_state: Any) -> bool:
    """Validate that the provided object is a valid game state.

    Args:
        game_state: The object to validate

    Returns:
        True if the object appears to be a valid game state, False otherwise
    """
    if game_state is None:
        return False

    # Check for basic required attributes
    if not hasattr(game_state, "players"):
        return False

    # Accept either known fields or cloning capability
    if not (hasattr(game_state, "phase") or hasattr(game_state, "_create_new_state")):
        return False

    return True


def create_error_result(step_name: str, error_message: str) -> StepResult:
    """Create a standardized error result.

    Args:
        step_name: The name of the step that failed
        error_message: The error message to include

    Returns:
        A StepResult indicating failure with the provided error message
    """
    return StepResult(success=False, step_name=step_name, error_message=error_message)
