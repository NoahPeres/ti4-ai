"""Shared validation utilities to eliminate code duplication."""

from collections.abc import Collection
from typing import Any, Callable, Optional, TypeVar, Union

T = TypeVar("T")


class ValidationError(ValueError):
    """Base class for validation errors with enhanced context."""

    def __init__(
        self, message: str, field_name: Optional[str] = None, value: Any = None
    ) -> None:
        super().__init__(message)
        self.field_name = field_name
        self.value = value


def validate_required(value: Any, field_name: str) -> None:
    """Validate that a value is not None or empty.

    Args:
        value: The value to validate
        field_name: Name of the field for error messages

    Raises:
        ValidationError: If value is None or empty
    """
    if value is None:
        raise ValidationError(
            f"{field_name} is required and cannot be None", field_name, value
        )

    # Check if value has length attribute and is empty
    if hasattr(value, "__len__") and len(value) == 0:
        raise ValidationError(
            f"{field_name} is required and cannot be empty", field_name, value
        )


def validate_non_empty_string(value: str, field_name: str) -> None:
    """Validate that a string is not None, empty, or whitespace-only.

    Args:
        value: The string to validate
        field_name: Name of the field for error messages

    Raises:
        ValidationError: If string is None, empty, or whitespace-only
    """
    if not value:
        raise ValidationError(f"{field_name} cannot be empty", field_name, value)

    if not value.strip():
        raise ValidationError(
            f"{field_name} cannot be whitespace-only", field_name, value
        )


def validate_collection_not_empty(collection: Collection[Any], field_name: str) -> None:
    """Validate that a collection is not None or empty.

    Args:
        collection: The collection to validate
        field_name: Name of the field for error messages

    Raises:
        ValidationError: If collection is None or empty
    """
    if collection is None:
        raise ValidationError(f"{field_name} cannot be None", field_name, collection)

    if len(collection) == 0:
        raise ValidationError(f"{field_name} cannot be empty", field_name, collection)


def validate_positive_number(value: Union[int, float], field_name: str) -> None:
    """Validate that a number is positive.

    Args:
        value: The number to validate
        field_name: Name of the field for error messages

    Raises:
        ValidationError: If number is not positive
    """
    if value is None:
        raise ValidationError(f"{field_name} cannot be None", field_name, value)

    if value <= 0:
        raise ValidationError(f"{field_name} must be positive", field_name, value)


def validate_callable(value: Any, field_name: str) -> None:
    """Validate that a value is callable.

    Args:
        value: The value to validate
        field_name: Name of the field for error messages

    Raises:
        ValidationError: If value is not callable
    """
    if not callable(value):
        raise ValidationError(f"{field_name} must be callable", field_name, value)


def validate_unique_collection(
    collection: Optional[Collection[Any]],
    field_name: str,
    key: Optional[Callable[[Any], Any]] = None,
) -> None:
    """Validate that all items in a collection are unique.

    Args:
        collection: The collection to validate
        field_name: Name of the field for error messages
        key: Optional function to extract key for uniqueness check

    Raises:
        ValidationError: If collection contains duplicates
    """
    if collection is None:
        raise ValidationError(f"{field_name} cannot be None", field_name, collection)

    seen: set[Any] = set()
    for item in collection:
        key_value = key(item) if key else item
        if key_value in seen:
            raise ValidationError(
                f"Duplicate item in {field_name}: {key_value} - collection must be unique",
                field_name,
                key_value,
            )
        seen.add(key_value)


def validate_minimum_count(
    collection: Optional[Collection[Any]], min_count: int, field_name: str
) -> None:
    """Validate that a collection has at least the minimum number of items.

    Args:
        collection: The collection to validate
        min_count: Minimum required count
        field_name: Name of the field for error messages

    Raises:
        ValidationError: If collection has fewer than min_count items
    """
    if collection is None:
        actual_count = 0
    else:
        actual_count = len(collection)

    if actual_count < min_count:
        raise ValidationError(
            f"{field_name} must have at least {min_count} items (minimum count), got {actual_count}",
            field_name,
            actual_count,
        )


def validate_maximum_count(
    collection: Optional[Collection[Any]], max_count: int, field_name: str
) -> None:
    """Validate that a collection has at most the maximum number of items.

    Args:
        collection: The collection to validate
        max_count: Maximum allowed count
        field_name: Name of the field for error messages

    Raises:
        ValidationError: If collection has more than max_count items
    """
    if collection is None:
        raise ValidationError(f"{field_name} cannot be None", field_name, collection)

    actual_count = len(collection)
    if actual_count > max_count:
        raise ValidationError(
            f"{field_name} must have at most {max_count} items (maximum count), got {actual_count}",
            field_name,
            actual_count,
        )


def validate_in_range(
    value: Union[int, float],
    min_val: Union[int, float],
    max_val: Union[int, float],
    field_name: str,
) -> None:
    """Validate that a number is within a specified range.

    Args:
        value: The number to validate
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)
        field_name: Name of the field for error messages

    Raises:
        ValidationError: If value is outside the range
    """
    if value is None:
        raise ValidationError(f"{field_name} cannot be None", field_name, value)

    if value < min_val or value > max_val:
        raise ValidationError(
            f"{field_name} must be in range between {min_val} and {max_val}, got {value}",
            field_name,
            value,
        )
