"""Command manager for handling command execution and history."""

from typing import Any, Optional

from ..core.game_state import GameState
from .base import GameCommand


class CommandManager:
    """Manages command execution, undo, and replay functionality."""

    def __init__(self) -> None:
        self._command_history: list[GameCommand] = []
        self._undo_stack: list[dict[str, Any]] = []

    def execute_command(self, command: GameCommand, game_state: GameState) -> GameState:
        """Execute command and store for potential undo."""
        if not command.can_execute(game_state):
            from ..core.validation import ValidationError

            raise ValidationError(
                "Command cannot be executed in current state", "command", command
            )

        # Store undo data before execution
        undo_data = command.get_undo_data()
        self._undo_stack.append(undo_data)

        # Execute command
        new_state = command.execute(game_state)

        # Store command in history
        self._command_history.append(command)

        return new_state

    def undo_last_command(self, game_state: GameState) -> GameState:
        """Undo the most recent command."""
        if not self._command_history:
            raise ValueError("No commands to undo")

        last_command = self._command_history.pop()
        self._undo_stack.pop()  # Remove corresponding undo data

        return last_command.undo(game_state)

    def get_command_history(self) -> list[GameCommand]:
        """Get the command history."""
        return self._command_history.copy()

    def replay_from_initial_state(self, initial_state: GameState) -> GameState:
        """Replay all commands from the initial state."""
        current_state = initial_state

        # Re-execute all commands in order
        for command in self._command_history:
            if command.can_execute(current_state):
                current_state = command.execute(current_state)

        return current_state

    def serialize_commands(self) -> list[dict[str, Any]]:
        """Serialize all commands for persistence."""
        return [command.serialize() for command in self._command_history]
