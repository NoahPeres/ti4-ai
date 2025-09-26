"""Tests for CommandExecutionError."""

from typing import Any

from ti4.commands.base import GameCommand
from ti4.core.game_state import GameState


class MockCommand(GameCommand):
    """Mock command for testing."""

    def execute(self, game_state: GameState) -> GameState:
        return game_state

    def undo(self, game_state: GameState) -> GameState:
        return game_state

    def can_execute(self, game_state: GameState) -> bool:
        return True

    def get_undo_data(self) -> dict[str, Any]:
        return {}

    def serialize(self) -> dict[str, Any]:
        return {"type": "mock"}

    def _publish_events(self, event_bus: Any, game_state: GameState) -> None:
        pass


class TestCommandExecutionError:
    """Test CommandExecutionError creation and functionality."""

    def test_command_execution_error_creation(self) -> None:
        """Test CommandExecutionError creation with command context."""
        # RED: This will fail because CommandExecutionError doesn't exist yet
        from ti4.core.exceptions import CommandExecutionError

        command = MockCommand()
        reason = "Invalid game state"
        context = {"state_id": "test_state"}

        error = CommandExecutionError(command, reason, context)

        assert str(error) == "Command execution failed: Invalid game state"
        assert error.command == command
        assert error.context == context
        assert hasattr(error, "timestamp")

    def test_command_execution_error_without_context(self) -> None:
        """Test CommandExecutionError creation without additional context."""
        # RED: This will fail because CommandExecutionError doesn't exist yet
        from ti4.core.exceptions import CommandExecutionError

        command = MockCommand()
        reason = "Command validation failed"

        error = CommandExecutionError(command, reason)

        assert str(error) == "Command execution failed: Command validation failed"
        assert error.command == command
        assert error.context == {}
        assert hasattr(error, "timestamp")
