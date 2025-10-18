"""Runtime type checking utilities for the TI4 framework.

This module provides decorators and utilities for runtime type validation
to complement static type checking with mypy.
"""

from collections.abc import Callable
from typing import Any, TypeVar

try:
    from beartype import beartype

    BEARTYPE_AVAILABLE = True
except ImportError:
    BEARTYPE_AVAILABLE = False

try:
    from typeguard import typechecked

    TYPEGUARD_AVAILABLE = True
except ImportError:
    TYPEGUARD_AVAILABLE = False


F = TypeVar("F", bound=Callable[..., Any])


def runtime_type_check(func: F) -> F:
    """Decorator to enable runtime type checking for a function.

    Uses beartype if available, falls back to typeguard, or provides
    a no-op decorator if neither is available.

    Args:
        func: The function to add runtime type checking to

    Returns:
        The decorated function with runtime type checking
    """
    if BEARTYPE_AVAILABLE:
        # Use beartype for comprehensive runtime type checking
        return beartype(func)
    elif TYPEGUARD_AVAILABLE:
        # Use typeguard as fallback
        return typechecked(func)
    else:
        # Simple fallback that just returns the original function
        # This avoids complex wrapper typing issues
        return func


def strict_type_check(func: F) -> F:
    """Strict runtime type checking that always validates types.

    This decorator provides more comprehensive type checking than the
    basic fallback, but may have performance implications.
    """
    if not BEARTYPE_AVAILABLE and not TYPEGUARD_AVAILABLE:
        raise RuntimeError(
            "Strict type checking requires beartype or typeguard. "
            "Install with: pip install beartype"
        )

    return runtime_type_check(func)


# Convenience decorators for different use cases
def validate_game_state(func: F) -> F:
    """Decorator specifically for functions that work with GameState objects."""
    return runtime_type_check(func)


def validate_player_actions(func: F) -> F:
    """Decorator for functions that handle player actions."""
    return runtime_type_check(func)


def validate_galaxy_operations(func: F) -> F:
    """Decorator for functions that perform galaxy/system operations."""
    return runtime_type_check(func)


def basic_type_validation(value: Any, expected_type: type, param_name: str) -> None:
    """Basic type validation utility function.

    Args:
        value: The value to validate
        expected_type: The expected type
        param_name: Name of the parameter for error messages

    Raises:
        TypeError: If the value doesn't match the expected type
    """
    if not isinstance(value, expected_type):
        raise TypeError(
            f"Parameter '{param_name}' expected {expected_type.__name__}, "
            f"got {type(value).__name__}"
        )
