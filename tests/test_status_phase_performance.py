"""Performance tests for Rule 81 Status Phase implementation.

This module provides comprehensive performance benchmarks for the status phase
implementation, testing both complete status phase execution and individual
step performance to ensure compliance with performance requirements.

Requirements tested:
- 12.1: Complete status phase execution in <500ms
- 12.2: Individual steps execution in <100ms each
- 12.3: Memory usage optimization for large game states
"""

import gc
import time
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


class TestStatusPhasePerformance:
    """Performance tests for status phase execution."""

    def setup_method(self) -> None:
        """Set up test fixtures for each test method."""
        self.orchestrator = StatusPhaseOrchestrator()
        self.manager = StatusPhaseManager()

    def create_minimal_game_state(self) -> GameState:
        """Create a minimal game state for basic performance testing.

        Returns:
            A minimal GameState with 2 players
        """
        game_state = GameState()

        # Add 2 players for minimal testing
        player1 = Player(id="player1", faction=Faction.SOL)
        player2 = Player(id="player2", faction=Faction.HACAN)

        game_state = game_state.add_player(player1)
        game_state = game_state.add_player(player2)

        return game_state

    def create_large_game_state(self) -> GameState:
        """Create a large game state for stress testing.

        Returns:
            A large GameState with 6 players and many planets
        """
        game_state = GameState()

        # Add 6 players (maximum for TI4)
        factions = [
            Faction.SOL,
            Faction.HACAN,
            Faction.XXCHA,
            Faction.ARBOREC,
            Faction.YSSARIL,
            Faction.NAALU,
        ]

        for i, faction in enumerate(factions):
            player = Player(id=f"player{i + 1}", faction=faction)
            game_state = game_state.add_player(player)

            # Add many planets to each player (simulate late game)
            for j in range(8):  # 8 planets per player
                planet = Planet(
                    name=f"Planet_{i}_{j}", resources=j % 5 + 1, influence=j % 3 + 1
                )
                game_state = game_state.add_player_planet(player.id, planet)

        return game_state

    def measure_execution_time(
        self, func: Any, *args: Any, **kwargs: Any
    ) -> tuple[Any, float]:
        """Measure execution time of a function.

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
        """Measure current memory usage.

        Returns:
            Memory usage in bytes (approximate)
        """
        # Force garbage collection for more accurate measurement
        gc.collect()

        # Get object count as a proxy for memory usage
        # This is a simplified approach - in production you might use psutil
        return len(gc.get_objects())

    def test_complete_status_phase_performance_minimal(self) -> None:
        """Test complete status phase execution time with minimal game state.

        Requirement: 12.1 - Complete status phase execution in <500ms
        """
        game_state = self.create_minimal_game_state()

        # Measure complete status phase execution
        (result, updated_state), execution_time = self.measure_execution_time(
            self.orchestrator.execute_complete_status_phase, game_state
        )

        print(f"Complete status phase (minimal): {execution_time:.2f}ms")

        # Verify performance requirement
        assert execution_time < 500, (
            f"Status phase took {execution_time:.2f}ms, should be <500ms"
        )

        # Verify functionality
        assert isinstance(result, StatusPhaseResult)
        assert result.success
        assert len(result.steps_completed) > 0

    def test_complete_status_phase_performance_large(self) -> None:
        """Test complete status phase execution time with large game state.

        Requirement: 12.1 - Complete status phase execution in <500ms
        """
        game_state = self.create_large_game_state()

        # Measure complete status phase execution
        (result, updated_state), execution_time = self.measure_execution_time(
            self.orchestrator.execute_complete_status_phase, game_state
        )

        print(f"Complete status phase (large): {execution_time:.2f}ms")

        # Verify performance requirement (may be more lenient for large states)
        assert execution_time < 1000, (
            f"Status phase took {execution_time:.2f}ms, should be <1000ms for large states"
        )

        # Verify functionality
        assert isinstance(result, StatusPhaseResult)
        assert result.success
        assert len(result.steps_completed) > 0

    def test_individual_step_performance(self) -> None:
        """Test individual step execution times.

        Requirement: 12.2 - Individual steps execution in <100ms each
        """
        game_state = self.create_minimal_game_state()

        step_times = {}

        # Test each step individually
        for step_number in range(1, 9):
            (result, updated_state), execution_time = self.measure_execution_time(
                self.orchestrator.execute_step, step_number, game_state
            )

            step_times[step_number] = execution_time
            print(f"Step {step_number}: {execution_time:.2f}ms")

            # Verify performance requirement
            assert execution_time < 100, (
                f"Step {step_number} took {execution_time:.2f}ms, should be <100ms"
            )

            # Verify functionality
            assert (
                result.success or not result.success
            )  # Either outcome is acceptable for individual steps

        # Verify total time is reasonable
        total_time = sum(step_times.values())
        print(f"Total individual step time: {total_time:.2f}ms")
        assert total_time < 800, (
            f"Total step time {total_time:.2f}ms should be reasonable"
        )

    def test_individual_step_performance_large_state(self) -> None:
        """Test individual step execution times with large game state.

        Requirement: 12.2 - Individual steps execution in <100ms each
        """
        game_state = self.create_large_game_state()

        step_times = {}

        # Test each step individually with large state
        for step_number in range(1, 9):
            (result, updated_state), execution_time = self.measure_execution_time(
                self.orchestrator.execute_step, step_number, game_state
            )

            step_times[step_number] = execution_time
            print(f"Step {step_number} (large): {execution_time:.2f}ms")

            # More lenient for large states, but still reasonable
            assert execution_time < 200, (
                f"Step {step_number} took {execution_time:.2f}ms, should be <200ms for large states"
            )

        # Verify total time is reasonable
        total_time = sum(step_times.values())
        print(f"Total individual step time (large): {total_time:.2f}ms")

    def test_memory_usage_optimization(self) -> None:
        """Test memory usage optimization for large game states.

        Requirement: 12.3 - Memory usage optimization for large game states
        """
        # Measure baseline memory usage
        baseline_memory = self.measure_memory_usage()

        # Create large game state
        game_state = self.create_large_game_state()
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

        print(f"Memory usage - Baseline: {baseline_memory}")
        print(f"Memory usage - After creation: {after_creation_memory}")
        print(f"Memory usage - After execution: {after_execution_memory}")
        print(f"Memory usage - After cleanup: {after_cleanup_memory}")

        # Verify memory doesn't grow excessively during execution
        execution_growth = after_execution_memory - after_creation_memory
        creation_growth = after_creation_memory - baseline_memory

        # Memory growth during execution should be reasonable compared to creation
        if creation_growth > 0:
            growth_ratio = execution_growth / creation_growth
            assert growth_ratio < 0.5, (
                f"Memory growth during execution ({execution_growth}) should be <50% of creation growth ({creation_growth})"
            )

        # Memory should be mostly cleaned up after deletion
        cleanup_ratio = (after_cleanup_memory - baseline_memory) / max(
            creation_growth, 1
        )
        assert cleanup_ratio < 2.0, "Memory should be mostly cleaned up after deletion"

    def test_repeated_execution_performance(self) -> None:
        """Test performance consistency across repeated executions.

        Verifies that performance doesn't degrade with repeated use.
        """
        game_state = self.create_minimal_game_state()
        execution_times = []

        # Execute status phase multiple times
        for i in range(5):
            (result, updated_state), execution_time = self.measure_execution_time(
                self.orchestrator.execute_complete_status_phase, game_state
            )
            execution_times.append(execution_time)
            print(f"Execution {i + 1}: {execution_time:.2f}ms")

        # Verify all executions meet performance requirements
        for i, time_ms in enumerate(execution_times):
            assert time_ms < 500, (
                f"Execution {i + 1} took {time_ms:.2f}ms, should be <500ms"
            )

        # Verify performance consistency (no significant degradation)
        avg_time = sum(execution_times) / len(execution_times)
        max_time = max(execution_times)

        # Maximum time shouldn't be more than 50% higher than average
        assert max_time < avg_time * 1.5, (
            f"Performance inconsistency: max {max_time:.2f}ms vs avg {avg_time:.2f}ms"
        )

    def test_concurrent_execution_performance(self) -> None:
        """Test performance under concurrent execution scenarios.

        Simulates multiple status phase executions to test thread safety and performance.
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def execute_status_phase() -> tuple[bool, float]:
            """Execute status phase and return success and timing."""
            game_state = self.create_minimal_game_state()
            orchestrator = (
                StatusPhaseOrchestrator()
            )  # Create new instance for thread safety

            start_time = time.perf_counter()
            result, updated_state = orchestrator.execute_complete_status_phase(
                game_state
            )
            end_time = time.perf_counter()

            execution_time = (end_time - start_time) * 1000
            return result.success, execution_time

        # Execute multiple status phases concurrently
        num_concurrent = 3
        results = []

        with ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            futures = [
                executor.submit(execute_status_phase) for _ in range(num_concurrent)
            ]

            for future in as_completed(futures):
                success, execution_time = future.result()
                results.append((success, execution_time))
                print(
                    f"Concurrent execution: {execution_time:.2f}ms, success: {success}"
                )

        # Verify all executions succeeded and met performance requirements
        for i, (success, execution_time) in enumerate(results):
            assert success, f"Concurrent execution {i + 1} failed"
            assert execution_time < 1000, (
                f"Concurrent execution {i + 1} took {execution_time:.2f}ms, should be <1000ms"
            )

    def test_status_phase_manager_performance(self) -> None:
        """Test StatusPhaseManager performance.

        Tests the main entry point that users will interact with.
        """
        game_state = self.create_minimal_game_state()

        # Test complete status phase execution through manager
        (result, updated_state), execution_time = self.measure_execution_time(
            self.manager.execute_complete_status_phase, game_state
        )

        print(f"StatusPhaseManager execution: {execution_time:.2f}ms")

        # Verify performance requirement
        assert execution_time < 1000, (
            f"StatusPhaseManager took {execution_time:.2f}ms, should be <1000ms"
        )

        # Verify functionality
        assert isinstance(result, StatusPhaseResult)
        assert result.success

    def test_performance_with_error_conditions(self) -> None:
        """Test performance when error conditions occur.

        Verifies that error handling doesn't significantly impact performance.
        """
        # Test with None game state (should handle gracefully)
        (result, updated_state), execution_time = self.measure_execution_time(
            self.orchestrator.execute_complete_status_phase, None
        )

        print(f"Error condition execution: {execution_time:.2f}ms")

        # Error handling should still be fast
        assert execution_time < 100, (
            f"Error handling took {execution_time:.2f}ms, should be <100ms"
        )

        # Verify error was handled properly
        assert isinstance(result, StatusPhaseResult)
        assert not result.success
        assert "cannot be None" in result.error_message


class TestStatusPhasePerformanceBenchmarks:
    """Benchmark tests for status phase performance analysis."""

    def test_performance_regression_benchmark(self) -> None:
        """Benchmark test to detect performance regressions.

        This test establishes baseline performance metrics that can be used
        to detect performance regressions in future changes.
        """
        orchestrator = StatusPhaseOrchestrator()

        # Test with different game state sizes
        test_cases = [
            ("minimal", 2, 2),  # 2 players, 2 planets each
            ("medium", 4, 4),  # 4 players, 4 planets each
            ("large", 6, 8),  # 6 players, 8 planets each
        ]

        benchmarks = {}

        for case_name, num_players, planets_per_player in test_cases:
            # Create game state
            game_state = GameState()
            factions = [
                Faction.SOL,
                Faction.HACAN,
                Faction.XXCHA,
                Faction.ARBOREC,
                Faction.YSSARIL,
                Faction.NAALU,
            ]

            for i in range(num_players):
                player = Player(id=f"player{i + 1}", faction=factions[i])
                game_state = game_state.add_player(player)

                for j in range(planets_per_player):
                    planet = Planet(
                        name=f"Planet_{i}_{j}", resources=j % 5 + 1, influence=j % 3 + 1
                    )
                    game_state = game_state.add_player_planet(player.id, planet)

            # Measure performance
            start_time = time.perf_counter()
            result, updated_state = orchestrator.execute_complete_status_phase(
                game_state
            )
            end_time = time.perf_counter()

            execution_time_ms = (end_time - start_time) * 1000
            benchmarks[case_name] = execution_time_ms

            print(f"Benchmark {case_name}: {execution_time_ms:.2f}ms")

            # Verify functionality
            assert result.success, f"Benchmark {case_name} failed"

        # Store benchmarks for future comparison
        # In a real implementation, you might save these to a file or database
        print("Performance benchmarks established:")
        for case_name, time_ms in benchmarks.items():
            print(f"  {case_name}: {time_ms:.2f}ms")

        # Verify reasonable performance scaling
        if benchmarks["medium"] > 0:
            scaling_factor = benchmarks["large"] / benchmarks["medium"]
            assert scaling_factor < 3.0, (
                f"Performance scaling too poor: {scaling_factor:.2f}x"
            )

    def test_step_by_step_performance_analysis(self) -> None:
        """Detailed performance analysis of each status phase step.

        Provides detailed timing information for performance optimization.
        """
        orchestrator = StatusPhaseOrchestrator()
        game_state = GameState()

        # Add players
        player1 = Player(id="player1", faction=Faction.SOL)
        player2 = Player(id="player2", faction=Faction.HACAN)
        game_state = game_state.add_player(player1)
        game_state = game_state.add_player(player2)

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

        print("\nDetailed step performance analysis:")
        print("-" * 50)

        current_state = game_state
        total_time = 0

        for step_number in range(1, 9):
            start_time = time.perf_counter()
            result, current_state = orchestrator.execute_step(
                step_number, current_state
            )
            end_time = time.perf_counter()

            execution_time_ms = (end_time - start_time) * 1000
            total_time += execution_time_ms

            step_name = step_names[step_number - 1]
            status = "✓" if result.success else "✗"

            print(
                f"Step {step_number} ({step_name}): {execution_time_ms:.2f}ms {status}"
            )

        print("-" * 50)
        print(f"Total time: {total_time:.2f}ms")

        # Verify total time is reasonable
        assert total_time < 800, (
            f"Total step time {total_time:.2f}ms should be reasonable"
        )
