"""Tests to verify that constants are being used correctly throughout the codebase."""

import pytest

from src.ti4.core.constants import (
    CircuitBreakerConstants,
    EventConstants,
    GameStateConstants,
    PerformanceConstants,
)
from src.ti4.core.error_recovery import CircuitBreaker, ErrorRecoveryManager
from src.ti4.core.events import CombatStartedEvent, PhaseChangedEvent, UnitMovedEvent
from src.ti4.performance.cache import GameStateCache
from src.ti4.performance.concurrent import ConcurrentGameManager


class TestEventConstants:
    """Test that event constants are used correctly."""

    def test_unit_moved_event_uses_constant(self):
        """Test that UnitMovedEvent uses the correct constant."""
        event = UnitMovedEvent(
            game_id="test",
            unit_id="unit1",
            from_system="sys1",
            to_system="sys2",
            player_id="player1",
        )
        assert event.event_type == EventConstants.UNIT_MOVED

    def test_combat_started_event_uses_constant(self):
        """Test that CombatStartedEvent uses the correct constant."""
        event = CombatStartedEvent(
            game_id="test", system_id="sys1", participants=["player1", "player2"]
        )
        assert event.event_type == EventConstants.COMBAT_STARTED

    def test_phase_changed_event_uses_constant(self):
        """Test that PhaseChangedEvent uses the correct constant."""
        event = PhaseChangedEvent(
            game_id="test", from_phase="setup", to_phase="strategy", round_number=1
        )
        assert event.event_type == EventConstants.PHASE_CHANGED


class TestPerformanceConstants:
    """Test that performance constants are used correctly."""

    def test_cache_uses_default_size_constant(self):
        """Test that GameStateCache uses the default size constant."""
        cache = GameStateCache()
        assert cache._max_size == PerformanceConstants.DEFAULT_CACHE_SIZE

    def test_cache_accepts_custom_size(self):
        """Test that GameStateCache accepts custom size."""
        custom_size = 500
        cache = GameStateCache(max_size=custom_size)
        assert cache._max_size == custom_size

    def test_concurrent_manager_uses_default_constants(self):
        """Test that ConcurrentGameManager uses default constants."""
        manager = ConcurrentGameManager()
        assert (
            manager._max_concurrent_games
            == PerformanceConstants.DEFAULT_MAX_CONCURRENT_GAMES
        )

    def test_circuit_breaker_uses_default_constants(self):
        """Test that CircuitBreaker uses default constants."""
        breaker = CircuitBreaker()
        assert (
            breaker.failure_threshold == PerformanceConstants.DEFAULT_FAILURE_THRESHOLD
        )
        assert breaker.recovery_timeout == PerformanceConstants.CIRCUIT_BREAKER_TIMEOUT
        assert breaker.state == CircuitBreakerConstants.STATE_CLOSED

    def test_error_recovery_manager_uses_default_constants(self):
        """Test that ErrorRecoveryManager uses default constants."""
        from src.ti4.core.error_recovery import TransientError

        manager = ErrorRecoveryManager()

        # Test that retry uses default constants
        call_count = 0

        def always_failing_operation():
            nonlocal call_count
            call_count += 1
            raise TransientError("Test transient failure")

        # This should retry the default number of times and then fail
        with pytest.raises(TransientError):
            manager.execute_with_retry(always_failing_operation)

        # Should have been called max_retries + 1 times (initial + retries)
        assert call_count == PerformanceConstants.DEFAULT_MAX_RETRIES + 1


class TestGameStateConstants:
    """Test that game state constants are used correctly."""

    def test_default_values_are_constants(self):
        """Test that default values match the constants."""
        assert GameStateConstants.DEFAULT_TACTIC_TOKENS == 3
        assert GameStateConstants.DEFAULT_FLEET_TOKENS == 3
        assert GameStateConstants.DEFAULT_STRATEGY_TOKENS == 2
        assert GameStateConstants.DEFAULT_RESOURCES == 0
        assert GameStateConstants.DEFAULT_INFLUENCE == 0
        assert GameStateConstants.DEFAULT_CURRENT_PLAYER_INDEX == 0
        assert GameStateConstants.DEFAULT_ROUND_NUMBER == 1


class TestConstantValues:
    """Test that constants have expected values."""

    def test_event_constants_values(self):
        """Test that event constants have expected string values."""
        assert EventConstants.UNIT_MOVED == "unit_moved"
        assert EventConstants.COMBAT_STARTED == "combat_started"
        assert EventConstants.PHASE_CHANGED == "phase_changed"

    def test_performance_constants_values(self):
        """Test that performance constants have reasonable values."""
        assert PerformanceConstants.DEFAULT_CACHE_SIZE == 1000
        assert PerformanceConstants.DEFAULT_MAX_CONCURRENT_GAMES == 100
        assert PerformanceConstants.CIRCUIT_BREAKER_TIMEOUT == 60.0
        assert PerformanceConstants.DEFAULT_RETRY_DELAY == 1.0
        assert PerformanceConstants.DEFAULT_MAX_RETRIES == 3
        assert PerformanceConstants.DEFAULT_FAILURE_THRESHOLD == 5

    def test_circuit_breaker_constants_values(self):
        """Test that circuit breaker constants have expected values."""
        assert CircuitBreakerConstants.STATE_CLOSED == "closed"
        assert CircuitBreakerConstants.STATE_OPEN == "open"
        assert CircuitBreakerConstants.STATE_HALF_OPEN == "half-open"


class TestConstantConsistency:
    """Test that constants are consistent across the codebase."""

    def test_token_constants_match_game_constants(self):
        """Test that token constants match the original game constants."""
        from src.ti4.core.constants import GameConstants

        # These should match the values in GameConstants
        assert (
            GameStateConstants.DEFAULT_TACTIC_TOKENS
            == GameConstants.STARTING_TACTIC_TOKENS
        )
        assert (
            GameStateConstants.DEFAULT_FLEET_TOKENS
            == GameConstants.STARTING_FLEET_TOKENS
        )
        assert (
            GameStateConstants.DEFAULT_STRATEGY_TOKENS
            == GameConstants.STARTING_STRATEGY_TOKENS
        )

    def test_timeout_constants_are_reasonable(self):
        """Test that timeout constants have reasonable values."""
        # Circuit breaker timeout should be reasonable (1 minute)
        assert 30.0 <= PerformanceConstants.CIRCUIT_BREAKER_TIMEOUT <= 300.0

        # Retry delay should be reasonable (1 second)
        assert 0.1 <= PerformanceConstants.DEFAULT_RETRY_DELAY <= 10.0

        # Operation sleep delay should be very small
        assert 0.001 <= PerformanceConstants.OPERATION_SLEEP_DELAY <= 0.1

        # Thresholds should be reasonable (1 hour)
        assert (
            1800 <= PerformanceConstants.INACTIVE_GAME_THRESHOLD <= 7200
        )  # 30 min to 2 hours
        assert (
            1800 <= PerformanceConstants.OLD_STATE_THRESHOLD <= 7200
        )  # 30 min to 2 hours
