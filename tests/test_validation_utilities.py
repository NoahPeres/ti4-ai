"""Tests for shared validation utilities."""

import pytest

from src.ti4.core.validation import (
    ValidationError,
    validate_callable,
    validate_collection_not_empty,
    validate_in_range,
    validate_maximum_count,
    validate_minimum_count,
    validate_non_empty_string,
    validate_positive_number,
    validate_required,
    validate_unique_collection,
)


class TestValidationError:
    """Test ValidationError class."""

    def test_validation_error_creation(self):
        """Test ValidationError can be created with context."""
        error = ValidationError("Test message", "test_field", "test_value")
        assert str(error) == "Test message"
        assert error.field_name == "test_field"
        assert error.value == "test_value"

    def test_validation_error_without_context(self):
        """Test ValidationError can be created without context."""
        error = ValidationError("Test message")
        assert str(error) == "Test message"
        assert error.field_name is None
        assert error.value is None


class TestValidateRequired:
    """Test validate_required function."""

    def test_validate_required_with_valid_value(self):
        """Test validate_required passes with valid values."""
        validate_required("test", "field")
        validate_required(123, "field")
        validate_required([1, 2, 3], "field")
        validate_required({"key": "value"}, "field")

    def test_validate_required_with_none(self):
        """Test validate_required raises error for None."""
        with pytest.raises(ValidationError) as exc_info:
            validate_required(None, "test_field")

        assert "test_field cannot be None" in str(exc_info.value)
        assert exc_info.value.field_name == "test_field"

    def test_validate_required_with_empty_collection(self):
        """Test validate_required raises error for empty collections."""
        with pytest.raises(ValidationError) as exc_info:
            validate_required([], "test_field")

        assert "test_field cannot be empty" in str(exc_info.value)

        with pytest.raises(ValidationError):
            validate_required({}, "test_field")

        with pytest.raises(ValidationError):
            validate_required("", "test_field")


class TestValidateNonEmptyString:
    """Test validate_non_empty_string function."""

    def test_validate_non_empty_string_with_valid_string(self):
        """Test validate_non_empty_string passes with valid strings."""
        validate_non_empty_string("test", "field")
        validate_non_empty_string("  test  ", "field")

    def test_validate_non_empty_string_with_empty_string(self):
        """Test validate_non_empty_string raises error for empty string."""
        with pytest.raises(ValidationError) as exc_info:
            validate_non_empty_string("", "test_field")

        assert "test_field cannot be empty" in str(exc_info.value)

    def test_validate_non_empty_string_with_none(self):
        """Test validate_non_empty_string raises error for None."""
        with pytest.raises(ValidationError):
            validate_non_empty_string(None, "test_field")

    def test_validate_non_empty_string_with_whitespace_only(self):
        """Test validate_non_empty_string raises error for whitespace-only string."""
        with pytest.raises(ValidationError) as exc_info:
            validate_non_empty_string("   ", "test_field")

        assert "test_field cannot be whitespace-only" in str(exc_info.value)


class TestValidateCollectionNotEmpty:
    """Test validate_collection_not_empty function."""

    def test_validate_collection_not_empty_with_valid_collections(self):
        """Test validate_collection_not_empty passes with non-empty collections."""
        validate_collection_not_empty([1, 2, 3], "field")
        validate_collection_not_empty({"key": "value"}, "field")
        validate_collection_not_empty("test", "field")

    def test_validate_collection_not_empty_with_empty_collection(self):
        """Test validate_collection_not_empty raises error for empty collections."""
        with pytest.raises(ValidationError) as exc_info:
            validate_collection_not_empty([], "test_field")

        assert "test_field cannot be empty" in str(exc_info.value)

    def test_validate_collection_not_empty_with_none(self):
        """Test validate_collection_not_empty raises error for None."""
        with pytest.raises(ValidationError) as exc_info:
            validate_collection_not_empty(None, "test_field")

        assert "test_field cannot be None" in str(exc_info.value)


class TestValidatePositiveNumber:
    """Test validate_positive_number function."""

    def test_validate_positive_number_with_valid_numbers(self):
        """Test validate_positive_number passes with positive numbers."""
        validate_positive_number(1, "field")
        validate_positive_number(1.5, "field")
        validate_positive_number(100, "field")

    def test_validate_positive_number_with_zero(self):
        """Test validate_positive_number raises error for zero."""
        with pytest.raises(ValidationError) as exc_info:
            validate_positive_number(0, "test_field")

        assert "test_field must be positive" in str(exc_info.value)

    def test_validate_positive_number_with_negative(self):
        """Test validate_positive_number raises error for negative numbers."""
        with pytest.raises(ValidationError):
            validate_positive_number(-1, "test_field")

    def test_validate_positive_number_with_none(self):
        """Test validate_positive_number raises error for None."""
        with pytest.raises(ValidationError):
            validate_positive_number(None, "test_field")


class TestValidateCallable:
    """Test validate_callable function."""

    def test_validate_callable_with_valid_callables(self):
        """Test validate_callable passes with callable objects."""
        validate_callable(lambda x: x, "field")
        validate_callable(print, "field")
        validate_callable(str, "field")

    def test_validate_callable_with_non_callable(self):
        """Test validate_callable raises error for non-callable objects."""
        with pytest.raises(ValidationError) as exc_info:
            validate_callable("not callable", "test_field")

        assert "test_field must be callable" in str(exc_info.value)


class TestValidateUniqueCollection:
    """Test validate_unique_collection function."""

    def test_validate_unique_collection_with_unique_items(self):
        """Test validate_unique_collection passes with unique items."""
        validate_unique_collection([1, 2, 3], "field")
        validate_unique_collection(["a", "b", "c"], "field")

    def test_validate_unique_collection_with_duplicates(self):
        """Test validate_unique_collection raises error for duplicates."""
        with pytest.raises(ValidationError) as exc_info:
            validate_unique_collection([1, 2, 2, 3], "test_field")

        assert "Duplicate item in test_field: 2" in str(exc_info.value)

    def test_validate_unique_collection_with_key_function(self):
        """Test validate_unique_collection with custom key function."""
        items = [{"id": 1}, {"id": 2}, {"id": 3}]
        validate_unique_collection(items, "field", key_func=lambda x: x["id"])

        # Test with duplicates
        items_with_duplicates = [{"id": 1}, {"id": 2}, {"id": 1}]
        with pytest.raises(ValidationError):
            validate_unique_collection(
                items_with_duplicates, "field", key_func=lambda x: x["id"]
            )

    def test_validate_unique_collection_with_none(self):
        """Test validate_unique_collection handles None gracefully."""
        validate_unique_collection(None, "field")  # Should not raise


class TestValidateMinimumCount:
    """Test validate_minimum_count function."""

    def test_validate_minimum_count_with_sufficient_items(self):
        """Test validate_minimum_count passes with sufficient items."""
        validate_minimum_count([1, 2, 3], 2, "field")
        validate_minimum_count([1, 2, 3], 3, "field")

    def test_validate_minimum_count_with_insufficient_items(self):
        """Test validate_minimum_count raises error for insufficient items."""
        with pytest.raises(ValidationError) as exc_info:
            validate_minimum_count([1], 2, "test_field")

        assert "test_field must have at least 2 items, got 1" in str(exc_info.value)

    def test_validate_minimum_count_with_none(self):
        """Test validate_minimum_count handles None as empty collection."""
        with pytest.raises(ValidationError):
            validate_minimum_count(None, 1, "test_field")


class TestValidateMaximumCount:
    """Test validate_maximum_count function."""

    def test_validate_maximum_count_with_acceptable_items(self):
        """Test validate_maximum_count passes with acceptable item count."""
        validate_maximum_count([1, 2], 3, "field")
        validate_maximum_count([1, 2, 3], 3, "field")

    def test_validate_maximum_count_with_too_many_items(self):
        """Test validate_maximum_count raises error for too many items."""
        with pytest.raises(ValidationError) as exc_info:
            validate_maximum_count([1, 2, 3, 4], 3, "test_field")

        assert "test_field must have at most 3 items, got 4" in str(exc_info.value)

    def test_validate_maximum_count_with_none(self):
        """Test validate_maximum_count handles None gracefully."""
        validate_maximum_count(None, 3, "field")  # Should not raise


class TestValidateInRange:
    """Test validate_in_range function."""

    def test_validate_in_range_with_valid_values(self):
        """Test validate_in_range passes with values in range."""
        validate_in_range(5, 1, 10, "field")
        validate_in_range(1, 1, 10, "field")  # Min boundary
        validate_in_range(10, 1, 10, "field")  # Max boundary

    def test_validate_in_range_with_value_below_range(self):
        """Test validate_in_range raises error for value below range."""
        with pytest.raises(ValidationError) as exc_info:
            validate_in_range(0, 1, 10, "test_field")

        assert "test_field must be between 1 and 10, got 0" in str(exc_info.value)

    def test_validate_in_range_with_value_above_range(self):
        """Test validate_in_range raises error for value above range."""
        with pytest.raises(ValidationError):
            validate_in_range(11, 1, 10, "test_field")

    def test_validate_in_range_with_none(self):
        """Test validate_in_range raises error for None."""
        with pytest.raises(ValidationError):
            validate_in_range(None, 1, 10, "test_field")
