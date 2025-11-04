"""Event system infrastructure for TI4 game framework."""

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from .validation import validate_non_empty_string


@dataclass(frozen=True)
class GameEvent:
    """Base class for all game events."""

    event_type: str
    game_id: str
    data: dict[str, Any]
    timestamp: float = field(default_factory=time.time)


@dataclass(frozen=True)
class UnitMovedEvent:
    """Event fired when a unit moves."""

    game_id: str
    unit_id: str
    from_system: str
    to_system: str
    player_id: str
    timestamp: float = field(default_factory=time.time)

    @property
    def event_type(self) -> str:
        from .constants import EventType

        return EventType.UNIT_MOVED.value

    @property
    def data(self) -> dict[str, Any]:
        return {
            "unit_id": self.unit_id,
            "from_system": self.from_system,
            "to_system": self.to_system,
            "player_id": self.player_id,
        }

    def to_game_event(self) -> GameEvent:
        """Convert to a GameEvent instance."""
        return GameEvent(
            event_type=self.event_type,
            game_id=self.game_id,
            data=self.data,
            timestamp=self.timestamp,
        )


@dataclass(frozen=True)
class CombatStartedEvent:
    """Event fired when combat begins."""

    game_id: str
    system_id: str
    participants: list[str]
    timestamp: float = field(default_factory=time.time)

    @property
    def event_type(self) -> str:
        from .constants import EventType

        return EventType.COMBAT_STARTED.value

    @property
    def data(self) -> dict[str, Any]:
        return {"system_id": self.system_id, "participants": self.participants}

    def to_game_event(self) -> GameEvent:
        """Convert to a GameEvent instance."""
        return GameEvent(
            event_type=self.event_type,
            game_id=self.game_id,
            data=self.data,
            timestamp=self.timestamp,
        )


@dataclass(frozen=True)
class PhaseChangedEvent:
    """Event fired when game phase changes."""

    game_id: str
    from_phase: str
    to_phase: str
    round_number: int
    timestamp: float = field(default_factory=time.time)

    @property
    def event_type(self) -> str:
        from .constants import EventType

        return EventType.PHASE_CHANGED.value

    @property
    def data(self) -> dict[str, Any]:
        return {
            "from_phase": self.from_phase,
            "to_phase": self.to_phase,
            "round_number": self.round_number,
        }

    def to_game_event(self) -> GameEvent:
        """Convert to a GameEvent instance."""
        return GameEvent(
            event_type=self.event_type,
            game_id=self.game_id,
            data=self.data,
            timestamp=self.timestamp,
        )


@dataclass(frozen=True)
class CustodiansTokenRemovedEvent:
    """Event fired when the Custodians Token is removed from Mecatol Rex (Rule 27)."""

    game_id: str
    player_id: str
    influence_spent: int
    system_id: str
    ground_force_id: str | None = None
    victory_points_awarded: int = 1
    agenda_phase_activated: bool = True
    timestamp: float = field(default_factory=time.time)

    @property
    def event_type(self) -> str:
        from .constants import EventType

        return EventType.CUSTODIANS_TOKEN_REMOVED.value

    @property
    def data(self) -> dict[str, Any]:
        return {
            "player_id": self.player_id,
            "influence_spent": self.influence_spent,
            "system_id": self.system_id,
            "ground_force_id": self.ground_force_id,
            "victory_points_awarded": self.victory_points_awarded,
            "agenda_phase_activated": self.agenda_phase_activated,
        }

    def to_game_event(self) -> GameEvent:
        """Convert to a GameEvent instance."""
        return GameEvent(
            event_type=self.event_type,
            game_id=self.game_id,
            data=self.data,
            timestamp=self.timestamp,
        )


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


def create_custodians_token_removed_event(
    game_id: str,
    player_id: str,
    influence_spent: int,
    system_id: str,
    ground_force_id: str | None,
    victory_points_awarded: int = 1,
    agenda_phase_activated: bool = True,
) -> CustodiansTokenRemovedEvent:
    """Create a custodians token removed event with validation."""
    validate_non_empty_string(game_id, "Game ID")
    validate_non_empty_string(player_id, "Player ID")
    validate_non_empty_string(system_id, "System ID")
    # Validate optional ground force identifier when provided
    if ground_force_id is not None:
        validate_non_empty_string(ground_force_id, "Ground Force ID")
    from .validation import validate_positive_number

    validate_positive_number(influence_spent, "Influence Spent")
    validate_positive_number(victory_points_awarded, "Victory Points Awarded")

    return CustodiansTokenRemovedEvent(
        game_id=game_id,
        player_id=player_id,
        influence_spent=influence_spent,
        system_id=system_id,
        ground_force_id=ground_force_id,
        victory_points_awarded=victory_points_awarded,
        agenda_phase_activated=agenda_phase_activated,
    )


class GameEventBus:
    """Central event bus for game event notifications."""

    def __init__(self) -> None:
        self._observers: dict[str, list[Callable[..., Any]]] = {}

    def subscribe(self, event_type: str, observer: Callable[..., Any]) -> None:
        """Subscribe to specific event types."""
        validate_non_empty_string(event_type, "Event type")
        from .validation import validate_callable

        validate_callable(observer, "Observer")

        if event_type not in self._observers:
            self._observers[event_type] = []
        self._observers[event_type].append(observer)

    def unsubscribe(self, event_type: str, observer: Callable[..., Any]) -> None:
        """Unsubscribe from event types."""
        validate_non_empty_string(event_type, "Event type")

        if event_type in self._observers and observer in self._observers[event_type]:
            self._observers[event_type].remove(observer)

    def publish(
        self,
        event: GameEvent
        | UnitMovedEvent
        | CombatStartedEvent
        | PhaseChangedEvent
        | CustodiansTokenRemovedEvent,
    ) -> None:
        """Publish event to all subscribers."""
        # Convert specific event types to GameEvent if needed
        if isinstance(
            event,
            (
                UnitMovedEvent,
                CombatStartedEvent,
                PhaseChangedEvent,
                CustodiansTokenRemovedEvent,
            ),
        ):
            game_event = event.to_game_event()
        else:
            game_event = event

        if game_event.event_type in self._observers:
            for observer in self._observers[game_event.event_type]:
                try:
                    observer(
                        event
                    )  # Pass the original event to maintain type information
                except Exception as e:
                    # Error isolation - continue notifying other observers
                    # Log the error for debugging purposes
                    import logging

                    logging.warning(
                        f"Observer {observer} failed to handle event {event}: {e}"
                    )
