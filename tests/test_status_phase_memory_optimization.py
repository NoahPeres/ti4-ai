"""Memory optimization tests for Rule 81 Status Phase implementation.

This module provides comprehensive memory optimization tests to ensure efficient
memory usage during status phase execution, particularly for large game states.

Requirements tested:
- 12.3: Memory usage optimization for large game states
- Memory leak detection and prevention
- Garbage collection efficiency
- Memory usage patterns across different game state sizes
"""

import gc
import sys
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


class MemoryTracker:
    """Utility class for tracking memory usage during tests."""

    def __init__(self) -> None:
        """Initialize memory tracker."""
        self.snapshots: list[dict[str, Any]] = []

    def take_snapshot(self, label: str) -> dict[str, Any]:
        """Take a memory usage snapshot.

        Args:
            label: Description of this snapshot

        Returns:
            Dictionary with memory usage information
        """
        gc.collect()  # Force garbage collection

        snapshot = {
            "label": label,
            "object_count": len(gc.get_objects()),
            "garbage_count": len(gc.garbage),
            "ref_count_total": sys.gettotalrefcount()
            if hasattr(sys, "gettotalrefcount")
            else 0,
        }

        self.snapshots.append(snapshot)
        return snapshot

    def get_memory_delta(self, start_label: str, end_label: str) -> dict[str, Any]:
        """Calculate memory usage delta between two snapshots.

        Args:
            start_label: Label of the starting snapshot
            end_label: Label of the ending snapshot

        Returns:
            Dictionary with memory usage deltas
        """
        start_snapshot = next(
            (s for s in self.snapshots if s["label"] == start_label), None
        )
        end_snapshot = next(
            (s for s in self.snapshots if s["label"] == end_label), None
        )

        if not start_snapshot or not end_snapshot:
            return {"error": "Snapshot not found"}

        return {
            "object_count_delta": end_snapshot["object_count"]
            - start_snapshot["object_count"],
            "garbage_count_delta": end_snapshot["garbage_count"]
            - start_snapshot["garbage_count"],
            "ref_count_delta": end_snapshot["ref_count_total"]
            - start_snapshot["ref_count_total"],
        }

    def print_summary(self) -> None:
        """Print a summary of all memory snapshots."""
        print("\nMemory Usage Summary:")
        print("-" * 50)
        for snapshot in self.snapshots:
            print(
                f"{snapshot['label']:20}: objects={snapshot['object_count']:6d}, "
                f"garbage={snapshot['garbage_count']:3d}"
            )


class TestStatusPhaseMemoryOptimization:
    """Memory optimization tests for status phase execution."""

    def setup_method(self) -> None:
        """Set up test fixtures for each test method."""
        self.orchestrator = StatusPhaseOrchestrator()
        self.manager = StatusPhaseManager()
        self.memory_tracker = MemoryTracker()

        # Force garbage collection before each test
        gc.collect()

    def create_large_game_state(
        self, num_players: int = 6, planets_per_player: int = 10
    ) -> GameState:
        """Create a large game state for memory testing.

        Args:
            num_players: Number of players (default 6 for maximum)
            planets_per_player: Number of planets per player

        Returns:
            Large GameState for memory testing
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

            # Add many planets to simulate late game
            for j in range(planets_per_player):
                planet = Planet(
                    name=f"Planet_{i}_{j}", resources=(j % 5) + 1, influence=(j % 3) + 1
                )
                game_state = game_state.add_player_planet(player.id, planet)

        return game_state

    def test_memory_usage_during_status_phase_execution(self) -> None:
        """Test memory usage patterns during status phase execution.

        Requirement: 12.3 - Memory usage optimization for large game states
        """
        # Take baseline snapshot
        self.memory_tracker.take_snapshot("baseline")

        # Create large game state
        game_state = self.create_large_game_state(6, 8)
        self.memory_tracker.take_snapshot("after_game_state_creation")

        # Execute status phase
        result, updated_state = self.orchestrator.execute_complete_status_phase(
            game_state
        )
        self.memory_tracker.take_snapshot("after_status_phase_execution")

        # Verify execution succeeded
        assert result.success, f"Status phase failed: {result.error_message}"

        # Clean up references
        del game_state, updated_state, result
        gc.collect()
        self.memory_tracker.take_snapshot("after_cleanup")

        # Analyze memory usage
        creation_delta = self.memory_tracker.get_memory_delta(
            "baseline", "after_game_state_creation"
        )
        execution_delta = self.memory_tracker.get_memory_delta(
            "after_game_state_creation", "after_status_phase_execution"
        )
        cleanup_delta = self.memory_tracker.get_memory_delta(
            "baseline", "after_cleanup"
        )

        self.memory_tracker.print_summary()

        print("\nMemory Analysis:")
        print(f"Creation delta: {creation_delta['object_count_delta']} objects")
        print(f"Execution delta: {execution_delta['object_count_delta']} objects")
        print(f"Cleanup delta: {cleanup_delta['object_count_delta']} objects")

        # Verify memory optimization requirements
        if creation_delta["object_count_delta"] > 0:
            # Memory growth during execution should be reasonable compared to creation
            growth_ratio = (
                execution_delta["object_count_delta"]
                / creation_delta["object_count_delta"]
            )
            assert growth_ratio < 2.0, (
                f"Memory growth during execution too high: {growth_ratio:.2f}"
            )

        # Memory should be mostly cleaned up after deletion
        cleanup_ratio = abs(cleanup_delta["object_count_delta"]) / max(
            creation_delta["object_count_delta"], 1
        )
        assert cleanup_ratio < 3.0, (
            f"Memory not properly cleaned up: {cleanup_ratio:.2f}"
        )

    def test_memory_leak_detection(self) -> None:
        """Test for memory leaks during repeated status phase executions.

        Verifies that memory usage doesn't grow unboundedly with repeated use.
        """
        game_state = self.create_large_game_state(4, 5)

        # Take baseline measurement
        self.memory_tracker.take_snapshot("leak_test_baseline")

        # Execute status phase multiple times
        for i in range(5):
            result, updated_state = self.orchestrator.execute_complete_status_phase(
                game_state
            )
            assert result.success, f"Iteration {i + 1} failed: {result.error_message}"

            # Clean up result and updated state
            del result, updated_state
            gc.collect()

            self.memory_tracker.take_snapshot(f"after_iteration_{i + 1}")

        # Analyze memory growth across iterations
        baseline_objects = self.memory_tracker.snapshots[0]["object_count"]
        final_objects = self.memory_tracker.snapshots[-1]["object_count"]

        memory_growth = final_objects - baseline_objects
        growth_per_iteration = memory_growth / 5

        print("\nMemory Leak Analysis:")
        print(f"Baseline objects: {baseline_objects}")
        print(f"Final objects: {final_objects}")
        print(f"Total growth: {memory_growth} objects")
        print(f"Growth per iteration: {growth_per_iteration:.1f} objects")

        # Verify no significant memory leaks
        # Allow some growth but it should be minimal
        assert memory_growth < 100, (
            f"Potential memory leak detected: {memory_growth} objects growth"
        )
        assert growth_per_iteration < 20, (
            f"Memory growth per iteration too high: {growth_per_iteration:.1f}"
        )

    def test_memory_usage_scaling_with_game_state_size(self) -> None:
        """Test memory usage scaling with different game state sizes.

        Verifies that memory usage scales reasonably with game state complexity.
        """
        test_cases = [
            ("small", 2, 2),
            ("medium", 4, 4),
            ("large", 6, 6),
            ("extra_large", 6, 10),
        ]

        memory_usage_by_size = {}

        for case_name, num_players, planets_per_player in test_cases:
            # Clean slate for each test
            gc.collect()
            baseline_objects = len(gc.get_objects())

            # Create game state
            game_state = self.create_large_game_state(num_players, planets_per_player)
            after_creation_objects = len(gc.get_objects())

            # Execute status phase
            result, updated_state = self.orchestrator.execute_complete_status_phase(
                game_state
            )
            after_execution_objects = len(gc.get_objects())

            # Calculate memory usage
            creation_objects = after_creation_objects - baseline_objects
            execution_objects = after_execution_objects - after_creation_objects
            total_objects = after_execution_objects - baseline_objects

            memory_usage_by_size[case_name] = {
                "creation_objects": creation_objects,
                "execution_objects": execution_objects,
                "total_objects": total_objects,
                "num_players": num_players,
                "planets_per_player": planets_per_player,
                "total_entities": num_players
                * (1 + planets_per_player),  # players + planets
            }

            # Verify execution succeeded before cleanup
            assert result.success, f"Status phase failed for {case_name}"

            # Clean up
            del game_state, updated_state, result
            gc.collect()

        # Analyze scaling
        print("\nMemory Usage Scaling Analysis:")
        print("-" * 60)
        for case_name, usage in memory_usage_by_size.items():
            objects_per_entity = usage["total_objects"] / usage["total_entities"]
            print(
                f"{case_name:12}: {usage['total_objects']:4d} objects "
                f"({objects_per_entity:.1f} per entity)"
            )

        # Verify reasonable scaling
        small_usage = memory_usage_by_size["small"]["total_objects"]
        large_usage = memory_usage_by_size["large"]["total_objects"]

        if small_usage > 0:
            scaling_factor = large_usage / small_usage
            # Memory usage should scale sub-linearly with game state size
            assert scaling_factor < 10, (
                f"Memory scaling too poor: {scaling_factor:.2f}x"
            )

    def test_garbage_collection_efficiency(self) -> None:
        """Test garbage collection efficiency during status phase execution.

        Verifies that objects are properly collected and no circular references exist.
        """
        # Enable garbage collection debugging
        gc.set_debug(gc.DEBUG_STATS)

        try:
            # Create and execute status phase multiple times
            for i in range(3):
                game_state = self.create_large_game_state(4, 4)

                # Track garbage before execution
                gc.collect()
                garbage_before = len(gc.garbage)

                # Execute status phase
                result, updated_state = self.orchestrator.execute_complete_status_phase(
                    game_state
                )
                assert result.success, f"Iteration {i + 1} failed"

                # Force garbage collection
                del game_state, updated_state, result
                collected = gc.collect()
                garbage_after = len(gc.garbage)

                print(
                    f"Iteration {i + 1}: collected {collected} objects, "
                    f"garbage before={garbage_before}, after={garbage_after}"
                )

                # Verify garbage collection is working efficiently
                assert garbage_after <= garbage_before + 5, (
                    f"Garbage accumulation detected: {garbage_after - garbage_before}"
                )

        finally:
            # Reset garbage collection debugging
            gc.set_debug(0)

    def test_memory_optimization_with_performance_features(self) -> None:
        """Test memory usage when performance optimization features are enabled.

        Verifies that performance optimizations don't cause memory issues.
        """
        # Test with performance optimization enabled
        optimized_manager = StatusPhaseManager(enable_performance_optimization=True)

        # Take baseline measurement
        gc.collect()
        baseline_objects = len(gc.get_objects())

        # Create large game state
        game_state = self.create_large_game_state(6, 8)
        after_creation_objects = len(gc.get_objects())

        # Execute with optimization
        result, updated_state = optimized_manager.execute_complete_status_phase(
            game_state
        )
        after_execution_objects = len(gc.get_objects())

        # Clean up
        del game_state, updated_state, result
        gc.collect()
        after_cleanup_objects = len(gc.get_objects())

        # Calculate memory usage
        creation_delta = after_creation_objects - baseline_objects
        execution_delta = after_execution_objects - after_creation_objects
        cleanup_delta = after_cleanup_objects - baseline_objects

        print("\nOptimized Memory Usage:")
        print(f"Creation: +{creation_delta} objects")
        print(f"Execution: +{execution_delta} objects")
        print(f"After cleanup: {cleanup_delta:+d} objects")

        # Verify memory optimization doesn't cause excessive memory usage
        if creation_delta > 0:
            growth_ratio = execution_delta / creation_delta
            assert growth_ratio < 0.8, (
                f"Optimized execution memory growth too high: {growth_ratio:.2f}"
            )

        # Memory should be cleaned up effectively
        cleanup_ratio = abs(cleanup_delta) / max(creation_delta, 1)
        assert cleanup_ratio < 0.4, (
            f"Optimized memory not properly cleaned up: {cleanup_ratio:.2f}"
        )

    def test_memory_usage_with_error_conditions(self) -> None:
        """Test memory usage when error conditions occur.

        Verifies that error handling doesn't cause memory leaks.
        """
        # Take baseline measurement
        gc.collect()
        baseline_objects = len(gc.get_objects())

        # Test various error conditions
        error_conditions = [
            ("none_game_state", None),
            ("invalid_game_state", "invalid"),
        ]

        for condition_name, game_state in error_conditions:
            # Execute with error condition
            result, updated_state = self.orchestrator.execute_complete_status_phase(
                game_state
            )

            # Verify error was handled
            assert not result.success, f"Expected failure for {condition_name}"

            # Clean up
            del result, updated_state
            gc.collect()

            # Check memory usage
            current_objects = len(gc.get_objects())
            memory_delta = current_objects - baseline_objects

            print(f"Error condition '{condition_name}': {memory_delta:+d} objects")

            # Error handling shouldn't cause significant memory growth
            assert abs(memory_delta) < 50, (
                f"Error handling caused memory growth: {memory_delta}"
            )

    def test_step_by_step_memory_usage(self) -> None:
        """Test memory usage for individual status phase steps.

        Analyzes memory usage patterns for each step to identify memory-intensive operations.
        """
        game_state = self.create_large_game_state(4, 4)
        current_state = game_state

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

        print("\nStep-by-Step Memory Usage Analysis:")
        print("-" * 50)

        # Take baseline measurement
        gc.collect()
        baseline_objects = len(gc.get_objects())

        for step_number in range(1, 9):
            # Execute step
            result, updated_state = self.orchestrator.execute_step(
                step_number, current_state
            )
            current_state = updated_state if result.success else current_state

            # Measure memory
            gc.collect()
            current_objects = len(gc.get_objects())
            memory_delta = current_objects - baseline_objects

            step_name = step_names[step_number - 1]
            status = "✓" if result.success else "✗"

            print(
                f"Step {step_number} ({step_name:20}): {memory_delta:+4d} objects {status}"
            )

            # Verify reasonable memory usage per step
            assert abs(memory_delta) < 200, (
                f"Step {step_number} used too much memory: {memory_delta}"
            )

        # Clean up final state
        del current_state, game_state
        gc.collect()
        final_objects = len(gc.get_objects())
        final_delta = final_objects - baseline_objects

        print(f"Final cleanup: {final_delta:+4d} objects")

        # Verify final cleanup is effective
        assert abs(final_delta) < 100, f"Final cleanup ineffective: {final_delta}"

    @pytest.mark.skipif(
        not hasattr(sys, "gettotalrefcount"),
        reason="Reference counting only available in debug builds",
    )
    def test_reference_counting_analysis(self) -> None:
        """Test reference counting to detect potential reference leaks.

        Only runs in debug Python builds that have sys.gettotalrefcount().
        """
        # Take baseline reference count
        gc.collect()
        baseline_refs = sys.gettotalrefcount()

        # Execute status phase multiple times
        for i in range(3):
            game_state = self.create_large_game_state(3, 3)
            result, updated_state = self.orchestrator.execute_complete_status_phase(
                game_state
            )

            # Clean up
            del game_state, updated_state, result
            gc.collect()

            current_refs = sys.gettotalrefcount()
            ref_delta = current_refs - baseline_refs

            print(f"Iteration {i + 1}: {ref_delta:+d} reference count delta")

            # Reference count should not grow significantly
            assert abs(ref_delta) < 100, f"Reference count growth detected: {ref_delta}"

    def test_memory_profiling_integration(self) -> None:
        """Test integration with memory profiling tools.

        Provides hooks for external memory profiling tools.
        """
        # This test demonstrates how to integrate with memory profiling
        # In practice, you might use tools like memory_profiler, pympler, etc.

        def memory_profile_decorator(func):
            """Decorator for memory profiling (placeholder)."""

            def wrapper(*args, **kwargs):
                # In real implementation, this would use actual profiling tools
                gc.collect()
                before = len(gc.get_objects())
                result = func(*args, **kwargs)
                after = len(gc.get_objects())
                print(f"Memory delta for {func.__name__}: {after - before} objects")
                return result

            return wrapper

        # Apply profiling to status phase execution
        profiled_execute = memory_profile_decorator(
            self.orchestrator.execute_complete_status_phase
        )

        # Execute with profiling
        game_state = self.create_large_game_state(4, 4)
        result, updated_state = profiled_execute(game_state)

        # Verify execution succeeded
        assert result.success, f"Profiled execution failed: {result.error_message}"

        # Clean up
        del game_state, updated_state, result
        gc.collect()


if __name__ == "__main__":
    # Run memory optimization tests when executed directly
    test_instance = TestStatusPhaseMemoryOptimization()
    test_instance.setup_method()

    print("Running Status Phase Memory Optimization Tests...")
    print("=" * 60)

    try:
        test_instance.test_memory_usage_during_status_phase_execution()
        test_instance.test_memory_leak_detection()
        test_instance.test_memory_usage_scaling_with_game_state_size()
        test_instance.test_step_by_step_memory_usage()
        print("\nAll memory optimization tests completed successfully!")
    except Exception as e:
        print(f"\nMemory test failed: {e}")
        raise
