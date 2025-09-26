"""Tests for enhanced exception hierarchy."""

import time

from ti4.core.exceptions import TI4GameError


class TestEnhancedExceptionHierarchy:
    """Test enhanced exception hierarchy with context information."""

    def test_ti4_game_error_has_context_and_timestamp(self) -> None:
        """Test that base TI4GameError includes context and timestamp."""
        # RED: This test will fail because TI4GameError doesn't have enhanced context yet
        context = {"player_id": "test_player", "action": "move_unit"}

        error = TI4GameError("Test error", context=context)

        assert error.context == context
        assert hasattr(error, "timestamp")
        assert isinstance(error.timestamp, float)
        assert error.timestamp <= time.time()

    def test_context_information_preservation(self) -> None:
        """Test that context information is properly preserved."""
        # RED: This will fail because context preservation isn't implemented yet
        context = {
            "game_id": "test_game_123",
            "player_id": "player_1",
            "system_id": "mecatol_rex",
            "unit_type": "dreadnought",
        }

        error = TI4GameError("Test error with rich context", context=context)

        assert error.context["game_id"] == "test_game_123"
        assert error.context["player_id"] == "player_1"
        assert error.context["system_id"] == "mecatol_rex"
        assert error.context["unit_type"] == "dreadnought"

    def test_empty_context_handling(self) -> None:
        """Test that exceptions handle empty or None context gracefully."""
        # RED: This will fail because enhanced context handling doesn't exist yet
        error1 = TI4GameError("Error with None context", context=None)
        error2 = TI4GameError("Error with empty context", context={})

        assert error1.context == {}
        assert error2.context == {}
        assert hasattr(error1, "timestamp")
        assert hasattr(error2, "timestamp")

    def test_exception_chaining_preserves_root_cause(self) -> None:
        """Test that exception chaining preserves root cause information."""
        # RED: This will fail because enhanced chaining doesn't exist yet
        root_cause = ValueError("Original error")
        context = {"operation": "unit_movement"}

        chained_error = TI4GameError(
            "Higher level error", context=context, cause=root_cause
        )

        assert chained_error.__cause__ == root_cause
        assert chained_error.context == context
