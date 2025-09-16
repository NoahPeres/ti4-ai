"""Enhanced logging system for TI4 game framework."""

import json
import logging
from typing import Any, Optional

from .events import GameEvent
from .exceptions import TI4GameError


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured logging output."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with structured data."""
        # Start with basic message
        message = super().format(record)

        # Add structured data if present
        if hasattr(record, "structured_data"):
            structured_data = record.structured_data
            structured_json = json.dumps(structured_data, indent=2)
            message = f"{message}\nStructured Data: {structured_json}"

        return message


class GameLogger:
    """Enhanced logging with structured data for game events and operations."""

    def __init__(self, game_id: str):
        """Initialize GameLogger for specific game instance."""
        self.game_id = game_id
        self.logger = logging.getLogger(f"ti4.game.{game_id}")

        # Configure logger if not already configured
        if not self.logger.handlers:
            self._configure_logger()

    def _configure_logger(self) -> None:
        """Configure logger with structured formatter."""
        self.logger.setLevel(logging.INFO)

        # Create console handler with structured formatter
        handler = logging.StreamHandler()
        formatter = StructuredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Prevent propagation to avoid duplicate logs
        self.logger.propagate = False

    def _build_base_extra(self, **additional_fields: Any) -> dict[str, Any]:
        """Build base extra data for logging with game_id and additional fields."""
        extra = {"game_id": self.game_id}
        extra.update(additional_fields)
        return extra

    def log_command(
        self,
        command: Any,  # GameCommand - avoiding circular import
        result: str,
        context: Optional[dict[str, Any]] = None,
    ) -> None:
        """Log command execution with structured context."""

        message = f"Command executed: {command.__class__.__name__}"
        command_type = command.serialize().get(
            "type", command.__class__.__name__.lower()
        )
        context = context or {}

        # Build structured data
        structured_data = {
            "game_id": self.game_id,
            "command_type": command_type,
            "result": result,
            "context": context,
        }

        # Log with structured data as extra
        extra = self._build_base_extra(
            command_type=command_type,
            result=result,
            context=context,
            structured_data=structured_data,
        )
        self.logger.info(message, extra=extra)

    def log_event(self, event: GameEvent) -> None:
        """Log game events with structured data."""
        message = f"Game event: {event.event_type}"

        # Build structured data
        structured_data = {
            "game_id": self.game_id,
            "event_type": event.event_type,
            "event_data": event.data,
            "timestamp": event.timestamp,
        }

        # Log with structured data as extra
        extra = self._build_base_extra(
            event_type=event.event_type,
            event_data=event.data,
            structured_data=structured_data,
        )
        self.logger.info(message, extra=extra)

    def log_error(
        self, error: Exception, context: Optional[dict[str, Any]] = None
    ) -> None:
        """Log errors with full context information."""
        message = f"Game error occurred: {str(error)}"
        context = context or {}
        error_context = getattr(error, "context", {})

        # Build structured data
        structured_data = {
            "game_id": self.game_id,
            "error_type": error.__class__.__name__,
            "error_message": str(error),
            "additional_context": context,
        }

        # Add TI4GameError specific context if available
        if isinstance(error, TI4GameError):
            structured_data["error_context"] = error.context
            structured_data["error_timestamp"] = str(error.timestamp)

        # Log with structured data as extra
        extra = self._build_base_extra(
            error_type=error.__class__.__name__,
            error_message=str(error),
            error_context=error_context,
            additional_context=context,
            structured_data=structured_data,
        )
        self.logger.error(message, extra=extra)
