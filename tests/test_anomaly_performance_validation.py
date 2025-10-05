"""
Performance validation tests for Rule 9: ANOMALIES

This module validates that the anomaly system maintains acceptable performance
characteristics and does not introduce significant overhead to existing
TI4 system operations.

LRR References:
- Rule 9: ANOMALIES (performance impact assessment)
"""

import gc
import time
from unittest.mock import Mock, patch

from src.ti4.core.anomaly_manager import AnomalyManager
from src.ti4.core.constants import AnomalyType
from src.ti4.core.dice import DiceRoll
from src.ti4.core.movement_rules import MovementContext, MovementRuleEngine
from src.ti4.core.system import System
from src.ti4.core.unit import Unit, UnitType


class TestAnomalySystemPerformance:
    """Test performance characteristics of anomaly system operations"""

    def setup_method(self):
        """Set up test fixtures"""
        self.anomaly_manager = AnomalyManager()
        self.movement_engine = MovementRuleEngine()

    def test_anomaly_system_creation_performance(self):
        """Test that anomaly system creation is performant"""
        start_time = time.time()

        # Create many anomaly systems
        systems = []
        for i in range(1000):
            system = self.anomaly_manager.create_anomaly_system(
                f"system_{i}", [AnomalyType.NEBULA]
            )
            systems.append(system)

        creation_time = time.time() - start_time

        # Should create 1000 systems in under 1 second
        assert creation_time < 1.0

        # Verify all systems were created correctly
        assert len(systems) == 1000
        for system in systems:
            assert system.is_anomaly()
            assert system.has_anomaly_type(AnomalyType.NEBULA)

    def test_anomaly_effects_query_performance(self):
        """Test that querying anomaly effects is performant"""
        # Create complex anomaly system
        complex_system = self.anomaly_manager.create_anomaly_system(
            "complex",
            [AnomalyType.NEBULA, AnomalyType.GRAVITY_RIFT, AnomalyType.ASTEROID_FIELD],
        )

        start_time = time.time()

        # Query effects many times
        for _ in range(10000):
            effects = self.anomaly_manager.get_anomaly_effects_summary(complex_system)
            assert effects is not None

        query_time = time.time() - start_time

        # Should handle 10,000 queries in under 1 second
        assert query_time < 1.0

    def test_movement_validation_performance_with_anomalies(self):
        """Test that movement validation performance is acceptable with anomalies"""
        # Create path with multiple anomaly systems
        systems = []
        for i in range(10):
            if i % 3 == 0:
                system = self.anomaly_manager.create_anomaly_system(
                    f"system_{i}", [AnomalyType.GRAVITY_RIFT]
                )
            elif i % 3 == 1:
                system = self.anomaly_manager.create_anomaly_system(
                    f"system_{i}", [AnomalyType.NEBULA]
                )
            else:
                system = System(f"system_{i}")
            systems.append(system)

        cruiser = Unit(UnitType.CRUISER, player_id="player1")

        # Mock dice rolls for gravity rifts
        with patch("src.ti4.core.dice.roll_die") as mock_dice:
            mock_dice.return_value = DiceRoll(6)  # Always survive

            # Mock active system for nebula validation
            with patch(
                "src.ti4.core.game_state.GameState.get_active_system"
            ) as mock_active:
                mock_active.return_value = systems[1]  # Make nebula active

                start_time = time.time()

                # Validate movement through complex paths many times
                for _ in range(1000):
                    context = MovementContext(
                        unit=cruiser,
                        origin=systems[0],
                        destination=systems[-1],
                        path=systems,
                        galaxy=Mock(),
                    )

                    result = self.movement_engine.validate_movement(context)
                    assert result is not None

                validation_time = time.time() - start_time

                # Should handle 1000 validations in under 2 seconds
                assert validation_time < 2.0

    def test_combat_modifier_calculation_performance(self):
        """Test that combat modifier calculations are performant"""
        # Create nebula system for combat bonuses
        nebula_system = self.anomaly_manager.create_anomaly_system(
            "nebula_combat", [AnomalyType.NEBULA]
        )

        start_time = time.time()

        # Calculate combat modifiers many times
        for _ in range(10000):
            defender_mods = self.anomaly_manager.get_combat_modifiers(
                nebula_system, is_defender=True
            )
            attacker_mods = self.anomaly_manager.get_combat_modifiers(
                nebula_system, is_defender=False
            )
            assert defender_mods is not None
            assert attacker_mods is not None

        calculation_time = time.time() - start_time

        # Should handle 10,000 calculations in under 0.5 seconds
        assert calculation_time < 0.5

    def test_dynamic_anomaly_assignment_performance(self):
        """Test that dynamic anomaly assignment/removal is performant"""
        # Create base system
        system = System("dynamic_test")

        start_time = time.time()

        # Perform many dynamic operations
        for i in range(1000):
            # Add anomaly type
            anomaly_type = list(AnomalyType)[i % len(AnomalyType)]
            self.anomaly_manager.add_anomaly_to_system(system, anomaly_type)

            # Query effects
            effects = self.anomaly_manager.get_anomaly_effects_summary(system)
            assert effects is not None

            # Remove anomaly type
            self.anomaly_manager.remove_anomaly_from_system(system, anomaly_type)

        operation_time = time.time() - start_time

        # Should handle 1000 add/remove cycles in under 1 second
        assert operation_time < 1.0

    def test_memory_usage_stability(self):
        """Test that memory usage remains stable during operations"""
        import os

        import psutil

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Perform many operations
        systems = []
        for i in range(1000):
            system = self.anomaly_manager.create_anomaly_system(
                f"memory_test_{i}", [AnomalyType.GRAVITY_RIFT]
            )
            systems.append(system)

            # Perform operations on each system
            self.anomaly_manager.get_anomaly_effects_summary(system)
            self.anomaly_manager.get_combat_modifiers(system, True)

        # Force garbage collection
        gc.collect()

        final_memory = process.memory_info().rss
        memory_growth = final_memory - initial_memory

        # Memory growth should be reasonable (less than 50MB for 1000 systems)
        assert memory_growth < 50 * 1024 * 1024  # 50MB in bytes

    def test_concurrent_access_performance(self):
        """Test performance under concurrent access patterns"""
        import queue
        import threading

        # Create shared anomaly system
        shared_system = self.anomaly_manager.create_anomaly_system(
            "concurrent_test", [AnomalyType.NEBULA, AnomalyType.GRAVITY_RIFT]
        )

        results_queue = queue.Queue()

        def worker():
            """Worker function for concurrent access"""
            start_time = time.time()
            for _ in range(100):
                self.anomaly_manager.get_anomaly_effects_summary(shared_system)
                self.anomaly_manager.get_combat_modifiers(shared_system, True)
            end_time = time.time()
            results_queue.put(end_time - start_time)

        # Start multiple threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check that all threads completed in reasonable time
        total_times = []
        while not results_queue.empty():
            total_times.append(results_queue.get())

        assert len(total_times) == 10
        # Each thread should complete in under 1 second
        for thread_time in total_times:
            assert thread_time < 1.0


class TestAnomalySystemScalability:
    """Test scalability characteristics of the anomaly system"""

    def setup_method(self):
        """Set up test fixtures"""
        self.anomaly_manager = AnomalyManager()

    def test_large_galaxy_with_many_anomalies(self):
        """Test performance with a large galaxy containing many anomaly systems"""
        # Create large galaxy with mixed systems
        systems = {}

        start_time = time.time()

        for i in range(5000):
            if i % 4 == 0:
                # 25% anomaly systems
                anomaly_types = [list(AnomalyType)[i % len(AnomalyType)]]
                system = self.anomaly_manager.create_anomaly_system(
                    f"system_{i}", anomaly_types
                )
            else:
                # 75% normal systems
                system = System(f"system_{i}")

            systems[f"system_{i}"] = system

        creation_time = time.time() - start_time

        # Should create 5000 systems in under 5 seconds
        assert creation_time < 5.0

        # Test querying performance across large galaxy
        start_time = time.time()

        anomaly_count = 0
        for system in systems.values():
            if hasattr(system, "is_anomaly") and system.is_anomaly():
                self.anomaly_manager.get_anomaly_effects_summary(system)
                anomaly_count += 1

        query_time = time.time() - start_time

        # Should query all systems in under 2 seconds
        assert query_time < 2.0
        assert anomaly_count > 1000  # Should have created ~1250 anomaly systems

    def test_complex_movement_paths_scalability(self):
        """Test scalability of movement validation through complex paths"""
        # Create very long path with mixed system types
        path_systems = []
        for i in range(100):
            if i % 5 == 0:
                system = self.anomaly_manager.create_anomaly_system(
                    f"path_system_{i}", [AnomalyType.GRAVITY_RIFT]
                )
            elif i % 5 == 1:
                system = self.anomaly_manager.create_anomaly_system(
                    f"path_system_{i}", [AnomalyType.NEBULA]
                )
            else:
                system = System(f"path_system_{i}")
            path_systems.append(system)

        cruiser = Unit(UnitType.CRUISER, player_id="player1")

        # Mock necessary components for validation
        with patch("src.ti4.core.dice.roll_die") as mock_dice:
            mock_dice.return_value = DiceRoll(6)  # Always survive gravity rifts

            with patch(
                "src.ti4.core.game_state.GameState.get_active_system"
            ) as mock_active:
                mock_active.return_value = path_systems[1]  # Make first nebula active

                start_time = time.time()

                # Validate movement through very long path
                context = MovementContext(
                    unit=cruiser,
                    origin=path_systems[0],
                    destination=path_systems[-1],
                    path=path_systems,
                    galaxy=Mock(),
                )

                result = self.movement_engine.validate_movement(context)

                validation_time = time.time() - start_time

                # Should validate 100-system path in under 0.1 seconds
                assert validation_time < 0.1
                assert result is not None

    def test_multiple_anomaly_types_per_system_scalability(self):
        """Test performance with systems having multiple anomaly types"""
        # Create systems with all possible anomaly type combinations
        systems = []

        start_time = time.time()

        # Generate all possible combinations of anomaly types
        anomaly_types = list(AnomalyType)
        for i in range(1000):
            # Create systems with 1-4 anomaly types
            num_types = (i % 4) + 1
            selected_types = anomaly_types[:num_types]

            system = self.anomaly_manager.create_anomaly_system(
                f"multi_anomaly_{i}", selected_types
            )
            systems.append(system)

        creation_time = time.time() - start_time

        # Should create 1000 multi-anomaly systems in under 2 seconds
        assert creation_time < 2.0

        # Test querying performance for complex systems
        start_time = time.time()

        for system in systems:
            self.anomaly_manager.get_anomaly_effects_summary(system)
            self.anomaly_manager.get_combat_modifiers(system, True)
            self.anomaly_manager.is_system_blocking_movement(system, False)

        query_time = time.time() - start_time

        # Should query all complex systems in under 1 second
        assert query_time < 1.0


class TestAnomalySystemResourceUsage:
    """Test resource usage characteristics of the anomaly system"""

    def setup_method(self):
        """Set up test fixtures"""
        self.anomaly_manager = AnomalyManager()

    def test_cpu_usage_during_intensive_operations(self):
        """Test CPU usage during intensive anomaly operations"""
        import os

        import psutil

        process = psutil.Process(os.getpid())

        # Measure CPU usage during intensive operations
        cpu_percent_before = process.cpu_percent()

        start_time = time.time()

        # Perform CPU-intensive operations
        for i in range(10000):
            system = self.anomaly_manager.create_anomaly_system(
                f"cpu_test_{i}", [AnomalyType.GRAVITY_RIFT, AnomalyType.NEBULA]
            )

            # Perform multiple operations per system
            self.anomaly_manager.get_anomaly_effects_summary(system)
            self.anomaly_manager.get_combat_modifiers(system, True)
            self.anomaly_manager.is_system_blocking_movement(system, False)

        operation_time = time.time() - start_time
        cpu_percent_after = process.cpu_percent()

        # Operations should complete in reasonable time
        assert operation_time < 10.0

        # CPU usage should not spike excessively
        # Note: This test might be environment-dependent
        cpu_increase = cpu_percent_after - cpu_percent_before
        assert cpu_increase < 90.0  # Should not max out CPU

    def test_memory_efficiency_with_large_datasets(self):
        """Test memory efficiency when working with large datasets"""
        import sys

        # Create large number of anomaly systems
        systems = []
        initial_size = 0

        for i in range(10000):
            system = self.anomaly_manager.create_anomaly_system(
                f"memory_efficiency_{i}", [AnomalyType.ASTEROID_FIELD]
            )
            systems.append(system)

            # Measure size of first system for baseline
            if i == 0:
                initial_size = sys.getsizeof(system)

        # Calculate total memory usage
        total_size = sum(sys.getsizeof(system) for system in systems)
        average_size = total_size / len(systems)

        # Average system size should not be significantly larger than initial
        size_ratio = average_size / initial_size
        assert size_ratio < 1.5  # Should not grow by more than 50%

        # Total memory usage should be reasonable (less than 100MB for 10k systems)
        assert total_size < 100 * 1024 * 1024  # 100MB in bytes

    def test_garbage_collection_efficiency(self):
        """Test that anomaly systems are properly garbage collected"""
        import gc
        import weakref

        # Create systems and weak references
        weak_refs = []

        for i in range(1000):
            system = self.anomaly_manager.create_anomaly_system(
                f"gc_test_{i}", [AnomalyType.NEBULA]
            )
            weak_refs.append(weakref.ref(system))

            # Use the system to ensure it's not optimized away
            self.anomaly_manager.get_anomaly_effects_summary(system)

        # Force garbage collection
        gc.collect()

        # Check how many systems are still referenced
        alive_count = sum(1 for ref in weak_refs if ref() is not None)

        # Most systems should be garbage collected
        # (Some might still be alive due to Python's GC behavior)
        gc_efficiency = (len(weak_refs) - alive_count) / len(weak_refs)
        assert gc_efficiency > 0.8  # At least 80% should be collected

    def test_caching_effectiveness(self):
        """Test that caching improves performance for repeated operations"""
        # Create complex anomaly system
        complex_system = self.anomaly_manager.create_anomaly_system(
            "cache_test",
            [AnomalyType.NEBULA, AnomalyType.GRAVITY_RIFT, AnomalyType.ASTEROID_FIELD],
        )

        # Measure time for first set of operations (cache miss)
        start_time = time.time()
        for _ in range(1000):
            self.anomaly_manager.get_anomaly_effects_summary(complex_system)
        first_run_time = time.time() - start_time

        # Measure time for second set of operations (cache hit)
        start_time = time.time()
        for _ in range(1000):
            self.anomaly_manager.get_anomaly_effects_summary(complex_system)
        second_run_time = time.time() - start_time

        # Second run should be faster due to caching
        # Note: This assumes the implementation uses caching
        speedup_ratio = first_run_time / second_run_time
        assert speedup_ratio >= 1.0  # Should be at least as fast, ideally faster
