"""Concurrent game support for TI4."""

import threading
import time
import uuid
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from src.ti4.core.game_state import GameState
from src.ti4.performance.monitoring import ResourceMonitor


@dataclass
class GameInstance:
    """Represents an isolated game instance."""

    game_id: str
    game_state: GameState
    lock: threading.RLock = field(default_factory=threading.RLock)
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    active_operations = 0


class ConcurrentGameManager:
    """Manages multiple concurrent game instances with thread safety."""

    def __init__(self, max_concurrent_games: Optional[int] = None) -> None:
        """Initialize the concurrent game manager."""
        if max_concurrent_games is None:
            from ..core.constants import PerformanceConstants

            max_concurrent_games = PerformanceConstants.DEFAULT_MAX_CONCURRENT_GAMES
        self._max_concurrent_games = max_concurrent_games
        self._games: dict[str, GameInstance] = {}
        self._global_lock = threading.RLock()
        self._monitor = ResourceMonitor()
        from ..core.constants import PerformanceConstants

        self._executor = ThreadPoolExecutor(
            max_workers=PerformanceConstants.DEFAULT_MAX_WORKERS,
            thread_name_prefix=PerformanceConstants.THREAD_NAME_PREFIX,
        )

    def create_game(self, game_id: Optional[str] = None) -> str:
        """Create a new game instance."""
        if game_id is None:
            game_id = str(uuid.uuid4())

        with self._global_lock:
            if game_id in self._games:
                raise ValueError(f"Game {game_id} already exists")

            # Check if we're at capacity
            if len(self._games) >= self._max_concurrent_games:
                self._cleanup_inactive_games()

                if len(self._games) >= self._max_concurrent_games:
                    raise RuntimeError("Maximum concurrent games limit reached")

            game_state = GameState(game_id=game_id)
            game_instance = GameInstance(game_id=game_id, game_state=game_state)

            self._games[game_id] = game_instance
            return game_id

    def get_game(self, game_id: str) -> Optional[GameInstance]:
        """Get a game instance by ID."""
        with self._global_lock:
            game_instance = self._games.get(game_id)
            if game_instance:
                game_instance.last_accessed = time.time()
            return game_instance

    def execute_game_operation(
        self, game_id: str, operation: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> Future[Any]:
        """Execute an operation on a game instance in a thread-safe manner."""
        game_instance = self.get_game(game_id)
        if not game_instance:
            raise ValueError(f"Game {game_id} not found")

        def safe_operation() -> Any:
            with game_instance.lock:
                game_instance.active_operations += 1
                try:
                    start_time = time.time()
                    result = operation(game_instance.game_state, *args, **kwargs)
                    duration = time.time() - start_time
                    operation_name = getattr(operation, "__name__", "unknown_operation")
                    self._monitor.record_operation_time(
                        f"game_operation_{operation_name}", duration
                    )
                    return result
                finally:
                    game_instance.active_operations -= 1

        return self._executor.submit(safe_operation)

    def remove_game(self, game_id: str) -> bool:
        """Remove a game instance."""
        with self._global_lock:
            game_instance = self._games.get(game_id)
            if not game_instance:
                return False

            # Wait for active operations to complete
            with game_instance.lock:
                while game_instance.active_operations > 0:
                    from ..core.constants import PerformanceConstants

                    time.sleep(
                        PerformanceConstants.OPERATION_SLEEP_DELAY
                    )  # Small delay to avoid busy waiting

                del self._games[game_id]
                return True

    def get_active_games(self) -> set[str]:
        """Get set of active game IDs."""
        with self._global_lock:
            return set(self._games.keys())

    def get_game_stats(self) -> dict[str, Any]:
        """Get statistics about managed games."""
        with self._global_lock:
            total_games = len(self._games)
            active_operations = sum(
                game.active_operations for game in self._games.values()
            )

            if self._games:
                avg_age = (
                    time.time()
                    - sum(game.created_at for game in self._games.values())
                    / total_games
                )
                oldest_game = min(game.created_at for game in self._games.values())
            else:
                avg_age = 0
                oldest_game = time.time()

            return {
                "total_games": total_games,
                "max_concurrent_games": self._max_concurrent_games,
                "active_operations": active_operations,
                "average_game_age_seconds": avg_age,
                "oldest_game_age_seconds": time.time() - oldest_game,
                "thread_pool_active": self._executor._threads is not None,
            }

    def _cleanup_inactive_games(self) -> None:
        """Remove inactive games to free up space."""
        current_time = time.time()
        from ..core.constants import PerformanceConstants

        inactive_threshold = current_time - PerformanceConstants.INACTIVE_GAME_THRESHOLD

        games_to_remove = []
        for game_id, game_instance in self._games.items():
            if (
                game_instance.last_accessed < inactive_threshold
                and game_instance.active_operations == 0
            ):
                games_to_remove.append(game_id)

        for game_id in games_to_remove:
            del self._games[game_id]

    def shutdown(self) -> None:
        """Shutdown the concurrent game manager."""
        with self._global_lock:
            # Wait for all operations to complete
            for game_instance in self._games.values():
                with game_instance.lock:
                    while game_instance.active_operations > 0:
                        from ..core.constants import PerformanceConstants

                        time.sleep(PerformanceConstants.OPERATION_SLEEP_DELAY)

            # Shutdown thread pool
            self._executor.shutdown(wait=True)

            # Clear games
            self._games.clear()


class ThreadSafeGameStateCache:
    """Thread-safe version of game state cache."""

    def __init__(self, max_size: Optional[int] = None) -> None:
        """Initialize thread-safe cache."""
        if max_size is None:
            from ..core.constants import PerformanceConstants

            max_size = PerformanceConstants.DEFAULT_CACHE_SIZE
        from src.ti4.performance.cache import GameStateCache

        self._cache = GameStateCache(max_size)
        self._lock = threading.RLock()

    def get_legal_moves(self, game_state: GameState, player_id: str) -> Any:
        """Thread-safe legal moves retrieval."""
        with self._lock:
            return self._cache.get_legal_moves(game_state, player_id)

    def are_systems_adjacent(self, system_id1: str, system_id2: str) -> bool:
        """Thread-safe adjacency check."""
        with self._lock:
            return self._cache.are_systems_adjacent(system_id1, system_id2)

    def find_shortest_path(
        self, start_system: str, end_system: str, max_distance: Optional[int] = None
    ) -> Any:
        """Thread-safe pathfinding."""
        if max_distance is None:
            from ..core.constants import GameConstants

            max_distance = GameConstants.DEFAULT_MOVEMENT_RANGE * 10
        with self._lock:
            return self._cache.find_shortest_path(
                start_system, end_system, max_distance
            )

    def invalidate_cache(
        self, game_state: Optional[GameState] = None, player_id: Optional[str] = None
    ) -> None:
        """Thread-safe cache invalidation."""
        with self._lock:
            self._cache.invalidate_cache(game_state, player_id)


# Global concurrent game manager
_global_game_manager: Optional[ConcurrentGameManager] = None
_manager_lock = threading.Lock()


def get_game_manager() -> ConcurrentGameManager:
    """Get the global concurrent game manager."""
    global _global_game_manager
    with _manager_lock:
        if _global_game_manager is None:
            _global_game_manager = ConcurrentGameManager()
        return _global_game_manager


def shutdown_game_manager() -> None:
    """Shutdown the global game manager."""
    global _global_game_manager
    with _manager_lock:
        if _global_game_manager:
            _global_game_manager.shutdown()
            _global_game_manager = None
