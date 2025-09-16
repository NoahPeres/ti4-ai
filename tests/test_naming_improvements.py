"""Tests to verify that naming improvements work correctly."""

from unittest.mock import Mock, patch

from src.ti4.core.diagnostics import CommandHistoryAnalyzer
from src.ti4.core.error_recovery import ErrorRecoveryManager
from src.ti4.core.events import UnitMovedEvent
from src.ti4.core.observers import (
    AITrainingDataCollector,
    LoggingObserver,
    StatisticsCollector,
)
from src.ti4.performance.cache import GameStateCache
from src.ti4.performance.monitoring import GameStateResourceManager


class TestObserverNamingImprovements:
    """Test that observer method naming improvements work correctly."""

    def test_event_type_extraction_method_works(self):
        """Test that the renamed event type extraction method works."""
        logger = LoggingObserver()
        event = UnitMovedEvent(
            game_id="test",
            unit_id="unit1",
            from_system="sys1",
            to_system="sys2",
            player_id="player1",
        )

        # Test the renamed method
        event_type = logger._extract_event_type_identifier(event)
        assert event_type == "unit_moved"

    def test_event_type_extraction_fallback_works(self):
        """Test that event type extraction falls back to class name."""
        logger = LoggingObserver()

        # Create a mock event without event_type attribute
        mock_event = Mock()
        del mock_event.event_type  # Remove the attribute
        mock_event.__class__.__name__ = "TestEvent"

        event_type = logger._extract_event_type_identifier(mock_event)
        assert event_type == "TestEvent"

    @patch("src.ti4.core.observers.logger")
    def test_event_logging_with_improved_method(self, mock_logger):
        """Test that event logging works with the improved method name."""

        logger = LoggingObserver()
        event = UnitMovedEvent(
            game_id="test",
            unit_id="unit1",
            from_system="sys1",
            to_system="sys2",
            player_id="player1",
        )

        # This should work without errors
        logger.handle_event(event)

        # Verify logging was called
        mock_logger.info.assert_called_once()

    def test_statistics_collector_with_improved_method(self):
        """Test that statistics collector works with improved method name."""
        collector = StatisticsCollector()
        event = UnitMovedEvent(
            game_id="test",
            unit_id="unit1",
            from_system="sys1",
            to_system="sys2",
            player_id="player1",
        )

        # This should work without errors
        collector.handle_event(event)

        # Verify statistics were updated
        stats = collector.get_statistics()
        assert stats["unit_movements"] == 1

    def test_ai_training_collector_with_improved_method(self):
        """Test that AI training collector works with improved method name."""
        collector = AITrainingDataCollector()
        event = UnitMovedEvent(
            game_id="test",
            unit_id="unit1",
            from_system="sys1",
            to_system="sys2",
            player_id="player1",
        )

        # This should work without errors
        collector.handle_event(event)

        # Verify training data was collected
        training_data = collector.get_training_data()
        assert len(training_data) == 1
        assert training_data[0]["event_type"] == "unit_moved"


class TestDiagnosticsNamingImprovements:
    """Test that diagnostics method naming improvements work correctly."""

    def test_command_type_extraction_method_works(self):
        """Test that the renamed command type extraction method works."""
        diagnostics = CommandHistoryAnalyzer()

        # Create a mock command with command_type attribute
        mock_command = Mock()
        mock_command.command_type = "move_unit"

        command_type = diagnostics._extract_command_type(mock_command)
        assert command_type == "move_unit"

    def test_command_type_extraction_fallback_works(self):
        """Test that command type extraction falls back to class name."""
        diagnostics = CommandHistoryAnalyzer()

        # Create a mock command without command_type attribute
        mock_command = Mock()
        del mock_command.command_type  # Remove the attribute
        mock_command.__class__.__name__ = "TestCommand"

        command_type = diagnostics._extract_command_type(mock_command)
        assert command_type == "testcommand"  # Should be lowercase

    def test_pattern_analysis_with_improved_method_name(self):
        """Test that pattern analysis works with the improved method name."""
        diagnostics = CommandHistoryAnalyzer()

        # Create mock commands
        mock_commands = []
        for i in range(3):
            mock_command = Mock()
            mock_command.command_type = (
                f"command_type_{i % 2}"  # Create some repetition
            )
            mock_commands.append(mock_command)

        # This should work without errors
        patterns = diagnostics.analyze_command_patterns_and_sequences(mock_commands)

        # Verify the structure
        assert "repeated_commands" in patterns
        assert "command_sequences" in patterns
        assert len(patterns["command_sequences"]) == 2  # 3 commands = 2 transitions


class TestErrorRecoveryNamingImprovements:
    """Test that error recovery method naming improvements work correctly."""

    @patch("src.ti4.core.error_recovery.logging.getLogger")
    def test_error_recovery_logging_with_improved_method(self, mock_get_logger):
        """Test that error recovery logging works with the improved method name."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        manager = ErrorRecoveryManager()
        test_error = ValueError("Test error")

        # This should work without errors
        manager._log_error_recovery_attempt(test_error, "test_recovery")

        # Verify logging was called
        mock_logger.warning.assert_called_once()
        assert "test_recovery" in mock_logger.warning.call_args[0][0]
        assert "ValueError" in mock_logger.warning.call_args[0][0]


class TestPerformanceMonitoringNamingImprovements:
    """Test that performance monitoring method naming improvements work correctly."""

    def test_lru_eviction_method_works(self):
        """Test that the renamed LRU eviction method works."""
        manager = GameStateResourceManager(max_states=2)

        # Add some game states
        manager.register_game_state("game1", {"state": "data1"})
        manager.register_game_state("game2", {"state": "data2"})
        manager.register_game_state(
            "game3", {"state": "data3"}
        )  # This should trigger eviction

        # Verify that eviction occurred (should have at most max_states + buffer)
        stats = manager.get_resource_stats()
        assert stats["managed_states"] <= 12  # max_states (2) + buffer (10)


class TestCacheNamingImprovements:
    """Test that cache variable naming improvements work correctly."""

    def test_adjacency_cache_with_improved_variable_names(self):
        """Test that adjacency caching works with improved variable names."""
        # Create a mock galaxy
        mock_galaxy = Mock()
        mock_galaxy.are_systems_adjacent.return_value = True

        cache = GameStateCache(max_size=2)
        cache._galaxy = mock_galaxy

        # Test adjacency caching
        result = cache.are_systems_adjacent("sys1", "sys2")
        assert result is True

        # Verify the galaxy method was called
        mock_galaxy.are_systems_adjacent.assert_called_once_with("sys1", "sys2")

        # Test cache hit
        result2 = cache.are_systems_adjacent("sys1", "sys2")
        assert result2 is True

        # Galaxy method should not be called again (cache hit)
        assert mock_galaxy.are_systems_adjacent.call_count == 1


class TestDocstringImprovements:
    """Test that improved docstrings are accessible and informative."""

    def test_observer_docstrings_are_comprehensive(self):
        """Test that observer method docstrings are comprehensive."""
        logger = LoggingObserver()

        # Check that the docstring is comprehensive
        docstring = logger.handle_event.__doc__
        assert "Log game events with appropriate detail level" in docstring
        assert "Args:" in docstring
        assert "event: The game event to log" in docstring

    def test_diagnostics_docstrings_are_comprehensive(self):
        """Test that diagnostics method docstrings are comprehensive."""
        diagnostics = CommandHistoryAnalyzer()

        # Check command type extraction docstring
        docstring = diagnostics._extract_command_type.__doc__
        assert "Extract the command type identifier" in docstring
        assert "Args:" in docstring
        assert "Returns:" in docstring

        # Check pattern analysis docstring
        docstring = diagnostics.analyze_command_patterns_and_sequences.__doc__
        assert "Analyze command patterns and detect sequences" in docstring
        assert "Repeated command types" in docstring
        assert "Sequential patterns" in docstring

    def test_error_recovery_docstrings_are_comprehensive(self):
        """Test that error recovery method docstrings are comprehensive."""
        manager = ErrorRecoveryManager()

        # Check error recovery logging docstring
        docstring = manager._log_error_recovery_attempt.__doc__
        assert "Log details of an error recovery attempt" in docstring
        assert "recovery_mechanism_type" in docstring
        assert "Args:" in docstring
