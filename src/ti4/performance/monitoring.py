"""Resource monitoring and management for TI4."""

import gc
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Optional

try:
    import psutil  # type: ignore

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


@dataclass
class PerformanceMetrics:
    """Container for performance metrics."""

    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    operation_count: int = 0
    average_operation_time: float = 0.0
    peak_memory_mb: float = 0.0
    timestamp: float = field(default_factory=time.time)


@dataclass
class ResourceUsage:
    """Container for resource usage information."""

    memory_mb: float
    cpu_percent: float
    timestamp: float = field(default_factory=time.time)


class ResourceMonitor:
    """Monitors system resource usage for TI4 operations."""

    def __init__(self) -> None:
        """Initialize the resource monitor."""
        self._process = psutil.Process() if PSUTIL_AVAILABLE else None
        self._metrics_history: list[PerformanceMetrics] = []
        self._operation_times: dict[str, list[float]] = defaultdict(list)
        self._peak_memory = 0.0
        self._start_time = time.time()

    def get_current_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        if not PSUTIL_AVAILABLE or not self._process:
            return 0.0

        try:
            memory_info = self._process.memory_info()
            memory_mb = float(memory_info.rss) / 1024 / 1024  # Convert bytes to MB
            self._peak_memory = max(self._peak_memory, memory_mb)
            return memory_mb
        except Exception:
            return 0.0

    def get_current_cpu_usage(self) -> float:
        """Get current CPU usage percentage."""
        if not PSUTIL_AVAILABLE or not self._process:
            return 0.0

        try:
            cpu_percent = self._process.cpu_percent()
            return float(cpu_percent) if cpu_percent is not None else 0.0
        except Exception:
            return 0.0

    def get_current_resource_usage(self) -> ResourceUsage:
        """Get current resource usage snapshot."""
        return ResourceUsage(
            memory_mb=self.get_current_memory_usage(),
            cpu_percent=self.get_current_cpu_usage(),
        )

    def record_operation_time(self, operation_name: str, duration: float) -> None:
        """Record the duration of an operation."""
        self._operation_times[operation_name].append(duration)

        # Keep only recent measurements
        from ..core.constants import PerformanceConstants

        if (
            len(self._operation_times[operation_name])
            > PerformanceConstants.MAX_OPERATION_HISTORY
        ):
            self._operation_times[operation_name] = self._operation_times[
                operation_name
            ][-PerformanceConstants.MAX_OPERATION_HISTORY :]

    def get_operation_stats(self, operation_name: str) -> dict[str, float]:
        """Get statistics for a specific operation."""
        times = self._operation_times.get(operation_name, [])
        if not times:
            return {"count": 0, "average": 0.0, "min": 0.0, "max": 0.0}

        return {
            "count": len(times),
            "average": sum(times) / len(times),
            "min": min(times),
            "max": max(times),
        }

    def collect_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics."""
        current_memory = self.get_current_memory_usage()
        current_cpu = self.get_current_cpu_usage()

        # Calculate average operation time across all operations
        all_times = []
        total_operations = 0
        for times in self._operation_times.values():
            all_times.extend(times)
            total_operations += len(times)

        avg_time = sum(all_times) / len(all_times) if all_times else 0.0

        metrics = PerformanceMetrics(
            memory_usage_mb=current_memory,
            cpu_usage_percent=current_cpu,
            operation_count=total_operations,
            average_operation_time=avg_time,
            peak_memory_mb=self._peak_memory,
        )

        self._metrics_history.append(metrics)

        # Keep only recent metrics (last 1000)
        if len(self._metrics_history) > 1000:
            self._metrics_history = self._metrics_history[-1000:]

        return metrics

    def get_metrics_history(self) -> list[PerformanceMetrics]:
        """Get historical performance metrics."""
        return self._metrics_history.copy()

    def cleanup_resources(self) -> None:
        """Perform resource cleanup."""
        # Clear old metrics
        if len(self._metrics_history) > 100:
            self._metrics_history = self._metrics_history[-100:]

        # Clear old operation times
        for operation_name in list(self._operation_times.keys()):
            times = self._operation_times[operation_name]
            if len(times) > 100:
                self._operation_times[operation_name] = times[-100:]

        # Force garbage collection
        gc.collect()

    def get_uptime(self) -> float:
        """Get monitor uptime in seconds."""
        return time.time() - self._start_time


class GameStateResourceManager:
    """Manages resources for game states."""

    def __init__(self, max_states: Optional[int] = None) -> None:
        """Initialize the resource manager."""
        if max_states is None:
            from ..core.constants import PerformanceConstants

            max_states = PerformanceConstants.DEFAULT_MAX_STATES
        self._max_states = max_states
        self._game_states: dict[str, Any] = {}  # game_id -> game_state
        self._access_times: dict[str, float] = {}  # game_id -> last_access_time
        self._monitor = ResourceMonitor()

    def register_game_state(self, game_id: str, game_state: Any) -> None:
        """Register a game state for resource management."""
        self._game_states[game_id] = game_state
        self._access_times[game_id] = time.time()

        # Cleanup if we exceed max states
        if len(self._game_states) > self._max_states:
            self._evict_least_recently_used_states()

    def access_game_state(self, game_id: str) -> Optional[Any]:
        """Access a game state and update access time."""
        if game_id in self._game_states:
            self._access_times[game_id] = time.time()
            return self._game_states[game_id]
        return None

    def remove_game_state(self, game_id: str) -> None:
        """Remove a game state from management."""
        self._game_states.pop(game_id, None)
        self._access_times.pop(game_id, None)

    def _evict_least_recently_used_states(self) -> None:
        """Remove the least recently used game states to free memory.

        This method implements an LRU (Least Recently Used) eviction policy
        to keep memory usage within bounds. It removes the oldest accessed
        states when the number of managed states exceeds the maximum limit.
        """
        if not self._access_times:
            return

        # Sort by access time and remove oldest (LRU eviction)
        states_sorted_by_access_time = sorted(
            self._access_times.items(), key=lambda x: x[1]
        )
        number_of_states_to_evict = (
            len(self._game_states) - self._max_states + 10
        )  # Remove extra for buffer

        for game_id, _ in states_sorted_by_access_time[:number_of_states_to_evict]:
            self.remove_game_state(game_id)

    def get_resource_stats(self) -> dict[str, Any]:
        """Get resource usage statistics."""
        current_usage = self._monitor.get_current_resource_usage()

        return {
            "managed_states": len(self._game_states),
            "max_states": self._max_states,
            "memory_usage_mb": current_usage.memory_mb,
            "cpu_usage_percent": current_usage.cpu_percent,
            "uptime_seconds": self._monitor.get_uptime(),
        }

    def cleanup_resources(self) -> None:
        """Perform comprehensive resource cleanup."""
        # Remove old states
        current_time = time.time()
        from ..core.constants import PerformanceConstants

        old_threshold = current_time - PerformanceConstants.OLD_STATE_THRESHOLD

        old_states = [
            game_id
            for game_id, access_time in self._access_times.items()
            if access_time < old_threshold
        ]

        for game_id in old_states:
            self.remove_game_state(game_id)

        # Cleanup monitor resources
        self._monitor.cleanup_resources()


# Global resource manager instance
_global_resource_manager: Optional[GameStateResourceManager] = None


def get_resource_manager() -> GameStateResourceManager:
    """Get the global resource manager instance."""
    global _global_resource_manager
    if _global_resource_manager is None:
        _global_resource_manager = GameStateResourceManager()
    return _global_resource_manager


def cleanup_global_resources() -> None:
    """Cleanup global resources."""
    global _global_resource_manager
    if _global_resource_manager:
        _global_resource_manager.cleanup_resources()
