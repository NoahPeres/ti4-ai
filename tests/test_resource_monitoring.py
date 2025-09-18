"""Tests for resource monitoring and management."""

import time
from unittest.mock import Mock, patch

import pytest

from src.ti4.core.game_state import GameState
from src.ti4.performance.monitoring import (
    GameStateResourceManager,
    PerformanceMetrics,
    ResourceMonitor,
    cleanup_global_resources,
    get_resource_manager,
)


class TestResourceMonitor:
    """Test cases for ResourceMonitor."""

    def test_monitor_initialization(self) -> None:
        """Test that monitor initializes correctly."""
        monitor = ResourceMonitor()
        assert monitor._peak_memory == 0.0
        assert len(monitor._metrics_history) == 0
        assert len(monitor._operation_times) == 0

    def test_memory_usage_tracking(self) -> None:
        """Test memory usage tracking."""
        monitor = ResourceMonitor()

        # Test with psutil available
        with patch("src.ti4.performance.monitoring.PSUTIL_AVAILABLE", True):
            mock_process = Mock()
            mock_process.memory_info.return_value.rss = (
                100 * 1024 * 1024
            )  # 100 MB in bytes
            monitor._process = mock_process

            memory_usage = monitor.get_current_memory_usage()
            assert memory_usage == 100.0  # Should be 100 MB
            assert monitor._peak_memory == 100.0

    def test_cpu_usage_tracking(self) -> None:
        """Test CPU usage tracking."""
        monitor = ResourceMonitor()

        # Test with psutil available
        with patch("src.ti4.performance.monitoring.PSUTIL_AVAILABLE", True):
            mock_process = Mock()
            mock_process.cpu_percent.return_value = 25.5
            monitor._process = mock_process

            cpu_usage = monitor.get_current_cpu_usage()
            assert cpu_usage == 25.5

    def test_operation_time_recording(self) -> None:
        """Test operation time recording."""
        monitor = ResourceMonitor()

        monitor.record_operation_time("test_operation", 0.1)
        monitor.record_operation_time("test_operation", 0.2)
        monitor.record_operation_time("test_operation", 0.15)

        stats = monitor.get_operation_stats("test_operation")
        assert stats["count"] == 3
        assert stats["average"] == pytest.approx(0.15, rel=1e-2)
        assert stats["min"] == 0.1
        assert stats["max"] == 0.2

    def test_metrics_collection(self) -> None:
        """Test performance metrics collection."""
        monitor = ResourceMonitor()

        # Record some operations
        monitor.record_operation_time("op1", 0.1)
        monitor.record_operation_time("op2", 0.2)

        with (
            patch.object(monitor, "get_current_memory_usage", return_value=50.0),
            patch.object(monitor, "get_current_cpu_usage", return_value=15.0),
        ):
            metrics = monitor.collect_metrics()

            assert metrics.memory_usage_mb == 50.0
            assert metrics.cpu_usage_percent == 15.0
            assert metrics.operation_count == 2
            assert metrics.average_operation_time == pytest.approx(0.15, rel=1e-2)

    def test_resource_cleanup(self) -> None:
        """Test resource cleanup functionality."""
        monitor = ResourceMonitor()

        # Add many metrics to trigger cleanup
        for _i in range(150):
            monitor._metrics_history.append(PerformanceMetrics())

        # Add many operation times
        for _i in range(150):
            monitor.record_operation_time("test_op", 0.1)

        monitor.cleanup_resources()

        # Should be reduced to 100 or fewer
        assert len(monitor._metrics_history) <= 100
        assert len(monitor._operation_times["test_op"]) <= 100


class TestGameStateResourceManager:
    """Test cases for GameStateResourceManager."""

    def test_manager_initialization(self) -> None:
        """Test that manager initializes correctly."""
        manager = GameStateResourceManager(max_states=50)
        assert manager._max_states == 50
        assert len(manager._game_states) == 0

    def test_game_state_registration(self) -> None:
        """Test game state registration."""
        manager = GameStateResourceManager()
        game_state = GameState(game_id="test_game")

        manager.register_game_state("test_game", game_state)

        assert "test_game" in manager._game_states
        assert "test_game" in manager._access_times
        assert manager._game_states["test_game"] == game_state

    def test_game_state_access(self) -> None:
        """Test game state access and time tracking."""
        manager = GameStateResourceManager()
        game_state = GameState(game_id="test_game")

        manager.register_game_state("test_game", game_state)
        initial_time = manager._access_times["test_game"]

        # Small delay to ensure time difference
        time.sleep(0.01)

        accessed_state = manager.access_game_state("test_game")
        updated_time = manager._access_times["test_game"]

        assert accessed_state == game_state
        assert updated_time > initial_time

    def test_game_state_removal(self) -> None:
        """Test game state removal."""
        manager = GameStateResourceManager()
        game_state = GameState(game_id="test_game")

        manager.register_game_state("test_game", game_state)
        manager.remove_game_state("test_game")

        assert "test_game" not in manager._game_states
        assert "test_game" not in manager._access_times

    def test_automatic_cleanup(self) -> None:
        """Test automatic cleanup when max states exceeded."""
        manager = GameStateResourceManager(max_states=3)

        # Add more states than the limit
        for i in range(5):
            game_state = GameState(game_id=f"game_{i}")
            manager.register_game_state(f"game_{i}", game_state)
            time.sleep(0.01)  # Ensure different access times

        # Should have cleaned up to be within limits
        assert len(manager._game_states) <= manager._max_states

    def test_resource_stats(self) -> None:
        """Test resource statistics collection."""
        manager = GameStateResourceManager(max_states=10)

        # Add some game states
        for i in range(3):
            game_state = GameState(game_id=f"game_{i}")
            manager.register_game_state(f"game_{i}", game_state)

        stats = manager.get_resource_stats()

        assert stats["managed_states"] == 3
        assert stats["max_states"] == 10
        assert "memory_usage_mb" in stats
        assert "cpu_usage_percent" in stats
        assert "uptime_seconds" in stats

    def test_resource_cleanup(self) -> None:
        """Test comprehensive resource cleanup."""
        manager = GameStateResourceManager()

        # Add some old game states
        old_time = time.time() - 7200  # 2 hours ago
        manager.register_game_state("old_game", GameState(game_id="old_game"))
        manager._access_times["old_game"] = old_time

        # Add a recent game state
        manager.register_game_state("new_game", GameState(game_id="new_game"))

        manager.cleanup_resources()

        # Old game should be removed, new game should remain
        assert "old_game" not in manager._game_states
        assert "new_game" in manager._game_states


class TestGlobalResourceManager:
    """Test cases for global resource manager."""

    def test_global_manager_singleton(self) -> None:
        """Test that global manager is a singleton."""
        manager1 = get_resource_manager()
        manager2 = get_resource_manager()

        assert manager1 is manager2

    def test_global_cleanup(self) -> None:
        """Test global resource cleanup."""
        manager = get_resource_manager()

        # Add some test data
        game_state = GameState(game_id="test_cleanup")
        manager.register_game_state("test_cleanup", game_state)

        # Cleanup should not raise errors
        cleanup_global_resources()

        # Manager should still be accessible
        assert get_resource_manager() is not None
