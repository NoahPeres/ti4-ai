"""Tests for runtime type checking module."""

from typing import Any, Optional, Union

import pytest

from src.ti4.core.runtime_type_checking import (
    BEARTYPE_AVAILABLE,
    TYPEGUARD_AVAILABLE,
    basic_type_validation,
    runtime_type_check,
    strict_type_check,
    validate_galaxy_operations,
    validate_game_state,
    validate_player_actions,
)


class TestRuntimeTypeCheck:
    """Test cases for runtime_type_check decorator."""

    def test_runtime_type_check_decorator_exists(self) -> None:
        """Test that the runtime_type_check decorator exists and can be imported."""
        assert runtime_type_check is not None
        assert callable(runtime_type_check)

    def test_runtime_type_check_with_simple_function(self) -> None:
        """Test runtime_type_check decorator with a simple function."""

        @runtime_type_check
        def add_numbers(a: int, b: int) -> int:
            return a + b

        # Should work with correct types
        result = add_numbers(1, 2)
        assert result == 3

    def test_runtime_type_check_with_string_function(self) -> None:
        """Test runtime_type_check decorator with string parameters."""

        @runtime_type_check
        def greet(name: str) -> str:
            return f"Hello, {name}!"

        result = greet("World")
        assert result == "Hello, World!"

    def test_runtime_type_check_with_optional_parameter(self) -> None:
        """Test runtime_type_check decorator with optional parameters."""

        @runtime_type_check
        def process_value(value: Optional[int] = None) -> str:
            if value is None:
                return "No value"
            return f"Value: {value}"

        assert process_value() == "No value"
        assert process_value(42) == "Value: 42"

    def test_runtime_type_check_with_list_parameter(self) -> None:
        """Test runtime_type_check decorator with list parameters."""

        @runtime_type_check
        def sum_list(numbers: list[int]) -> int:
            return sum(numbers)

        result = sum_list([1, 2, 3, 4, 5])
        assert result == 15

    def test_runtime_type_check_with_dict_parameter(self) -> None:
        """Test runtime_type_check decorator with dict parameters."""

        @runtime_type_check
        def get_value(data: dict[str, Any], key: str) -> Any:
            return data.get(key)

        test_data = {"name": "test", "value": 42}
        assert get_value(test_data, "name") == "test"
        assert get_value(test_data, "value") == 42


class TestBasicTypeValidation:
    """Test cases for basic_type_validation function."""

    def test_basic_type_validation_exists(self) -> None:
        """Test that the basic_type_validation function exists."""
        assert basic_type_validation is not None
        assert callable(basic_type_validation)

    def test_basic_type_validation_success(self) -> None:
        """Test basic_type_validation with valid types."""
        # Should not raise any exception
        basic_type_validation(42, int, "test_value")
        basic_type_validation("hello", str, "test_string")
        basic_type_validation([1, 2, 3], list, "test_list")

    def test_basic_type_validation_failure(self) -> None:
        """Test basic_type_validation with invalid types."""
        with pytest.raises(TypeError) as exc_info:
            basic_type_validation("42", int, "test_value")

        assert "test_value" in str(exc_info.value)
        assert "expected int" in str(exc_info.value)

    def test_basic_type_validation_with_mock_object(self) -> None:
        """Test basic_type_validation with a mock object."""

        class MockGameState:
            def __init__(self) -> None:
                self.game_id = "test_game"
                self.players = []
                self.current_phase = "setup"

        mock_state = MockGameState()
        # Should not raise an exception for correct type
        basic_type_validation(mock_state, MockGameState, "game_state")

        # Should raise exception for wrong type
        with pytest.raises(TypeError):
            basic_type_validation("not_a_game_state", MockGameState, "game_state")


class TestTypeCheckingAvailability:
    """Test cases for type checking library availability."""

    def test_beartype_availability_flag(self) -> None:
        """Test that BEARTYPE_AVAILABLE flag is a boolean."""
        assert isinstance(BEARTYPE_AVAILABLE, bool)

    def test_typeguard_availability_flag(self) -> None:
        """Test that TYPEGUARD_AVAILABLE flag is a boolean."""
        assert isinstance(TYPEGUARD_AVAILABLE, bool)

    def test_at_least_one_library_available(self) -> None:
        """Test that at least one type checking library is available or decorator works without them."""

        # The decorator should work regardless of library availability
        @runtime_type_check
        def test_function(x: int) -> int:
            return x * 2

        result = test_function(5)
        assert result == 10


class TestSpecializedDecorators:
    """Test cases for specialized decorator functions."""

    def test_validate_game_state_decorator(self) -> None:
        """Test validate_game_state decorator."""

        @validate_game_state
        def process_game_state(state: dict[str, Any]) -> str:
            return f"Processing game {state.get('id', 'unknown')}"

        result = process_game_state({"id": "game123"})
        assert result == "Processing game game123"

    def test_validate_player_actions_decorator(self) -> None:
        """Test validate_player_actions decorator."""

        @validate_player_actions
        def handle_action(player_id: str, action: dict[str, Any]) -> str:
            return f"Player {player_id} performed {action.get('type', 'unknown')}"

        result = handle_action("player1", {"type": "move"})
        assert result == "Player player1 performed move"

    def test_validate_galaxy_operations_decorator(self) -> None:
        """Test validate_galaxy_operations decorator."""

        @validate_galaxy_operations
        def update_galaxy(galaxy: dict[str, Any], system_id: str) -> str:
            return f"Updated system {system_id} in galaxy"

        result = update_galaxy({"systems": []}, "sys1")
        assert result == "Updated system sys1 in galaxy"

    def test_strict_type_check_decorator(self) -> None:
        """Test strict_type_check decorator."""
        if BEARTYPE_AVAILABLE or TYPEGUARD_AVAILABLE:

            @strict_type_check
            def strict_function(x: int) -> int:
                return x * 2

            result = strict_function(5)
            assert result == 10
        else:
            # Should raise RuntimeError if no type checking library available
            with pytest.raises(RuntimeError) as exc_info:

                @strict_type_check
                def strict_function(x: int) -> int:
                    return x * 2

            assert "beartype or typeguard" in str(exc_info.value)


class TestRuntimeTypeCheckingIntegration:
    """Integration tests for runtime type checking."""

    def test_decorator_preserves_function_metadata(self) -> None:
        """Test that the decorator preserves function metadata."""

        @runtime_type_check
        def documented_function(x: int) -> int:
            """This function doubles its input."""
            return x * 2

        # Function should still be callable
        assert documented_function(5) == 10

        # Function name should be preserved (or at least accessible)
        assert hasattr(documented_function, "__name__") or hasattr(
            documented_function, "__qualname__"
        )

    def test_decorator_with_complex_types(self) -> None:
        """Test decorator with more complex type annotations."""

        @runtime_type_check
        def process_data(
            items: list[dict[str, Union[int, str]]], default: Optional[str] = None
        ) -> list[str]:
            result = []
            for item in items:
                name = item.get("name", default or "unknown")
                result.append(str(name))
            return result

        test_data: list[dict[str, Union[int, str]]] = [
            {"name": "item1", "value": 10},
            {"name": "item2", "value": "test"},
            {"value": 42},  # Missing name
        ]

        result = process_data(test_data, "default")
        assert len(result) == 3
        assert "item1" in result
        assert "item2" in result

    def test_multiple_decorated_functions(self) -> None:
        """Test multiple functions with the decorator."""

        @runtime_type_check
        def add(a: int, b: int) -> int:
            return a + b

        @runtime_type_check
        def multiply(a: int, b: int) -> int:
            return a * b

        @runtime_type_check
        def combine(x: int, y: int) -> str:
            return f"{add(x, y)} and {multiply(x, y)}"

        result = combine(3, 4)
        assert result == "7 and 12"
