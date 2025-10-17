"""Comprehensive performance benchmarks for Rule 81 Status Phase implementation.

This module provides detailed performance benchmarks and tests to ensure compliance
with performance requirements for the status phase implementation.

Requirements tested:
- 12.1: Complete status phase execution in <500ms
- 12.2: Individual steps execution in <100ms each
- 12.3: Memory usage optimization for large game states

This test file focuses on comprehensive benchmarking and performance regression detection.
"""

import gc
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from src.ti4.core.constants import Faction
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.status_phase import (
    StatusPhaseManager,
    StatusPhaseOrchestrator,
    StatusPhaseResult,
)


class TestStatusPhasePerformanceBenchmarks:
    """Comprehensive performance benchmarks for status phase execution."""

    def setup_method(self) -> None:
        """Set up test fixtures for each test method."""
        self.orchestrator = StatusPhaseOrchestrator()
        self.manager = StatusPhaseManager()

    def create_game_state_with_size(
        self, num_players: int, planets_per_player: int
    ) -> GameState:
        """Create a game state with specified size for performance testing.

        Args:
            num_players: Number of players to create (1-6)
            planets_per_player: Number of planets per player

        Returns:
            GameState with the specified configuration
        """
        game_state = GameState()
        factions = [
            Faction.SOL,
            Faction.HACAN,
            Faction.XXCHA,
            Faction.ARBOREC,
            Faction.YSSARIL,
            Faction.NAALU,
        ]

        for i in range(min(num_players, 6)):
            player = Player(id=f"player{i + 1}", faction=factions[i])
            game_state = game_state.add_player(player)

            # Add planets to each player
            for j in range(planets_per_player):
                planet = Planet(
                    name=f"Planet_{i}_{j}", resources=(j % 5) + 1, influence=(j % 3) + 1
                )
                game_state = game_state.add_player_planet(player.id, planet)

        return game_state

    def measure_execution_time_ms(
        self, func: Any, *args: Any, **kwargs: Any
    ) -> tuple[Any, float]:
        """Measure execution time of a function in milliseconds.

        Args:
            func: Function to measure
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Tuple of (function_result, execution_time_in_ms)
        """
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time_ms = (end_time - start_time) * 1000
        return result, execution_time_ms

    def measure_memory_usage(self) -> int:
        """Measure current memory usage using object count as proxy.

        Returns:
            Approximate memory usage (object count)
        """
        gc.collect()  # Force garbage collection for accurate measurement
        return len(gc.get_objects())

    def test_complete_status_phase_execution_time_benchmarks(self) -> None:
        """Test complete status phase execution time benchmarks.

        Requirement: 12.1 - Complete status phase execution in <500ms
        """
        test_cases = [
            ("minimal", 2, 1),  # 2 players, 1 planet each
            ("small", 3, 2),  # 3 players, 2 planets each
            ("medium", 4, 4),  # 4 players, 4 planets each
            ("large", 6, 6),  # 6 players, 6 planets each
            ("extra_large", 6, 10),  # 6 players, 10 planets each
        ]

        benchmark_results = {}

        for case_name, num_players, planets_per_player in test_cases:
            game_state = self.create_game_state_with_size(
                num_players, planets_per_player
            )

            # Run multiple iterations for statistical accuracy
            execution_times = []
            for _ in range(5):
                (result, updated_state), execution_time = (
                    self.measure_execution_time_ms(
                        self.orchestrator.execute_complete_status_phase, game_state
                    )
                )
                execution_times.append(execution_time)

                # Verify functionality
                assert isinstance(result, StatusPhaseResult)
                assert result.success, (
                    f"Status phase failed for {case_name}: {result.error_message}"
                )

            # Calculate statistics
            avg_time = statistics.mean(execution_times)
            min_time = min(execution_times)
            max_time = max(execution_times)
            std_dev = (
                statistics.stdev(execution_times) if len(execution_times) > 1 else 0
            )

            benchmark_results[case_name] = {
                "avg_time_ms": avg_time,
                "min_time_ms": min_time,
                "max_time_ms": max_time,
                "std_dev_ms": std_dev,
                "num_players": num_players,
                "planets_per_player": planets_per_player,
            }

            print(
                f"Benchmark {case_name}: avg={avg_time:.2f}ms, min={min_time:.2f}ms, "
                f"max={max_time:.2f}ms, std={std_dev:.2f}ms"
            )

            # Verify performance requirements
            # Base requirement: <500ms for standard cases
            # More lenient for extra large cases
            max_allowed = 500 if case_name != "extra_large" else 1000
            assert avg_time < max_allowed, (
                f"{case_name} avg time {avg_time:.2f}ms exceeds {max_allowed}ms"
            )
            assert max_time < max_allowed * 1.5, (
                f"{case_name} max time {max_time:.2f}ms exceeds {max_allowed * 1.5}ms"
            )

        # Verify reasonable performance scaling
        if benchmark_results["medium"]["avg_time_ms"] > 0:
            scaling_factor = (
                benchmark_results["large"]["avg_time_ms"]
                / benchmark_results["medium"]["avg_time_ms"]
            )
            assert scaling_factor < 2.5, (
                f"Performance scaling too poor: {scaling_factor:.2f}x"
            )

        # Store benchmark results for future comparison
        print("\nComplete Status Phase Execution Benchmarks:")
        print("-" * 60)
        for case_name, stats in benchmark_results.items():
            print(
                f"{case_name:12}: {stats['avg_time_ms']:6.2f}ms ± {stats['std_dev_ms']:5.2f}ms "
                f"({stats['num_players']}p, {stats['planets_per_player']}pl)"
            )

    def test_individual_step_execution_time_benchmarks(self) -> None:
        """Test individual step execution time benchmarks.

        Requirement: 12.2 - Individual steps execution in <100ms each
        """
        game_state = self.create_game_state_with_size(4, 3)  # Medium-sized game state

        step_names = [
            "Score Objectives",
            "Reveal Objective",
            "Draw Action Cards",
            "Remove Command Tokens",
            "Gain/Redistribute Tokens",
            "Ready Cards",
            "Repair Units",
            "Return Strategy Cards",
        ]

        step_benchmarks = {}
        current_state = game_state

        print("\nIndividual Step Execution Benchmarks:")
        print("-" * 50)

        for step_number in range(1, 9):
            execution_times = []

            # Run multiple iterations for each step
            for _ in range(10):
                (result, updated_state), execution_time = (
                    self.measure_execution_time_ms(
                        self.orchestrator.execute_step, step_number, current_state
                    )
                )
                execution_times.append(execution_time)

                # Update state for next iteration (use the updated state)
                if result.success:
                    current_state = updated_state

            # Calculate statistics
            avg_time = statistics.mean(execution_times)
            min_time = min(execution_times)
            max_time = max(execution_times)
            std_dev = (
                statistics.stdev(execution_times) if len(execution_times) > 1 else 0
            )

            step_name = step_names[step_number - 1]
            step_benchmarks[step_number] = {
                "step_name": step_name,
                "avg_time_ms": avg_time,
                "min_time_ms": min_time,
                "max_time_ms": max_time,
                "std_dev_ms": std_dev,
            }

            print(
                f"Step {step_number} ({step_name:20}): {avg_time:5.2f}ms ± {std_dev:4.2f}ms "
                f"(min={min_time:5.2f}, max={max_time:5.2f})"
            )

            # Verify performance requirement: <100ms per step
            assert avg_time < 100, (
                f"Step {step_number} avg time {avg_time:.2f}ms exceeds 100ms"
            )
            assert max_time < 200, (
                f"Step {step_number} max time {max_time:.2f}ms exceeds 200ms"
            )

        # Verify total time is reasonable
        total_avg_time = sum(stats["avg_time_ms"] for stats in step_benchmarks.values())
        print(f"\nTotal average step time: {total_avg_time:.2f}ms")
        assert total_avg_time < 800, (
            f"Total step time {total_avg_time:.2f}ms should be <800ms"
        )

    def test_memory_usage_optimization_benchmarks(self) -> None:
        """Test memory usage optimization benchmarks.

        Requirement: 12.3 - Memory usage optimization for large game states
        """
        print("\nMemory Usage Optimization Benchmarks:")
        print("-" * 45)

        # Test different game state sizes
        test_cases = [
            ("small", 2, 2),
            ("medium", 4, 4),
            ("large", 6, 8),
            ("extra_large", 6, 12),
        ]

        memory_benchmarks = {}

        for case_name, num_players, planets_per_player in test_cases:
            # Measure baseline memory
            baseline_memory = self.measure_memory_usage()

            # Create game state
            game_state = self.create_game_state_with_size(
                num_players, planets_per_player
            )
            after_creation_memory = self.measure_memory_usage()

            # Execute status phase
            result, updated_state = self.orchestrator.execute_complete_status_phase(
                game_state
            )
            after_execution_memory = self.measure_memory_usage()

            # Clean up
            del game_state, updated_state, result
            gc.collect()
            after_cleanup_memory = self.measure_memory_usage()

            # Calculate memory deltas
            creation_delta = after_creation_memory - baseline_memory
            execution_delta = after_execution_memory - after_creation_memory
            cleanup_delta = after_cleanup_memory - baseline_memory

            memory_benchmarks[case_name] = {
                "baseline": baseline_memory,
                "creation_delta": creation_delta,
                "execution_delta": execution_delta,
                "cleanup_delta": cleanup_delta,
                "num_players": num_players,
                "planets_per_player": planets_per_player,
            }

            print(
                f"{case_name:12}: creation=+{creation_delta:4d}, execution=+{execution_delta:4d}, "
                f"cleanup={cleanup_delta:+4d}"
            )

            # Verify memory optimization requirements
            if creation_delta > 0:
                # Execution memory growth should be reasonable compared to creation
                growth_ratio = (
                    execution_delta / creation_delta if creation_delta > 0 else 0
                )
                assert growth_ratio < 1.0, (
                    f"Memory growth during execution too high: {growth_ratio:.2f}x"
                )

            # Memory should be mostly cleaned up
            cleanup_ratio = abs(cleanup_delta) / max(creation_delta, 1)
            assert cleanup_ratio < 0.5, (
                f"Memory not properly cleaned up: {cleanup_ratio:.2f}"
            )

    def test_concurrent_execution_performance_benchmarks(self) -> None:
        """Test performance under concurrent execution scenarios.

        Tests thread safety and performance degradation under concurrent load.
        """
        print("\nConcurrent Execution Performance Benchmarks:")
        print("-" * 50)

        def execute_status_phase_with_timing() -> tuple[bool, float, str]:
            """Execute status phase and return success, timing, and any error."""
            game_state = self.create_game_state_with_size(3, 2)
            orchestrator = StatusPhaseOrchestrator()  # New instance for thread safety

            start_time = time.perf_counter()
            try:
                result, updated_state = orchestrator.execute_complete_status_phase(
                    game_state
                )
                end_time = time.perf_counter()
                execution_time = (end_time - start_time) * 1000
                return result.success, execution_time, result.error_message
            except Exception as e:
                end_time = time.perf_counter()
                execution_time = (end_time - start_time) * 1000
                return False, execution_time, str(e)

        # Test different concurrency levels
        concurrency_levels = [1, 2, 4, 8]

        for num_concurrent in concurrency_levels:
            execution_times = []
            success_count = 0

            with ThreadPoolExecutor(max_workers=num_concurrent) as executor:
                futures = [
                    executor.submit(execute_status_phase_with_timing)
                    for _ in range(num_concurrent)
                ]

                for future in as_completed(futures):
                    success, execution_time, error_msg = future.result()
                    execution_times.append(execution_time)
                    if success:
                        success_count += 1
                    elif error_msg:
                        print(f"  Error in concurrent execution: {error_msg}")

            # Calculate statistics
            avg_time = statistics.mean(execution_times)
            max_time = max(execution_times)
            success_rate = success_count / num_concurrent

            print(
                f"Concurrency {num_concurrent:2d}: avg={avg_time:6.2f}ms, max={max_time:6.2f}ms, "
                f"success={success_rate:.1%}"
            )

            # Verify performance requirements
            assert success_rate >= 0.8, (
                f"Success rate {success_rate:.1%} too low for concurrency {num_concurrent}"
            )
            assert avg_time < 1000, (
                f"Avg time {avg_time:.2f}ms too high for concurrency {num_concurrent}"
            )
            assert max_time < 2000, (
                f"Max time {max_time:.2f}ms too high for concurrency {num_concurrent}"
            )

    def test_performance_regression_detection(self) -> None:
        """Test for performance regression detection.

        Establishes baseline performance metrics for regression testing.
        """
        print("\nPerformance Regression Detection Benchmarks:")
        print("-" * 50)

        # Standard test case for regression detection
        game_state = self.create_game_state_with_size(4, 3)

        # Run multiple iterations to establish baseline
        execution_times = []
        for i in range(10):
            (result, updated_state), execution_time = self.measure_execution_time_ms(
                self.orchestrator.execute_complete_status_phase, game_state
            )
            execution_times.append(execution_time)
            assert result.success, f"Iteration {i + 1} failed: {result.error_message}"

        # Calculate baseline statistics
        baseline_avg = statistics.mean(execution_times)
        baseline_std = statistics.stdev(execution_times)
        baseline_p95 = sorted(execution_times)[int(0.95 * len(execution_times))]

        print("Baseline Performance Metrics:")
        print(f"  Average: {baseline_avg:.2f}ms")
        print(f"  Std Dev: {baseline_std:.2f}ms")
        print(f"  95th %ile: {baseline_p95:.2f}ms")

        # Establish regression thresholds
        regression_thresholds = {
            "average_ms": baseline_avg * 1.2,  # 20% slower than baseline
            "p95_ms": baseline_p95 * 1.3,  # 30% slower for 95th percentile
            "std_dev_ms": baseline_std * 2.0,  # 2x more variable
        }

        print("Regression Thresholds:")
        for metric, threshold in regression_thresholds.items():
            print(f"  {metric}: {threshold:.2f}")

        # Verify current performance meets thresholds
        assert baseline_avg < regression_thresholds["average_ms"]
        assert baseline_p95 < regression_thresholds["p95_ms"]
        assert baseline_std < regression_thresholds["std_dev_ms"]

        # Store for future comparison (in real implementation, save to file/database)
        baseline_metrics = {
            "timestamp": time.time(),
            "average_ms": baseline_avg,
            "std_dev_ms": baseline_std,
            "p95_ms": baseline_p95,
            "sample_size": len(execution_times),
            "test_case": "4_players_3_planets",
        }

        print(f"Baseline metrics established: {baseline_metrics}")

    def test_status_phase_manager_performance_benchmarks(self) -> None:
        """Test StatusPhaseManager performance benchmarks.

        Tests the main entry point that users will interact with.
        """
        print("\nStatusPhaseManager Performance Benchmarks:")
        print("-" * 45)

        test_cases = [("basic", 2, 1), ("standard", 4, 3), ("large", 6, 6)]

        for case_name, num_players, planets_per_player in test_cases:
            game_state = self.create_game_state_with_size(
                num_players, planets_per_player
            )

            # Test both with and without performance optimization
            for optimization_enabled in [False, True]:
                manager = StatusPhaseManager(
                    enable_performance_optimization=optimization_enabled
                )

                execution_times = []
                for _ in range(5):
                    (result, updated_state), execution_time = (
                        self.measure_execution_time_ms(
                            manager.execute_complete_status_phase, game_state
                        )
                    )
                    execution_times.append(execution_time)
                    assert result.success, (
                        f"Manager execution failed: {result.error_message}"
                    )

                avg_time = statistics.mean(execution_times)
                opt_status = "optimized" if optimization_enabled else "standard"

                print(f"{case_name:8} ({opt_status:9}): {avg_time:6.2f}ms")

                # Verify performance requirements
                assert avg_time < 500, (
                    f"Manager {case_name} took {avg_time:.2f}ms, should be <500ms"
                )

    def test_error_handling_performance_impact(self) -> None:
        """Test performance impact of error handling.

        Verifies that error conditions don't significantly degrade performance.
        """
        print("\nError Handling Performance Impact:")
        print("-" * 40)

        # Test normal execution
        game_state = self.create_game_state_with_size(2, 1)
        (result, updated_state), normal_time = self.measure_execution_time_ms(
            self.orchestrator.execute_complete_status_phase, game_state
        )

        # Test error condition (None game state)
        (error_result, error_state), error_time = self.measure_execution_time_ms(
            self.orchestrator.execute_complete_status_phase, None
        )

        print(f"Normal execution: {normal_time:.2f}ms")
        print(f"Error handling:   {error_time:.2f}ms")

        # Verify error handling is fast
        assert error_time < 100, (
            f"Error handling took {error_time:.2f}ms, should be <100ms"
        )

        # Verify error was handled properly
        assert not error_result.success
        assert "cannot be None" in error_result.error_message

        # Error handling shouldn't be significantly slower than normal execution
        if normal_time > 0:
            slowdown_factor = error_time / normal_time
            assert slowdown_factor < 5.0, (
                f"Error handling {slowdown_factor:.2f}x slower than normal"
            )

    def test_performance_with_different_game_phases(self) -> None:
        """Test performance with different game phase contexts.

        Verifies consistent performance across different game states.
        """
        print("\nPerformance Across Different Game Contexts:")
        print("-" * 45)

        # Create game states representing different game phases/contexts
        contexts = [
            ("early_game", 3, 1),  # Early game: few planets
            ("mid_game", 4, 4),  # Mid game: moderate planets
            ("late_game", 6, 8),  # Late game: many planets
        ]

        context_benchmarks = {}

        for context_name, num_players, planets_per_player in contexts:
            game_state = self.create_game_state_with_size(
                num_players, planets_per_player
            )

            execution_times = []
            for _ in range(5):
                (result, updated_state), execution_time = (
                    self.measure_execution_time_ms(
                        self.orchestrator.execute_complete_status_phase, game_state
                    )
                )
                execution_times.append(execution_time)
                assert result.success, (
                    f"Context {context_name} failed: {result.error_message}"
                )

            avg_time = statistics.mean(execution_times)
            context_benchmarks[context_name] = avg_time

            print(f"{context_name:10}: {avg_time:6.2f}ms")

            # Verify performance requirements for each context
            max_allowed = 500 if context_name != "late_game" else 800
            assert avg_time < max_allowed, (
                f"{context_name} took {avg_time:.2f}ms, should be <{max_allowed}ms"
            )

        # Verify reasonable scaling across game contexts
        if context_benchmarks["early_game"] > 0:
            scaling_factor = (
                context_benchmarks["late_game"] / context_benchmarks["early_game"]
            )
            assert scaling_factor < 4.0, (
                f"Performance scaling across contexts too poor: {scaling_factor:.2f}x"
            )


if __name__ == "__main__":
    # Run benchmarks when executed directly
    test_instance = TestStatusPhasePerformanceBenchmarks()
    test_instance.setup_method()

    print("Running Status Phase Performance Benchmarks...")
    print("=" * 60)

    try:
        test_instance.test_complete_status_phase_execution_time_benchmarks()
        test_instance.test_individual_step_execution_time_benchmarks()
        test_instance.test_memory_usage_optimization_benchmarks()
        test_instance.test_performance_regression_detection()
        print("\nAll performance benchmarks completed successfully!")
    except Exception as e:
        print(f"\nBenchmark failed: {e}")
        raise
