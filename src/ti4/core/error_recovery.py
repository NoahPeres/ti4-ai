"""Error recovery mechanisms for TI4 game framework."""

import logging
import time
from typing import Any, Callable, Optional

from .exceptions import TI4GameError


class TransientError(TI4GameError):
    """Exception for transient errors that should be retried."""

    pass


class CircuitBreakerOpenError(TI4GameError):
    """Exception raised when circuit breaker is open."""

    pass


class RecoveryStrategy:
    """Base class for error recovery strategies."""

    def __init__(self, strategy_func: Callable[[Exception, dict[str, Any]], Any]):
        self.strategy_func = strategy_func

    def recover(self, error: Exception, context: dict[str, Any]) -> Any:
        """Execute recovery strategy."""
        return self.strategy_func(error, context)


class CircuitBreaker:
    """Circuit breaker implementation for preventing cascading failures."""

    def __init__(self, failure_threshold: int = None, recovery_timeout: float = None):
        from .constants import CircuitBreakerConstants, PerformanceConstants

        if failure_threshold is None:
            failure_threshold = PerformanceConstants.DEFAULT_FAILURE_THRESHOLD
        if recovery_timeout is None:
            recovery_timeout = PerformanceConstants.CIRCUIT_BREAKER_TIMEOUT

        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = CircuitBreakerConstants.STATE_CLOSED

    def can_execute(self) -> bool:
        """Check if operation can be executed."""
        if self.state == "closed":
            return True
        elif self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half-open"
                return True
            return False
        else:  # half-open
            return True

    def record_success(self) -> None:
        """Record successful operation."""
        from .constants import CircuitBreakerConstants

        self.failure_count = 0
        self.state = CircuitBreakerConstants.STATE_CLOSED

    def record_failure(self) -> None:
        """Record failed operation."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "open"


class ErrorRecoveryManager:
    """Manages error recovery mechanisms for different failure types."""

    def __init__(self):
        self.recovery_strategies: dict[type[Exception], RecoveryStrategy] = {}
        self.circuit_breakers: dict[str, CircuitBreaker] = {}
        self.logger = logging.getLogger(__name__)

    def register_recovery_strategy(
        self,
        error_type: type[Exception],
        strategy_func: Callable[[Exception, dict[str, Any]], Any],
    ) -> None:
        """Register a recovery strategy for specific error type."""
        self.recovery_strategies[error_type] = RecoveryStrategy(strategy_func)

    def execute_with_fallback(
        self,
        operation: Callable[[], Any],
        fallback: Callable[[], Any],
        is_critical: bool = True,
    ) -> Any:
        """Execute operation with fallback for non-critical failures."""
        try:
            return operation()
        except Exception as e:
            if not is_critical:
                self._log_recovery(e, "fallback")
                return fallback()
            else:
                raise

    def execute_with_retry(
        self,
        operation: Callable[[], Any],
        max_retries: int = None,
        retry_delay: float = None,
    ) -> Any:
        from .constants import PerformanceConstants

        if max_retries is None:
            max_retries = PerformanceConstants.DEFAULT_MAX_RETRIES
        if retry_delay is None:
            retry_delay = PerformanceConstants.DEFAULT_RETRY_DELAY
        """Execute operation with automatic retry for transient errors."""
        last_exception = None

        for attempt in range(max_retries + 1):
            try:
                result = operation()
                if attempt > 0:
                    self.logger.info(f"Operation succeeded after {attempt} retries")
                return result
            except TransientError as e:
                last_exception = e
                if attempt < max_retries:
                    self.logger.warning(
                        f"Transient error on attempt {attempt + 1}, retrying in {retry_delay}s: {e}"
                    )
                    time.sleep(retry_delay)
                else:
                    self.logger.error(f"Operation failed after {max_retries} retries")
            except Exception:
                # Non-transient errors are not retried
                raise

        # If we get here, all retries were exhausted
        raise last_exception

    def execute_with_circuit_breaker(
        self,
        operation: Callable[[], Any],
        operation_id: str,
        failure_threshold: int = None,
    ) -> Any:
        from .constants import PerformanceConstants

        if failure_threshold is None:
            failure_threshold = PerformanceConstants.DEFAULT_FAILURE_THRESHOLD
        """Execute operation with circuit breaker pattern."""
        if operation_id not in self.circuit_breakers:
            self.circuit_breakers[operation_id] = CircuitBreaker(failure_threshold)

        circuit_breaker = self.circuit_breakers[operation_id]

        if not circuit_breaker.can_execute():
            raise CircuitBreakerOpenError(
                f"Circuit breaker open for operation: {operation_id}"
            )

        try:
            result = operation()
            circuit_breaker.record_success()
            return result
        except Exception:
            circuit_breaker.record_failure()
            raise

    def execute_with_recovery(
        self, operation: Callable[[], Any], context: Optional[dict[str, Any]] = None
    ) -> Any:
        """Execute operation with registered recovery strategies."""
        context = context or {}

        try:
            return operation()
        except Exception as e:
            # Try to find a recovery strategy for this error type
            for error_type, strategy in self.recovery_strategies.items():
                if isinstance(e, error_type):
                    self._log_error_recovery_attempt(e, "strategy")
                    return strategy.recover(e, context)

            # No recovery strategy found, re-raise
            raise

    def _log_recovery(
        self, error: Exception, recovery_type: str, context: dict[str, Any] = None
    ) -> None:
        """Log recovery attempt details."""
        self._log_error_recovery_attempt(error, recovery_type)

    def _log_error_recovery_attempt(
        self, error: Exception, recovery_mechanism_type: str
    ) -> None:
        """Log details of an error recovery attempt.

        This method logs information about error recovery attempts, including
        the error type, recovery mechanism used, and any additional context
        available from TI4GameError instances.

        Args:
            error: The exception that triggered recovery
            recovery_mechanism_type: Type of recovery mechanism used (e.g., 'strategy', 'fallback')
        """
        self.logger.warning(
            f"Error recovery ({recovery_mechanism_type}) for {error.__class__.__name__}: {error}"
        )

        # If it's a TI4GameError, preserve the context
        if isinstance(error, TI4GameError):
            self.logger.debug(f"Error context: {error.context}")
