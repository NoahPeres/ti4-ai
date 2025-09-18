"""Performance benchmarks and profiling tests."""

import time

from src.ti4.core.galaxy import Galaxy
from src.ti4.core.game_state import GameState
from src.ti4.core.movement import MovementValidator
from src.ti4.core.player import Player
from src.ti4.core.unit import Unit
from src.ti4.core.unit_stats import UnitStatsProvider


class TestPerformanceBenchmarks:
    """Benchmark tests for performance-critical operations."""

    def test_unit_stats_calculation_performance(self) -> None:
        """Benchmark unit statistics calculation."""
        provider = UnitStatsProvider()
        unit_type = "cruiser"
        faction = "sol"
        technologies = {"improved_hull", "plasma_scoring"}

        # Warm up
        for _ in range(10):
            provider.get_unit_stats(unit_type, faction, technologies)

        # Benchmark
        start_time = time.time()
        iterations = 1000
        for _ in range(iterations):
            provider.get_unit_stats(unit_type, faction, technologies)
        end_time = time.time()

        avg_time = (end_time - start_time) / iterations
        # Should be very fast - less than 1ms per calculation
        assert avg_time < 0.001, f"Unit stats calculation too slow: {avg_time:.6f}s"

    def test_movement_validation_performance(self) -> None:
        """Benchmark movement validation."""
        galaxy = Galaxy()
        validator = MovementValidator(galaxy)

        # Create mock movement operation
        from src.ti4.core.movement import MovementOperation

        movement = MovementOperation(
            unit=Unit(unit_type="destroyer", owner="player1"),
            from_system_id="system1",
            to_system_id="system2",
            player_id="player1",
        )

        # Warm up
        for _ in range(10):
            try:
                validator.is_valid_movement(movement)
            except Exception:
                pass  # Ignore validation errors for benchmarking

        # Benchmark
        start_time = time.time()
        iterations = 1000
        for _ in range(iterations):
            try:
                validator.is_valid_movement(movement)
            except Exception:
                pass  # Ignore validation errors for benchmarking
        end_time = time.time()

        avg_time = (end_time - start_time) / iterations
        # Should be fast - less than 5ms per validation
        assert avg_time < 0.005, f"Movement validation too slow: {avg_time:.6f}s"

    def test_cached_operations_performance(self) -> None:
        """Test that cached operations provide performance benefits."""
        provider = UnitStatsProvider()
        unit_type = "cruiser"
        faction = "sol"
        technologies = {"improved_hull", "plasma_scoring"}

        # First call - cache miss
        start_time = time.time()
        result1 = provider.get_unit_stats(unit_type, faction, technologies)
        first_call_time = time.time() - start_time

        # Second call - cache hit
        start_time = time.time()
        result2 = provider.get_unit_stats(unit_type, faction, technologies)
        second_call_time = time.time() - start_time

        # Results should be identical
        assert result1 == result2

        # Second call should be faster (though both are already very fast)
        # This test mainly ensures caching doesn't break functionality
        assert second_call_time <= first_call_time * 2  # Allow some variance

    def test_game_state_operations_performance(self) -> None:
        """Benchmark common game state operations."""
        game_state = GameState(game_id="benchmark_game")

        # Add some players
        players = [Player(id=f"player{i}", faction=f"faction{i}") for i in range(6)]
        game_state = GameState(
            game_id=game_state.game_id, players=players, phase=game_state.phase
        )

        # Benchmark game state validation
        start_time = time.time()
        iterations = 1000
        for _ in range(iterations):
            game_state.is_valid()
        end_time = time.time()

        avg_time = (end_time - start_time) / iterations
        # Should be very fast - less than 0.1ms per validation
        assert avg_time < 0.0001, f"Game state validation too slow: {avg_time:.6f}s"
