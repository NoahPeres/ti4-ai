"""Optimizer protocol definitions to avoid circular imports.

Defines structural protocols for performance monitoring and optimizer interfaces
that can be shared by core orchestrators and optimizer implementations without
introducing import cycles.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from types import TracebackType
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from ti4.core.game_state import GameState
    from ti4.core.status_phase_performance import StatusPhasePerformanceReport


@runtime_checkable
class MetricsProtocol(Protocol):
    """Minimal metrics protocol used by performance monitoring."""

    success: bool
    error_message: str | None
    execution_time_ms: float


@runtime_checkable
class CMProtocol(Protocol):
    """Protocol for context managers yielding metrics objects."""

    def __enter__(self) -> MetricsProtocol: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool | None: ...


@runtime_checkable
class PerformanceOptimizerProtocol(Protocol):
    """Protocol for performance optimizers."""

    enable_memory_optimization: bool
    enable_caching: bool

    def monitor_performance(self, operation_name: str) -> CMProtocol: ...

    def optimize_for_large_game_states(self, game_state: GameState) -> GameState: ...

    def add_performance_report(self, report: StatusPhasePerformanceReport) -> None: ...

    def get_latest_report(self) -> StatusPhasePerformanceReport | None: ...

    def get_performance_trends(self) -> dict[str, float | int | bool]: ...

    def meets_performance_requirements(self) -> bool: ...

    def clear_cache(self) -> None: ...

    def get_cache_statistics(self) -> dict[str, Any]: ...


# A reusable no-op context manager compliant with CMProtocol
@contextmanager
def null_metrics_cm() -> Iterator[MetricsProtocol]:
    class _NullMetrics:
        success: bool
        error_message: str | None
        execution_time_ms: float

        def __init__(self) -> None:
            self.success = True
            self.error_message = None
            self.execution_time_ms = 0.0

    metrics = _NullMetrics()
    try:
        yield metrics
    finally:
        # No timing or special handling for null metrics
        pass
