"""Event observer implementations for TI4 game framework."""

import logging
from abc import ABC, abstractmethod
from typing import Any

from .events import (
    CombatStartedEvent,
    GameEvent,
    GameEventBus,
    PhaseChangedEvent,
    UnitMovedEvent,
)

# Set up logger
logger = logging.getLogger(__name__)


class EventObserver(ABC):
    """Base class for event observers."""

    @abstractmethod
    def handle_event(
        self,
        event: GameEvent | UnitMovedEvent | CombatStartedEvent | PhaseChangedEvent,
    ) -> None:
        """Handle a game event."""
        pass

    def register_with_bus(self, event_bus: GameEventBus) -> None:
        """Register this observer with an event bus for all event types."""
        # For now, register for all known event types
        from .constants import EventConstants

        event_types = [
            EventConstants.UNIT_MOVED,
            EventConstants.COMBAT_STARTED,
            EventConstants.PHASE_CHANGED,
        ]
        for event_type in event_types:
            event_bus.subscribe(event_type, self.handle_event)

    def _extract_event_type_identifier(
        self,
        event: GameEvent | UnitMovedEvent | CombatStartedEvent | PhaseChangedEvent,
    ) -> str:
        """Extract the event type identifier from a game event object.

        This method provides a consistent way to get the event type identifier
        from any game event, falling back to the class name if no explicit
        event_type attribute is available.

        Args:
            event: The game event to extract the type from

        Returns:
            str: The event type identifier (e.g., 'unit_moved', 'combat_started')
                or the class name if no event_type attribute exists
        """
        if hasattr(event, "event_type"):
            return event.event_type
        else:
            return type(event).__name__


class LoggingObserver(EventObserver):
    """Observer that logs game events."""

    def handle_event(
        self,
        event: GameEvent | UnitMovedEvent | CombatStartedEvent | PhaseChangedEvent,
    ) -> None:
        """Log game events with appropriate detail level.

        This method processes game events and logs them with contextual information
        based on the event type. Different event types are logged with different
        levels of detail to provide useful debugging and monitoring information.

        Args:
            event: The game event to log
        """
        event_type = self._extract_event_type_identifier(event)
        self._log_event_by_type(event, event_type)

    def _log_event_by_type(
        self,
        event: GameEvent | UnitMovedEvent | CombatStartedEvent | PhaseChangedEvent,
        event_type: str,
    ) -> None:
        """Log an event with type-specific formatting.

        Args:
            event: The game event to log
            event_type: The type of the event
        """
        from .constants import EventConstants

        if event_type == EventConstants.UNIT_MOVED:
            self._log_unit_moved_event(event)
        elif event_type == EventConstants.PHASE_CHANGED:
            self._log_phase_changed_event(event)
        elif event_type == EventConstants.COMBAT_STARTED:
            self._log_combat_started_event(event)
        else:
            self._log_generic_event(event, event_type)

    def _log_unit_moved_event(
        self,
        event: GameEvent | UnitMovedEvent | CombatStartedEvent | PhaseChangedEvent,
    ) -> None:
        """Log a unit moved event with specific details.

        Args:
            event: The unit moved event to log
        """
        # Access data through the event's data dictionary
        data = event.data
        logger.info(
            f"Unit moved: {data['unit_id']} from {data['from_system']} to {data['to_system']} by {data['player_id']}"
        )

    def _log_phase_changed_event(
        self,
        event: GameEvent | UnitMovedEvent | CombatStartedEvent | PhaseChangedEvent,
    ) -> None:
        """Log a phase changed event with specific details.

        Args:
            event: The phase changed event to log
        """
        data = event.data
        logger.info(
            f"Phase changed: {data['from_phase']} -> {data['to_phase']} (Round {data['round_number']})"
        )

    def _log_combat_started_event(
        self,
        event: GameEvent | UnitMovedEvent | CombatStartedEvent | PhaseChangedEvent,
    ) -> None:
        """Log a combat started event with specific details.

        Args:
            event: The combat started event to log
        """
        data = event.data
        logger.info(
            f"Combat started in {data['system_id']} with participants: {data['participants']}"
        )

    def _log_generic_event(
        self,
        event: GameEvent | UnitMovedEvent | CombatStartedEvent | PhaseChangedEvent,
        event_type: str,
    ) -> None:
        """Log a generic event with basic information.

        Args:
            event: The game event to log
            event_type: The type of the event
        """
        logger.info(f"Game event: {event_type} in game {event.game_id}")


class StatisticsCollector(EventObserver):
    """Observer that collects game statistics."""

    def __init__(self) -> None:
        self._statistics: dict[str, Any] = {
            "unit_movements": 0,
            "phase_changes": 0,
            "player_actions": {},
            "current_round": 1,
        }

    def handle_event(
        self,
        event: GameEvent | UnitMovedEvent | CombatStartedEvent | PhaseChangedEvent,
    ) -> None:
        """Process game events and update statistical counters.

        This method analyzes game events and maintains various statistics
        including unit movements, phase changes, and player action counts.
        The collected statistics can be used for game analysis and balancing.

        Args:
            event: The game event to process for statistics
        """
        event_type = self._extract_event_type_identifier(event)

        from .constants import EventConstants

        if event_type == EventConstants.UNIT_MOVED:
            self._statistics["unit_movements"] += 1
            player_id = event.data.get("player_id")
            if player_id and player_id not in self._statistics["player_actions"]:
                self._statistics["player_actions"][player_id] = 0
            if player_id:
                self._statistics["player_actions"][player_id] += 1

        elif event_type == EventConstants.PHASE_CHANGED:
            self._statistics["phase_changes"] += 1
            round_number = event.data.get("round_number")
            if round_number:
                self._statistics["current_round"] = round_number

    def get_statistics(self) -> dict[str, Any]:
        """Get collected statistics."""
        return self._statistics.copy()


class AITrainingDataCollector(EventObserver):
    """Observer that collects data for AI training."""

    def __init__(self) -> None:
        self._training_data: list[dict[str, Any]] = []

    def handle_event(
        self,
        event: GameEvent | UnitMovedEvent | CombatStartedEvent | PhaseChangedEvent,
    ) -> None:
        """Collect and structure game event data for AI training purposes.

        This method processes game events and converts them into structured
        training records that can be used for machine learning and AI training.
        Each event type is processed differently to extract relevant features
        for training data.

        Args:
            event: The game event to process for training data collection
        """
        event_type = self._extract_event_type_identifier(event)
        training_record = self._create_base_training_record(event, event_type)
        self._enrich_training_record_with_event_data(training_record, event, event_type)
        self._training_data.append(training_record)

    def _create_base_training_record(
        self,
        event: GameEvent | UnitMovedEvent | CombatStartedEvent | PhaseChangedEvent,
        event_type: str,
    ) -> dict[str, Any]:
        """Create the base training record with common fields.

        Args:
            event: The game event to extract base data from
            event_type: The type of the event

        Returns:
            Dict containing base training record fields
        """
        return {
            "event_type": event_type,
            "game_id": event.game_id,
            "timestamp": event.timestamp,
        }

    def _enrich_training_record_with_event_data(
        self,
        training_record: dict[str, Any],
        event: GameEvent | UnitMovedEvent | CombatStartedEvent | PhaseChangedEvent,
        event_type: str,
    ) -> None:
        """Enrich the training record with event-specific data.

        Args:
            training_record: The base training record to enrich
            event: The game event containing specific data
            event_type: The type of the event
        """
        from .constants import EventConstants

        if event_type == EventConstants.UNIT_MOVED:
            self._add_unit_moved_data(training_record, event)
        elif event_type == EventConstants.COMBAT_STARTED:
            self._add_combat_started_data(training_record, event)
        elif event_type == EventConstants.PHASE_CHANGED:
            self._add_phase_changed_data(training_record, event)

    def _add_unit_moved_data(
        self,
        training_record: dict[str, Any],
        event: GameEvent | UnitMovedEvent | CombatStartedEvent | PhaseChangedEvent,
    ) -> None:
        """Add unit movement specific data to training record.

        Args:
            training_record: The training record to update
            event: The unit moved event
        """
        training_record.update(event.data)

    def _add_combat_started_data(
        self,
        training_record: dict[str, Any],
        event: GameEvent | UnitMovedEvent | CombatStartedEvent | PhaseChangedEvent,
    ) -> None:
        """Add combat started specific data to training record.

        Args:
            training_record: The training record to update
            event: The combat started event
        """
        training_record.update(event.data)

    def _add_phase_changed_data(
        self,
        training_record: dict[str, Any],
        event: GameEvent | UnitMovedEvent | CombatStartedEvent | PhaseChangedEvent,
    ) -> None:
        """Add phase changed specific data to training record.

        Args:
            training_record: The training record to update
            event: The phase changed event
        """
        training_record.update(event.data)

    def get_training_data(self) -> list[dict[str, Any]]:
        """Get collected training data."""
        return self._training_data.copy()

    def export_training_data(self) -> list[dict[str, Any]]:
        """Export training data (same as get_training_data for now)."""
        return self.get_training_data()
