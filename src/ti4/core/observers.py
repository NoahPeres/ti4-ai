"""Event observer implementations for TI4 game framework."""

import logging
import time
from abc import ABC, abstractmethod
from typing import Any

from .events import (
    CombatStartedEvent,
    CustodiansTokenRemovedEvent,
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
        event: GameEvent
        | UnitMovedEvent
        | CombatStartedEvent
        | PhaseChangedEvent
        | CustodiansTokenRemovedEvent,
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
            EventConstants.CUSTODIANS_TOKEN_REMOVED,
        ]
        for event_type in event_types:
            event_bus.subscribe(event_type, self.handle_event)

    def _extract_event_type_identifier(
        self,
        event: GameEvent,
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

    def _ensure_game_event(
        self,
        event: GameEvent
        | UnitMovedEvent
        | CombatStartedEvent
        | PhaseChangedEvent
        | CustodiansTokenRemovedEvent,
    ) -> GameEvent:
        """Normalize any event to a base GameEvent for consistent handling."""
        if isinstance(event, GameEvent):
            return event
        # Convert known specialized events to GameEvent
        if isinstance(event, UnitMovedEvent):
            return event.to_game_event()
        if isinstance(event, CombatStartedEvent):
            return event.to_game_event()
        if isinstance(event, PhaseChangedEvent):
            return event.to_game_event()
        if isinstance(event, CustodiansTokenRemovedEvent):
            return event.to_game_event()
        # Fallback: construct a GameEvent from available attributes
        event_type = getattr(event, "event_type", type(event).__name__)
        game_id = getattr(event, "game_id", "")
        data = getattr(event, "data", {})
        timestamp = getattr(event, "timestamp", time.time())
        return GameEvent(
            event_type=event_type, game_id=game_id, data=data, timestamp=timestamp
        )


class LoggingObserver(EventObserver):
    """Observer that logs game events."""

    def handle_event(
        self,
        event: GameEvent
        | UnitMovedEvent
        | CombatStartedEvent
        | PhaseChangedEvent
        | CustodiansTokenRemovedEvent,
    ) -> None:
        """Log game events with appropriate detail level.

        This method processes game events and logs them with contextual information
        based on the event type. Different event types are logged with different
        levels of detail to provide useful debugging and monitoring information.

        Args:
            event: The game event to log
        """
        base_event = self._ensure_game_event(event)
        event_type = self._extract_event_type_identifier(base_event)
        self._log_event_by_type(base_event, event_type)

    def _log_event_by_type(
        self,
        event: GameEvent,
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
        elif event_type == EventConstants.CUSTODIANS_TOKEN_REMOVED:
            self._log_custodians_token_removed_event(event)
        else:
            self._log_generic_event(event, event_type)

    def _log_unit_moved_event(
        self,
        event: GameEvent,
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
        event: GameEvent,
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
        event: GameEvent,
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
        event: GameEvent,
        event_type: str,
    ) -> None:
        """Log a generic event with basic information.

        Args:
            event: The game event to log
            event_type: The type of the event
        """
        logger.info(f"Game event: {event_type} in game {event.game_id}")

    def _log_custodians_token_removed_event(self, event: GameEvent) -> None:
        """Log a custodians token removed event with specific details."""
        data = event.data
        logger.info(
            "Custodians Token removed: player=%s, influence_spent=%s, system=%s, ground_force_id=%s, vp_awarded=%s, agenda_phase_activated=%s",
            data.get("player_id"),
            data.get("influence_spent"),
            data.get("system_id"),
            data.get("ground_force_id"),
            data.get("victory_points_awarded"),
            data.get("agenda_phase_activated"),
        )


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
        event: GameEvent
        | UnitMovedEvent
        | CombatStartedEvent
        | PhaseChangedEvent
        | CustodiansTokenRemovedEvent,
    ) -> None:
        """Process game events and update statistical counters.

        This method analyzes game events and maintains various statistics
        including unit movements, phase changes, and player action counts.
        The collected statistics can be used for game analysis and balancing.

        Args:
            event: The game event to process for statistics
        """
        base_event = self._ensure_game_event(event)
        event_type = self._extract_event_type_identifier(base_event)

        from .constants import EventConstants

        if event_type == EventConstants.UNIT_MOVED:
            self._statistics["unit_movements"] += 1
            player_id = base_event.data.get("player_id")
            if player_id and player_id not in self._statistics["player_actions"]:
                self._statistics["player_actions"][player_id] = 0
            if player_id:
                self._statistics["player_actions"][player_id] += 1

        elif event_type == EventConstants.PHASE_CHANGED:
            self._statistics["phase_changes"] += 1
            round_number = base_event.data.get("round_number")
            if round_number:
                self._statistics["current_round"] = round_number
        elif event_type == EventConstants.CUSTODIANS_TOKEN_REMOVED:
            # Track player action count and a simple counter for removals
            player_id = base_event.data.get("player_id")
            if player_id and player_id not in self._statistics["player_actions"]:
                self._statistics["player_actions"][player_id] = 0
            if player_id:
                self._statistics["player_actions"][player_id] += 1

    def get_statistics(self) -> dict[str, Any]:
        """Get collected statistics."""
        return self._statistics.copy()


class AITrainingDataCollector(EventObserver):
    """Observer that collects data for AI training."""

    def __init__(self) -> None:
        self._training_data: list[dict[str, Any]] = []

    def handle_event(
        self,
        event: GameEvent
        | UnitMovedEvent
        | CombatStartedEvent
        | PhaseChangedEvent
        | CustodiansTokenRemovedEvent,
    ) -> None:
        """Collect and structure game event data for AI training purposes.

        This method processes game events and converts them into structured
        training records that can be used for machine learning and AI training.
        Each event type is processed differently to extract relevant features
        for training data.

        Args:
            event: The game event to process for training data collection
        """
        base_event = self._ensure_game_event(event)
        event_type = self._extract_event_type_identifier(base_event)
        training_record = self._create_base_training_record(base_event, event_type)
        self._enrich_training_record_with_event_data(
            training_record, base_event, event_type
        )
        self._training_data.append(training_record)

    def _create_base_training_record(
        self, event: GameEvent, event_type: str
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
        self, training_record: dict[str, Any], event: GameEvent, event_type: str
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
        elif event_type == EventConstants.CUSTODIANS_TOKEN_REMOVED:
            self._add_custodians_token_removed_data(training_record, event)

    def _add_unit_moved_data(
        self, training_record: dict[str, Any], event: GameEvent
    ) -> None:
        """Add unit movement specific data to training record.

        Args:
            training_record: The training record to update
            event: The unit moved event
        """
        training_record.update(event.data)

    def _add_combat_started_data(
        self, training_record: dict[str, Any], event: GameEvent
    ) -> None:
        """Add combat started specific data to training record.

        Args:
            training_record: The training record to update
            event: The combat started event
        """
        training_record.update(event.data)

    def _add_phase_changed_data(
        self, training_record: dict[str, Any], event: GameEvent
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

    def _add_custodians_token_removed_data(
        self, training_record: dict[str, Any], event: GameEvent
    ) -> None:
        """Add custodians token removed specific data to training record."""
        training_record.update(event.data)
