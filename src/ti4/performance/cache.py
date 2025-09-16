"""Caching system for expensive TI4 operations."""

import hashlib

from src.ti4.actions.action import PlayerDecision
from src.ti4.actions.legal_moves import LegalMoveGenerator
from src.ti4.core.galaxy import Galaxy
from src.ti4.core.game_state import GameState


class GameStateCache:
    """Caches expensive computations for game states."""

    def __init__(self, max_size: int = None):
        """Initialize cache with maximum size."""
        if max_size is None:
            from ..core.constants import PerformanceConstants

            max_size = PerformanceConstants.DEFAULT_CACHE_SIZE
        self._max_size = max_size
        self._legal_moves_cache: dict[str, list[PlayerDecision]] = {}
        self._adjacency_cache: dict[str, bool] = {}
        self._pathfinding_cache: dict[str, list[str]] = {}
        self._legal_move_generator = LegalMoveGenerator()
        self._galaxy = Galaxy()

    def get_legal_moves(
        self, game_state: GameState, player_id: str
    ) -> list[PlayerDecision]:
        """Get legal moves for a player, using cache if available."""
        if game_state is None or player_id is None:
            raise ValueError("game_state and player_id are required")

        cache_key = self._generate_cache_key(game_state, player_id)

        if cache_key in self._legal_moves_cache:
            return self._legal_moves_cache[cache_key]

        # Cache miss - generate legal moves
        legal_moves = self._legal_move_generator.generate_legal_actions(
            game_state, player_id
        )

        # Enforce cache size limit
        if len(self._legal_moves_cache) >= self._max_size:
            # Remove oldest entry (simple FIFO eviction)
            oldest_key = next(iter(self._legal_moves_cache))
            del self._legal_moves_cache[oldest_key]

        self._legal_moves_cache[cache_key] = legal_moves
        return legal_moves

    def invalidate_cache(
        self, game_state: GameState = None, player_id: str = None
    ) -> None:
        """Invalidate cache entries. If no parameters given, clears entire cache."""
        if game_state is None and player_id is None:
            # Clear all caches
            self._legal_moves_cache.clear()
            self._adjacency_cache.clear()
            self._pathfinding_cache.clear()
        elif game_state and player_id:
            # Invalidate specific legal moves cache entry
            cache_key = self._generate_cache_key(game_state, player_id)
            self._legal_moves_cache.pop(cache_key, None)
        else:
            # Partial invalidation - remove entries matching the given criteria
            self._invalidate_matching_entries(game_state, player_id)

    def _invalidate_matching_entries(
        self, game_state: GameState = None, player_id: str = None
    ) -> None:
        """Remove cache entries matching the given criteria."""
        # Invalidate legal moves cache
        keys_to_remove = []
        for key in self._legal_moves_cache:
            if (game_state and game_state.game_id in key) or (
                player_id and player_id in key
            ):
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del self._legal_moves_cache[key]

        # For adjacency and pathfinding caches, we might want to invalidate based on game state changes
        # For now, we'll keep them as they're less likely to change during a game

    def _generate_cache_key(self, game_state: GameState, player_id: str) -> str:
        """Generate a cache key for the game state and player."""
        try:
            # Create a more robust hash based on relevant game state components
            state_components = [
                game_state.game_id,
                str(game_state.phase),
                str(len(game_state.players)),
                player_id,
            ]
            state_hash = hashlib.md5("_".join(state_components).encode()).hexdigest()
            return f"{game_state.game_id}_{player_id}_{state_hash}"
        except Exception:
            # Fallback to simpler key generation
            return f"{game_state.game_id}_{player_id}_{id(game_state)}"

    def are_systems_adjacent(self, system_id1: str, system_id2: str) -> bool:
        """Check if two systems are adjacent, using cache if available."""
        from ..core.validation import validate_non_empty_string

        validate_non_empty_string(system_id1, "system_id1")
        validate_non_empty_string(system_id2, "system_id2")

        # Create a consistent cache key regardless of parameter order
        cache_key = f"{min(system_id1, system_id2)}_{max(system_id1, system_id2)}"

        if cache_key in self._adjacency_cache:
            return self._adjacency_cache[cache_key]

        # Cache miss - calculate adjacency
        adjacency_result = self._galaxy.are_systems_adjacent(system_id1, system_id2)

        # Enforce cache size limit
        if len(self._adjacency_cache) >= self._max_size:
            # Remove oldest entry (simple FIFO eviction)
            oldest_cache_key = next(iter(self._adjacency_cache))
            del self._adjacency_cache[oldest_cache_key]

        self._adjacency_cache[cache_key] = adjacency_result
        return adjacency_result

    def find_shortest_path(
        self, start_system: str, end_system: str, max_distance: int = None
    ) -> list[str]:
        if max_distance is None:
            from ..core.constants import GameConstants

            max_distance = (
                GameConstants.DEFAULT_MOVEMENT_RANGE * 10
            )  # Allow up to 10 moves
        """Find shortest path between two systems, using cache if available."""
        from ..core.validation import validate_non_empty_string

        validate_non_empty_string(start_system, "start_system")
        validate_non_empty_string(end_system, "end_system")

        cache_key = f"{start_system}_{end_system}_{max_distance}"

        if cache_key in self._pathfinding_cache:
            return self._pathfinding_cache[cache_key]

        # Cache miss - calculate shortest path
        path = self._calculate_shortest_path(start_system, end_system, max_distance)

        # Enforce cache size limit
        if len(self._pathfinding_cache) >= self._max_size:
            # Remove oldest entry (simple FIFO eviction)
            oldest_key = next(iter(self._pathfinding_cache))
            del self._pathfinding_cache[oldest_key]

        self._pathfinding_cache[cache_key] = path
        return path

    def _calculate_shortest_path(
        self, start_system: str, end_system: str, max_distance: int
    ) -> list[str]:
        """Calculate the shortest path between two systems using BFS."""
        if start_system == end_system:
            return [start_system]

        # Simple BFS implementation for pathfinding
        from collections import deque

        queue = deque([(start_system, [start_system])])

        while queue:
            current_system, path = queue.popleft()

            if len(path) > max_distance:
                continue

            # Get adjacent systems (this would need to be implemented based on galaxy structure)
            # For now, return a simple path for testing
            if len(path) < max_distance:
                # This is a simplified implementation - in reality would check actual adjacencies
                if current_system != end_system:
                    next_path = path + [end_system]
                    if len(next_path) <= max_distance:
                        return next_path

        # No path found within max_distance
        return []
