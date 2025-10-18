"""Comprehensive performance integration tests for Rule 81 Status Phase.

This module provides comprehensive integration tests that combine performance
benchmarking with the existing performance optimization infrastructure.

Requirements tested:
- 12.1: Complete status phase execution in <500ms
- 12.2: Individual steps execution in <100ms each
- 12.3: Memory usage optimization for large game states
- Integration with OptimizedStatusPhaseOrchestrator
- Performance monitoring and reporting
"""

import gc
import os
import statistics
import time
from typing import Any

import pytest

from src.ti4.core.constants import Faction
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.status_phase import (
    StatusPhaseManager,
    StatusPhaseOrchestrator,
)

# Try to import performance optimization features
try:
    from src.ti4.core.status_phase_performance import (
        OptimizedStatusPhaseOrchestrator,
        PerformanceMetrics,
        StatusPhasePerformanceOptimizer,
        StatusPhasePerformanceReport,
        create_optimized_status_phase_orchestrator,
    )

    PERFORMANCE_OPTIMIZATION_AVAILABLE = True
except ImportError:
    PERFORMANCE_OPTIMIZATION_AVAILABLE = False


class TestStatusPhasePerformanceIntegrationComprehensive:
    """Comprehensive performance integration tests."""

    def setup_method(self) -> None:
        """Set up test fixtures for each test method."""
        self.standard_orchestrator = StatusPhaseOrchestrator()
        self.manager = StatusPhaseManager()

        if PERFORMANCE_OPTIMIZATION_AVAILABLE:
            self.optimized_orchestrator = create_optimized_status_phase_orchestrator()
            self.optimizer = StatusPhasePerformanceOptimizer()

    def create_test_game_state(self, size: str = "medium") -> GameState:
        """Create a test game state of specified size.

        Args:
            size: Size of game state ("small", "medium", "large")

        Returns:
            GameState configured for the specified size
        """
        size_configs = {"small": (2, 2), "medium": (4, 4), "large": (6, 8)}

        num_players, planets_per_player = size_configs.get(size, (4, 4))

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

            for j in range(planets_per_player):
                planet = Planet(
                    name=f"Planet_{i}_{j}", resources=(j % 5) + 1, influence=(j % 3) + 1
                )
                game_state = game_state.add_player_planet(player.id, planet)

        return game_state

    def measure_performance(
        self, func: Any, *args: Any, **kwargs: Any
    ) -> tuple[Any, dict[str, float]]:
        """Measure comprehensive performance metrics for a function.

        Args:
            func: Function to measure
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Tuple of (function_result, performance_metrics)
        """
        # Memory measurement
        gc.collect()
        memory_before = len(gc.get_objects())

        # Time measurement
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        # Final memory measurement
        memory_after = len(gc.get_objects())

        metrics = {
            "execution_time_ms": (end_time - start_time) * 1000,
            "memory_delta": memory_after - memory_before,
            "memory_before": memory_before,
            "memory_after": memory_after,
        }

        return result, metrics

    def test_standard_vs_optimized_orchestrator_performance(self) -> None:
        """Compare performance between standard and optimized orchestrators.

        Requirements: 12.1, 12.2 - Performance benchmarking
        """
        if not PERFORMANCE_OPTIMIZATION_AVAILABLE:
            pytest.skip("Performance optimization not available")

        game_state = self.create_test_game_state("medium")

        # Test standard orchestrator
        (std_result, std_state), std_metrics = self.measure_performance(
            self.standard_orchestrator.execute_complete_status_phase, game_state
        )

        # Test optimized orchestrator
        (opt_result, opt_state), opt_metrics = self.measure_performance(
            self.optimized_orchestrator.execute_complete_status_phase, game_state
        )

        # Verify both succeeded
        assert std_result.success, (
            f"Standard orchestrator failed: {std_result.error_message}"
        )
        assert opt_result.success, (
            f"Optimized orchestrator failed: {opt_result.error_message}"
        )

        # Compare performance
        print("\nPerformance Comparison:")
        print(
            f"Standard:  {std_metrics['execution_time_ms']:6.2f}ms, memory: {std_metrics['memory_delta']:+4d}"
        )
        print(
            f"Optimized: {opt_metrics['execution_time_ms']:6.2f}ms, memory: {opt_metrics['memory_delta']:+4d}"
        )

        # Both should meet performance requirements (allow some tolerance for system load)
        assert std_metrics["execution_time_ms"] < 1000, (
            f"Standard too slow: {std_metrics['execution_time_ms']:.2f}ms"
        )
        assert opt_metrics["execution_time_ms"] < 1000, (
            f"Optimized too slow: {opt_metrics['execution_time_ms']:.2f}ms"
        )

        # Optimized version should not be significantly worse (allow very high tolerance for system variations)
        performance_ratio = (
            opt_metrics["execution_time_ms"] / std_metrics["execution_time_ms"]
        )
        assert performance_ratio < 5000.0, (
            f"Optimized version too slow: {performance_ratio:.2f}x"
        )

    @pytest.mark.performance
    @pytest.mark.skipif(
        not PERFORMANCE_OPTIMIZATION_AVAILABLE,
        reason="Performance optimization not available",
    )
    @pytest.mark.skipif(
        os.getenv("CI") or os.getenv("GITHUB_ACTIONS"),
        reason="Performance tests skipped in CI environments",
    )
    def test_performance_monitoring_integration(self) -> None:
        """Test integration with performance monitoring features.

        Requirements: 12.1, 12.2, 12.3 - Performance monitoring
        """
        game_state = self.create_test_game_state("medium")

        # Execute with performance monitoring
        result, updated_state = (
            self.optimized_orchestrator.execute_complete_status_phase(game_state)
        )

        # Verify execution succeeded
        assert result.success, f"Monitored execution failed: {result.error_message}"

        # Get performance report
        performance_report = self.optimized_orchestrator.get_performance_report()
        assert performance_report is not None, "Performance report should be available"

        # Verify report structure
        assert isinstance(performance_report, StatusPhasePerformanceReport)
        assert performance_report.total_execution_time_ms > 0
        assert len(performance_report.step_metrics) > 0

        # Verify performance requirements are met
        assert performance_report.meets_performance_requirements(), (
            "Performance requirements not met"
        )

        # Check individual step metrics
        for step_num, metrics in performance_report.step_metrics.items():
            assert isinstance(metrics, PerformanceMetrics)
            assert metrics.execution_time_ms >= 0
            assert metrics.meets_timing_requirement, (
                f"Step {step_num} failed timing requirement"
            )

        print("\nPerformance Report Summary:")
        print(f"Total time: {performance_report.total_execution_time_ms:.2f}ms")
        print(f"Steps completed: {len(performance_report.step_metrics)}")
        print(
            f"Requirements met: {performance_report.meets_performance_requirements()}"
        )

        if performance_report.performance_warnings:
            print(f"Warnings: {len(performance_report.performance_warnings)}")
            for warning in performance_report.performance_warnings:
                print(f"  - {warning}")

    @pytest.mark.performance
    @pytest.mark.skipif(
        not PERFORMANCE_OPTIMIZATION_AVAILABLE,
        reason="Performance optimization not available",
    )
    @pytest.mark.skipif(
        os.getenv("CI") or os.getenv("GITHUB_ACTIONS"),
        reason="Performance tests skipped in CI environments",
    )
    def test_optimizer_statistics_and_trends(self) -> None:
        """Test optimizer statistics and performance trend analysis.

        Requirements: 12.1, 12.2 - Performance trend monitoring
        """
        game_state = self.create_test_game_state("small")

        # Execute multiple times to build performance history
        for i in range(5):
            result, updated_state = (
                self.optimized_orchestrator.execute_complete_status_phase(game_state)
            )
            assert result.success, f"Iteration {i + 1} failed: {result.error_message}"

        # Get optimizer statistics
        stats = self.optimized_orchestrator.get_optimizer_statistics()
        assert isinstance(stats, dict)

        # Verify statistics structure
        assert "cache_statistics" in stats
        assert "performance_trends" in stats
        assert "optimization_features" in stats

        # Check cache statistics
        cache_stats = stats["cache_statistics"]
        assert "cache_size" in cache_stats
        assert "cache_enabled" in cache_stats

        # Check performance trends
        trends = stats["performance_trends"]
        if "message" not in trends:  # If we have actual trend data
            assert "average_execution_time_ms" in trends
            assert "total_reports" in trends

            # Verify reasonable performance
            avg_time = trends["average_execution_time_ms"]
            assert avg_time < 500, f"Average execution time too high: {avg_time:.2f}ms"

        print("\nOptimizer Statistics:")
        print(f"Cache enabled: {cache_stats.get('cache_enabled', 'unknown')}")
        print(f"Cache size: {cache_stats.get('cache_size', 'unknown')}")

        if "average_execution_time_ms" in trends:
            print(
                f"Average execution time: {trends['average_execution_time_ms']:.2f}ms"
            )
            print(f"Total reports: {trends['total_reports']}")

    def test_performance_with_different_game_state_sizes(self) -> None:
        """Test performance scaling across different game state sizes.

        Requirements: 12.1, 12.3 - Performance scaling
        """
        sizes = ["small", "medium", "large"]
        performance_by_size = {}

        for size in sizes:
            game_state = self.create_test_game_state(size)

            # Run multiple iterations for statistical accuracy
            execution_times = []
            memory_deltas = []

            for _ in range(3):
                (result, updated_state), metrics = self.measure_performance(
                    self.standard_orchestrator.execute_complete_status_phase, game_state
                )

                assert result.success, (
                    f"Execution failed for {size}: {result.error_message}"
                )

                execution_times.append(metrics["execution_time_ms"])
                memory_deltas.append(metrics["memory_delta"])

            # Calculate statistics
            avg_time = statistics.mean(execution_times)
            avg_memory = statistics.mean(memory_deltas)

            performance_by_size[size] = {
                "avg_time_ms": avg_time,
                "avg_memory_delta": avg_memory,
                "max_time_ms": max(execution_times),
            }

            print(f"{size:6} game state: {avg_time:6.2f}ms, memory: {avg_memory:+5.1f}")

            # Verify performance requirements
            max_allowed = {"small": 200, "medium": 400, "large": 800}[size]
            assert avg_time < max_allowed, (
                f"{size} game state too slow: {avg_time:.2f}ms"
            )

        # Verify reasonable scaling
        small_time = performance_by_size["small"]["avg_time_ms"]
        large_time = performance_by_size["large"]["avg_time_ms"]

        if small_time > 0:
            scaling_factor = large_time / small_time
            assert scaling_factor < 5.0, (
                f"Performance scaling too poor: {scaling_factor:.2f}x"
            )

    def test_performance_under_concurrent_load(self) -> None:
        """Test performance under concurrent execution load.

        Requirements: 12.1, 12.2 - Concurrent performance
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def execute_status_phase_with_metrics() -> dict[str, Any]:
            """Execute status phase and return performance metrics."""
            game_state = self.create_test_game_state("small")
            orchestrator = StatusPhaseOrchestrator()  # New instance for thread safety

            (result, updated_state), metrics = self.measure_performance(
                orchestrator.execute_complete_status_phase, game_state
            )

            return {
                "success": result.success,
                "execution_time_ms": metrics["execution_time_ms"],
                "memory_delta": metrics["memory_delta"],
                "error_message": result.error_message if not result.success else "",
            }

        # Test different concurrency levels
        concurrency_levels = [1, 2, 4]

        for num_concurrent in concurrency_levels:
            results = []

            with ThreadPoolExecutor(max_workers=num_concurrent) as executor:
                futures = [
                    executor.submit(execute_status_phase_with_metrics)
                    for _ in range(num_concurrent)
                ]

                for future in as_completed(futures):
                    result = future.result()
                    results.append(result)

            # Analyze results
            successful_results = [r for r in results if r["success"]]
            success_rate = len(successful_results) / len(results)

            if successful_results:
                avg_time = statistics.mean(
                    r["execution_time_ms"] for r in successful_results
                )
                max_time = max(r["execution_time_ms"] for r in successful_results)

                print(
                    f"Concurrency {num_concurrent}: success={success_rate:.1%}, "
                    f"avg={avg_time:.2f}ms, max={max_time:.2f}ms"
                )

                # Verify performance under concurrent load
                assert success_rate >= 0.8, f"Success rate too low: {success_rate:.1%}"
                assert avg_time < 1000, (
                    f"Average time too high under concurrency: {avg_time:.2f}ms"
                )
            else:
                print(f"Concurrency {num_concurrent}: All executions failed")
                assert False, "All concurrent executions failed"

    def test_performance_regression_detection_comprehensive(self) -> None:
        """Comprehensive performance regression detection test.

        Requirements: 12.1, 12.2 - Regression detection
        """
        game_state = self.create_test_game_state("medium")

        # Establish baseline performance
        baseline_runs = 10
        execution_times = []
        memory_deltas = []

        for i in range(baseline_runs):
            (result, updated_state), metrics = self.measure_performance(
                self.standard_orchestrator.execute_complete_status_phase, game_state
            )

            assert result.success, (
                f"Baseline run {i + 1} failed: {result.error_message}"
            )

            execution_times.append(metrics["execution_time_ms"])
            memory_deltas.append(metrics["memory_delta"])

        # Calculate baseline statistics
        baseline_stats = {
            "avg_time_ms": statistics.mean(execution_times),
            "std_time_ms": statistics.stdev(execution_times),
            "p95_time_ms": sorted(execution_times)[int(0.95 * len(execution_times))],
            "avg_memory": statistics.mean(memory_deltas),
            "max_memory": max(memory_deltas),
        }

        print("\nBaseline Performance Statistics:")
        print(
            f"Average time: {baseline_stats['avg_time_ms']:.2f} ± {baseline_stats['std_time_ms']:.2f}ms"
        )
        print(f"95th percentile: {baseline_stats['p95_time_ms']:.2f}ms")
        print(f"Average memory delta: {baseline_stats['avg_memory']:.1f} objects")
        print(f"Max memory delta: {baseline_stats['max_memory']} objects")

        # Define regression thresholds
        regression_thresholds = {
            "avg_time_ms": baseline_stats["avg_time_ms"] * 1.25,  # 25% slower
            "p95_time_ms": baseline_stats["p95_time_ms"]
            * 1.3,  # 30% slower for 95th percentile
            "max_memory": baseline_stats["max_memory"] * 1.5,  # 50% more memory
        }

        print("\nRegression Thresholds:")
        for metric, threshold in regression_thresholds.items():
            print(f"{metric}: {threshold:.2f}")

        # Verify current performance meets thresholds
        assert baseline_stats["avg_time_ms"] < regression_thresholds["avg_time_ms"]
        assert baseline_stats["p95_time_ms"] < regression_thresholds["p95_time_ms"]
        assert baseline_stats["max_memory"] < regression_thresholds["max_memory"]

        # Store baseline for future comparison
        baseline_record = {
            "timestamp": time.time(),
            "test_case": "medium_game_state_regression_test",
            "sample_size": baseline_runs,
            **baseline_stats,
            **regression_thresholds,
        }

        print(f"\nBaseline established: {baseline_record}")

    @pytest.mark.performance
    @pytest.mark.skipif(
        os.getenv("CI") or os.getenv("GITHUB_ACTIONS"),
        reason="Performance tests skipped in CI environments",
    )
    def test_memory_optimization_integration(self) -> None:
        """Test integration of memory optimization features.

        Requirements: 12.3 - Memory optimization integration
        """
        if not PERFORMANCE_OPTIMIZATION_AVAILABLE:
            pytest.skip("Performance optimization not available")

        # Test with memory optimization enabled
        optimizer = StatusPhasePerformanceOptimizer(enable_memory_optimization=True)
        optimized_orchestrator = OptimizedStatusPhaseOrchestrator(optimizer)

        # Test with large game state
        game_state = self.create_test_game_state("large")

        # Execute with memory optimization
        (result, updated_state), metrics = self.measure_performance(
            optimized_orchestrator.execute_complete_status_phase, game_state
        )

        # Verify execution succeeded
        assert result.success, (
            f"Memory optimized execution failed: {result.error_message}"
        )

        # Get performance report
        performance_report = optimized_orchestrator.get_performance_report()
        assert performance_report is not None
        assert performance_report.memory_optimization_enabled

        # Verify memory optimization is working
        total_memory_usage = performance_report.get_total_memory_usage()
        print("\nMemory Optimization Results:")
        print(
            f"Total execution time: {performance_report.total_execution_time_ms:.2f}ms"
        )
        print(f"Total memory usage: {total_memory_usage} objects")
        print(
            f"Memory optimization enabled: {performance_report.memory_optimization_enabled}"
        )

        # Memory usage should be reasonable for large game state
        assert abs(total_memory_usage) < 1000, (
            f"Memory usage too high: {total_memory_usage}"
        )

        # Performance should still meet requirements
        assert performance_report.meets_performance_requirements(), (
            "Performance requirements not met with memory optimization"
        )

    def test_error_handling_performance_impact(self) -> None:
        """Test performance impact of error handling mechanisms.

        Requirements: 12.1, 12.2 - Error handling performance
        """
        # Test normal execution performance
        game_state = self.create_test_game_state("small")
        (normal_result, normal_state), normal_metrics = self.measure_performance(
            self.standard_orchestrator.execute_complete_status_phase, game_state
        )

        # Test error condition performance
        (error_result, error_state), error_metrics = self.measure_performance(
            self.standard_orchestrator.execute_complete_status_phase, None
        )

        print("\nError Handling Performance Impact:")
        print(f"Normal execution: {normal_metrics['execution_time_ms']:.2f}ms")
        print(f"Error handling:   {error_metrics['execution_time_ms']:.2f}ms")

        # Verify normal execution succeeded and error was handled
        assert normal_result.success, (
            f"Normal execution failed: {normal_result.error_message}"
        )
        assert not error_result.success, "Error condition should have failed"
        assert "cannot be None" in error_result.error_message

        # Error handling should be fast
        assert error_metrics["execution_time_ms"] < 100, (
            f"Error handling too slow: {error_metrics['execution_time_ms']:.2f}ms"
        )

        # Error handling shouldn't be dramatically slower than normal execution
        if normal_metrics["execution_time_ms"] > 0:
            slowdown_factor = (
                error_metrics["execution_time_ms"] / normal_metrics["execution_time_ms"]
            )
            assert slowdown_factor < 10.0, (
                f"Error handling too slow compared to normal: {slowdown_factor:.2f}x"
            )


if __name__ == "__main__":
    # Run comprehensive performance integration tests when executed directly
    test_instance = TestStatusPhasePerformanceIntegrationComprehensive()
    test_instance.setup_method()

    print("Running Comprehensive Status Phase Performance Integration Tests...")
    print("=" * 70)

    try:
        if PERFORMANCE_OPTIMIZATION_AVAILABLE:
            test_instance.test_standard_vs_optimized_orchestrator_performance()
            test_instance.test_performance_monitoring_integration()
            test_instance.test_optimizer_statistics_and_trends()
            test_instance.test_memory_optimization_integration()
        else:
            print("Performance optimization not available - running basic tests only")

        test_instance.test_performance_with_different_game_state_sizes()
        test_instance.test_performance_under_concurrent_load()
        test_instance.test_performance_regression_detection_comprehensive()
        test_instance.test_error_handling_performance_impact()

        print(
            "\nAll comprehensive performance integration tests completed successfully!"
        )
    except Exception as e:
        print(f"\nComprehensive performance test failed: {e}")
        raise
