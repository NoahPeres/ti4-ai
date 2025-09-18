"""Tests for GameLogger structured logging system."""

import logging
from typing import Any
from unittest.mock import patch

from src.ti4.commands.base import GameCommand
from src.ti4.core.events import GameEvent
from src.ti4.core.game_state import GameState


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
        return {"type": "mock", "data": "test"}

    def _publish_events(self, event_bus: Any, game_state: GameState) -> None:
        pass


class TestGameLogger:
    """Test GameLogger structured logging functionality."""

    def test_game_logger_creation(self) -> None:
        """Test GameLogger creation with game ID."""
        # RED: This will fail because GameLogger doesn't exist yet
        from src.ti4.core.logging import GameLogger

        game_id = "test_game_123"
        logger = GameLogger(game_id)

        assert logger.game_id == game_id
        assert logger.logger.name == f"ti4.game.{game_id}"

    def test_command_logging_with_context(self) -> None:
        """Test logging command execution with structured context."""
        # RED: This will fail because GameLogger doesn't exist yet
        from src.ti4.core.logging import GameLogger

        game_id = "test_game_123"
        logger = GameLogger(game_id)
        command = MockCommand()
        context = {"player_id": "player_1", "turn": 5}

        # Capture log output
        with patch("logging.Logger.info") as mock_info:
            logger.log_command(command, "success", context)

            # Verify structured logging call
            mock_info.assert_called_once()
            call_args = mock_info.call_args[0]
            assert "Command executed" in call_args[0]

            # Verify extra data contains structured information
            extra_data = mock_info.call_args[1]["extra"]
            assert extra_data["game_id"] == game_id
            assert extra_data["command_type"] == "mock"
            assert extra_data["result"] == "success"
            assert extra_data["context"] == context

    def test_event_logging(self) -> None:
        """Test logging game events with structured data."""
        # RED: This will fail because GameLogger doesn't exist yet
        from src.ti4.core.logging import GameLogger

        game_id = "test_game_123"
        logger = GameLogger(game_id)

        event = GameEvent(
            event_type="unit_moved",
            game_id=game_id,
            data={"unit_id": "dreadnought_1", "from": "system_a", "to": "system_b"},
        )

        # Capture log output
        with patch("logging.Logger.info") as mock_info:
            logger.log_event(event)

            # Verify structured logging call
            mock_info.assert_called_once()
            call_args = mock_info.call_args[0]
            assert "Game event" in call_args[0]

            # Verify extra data contains event information
            extra_data = mock_info.call_args[1]["extra"]
            assert extra_data["game_id"] == game_id
            assert extra_data["event_type"] == "unit_moved"
            assert extra_data["event_data"] == event.data

    def test_error_logging_with_context(self) -> None:
        """Test logging errors with full context information."""
        # RED: This will fail because GameLogger doesn't exist yet
        from src.ti4.core.exceptions import TI4GameError
        from src.ti4.core.logging import GameLogger

        game_id = "test_game_123"
        logger = GameLogger(game_id)

        error = TI4GameError("Test error", context={"operation": "unit_movement"})
        context = {"player_id": "player_1", "system_id": "mecatol_rex"}

        # Capture log output
        with patch("logging.Logger.error") as mock_error:
            logger.log_error(error, context)

            # Verify structured logging call
            mock_error.assert_called_once()
            call_args = mock_error.call_args[0]
            assert "Game error occurred" in call_args[0]

            # Verify extra data contains error information
            extra_data = mock_error.call_args[1]["extra"]
            assert extra_data["game_id"] == game_id
            assert extra_data["error_type"] == "TI4GameError"
            assert extra_data["error_message"] == "Test error"
            assert extra_data["error_context"] == error.context
            assert extra_data["additional_context"] == context

    def test_logger_configuration(self) -> None:
        """Test that logger is properly configured for structured output."""
        # RED: This will fail because GameLogger doesn't exist yet
        from src.ti4.core.logging import GameLogger

        game_id = "test_game_123"
        logger = GameLogger(game_id)

        # Verify logger configuration
        assert logger.logger.level == logging.INFO
        assert len(logger.logger.handlers) > 0

        # Verify formatter is configured for structured output
        handler = logger.logger.handlers[0]
        assert hasattr(handler, "formatter")
        assert handler.formatter is not None
