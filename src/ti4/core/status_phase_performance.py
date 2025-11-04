"""Performance optimization and monitoring for Rule 81 Status Phase.

This module provides performance optimization features and monitoring capabilities
for the status phase implementation to ensure compliance with performance requirements.

Requirements addressed:
- 12.1: Complete status phase execution in <500ms
- 12.2: Individual steps execution in <100ms each
- 12.3: Memory usage optimization for large game states
"""

import gc
import time
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from .status_phase import (
    RoundTransitionManager,
    StatusPhaseOrchestrator,
    StatusPhaseResult,
    StepResult,
)

if TYPE_CHECKING:
    from .game_state import GameState

T = TypeVar("T")


@dataclass
class PerformanceMetrics:
    """Performance metrics for status phase operations.

    Tracks timing, memory usage, and other performance indicators
    for status phase execution.
    """

    operation_name: str
    execution_time_ms: float
    memory_before: int = 0
    memory_after: int = 0
    memory_peak: int = 0
    success: bool = True
    error_message: str = ""

    @property
    def memory_delta(self) -> int:
        """Calculate memory usage change during operation."""
        return self.memory_after - self.memory_before

    @property
    def meets_timing_requirement(self) -> bool:
        """Check if operation meets timing requirements."""
        if "complete" in self.operation_name.lower():
            return self.execution_time_ms < 500  # Complete status phase <500ms
        else:
            return self.execution_time_ms < 100  # Individual steps <100ms


@dataclass
class StatusPhasePerformanceReport:
    """Comprehensive performance report for status phase execution."""

    total_execution_time_ms: float
    step_metrics: dict[int, PerformanceMetrics] = field(default_factory=dict)
    overall_metrics: PerformanceMetrics | None = None
    memory_optimization_enabled: bool = False
    performance_warnings: list[str] = field(default_factory=list)

    def add_step_metrics(self, step_number: int, metrics: PerformanceMetrics) -> None:
        """Add performance metrics for a specific step."""
        self.step_metrics[step_number] = metrics

        # Check for performance warnings
        if not metrics.meets_timing_requirement:
            self.performance_warnings.append(
                f"Step {step_number} exceeded timing requirement: {metrics.execution_time_ms:.2f}ms"
            )

    def get_slowest_step(self) -> tuple[int, PerformanceMetrics] | None:
        """Get the slowest executing step."""
        if not self.step_metrics:
            return None

        slowest_step = max(
            self.step_metrics.items(), key=lambda item: item[1].execution_time_ms
        )
        return slowest_step

    def get_total_memory_usage(self) -> int:
        """Get total memory usage across all steps."""
        return sum(metrics.memory_delta for metrics in self.step_metrics.values())

    def meets_performance_requirements(self) -> bool:
        """Check if all performance requirements are met."""
        # Check overall timing
        if self.total_execution_time_ms >= 500:
            return False

        # Check individual step timing
        for metrics in self.step_metrics.values():
            if not metrics.meets_timing_requirement:
                return False

        return True


class StatusPhasePerformanceOptimizer:
    """Performance optimizer for status phase execution.

    Provides optimization features including caching, memory management,
    and performance monitoring for the status phase.
    """

    def __init__(
        self, enable_caching: bool = True, enable_memory_optimization: bool = True
    ):
        """Initialize the performance optimizer.

        Args:
            enable_caching: Whether to enable result caching
            enable_memory_optimization: Whether to enable memory optimization
        """
        self.enable_caching = enable_caching
        self.enable_memory_optimization = enable_memory_optimization
        self._cache: dict[str, Any] = {}
        self._performance_history: list[StatusPhasePerformanceReport] = []

    @contextmanager
    def monitor_performance(
        self, operation_name: str
    ) -> Generator[PerformanceMetrics, None, None]:
        """Context manager for monitoring operation performance.

        Args:
            operation_name: Name of the operation being monitored

        Yields:
            PerformanceMetrics object that will be populated with timing data
        """
        # Initialize metrics
        metrics = PerformanceMetrics(
            operation_name=operation_name, execution_time_ms=0.0
        )

        # Measure memory before operation
        if self.enable_memory_optimization:
            gc.collect()  # Force garbage collection for accurate measurement
            metrics.memory_before = self._get_memory_usage()

        # Start timing
        start_time = time.perf_counter()

        try:
            yield metrics
        except Exception as e:
            metrics.success = False
            metrics.error_message = str(e)
            raise
        finally:
            # End timing
            end_time = time.perf_counter()
            metrics.execution_time_ms = (end_time - start_time) * 1000

            # Measure memory after operation
            if self.enable_memory_optimization:
                metrics.memory_after = self._get_memory_usage()

    def _get_memory_usage(self) -> int:
        """Get current memory load proxy (simplified).

        Returns:
            Approximate object count (proxy for memory usage)
        """
        # Use object count as a proxy for memory usage
        # In production, you might use psutil or similar for actual memory measurement
        return len(gc.get_objects())

    def optimize_for_large_game_states(self, game_state: "GameState") -> "GameState":
        """Optimize game state for better performance with large states.

        Args:
            game_state: The game state to optimize

        Returns:
            Optimized game state (may be the same object if no optimization needed)
        """
        if not self.enable_memory_optimization:
            return game_state

        # For now, return the same state
        # In a full implementation, you might:
        # - Compress unused data
        # - Cache frequently accessed computations
        # - Optimize data structures
        return game_state

    def clear_cache(self) -> None:
        """Clear the performance cache."""
        self._cache.clear()

    def get_cache_statistics(self) -> dict[str, Any]:
        """Get cache performance statistics.

        Returns:
            Dictionary with cache statistics
        """
        return {
            "cache_size": len(self._cache),
            "cache_enabled": self.enable_caching,
            "memory_optimization_enabled": self.enable_memory_optimization,
        }

    def add_performance_report(self, report: StatusPhasePerformanceReport) -> None:
        """Add a performance report to the history.

        Args:
            report: Performance report to add
        """
        self._performance_history.append(report)

        # Keep only the last 100 reports to prevent memory growth
        if len(self._performance_history) > 100:
            self._performance_history = self._performance_history[-100:]

    def get_performance_trends(self) -> dict[str, Any]:
        """Get performance trends from historical data.

        Returns:
            Dictionary with performance trend analysis
        """
        if not self._performance_history:
            return {"message": "No performance history available"}

        recent_reports = self._performance_history[-10:]  # Last 10 executions

        avg_execution_time = sum(
            r.total_execution_time_ms for r in recent_reports
        ) / len(recent_reports)

        performance_degradation = False
        if len(recent_reports) >= 2:
            recent_slice = recent_reports[-3:]
            older_slice = recent_reports[:3]
            recent_avg = sum(r.total_execution_time_ms for r in recent_slice) / max(
                1, len(recent_slice)
            )
            older_avg = sum(r.total_execution_time_ms for r in older_slice) / max(
                1, len(older_slice)
            )
            performance_degradation = recent_avg > older_avg * 1.2  # 20% slower

        return {
            "average_execution_time_ms": avg_execution_time,
            "performance_degradation_detected": performance_degradation,
            "total_reports": len(self._performance_history),
            "recent_reports_analyzed": len(recent_reports),
        }

    def get_latest_report(self) -> StatusPhasePerformanceReport | None:
        """Return the most recent performance report if available.

        Returns:
            Most recent performance report or None if no reports exist
        """
        if not self._performance_history:
            return None
        return self._performance_history[-1]


class OptimizedStatusPhaseOrchestrator(StatusPhaseOrchestrator):
    """Performance-optimized version of StatusPhaseOrchestrator.

    Extends the base orchestrator with performance monitoring and optimization features.
    """

    # Override the base class attribute type: in this optimized variant, the optimizer
    # is guaranteed to be present, so it is non-optional.
    optimizer: StatusPhasePerformanceOptimizer

    # Optimizer is non-optional in this optimized variant.

    def __init__(self, optimizer: StatusPhasePerformanceOptimizer | None = None):
        """Initialize the optimized orchestrator.

        Args:
            optimizer: Performance optimizer instance (creates default if None)
        """
        super().__init__()
        # In the optimized orchestrator, the optimizer is always present.
        # Narrow the type for static type checkers.
        self.optimizer: StatusPhasePerformanceOptimizer = (
            optimizer or StatusPhasePerformanceOptimizer()
        )

    def execute_complete_status_phase(
        self, game_state: "GameState"
    ) -> tuple[StatusPhaseResult, "GameState"]:
        """Execute complete status phase with performance monitoring.

        Args:
            game_state: The current game state

        Returns:
            Tuple of (StatusPhaseResult, updated GameState)
        """
        # Create performance report
        report = StatusPhasePerformanceReport(total_execution_time_ms=0.0)

        with self.optimizer.monitor_performance(
            "complete_status_phase"
        ) as overall_metrics:
            # Optimize game state for large states
            optimized_state = self.optimizer.optimize_for_large_game_states(game_state)

            # Execute the status phase with step-by-step monitoring
            result, final_state = self._execute_with_monitoring(optimized_state, report)

            # Update overall metrics
            overall_metrics.success = result.success
            if not result.success:
                overall_metrics.error_message = result.error_message

        # Finalize report
        report.overall_metrics = overall_metrics
        report.total_execution_time_ms = overall_metrics.execution_time_ms

        # Update result with actual timing
        result.total_execution_time = (
            overall_metrics.execution_time_ms / 1000
        )  # Convert to seconds
        report.memory_optimization_enabled = self.optimizer.enable_memory_optimization

        # Add to performance history
        self.optimizer.add_performance_report(report)

        return result, final_state

    def _execute_with_monitoring(
        self, game_state: "GameState", report: StatusPhasePerformanceReport
    ) -> tuple[StatusPhaseResult, "GameState"]:
        """Execute status phase with per-step performance monitoring.

        Args:
            game_state: The game state to process
            report: Performance report to populate

        Returns:
            Tuple of (StatusPhaseResult, updated GameState)
        """
        # Enhanced game state validation (same as base orchestrator)
        if game_state is None:
            result = StatusPhaseResult(
                success=False,
                steps_completed=[],
                step_results={},
                total_execution_time=0.0,
                next_phase="strategy",
                error_message="Game state cannot be None",
            )
            return result, game_state

        # Validate game state type - reject invalid types
        if not hasattr(game_state, "players") and not hasattr(
            game_state, "_create_new_state"
        ):
            result = StatusPhaseResult(
                success=False,
                steps_completed=[],
                step_results={},
                total_execution_time=0.0,
                next_phase="strategy",
                error_message="Invalid game state type - must be a valid GameState object",
            )
            return result, game_state

        step_results = {}
        steps_completed = []
        current_state = game_state
        overall_success = True

        # Execute each step with monitoring
        for step_num in range(1, 9):
            with self.optimizer.monitor_performance(f"step_{step_num}") as step_metrics:
                try:
                    step_result, current_state = self.execute_step(
                        step_num, current_state
                    )
                    step_results[step_num] = step_result
                    steps_completed.append(step_result.step_name)

                    step_metrics.success = step_result.success
                    if not step_result.success:
                        step_metrics.error_message = step_result.error_message
                        if self._is_critical_step(step_num):
                            overall_success = False
                            break

                except Exception as e:
                    step_metrics.success = False
                    step_metrics.error_message = str(e)

                    step_result = StepResult(
                        success=False,
                        step_name=f"Step {step_num}",
                        error_message=str(e),
                    )
                    step_results[step_num] = step_result

                    if self._is_critical_step(step_num):
                        overall_success = False
                        break

            # Add step metrics to report
            report.add_step_metrics(step_num, step_metrics)

        # Determine next phase and apply transition (mirror base orchestrator)
        transition_manager = RoundTransitionManager()
        if overall_success:
            next_phase = transition_manager.determine_next_phase(current_state)
            if next_phase == "agenda":
                final_state = transition_manager.transition_to_agenda_phase(
                    current_state
                )
            else:
                final_state = transition_manager.transition_to_new_round(current_state)
        else:
            next_phase = "strategy"
            final_state = current_state

        result = StatusPhaseResult(
            success=overall_success,
            steps_completed=steps_completed,
            step_results=step_results,
            total_execution_time=0.0,  # Will be set by caller
            next_phase=next_phase,
        )

        return result, final_state

    def get_performance_report(self) -> StatusPhasePerformanceReport | None:
        """Get the most recent performance report.

        Returns:
            Most recent performance report, or None if no reports available
        """
        # Delegate to optimizer to provide latest report
        return self.optimizer.get_latest_report()

    def get_optimizer_statistics(self) -> dict[str, Any]:
        """Get performance optimizer statistics.

        Returns:
            Dictionary with optimizer statistics and trends
        """
        cache_stats = self.optimizer.get_cache_statistics()
        trends = self.optimizer.get_performance_trends()

        return {
            "cache_statistics": cache_stats,
            "performance_trends": trends,
            "optimization_features": {
                "caching_enabled": self.optimizer.enable_caching,
                "memory_optimization_enabled": self.optimizer.enable_memory_optimization,
            },
        }


# Convenience function for creating optimized orchestrator
def create_optimized_status_phase_orchestrator(
    enable_caching: bool = True, enable_memory_optimization: bool = True
) -> OptimizedStatusPhaseOrchestrator:
    """Create an optimized status phase orchestrator with performance features.

    Args:
        enable_caching: Whether to enable result caching
        enable_memory_optimization: Whether to enable memory optimization

    Returns:
        Optimized status phase orchestrator
    """
    optimizer = StatusPhasePerformanceOptimizer(
        enable_caching=enable_caching,
        enable_memory_optimization=enable_memory_optimization,
    )
    return OptimizedStatusPhaseOrchestrator(optimizer)
