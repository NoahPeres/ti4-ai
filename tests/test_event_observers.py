"""Tests for event observer implementations."""

from unittest.mock import patch

from src.ti4.core.events import (
    GameEventBus,
    create_combat_started_event,
    create_phase_changed_event,
    create_unit_moved_event,
)
from src.ti4.core.observers import (
    AITrainingDataCollector,
    LoggingObserver,
    StatisticsCollector,
)


class TestLoggingObserver:
    """Test the logging observer."""

    def test_logging_observer_creation(self) -> None:
        """Test that LoggingObserver can be created."""
        observer = LoggingObserver()
        assert observer is not None

    def test_logging_observer_logs_unit_moved_event(self) -> None:
        """Test that LoggingObserver logs unit moved events."""
        observer = LoggingObserver()

        event = create_unit_moved_event(
            game_id="game_123",
            unit_id="unit_456",
            from_system="system_1",
            to_system="system_2",
            player_id="player_1",
        )

        with patch("src.ti4.core.observers.logger") as mock_logger:
            observer.handle_event(event)

            # Verify logging was called
            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[0][0]
            assert "Unit moved" in call_args
            assert "unit_456" in call_args
            assert "player_1" in call_args

    def test_logging_observer_logs_phase_changed_event(self) -> None:
        """Test that LoggingObserver logs phase changed events."""
        observer = LoggingObserver()

        event = create_phase_changed_event(
            game_id="game_123", from_phase="action", to_phase="status", round_number=3
        )

        with patch("src.ti4.core.observers.logger") as mock_logger:
            observer.handle_event(event)

            # Verify logging was called
            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[0][0]
            assert "Phase changed" in call_args
            assert "action" in call_args
            assert "status" in call_args

    def test_logging_observer_can_be_registered_with_event_bus(self) -> None:
        """Test that LoggingObserver can be registered with event bus."""
        event_bus = GameEventBus()
        observer = LoggingObserver()

        # Should not raise exception
        observer.register_with_bus(event_bus)

        # Test that it receives events
        event = create_unit_moved_event(
            game_id="game_123",
            unit_id="unit_456",
            from_system="system_1",
            to_system="system_2",
            player_id="player_1",
        )

        with patch("src.ti4.core.observers.logger") as mock_logger:
            event_bus.publish(event)
            mock_logger.info.assert_called_once()


class TestStatisticsCollector:
    """Test the statistics collector observer."""

    def test_statistics_collector_creation(self) -> None:
        """Test that StatisticsCollector can be created."""
        collector = StatisticsCollector()
        assert collector is not None

    def test_statistics_collector_tracks_unit_movements(self) -> None:
        """Test that StatisticsCollector tracks unit movement statistics."""
        collector = StatisticsCollector()

        event = create_unit_moved_event(
            game_id="game_123",
            unit_id="unit_456",
            from_system="system_1",
            to_system="system_2",
            player_id="player_1",
        )

        collector.handle_event(event)

        stats = collector.get_statistics()
        assert stats["unit_movements"] == 1
        assert stats["player_actions"]["player_1"] == 1

    def test_statistics_collector_tracks_phase_changes(self) -> None:
        """Test that StatisticsCollector tracks phase change statistics."""
        collector = StatisticsCollector()

        event = create_phase_changed_event(
            game_id="game_123", from_phase="action", to_phase="status", round_number=3
        )

        collector.handle_event(event)

        stats = collector.get_statistics()
        assert stats["phase_changes"] == 1
        assert stats["current_round"] == 3

    def test_statistics_collector_accumulates_statistics(self) -> None:
        """Test that StatisticsCollector accumulates statistics over multiple events."""
        collector = StatisticsCollector()

        # Add multiple events
        for i in range(3):
            event = create_unit_moved_event(
                game_id="game_123",
                unit_id=f"unit_{i}",
                from_system="system_1",
                to_system="system_2",
                player_id="player_1",
            )
            collector.handle_event(event)

        stats = collector.get_statistics()
        assert stats["unit_movements"] == 3
        assert stats["player_actions"]["player_1"] == 3

    def test_statistics_collector_can_be_registered_with_event_bus(self) -> None:
        """Test that StatisticsCollector can be registered with event bus."""
        event_bus = GameEventBus()
        collector = StatisticsCollector()

        # Should not raise exception
        collector.register_with_bus(event_bus)

        # Test that it receives and processes events
        event = create_unit_moved_event(
            game_id="game_123",
            unit_id="unit_456",
            from_system="system_1",
            to_system="system_2",
            player_id="player_1",
        )

        event_bus.publish(event)

        stats = collector.get_statistics()
        assert stats["unit_movements"] == 1


class TestAITrainingDataCollector:
    """Test the AI training data collector observer."""

    def test_ai_training_data_collector_creation(self) -> None:
        """Test that AITrainingDataCollector can be created."""
        collector = AITrainingDataCollector()
        assert collector is not None

    def test_ai_training_data_collector_collects_unit_movements(self) -> None:
        """Test that AITrainingDataCollector collects unit movement data."""
        collector = AITrainingDataCollector()

        event = create_unit_moved_event(
            game_id="game_123",
            unit_id="unit_456",
            from_system="system_1",
            to_system="system_2",
            player_id="player_1",
        )

        collector.handle_event(event)

        training_data = collector.get_training_data()
        assert len(training_data) == 1
        assert training_data[0]["event_type"] == "unit_moved"
        assert training_data[0]["player_id"] == "player_1"
        assert training_data[0]["from_system"] == "system_1"
        assert training_data[0]["to_system"] == "system_2"

    def test_ai_training_data_collector_collects_combat_events(self) -> None:
        """Test that AITrainingDataCollector collects combat event data."""
        collector = AITrainingDataCollector()

        event = create_combat_started_event(
            game_id="game_123",
            system_id="system_1",
            participants=["player_1", "player_2"],
        )

        collector.handle_event(event)

        training_data = collector.get_training_data()
        assert len(training_data) == 1
        assert training_data[0]["event_type"] == "combat_started"
        assert training_data[0]["system_id"] == "system_1"
        assert training_data[0]["participants"] == ["player_1", "player_2"]

    def test_ai_training_data_collector_exports_data(self) -> None:
        """Test that AITrainingDataCollector can export training data."""
        collector = AITrainingDataCollector()

        # Add some events
        event1 = create_unit_moved_event(
            game_id="game_123",
            unit_id="unit_456",
            from_system="system_1",
            to_system="system_2",
            player_id="player_1",
        )

        event2 = create_phase_changed_event(
            game_id="game_123", from_phase="action", to_phase="status", round_number=3
        )

        collector.handle_event(event1)
        collector.handle_event(event2)

        # Export data
        exported_data = collector.export_training_data()

        assert len(exported_data) == 2
        assert exported_data[0]["event_type"] == "unit_moved"
        assert exported_data[1]["event_type"] == "phase_changed"

    def test_ai_training_data_collector_can_be_registered_with_event_bus(self) -> None:
        """Test that AITrainingDataCollector can be registered with event bus."""
        event_bus = GameEventBus()
        collector = AITrainingDataCollector()

        # Should not raise exception
        collector.register_with_bus(event_bus)

        # Test that it receives and processes events
        event = create_unit_moved_event(
            game_id="game_123",
            unit_id="unit_456",
            from_system="system_1",
            to_system="system_2",
            player_id="player_1",
        )

        event_bus.publish(event)

        training_data = collector.get_training_data()
        assert len(training_data) == 1


class TestObserverIntegration:
    """Test integration scenarios with multiple observers."""

    def test_multiple_observers_can_be_registered(self) -> None:
        """Test that multiple observers can be registered with the same event bus."""
        event_bus = GameEventBus()

        logging_observer = LoggingObserver()
        stats_collector = StatisticsCollector()
        ai_collector = AITrainingDataCollector()

        # Register all observers
        logging_observer.register_with_bus(event_bus)
        stats_collector.register_with_bus(event_bus)
        ai_collector.register_with_bus(event_bus)

        # Publish an event
        event = create_unit_moved_event(
            game_id="game_123",
            unit_id="unit_456",
            from_system="system_1",
            to_system="system_2",
            player_id="player_1",
        )

        with patch("src.ti4.core.observers.logger"):
            event_bus.publish(event)

        # Verify all observers processed the event
        stats = stats_collector.get_statistics()
        assert stats["unit_movements"] == 1

        training_data = ai_collector.get_training_data()
        assert len(training_data) == 1
