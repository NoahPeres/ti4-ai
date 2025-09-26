"""Tests for performance caching system."""

from unittest.mock import Mock, patch

from ti4.actions.action import PlayerDecision
from ti4.core.game_state import GameState
from ti4.performance.cache import GameStateCache


class TestGameStateCache:
    """Test cases for GameStateCache."""

    def test_cache_initialization(self) -> None:
        """Test that cache initializes with correct parameters."""
        cache = GameStateCache(max_size=500)
        assert cache._max_size == 500

    def test_cache_legal_moves_miss_then_hit(self) -> None:
        """Test cache miss followed by cache hit for legal moves."""
        cache = GameStateCache()
        game_state = GameState(game_id="test_game")
        player_id = "player1"

        # Mock the expensive legal move generation
        mock_moves = [Mock(spec=PlayerDecision)]

        with patch(
            "ti4.actions.legal_moves.LegalMoveGenerator.generate_legal_actions",
            return_value=mock_moves,
        ) as mock_generator:
            # First call should miss cache and call generator
            result1 = cache.get_legal_moves(game_state, player_id)
            assert result1 == mock_moves
            assert mock_generator.call_count == 1

            # Second call should hit cache and not call generator
            result2 = cache.get_legal_moves(game_state, player_id)
            assert result2 == mock_moves
            assert mock_generator.call_count == 1  # Should not increase

    def test_cache_invalidation(self) -> None:
        """Test cache invalidation functionality."""
        cache = GameStateCache()
        game_state = GameState(game_id="test_game")
        player_id = "player1"

        mock_moves = [Mock(spec=PlayerDecision)]

        with patch(
            "ti4.actions.legal_moves.LegalMoveGenerator.generate_legal_actions",
            return_value=mock_moves,
        ) as mock_generator:
            # Fill cache
            cache.get_legal_moves(game_state, player_id)
            assert mock_generator.call_count == 1

            # Invalidate cache
            cache.invalidate_cache()

            # Next call should miss cache and call generator again
            cache.get_legal_moves(game_state, player_id)
            assert mock_generator.call_count == 2

    def test_adjacency_caching(self) -> None:
        """Test caching of adjacency calculations."""
        cache = GameStateCache()

        # Mock the galaxy adjacency check
        with patch(
            "ti4.core.galaxy.Galaxy.are_systems_adjacent", return_value=True
        ) as mock_adjacency:
            # First call should miss cache and call adjacency check
            result1 = cache.are_systems_adjacent("system1", "system2")
            assert result1 is True
            assert mock_adjacency.call_count == 1

            # Second call should hit cache and not call adjacency check
            result2 = cache.are_systems_adjacent("system1", "system2")
            assert result2 is True
            assert mock_adjacency.call_count == 1  # Should not increase

    def test_pathfinding_caching(self) -> None:
        """Test caching of pathfinding calculations."""
        cache = GameStateCache()

        # Mock pathfinding result
        mock_path = ["system1", "system2", "system3"]

        with patch.object(
            cache, "_calculate_shortest_path", return_value=mock_path
        ) as mock_pathfind:
            # First call should miss cache and call pathfinding
            result1 = cache.find_shortest_path("system1", "system3", max_distance=3)
            assert result1 == mock_path
            assert mock_pathfind.call_count == 1

            # Second call should hit cache and not call pathfinding
            result2 = cache.find_shortest_path("system1", "system3", max_distance=3)
            assert result2 == mock_path
            assert mock_pathfind.call_count == 1  # Should not increase

    def test_cache_performance_improvement(self) -> None:
        """Test that cache provides performance improvement."""
        import time

        cache = GameStateCache()
        game_state = GameState(game_id="perf_test")
        player_id = "player1"

        # Mock expensive operation
        def slow_legal_moves(*args, **kwargs) -> None:
            time.sleep(0.01)  # Simulate expensive operation
            return [Mock(spec=PlayerDecision)]

        with patch(
            "ti4.actions.legal_moves.LegalMoveGenerator.generate_legal_actions",
            side_effect=slow_legal_moves,
        ):
            # First call - should be slow
            start_time = time.time()
            cache.get_legal_moves(game_state, player_id)
            first_call_time = time.time() - start_time

            # Second call - should be fast (cached)
            start_time = time.time()
            cache.get_legal_moves(game_state, player_id)
            second_call_time = time.time() - start_time

            # Cache should provide significant speedup
            assert second_call_time < first_call_time / 2
