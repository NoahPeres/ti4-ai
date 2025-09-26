"""Test the event system infrastructure."""

import dataclasses
from unittest.mock import Mock

import pytest

from ti4.core.events import (
    CombatStartedEvent,
    GameEvent,
    GameEventBus,
    PhaseChangedEvent,
    UnitMovedEvent,
    create_combat_started_event,
    create_phase_changed_event,
    create_unit_moved_event,
)


class TestGameEvent:
    """Test the base GameEvent class."""

    def test_game_event_creation(self) -> None:
        """Test that GameEvent can be created with required properties."""
        event = GameEvent(
            event_type="test_event", game_id="game_123", data={"key": "value"}
        )

        assert event.event_type == "test_event"
        assert event.game_id == "game_123"
        assert event.data == {"key": "value"}
        assert event.timestamp > 0  # Should have a timestamp

    def test_game_event_immutable(self) -> None:
        """Test that GameEvent instances are immutable."""
        event = GameEvent(
            event_type="test_event", game_id="game_123", data={"key": "value"}
        )

        # Should not be able to modify the event (frozen dataclass)
        with pytest.raises((AttributeError, dataclasses.FrozenInstanceError)):
            event.data = {"modified": "data"}


class TestGameEventBus:
    """Test the GameEventBus class."""

    def test_event_bus_creation(self) -> None:
        """Test that GameEventBus can be created."""
        bus = GameEventBus()
        assert bus is not None

    def test_subscribe_to_event_type(self) -> None:
        """Test subscribing to an event type."""
        bus = GameEventBus()
        observer = Mock()

        bus.subscribe("test_event", observer)

        # Should not raise any exceptions
        assert True

    def test_unsubscribe_from_event_type(self) -> None:
        """Test unsubscribing from an event type."""
        bus = GameEventBus()
        observer = Mock()

        bus.subscribe("test_event", observer)
        bus.unsubscribe("test_event", observer)

        # Should not raise any exceptions
        assert True

    def test_publish_event_to_subscribers(self) -> None:
        """Test publishing an event to subscribers."""
        bus = GameEventBus()
        observer = Mock()

        bus.subscribe("test_event", observer)

        event = GameEvent(
            event_type="test_event", game_id="game_123", data={"key": "value"}
        )

        bus.publish(event)

        # Observer should have been called with the event
        observer.assert_called_once_with(event)

    def test_publish_event_to_multiple_subscribers(self) -> None:
        """Test publishing an event to multiple subscribers."""
        bus = GameEventBus()
        observer1 = Mock()
        observer2 = Mock()

        bus.subscribe("test_event", observer1)
        bus.subscribe("test_event", observer2)

        event = GameEvent(
            event_type="test_event", game_id="game_123", data={"key": "value"}
        )

        bus.publish(event)

        # Both observers should have been called
        observer1.assert_called_once_with(event)
        observer2.assert_called_once_with(event)

    def test_publish_event_only_to_matching_subscribers(self) -> None:
        """Test that events are only published to matching event type subscribers."""
        bus = GameEventBus()
        observer1 = Mock()
        observer2 = Mock()

        bus.subscribe("event_type_1", observer1)
        bus.subscribe("event_type_2", observer2)

        event = GameEvent(
            event_type="event_type_1", game_id="game_123", data={"key": "value"}
        )

        bus.publish(event)

        # Only observer1 should have been called
        observer1.assert_called_once_with(event)
        observer2.assert_not_called()

    def test_unsubscribed_observer_not_called(self) -> None:
        """Test that unsubscribed observers are not called."""
        bus = GameEventBus()
        observer = Mock()

        bus.subscribe("test_event", observer)
        bus.unsubscribe("test_event", observer)

        event = GameEvent(
            event_type="test_event", game_id="game_123", data={"key": "value"}
        )

        bus.publish(event)

        # Observer should not have been called
        observer.assert_not_called()

    def test_error_isolation_in_observers(self) -> None:
        """Test that if one observer fails, others still receive events."""
        bus = GameEventBus()
        failing_observer = Mock(side_effect=Exception("Observer failed"))
        working_observer = Mock()

        bus.subscribe("test_event", failing_observer)
        bus.subscribe("test_event", working_observer)

        event = GameEvent(
            event_type="test_event", game_id="game_123", data={"key": "value"}
        )

        # Should not raise exception despite failing observer
        bus.publish(event)

        # Both observers should have been called
        failing_observer.assert_called_once_with(event)
        working_observer.assert_called_once_with(event)

    def test_subscribe_validation(self) -> None:
        """Test that subscribe validates inputs."""
        bus = GameEventBus()

        # Empty event type should raise ValueError
        with pytest.raises(ValueError, match="Event type cannot be empty"):
            bus.subscribe("", Mock())

    def test_unsubscribe_validation(self) -> None:
        """Test that unsubscribe validates inputs."""
        bus = GameEventBus()

        # Empty event type should raise ValueError
        with pytest.raises(ValueError, match="Event type cannot be empty"):
            bus.unsubscribe("", Mock())


class TestSpecificGameEvents:
    """Test specific game event classes."""

    def test_unit_moved_event_creation(self) -> None:
        """Test creating a UnitMovedEvent."""
        event = UnitMovedEvent(
            game_id="game_123",
            unit_id="unit_456",
            from_system="system_1",
            to_system="system_2",
            player_id="player_1",
        )

        assert event.event_type == "unit_moved"
        assert event.game_id == "game_123"
        assert event.unit_id == "unit_456"
        assert event.from_system == "system_1"
        assert event.to_system == "system_2"
        assert event.player_id == "player_1"
        assert event.timestamp > 0

    def test_combat_started_event_creation(self) -> None:
        """Test creating a CombatStartedEvent."""
        participants = ["player_1", "player_2"]
        event = CombatStartedEvent(
            game_id="game_123", system_id="system_1", participants=participants
        )

        assert event.event_type == "combat_started"
        assert event.game_id == "game_123"
        assert event.system_id == "system_1"
        assert event.participants == participants
        assert event.timestamp > 0

    def test_phase_changed_event_creation(self) -> None:
        """Test creating a PhaseChangedEvent."""
        event = PhaseChangedEvent(
            game_id="game_123", from_phase="action", to_phase="status", round_number=3
        )

        assert event.event_type == "phase_changed"
        assert event.game_id == "game_123"
        assert event.from_phase == "action"
        assert event.to_phase == "status"
        assert event.round_number == 3
        assert event.timestamp > 0


class TestEventFactoryMethods:
    """Test event factory methods for consistent creation."""

    def test_create_unit_moved_event(self) -> None:
        """Test factory method for creating unit moved events."""
        event = create_unit_moved_event(
            game_id="game_123",
            unit_id="unit_456",
            from_system="system_1",
            to_system="system_2",
            player_id="player_1",
        )

        assert isinstance(event, UnitMovedEvent)
        assert event.event_type == "unit_moved"
        assert event.unit_id == "unit_456"

    def test_create_combat_started_event(self) -> None:
        """Test factory method for creating combat started events."""
        participants = ["player_1", "player_2"]
        event = create_combat_started_event(
            game_id="game_123", system_id="system_1", participants=participants
        )

        assert isinstance(event, CombatStartedEvent)
        assert event.event_type == "combat_started"
        assert event.system_id == "system_1"

    def test_create_phase_changed_event(self) -> None:
        """Test factory method for creating phase changed events."""
        event = create_phase_changed_event(
            game_id="game_123", from_phase="action", to_phase="status", round_number=3
        )

        assert isinstance(event, PhaseChangedEvent)
        assert event.event_type == "phase_changed"
        assert event.from_phase == "action"

    def test_factory_methods_validate_inputs(self) -> None:
        """Test that factory methods validate inputs."""
        # Empty game_id should raise ValueError
        with pytest.raises(ValueError, match="Game ID cannot be empty"):
            create_unit_moved_event("", "unit_1", "sys_1", "sys_2", "player_1")

        # Empty participants list should raise ValueError
        with pytest.raises(ValueError, match="Participants cannot be empty"):
            create_combat_started_event("game_123", "system_1", [])

        # Invalid round number should raise ValueError
        with pytest.raises(ValueError, match="Round number must be positive"):
            create_phase_changed_event("game_123", "action", "status", 0)
