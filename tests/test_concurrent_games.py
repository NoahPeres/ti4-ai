"""Tests for concurrent game support."""

import threading
import time
from concurrent.futures import as_completed

import pytest

from src.ti4.core.game_state import GameState
from src.ti4.performance.concurrent import (
    ConcurrentGameManager,
    ThreadSafeGameStateCache,
    get_game_manager,
    shutdown_game_manager,
)


class TestConcurrentGameManager:
    """Test cases for ConcurrentGameManager."""

    def test_manager_initialization(self):
        """Test that manager initializes correctly."""
        manager = ConcurrentGameManager(max_concurrent_games=50)
        assert manager._max_concurrent_games == 50
        assert len(manager._games) == 0

    def test_create_game(self):
        """Test game creation."""
        manager = ConcurrentGameManager()

        # Create game with auto-generated ID
        game_id1 = manager.create_game()
        assert game_id1 is not None
        assert game_id1 in manager._games

        # Create game with specific ID
        game_id2 = manager.create_game("test_game")
        assert game_id2 == "test_game"
        assert "test_game" in manager._games

        # Try to create duplicate game
        with pytest.raises(ValueError, match="already exists"):
            manager.create_game("test_game")

    def test_get_game(self):
        """Test game retrieval."""
        manager = ConcurrentGameManager()
        manager.create_game("test_game")

        game_instance = manager.get_game("test_game")
        assert game_instance is not None
        assert game_instance.game_id == "test_game"

        # Test non-existent game
        assert manager.get_game("non_existent") is None

    def test_remove_game(self):
        """Test game removal."""
        manager = ConcurrentGameManager()
        manager.create_game("test_game")

        # Remove existing game
        assert manager.remove_game("test_game") is True
        assert "test_game" not in manager._games

        # Try to remove non-existent game
        assert manager.remove_game("non_existent") is False

    def test_concurrent_game_creation(self):
        """Test concurrent game creation."""
        manager = ConcurrentGameManager()
        created_games = []
        errors = []
        game_counter = 0
        counter_lock = threading.Lock()

        def create_games(thread_id):
            nonlocal game_counter
            try:
                for _i in range(10):
                    # Use a combination of thread_id and counter for uniqueness
                    with counter_lock:
                        game_counter += 1
                        unique_id = game_counter

                    game_id = manager.create_game(
                        f"concurrent_game_{thread_id}_{unique_id}"
                    )
                    created_games.append(game_id)
            except Exception as e:
                errors.append(e)

        # Create multiple threads
        threads = []
        for thread_num in range(5):
            thread = threading.Thread(target=create_games, args=(thread_num,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check results
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(created_games) == 50  # 5 threads * 10 games each
        assert len(set(created_games)) == 50  # All games should be unique

    def test_execute_game_operation(self):
        """Test thread-safe game operation execution."""
        manager = ConcurrentGameManager()
        game_id = manager.create_game("test_game")

        def test_operation(game_state, value):
            # Simulate some work
            time.sleep(0.01)
            return value * 2

        # Execute operation
        future = manager.execute_game_operation(game_id, test_operation, 5)
        result = future.result(timeout=1.0)

        assert result == 10

    def test_concurrent_operations_on_same_game(self):
        """Test multiple concurrent operations on the same game."""
        manager = ConcurrentGameManager()
        game_id = manager.create_game("test_game")

        results = []

        def increment_operation(game_state, increment):
            # Simulate some work and return the increment
            time.sleep(0.01)
            return increment

        # Submit multiple operations concurrently
        futures = []
        for i in range(10):
            future = manager.execute_game_operation(game_id, increment_operation, i)
            futures.append(future)

        # Collect results
        for future in as_completed(futures, timeout=5.0):
            results.append(future.result())

        # All operations should complete successfully
        assert len(results) == 10
        assert sorted(results) == list(range(10))

    def test_game_stats(self):
        """Test game statistics collection."""
        manager = ConcurrentGameManager(max_concurrent_games=10)

        # Create some games
        for i in range(3):
            manager.create_game(f"game_{i}")

        stats = manager.get_game_stats()

        assert stats["total_games"] == 3
        assert stats["max_concurrent_games"] == 10
        assert stats["active_operations"] == 0
        assert "average_game_age_seconds" in stats
        assert "oldest_game_age_seconds" in stats

    def test_max_concurrent_games_limit(self):
        """Test maximum concurrent games limit."""
        manager = ConcurrentGameManager(max_concurrent_games=2)

        # Create games up to limit
        manager.create_game("game_1")
        manager.create_game("game_2")

        # Third game should trigger cleanup or raise error
        with pytest.raises(
            RuntimeError, match="Maximum concurrent games limit reached"
        ):
            manager.create_game("game_3")

    def test_manager_shutdown(self):
        """Test manager shutdown."""
        manager = ConcurrentGameManager()
        manager.create_game("test_game")

        # Shutdown should complete without errors
        manager.shutdown()

        # Games should be cleared
        assert len(manager._games) == 0


class TestThreadSafeGameStateCache:
    """Test cases for ThreadSafeGameStateCache."""

    def test_cache_initialization(self):
        """Test cache initialization."""
        cache = ThreadSafeGameStateCache(max_size=500)
        assert cache._cache._max_size == 500

    def test_concurrent_cache_access(self):
        """Test concurrent access to cache."""
        cache = ThreadSafeGameStateCache()
        GameState(game_id="test_game")

        results = []
        errors = []

        def cache_operation():
            try:
                # Test different cache operations
                cache.are_systems_adjacent("system1", "system2")
                cache.find_shortest_path("system1", "system3")
                results.append("success")
            except Exception as e:
                errors.append(e)

        # Create multiple threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=cache_operation)
            threads.append(thread)
            thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join()

        # Check results
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 10


class TestStressTesting:
    """Stress tests for concurrent game support."""

    def test_high_concurrency_stress(self):
        """Stress test with high concurrency."""
        manager = ConcurrentGameManager(max_concurrent_games=50)

        def stress_operations():
            try:
                # Create a game
                game_id = manager.create_game()

                # Perform multiple operations
                def dummy_operation(game_state):
                    time.sleep(0.001)  # Very short operation
                    return "done"

                futures = []
                for _ in range(5):
                    future = manager.execute_game_operation(game_id, dummy_operation)
                    futures.append(future)

                # Wait for operations to complete
                for future in futures:
                    future.result(timeout=1.0)

                # Remove the game
                manager.remove_game(game_id)

            except Exception as e:
                pytest.fail(f"Stress test failed: {e}")

        # Run stress test with multiple threads
        threads = []
        for _ in range(20):
            thread = threading.Thread(target=stress_operations)
            threads.append(thread)
            thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join(timeout=10.0)
            if thread.is_alive():
                pytest.fail("Stress test thread did not complete in time")

        # Cleanup
        manager.shutdown()

    def test_memory_usage_under_load(self):
        """Test memory usage doesn't grow excessively under load."""
        manager = ConcurrentGameManager(max_concurrent_games=20)

        # Create and destroy games repeatedly
        for cycle in range(5):
            game_ids = []

            # Create games
            for i in range(10):
                game_id = manager.create_game(f"cycle_{cycle}_game_{i}")
                game_ids.append(game_id)

            # Perform operations on each game
            for game_id in game_ids:

                def simple_operation(game_state):
                    return "completed"

                future = manager.execute_game_operation(game_id, simple_operation)
                future.result(timeout=1.0)

            # Remove all games
            for game_id in game_ids:
                manager.remove_game(game_id)

            # Verify games are cleaned up
            assert len(manager._games) == 0

        manager.shutdown()


class TestGlobalGameManager:
    """Test cases for global game manager."""

    def test_global_manager_singleton(self):
        """Test that global manager is a singleton."""
        manager1 = get_game_manager()
        manager2 = get_game_manager()

        assert manager1 is manager2

    def test_global_manager_shutdown(self):
        """Test global manager shutdown."""
        manager = get_game_manager()
        manager.create_game("test_shutdown")

        # Shutdown should work without errors
        shutdown_game_manager()

        # New manager should be created on next access
        new_manager = get_game_manager()
        assert new_manager is not manager
