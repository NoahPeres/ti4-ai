"""Event system infrastructure for TI4 game framework."""

import time
from dataclasses import dataclass
from typing import Any, Callable

from .validation import validate_non_empty_string


@dataclass(frozen=True)
class GameEvent:
    """Base class for all game events."""

    event_type: str
    game_id: str
    data: dict[str, Any]
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            object.__setattr__(self, "timestamp", time.time())


@dataclass(frozen=True)
class UnitMovedEvent:
    """Event fired when a unit moves."""

    game_id: str
    unit_id: str
    from_system: str
    to_system: str
    player_id: str
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            object.__setattr__(self, "timestamp", time.time())

    @property
    def event_type(self) -> str:
        from .constants import EventConstants

        return EventConstants.UNIT_MOVED

    @property
    def data(self) -> dict[str, Any]:
        return {
            "unit_id": self.unit_id,
            "from_system": self.from_system,
            "to_system": self.to_system,
            "player_id": self.player_id,
        }


@dataclass(frozen=True)
class CombatStartedEvent:
    """Event fired when combat begins."""

    game_id: str
    system_id: str
    participants: list[str]
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            object.__setattr__(self, "timestamp", time.time())

    @property
    def event_type(self) -> str:
        from .constants import EventConstants

        return EventConstants.COMBAT_STARTED

    @property
    def data(self) -> dict[str, Any]:
        return {"system_id": self.system_id, "participants": self.participants}


@dataclass(frozen=True)
class PhaseChangedEvent:
    """Event fired when game phase changes."""

    game_id: str
    from_phase: str
    to_phase: str
    round_number: int
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            object.__setattr__(self, "timestamp", time.time())

    @property
    def event_type(self) -> str:
        from .constants import EventConstants

        return EventConstants.PHASE_CHANGED

    @property
    def data(self) -> dict[str, Any]:
        return {
            "from_phase": self.from_phase,
            "to_phase": self.to_phase,
            "round_number": self.round_number,
        }


# Factory methods for consistent event creation
def create_unit_moved_event(
    game_id: str, unit_id: str, from_system: str, to_system: str, player_id: str
) -> UnitMovedEvent:
    """Create a unit moved event with validation."""
    validate_non_empty_string(game_id, "Game ID")
    validate_non_empty_string(unit_id, "Unit ID")
    validate_non_empty_string(from_system, "From system")
    validate_non_empty_string(to_system, "To system")
    validate_non_empty_string(player_id, "Player ID")

    return UnitMovedEvent(
        game_id=game_id,
        unit_id=unit_id,
        from_system=from_system,
        to_system=to_system,
        player_id=player_id,
    )


def create_combat_started_event(
    game_id: str, system_id: str, participants: list[str]
) -> CombatStartedEvent:
    """Create a combat started event with validation."""
    validate_non_empty_string(game_id, "Game ID")
    validate_non_empty_string(system_id, "System ID")
    from .validation import validate_collection_not_empty

    validate_collection_not_empty(participants, "Participants")

    return CombatStartedEvent(
        game_id=game_id, system_id=system_id, participants=participants
    )


def create_phase_changed_event(
    game_id: str, from_phase: str, to_phase: str, round_number: int
) -> PhaseChangedEvent:
    """Create a phase changed event with validation."""
    validate_non_empty_string(game_id, "Game ID")
    validate_non_empty_string(from_phase, "From phase")
    validate_non_empty_string(to_phase, "To phase")
    from .validation import validate_positive_number

    validate_positive_number(round_number, "Round number")

    return PhaseChangedEvent(
        game_id=game_id,
        from_phase=from_phase,
        to_phase=to_phase,
        round_number=round_number,
    )


class GameEventBus:
    """Central event bus for game event notifications."""

    def __init__(self):
        self._observers: dict[str, list[Callable]] = {}

    def subscribe(self, event_type: str, observer: Callable) -> None:
        """Subscribe to specific event types."""
        validate_non_empty_string(event_type, "Event type")
        from .validation import validate_callable

        validate_callable(observer, "Observer")

        if event_type not in self._observers:
            self._observers[event_type] = []
        self._observers[event_type].append(observer)

    def unsubscribe(self, event_type: str, observer: Callable) -> None:
        """Unsubscribe from event types."""
        validate_non_empty_string(event_type, "Event type")

        if event_type in self._observers and observer in self._observers[event_type]:
            self._observers[event_type].remove(observer)

    def publish(self, event: GameEvent) -> None:
        """Publish event to all subscribers."""
        if event.event_type in self._observers:
            for observer in self._observers[event.event_type]:
                try:
                    observer(event)
                except Exception:
                    # Error isolation - continue notifying other observers
                    pass
