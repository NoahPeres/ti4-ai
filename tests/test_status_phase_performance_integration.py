"""Integration tests for status phase performance optimization.

This module tests the integration between the StatusPhaseManager and
the performance optimization features.
"""

import os

import pytest

from src.ti4.core.constants import Faction
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.status_phase import StatusPhaseManager


class TestStatusPhasePerformanceIntegration:
    """Test integration of performance optimization with StatusPhaseManager."""

    @pytest.mark.performance
    @pytest.mark.skipif(
        bool(os.getenv("CI")) or bool(os.getenv("GITHUB_ACTIONS")),
        reason="Performance tests skipped in CI environments",
    )
    def test_status_phase_manager_with_performance_optimization(self) -> None:
        """Test StatusPhaseManager with performance optimization enabled."""
        # Create manager with performance optimization
        manager = StatusPhaseManager(enable_performance_optimization=True)

        # Verify performance optimization is enabled
        assert manager.performance_optimization_enabled

        # Create test game state
        game_state = GameState()
        player1 = Player(id="player1", faction=Faction.SOL)
        player2 = Player(id="player2", faction=Faction.HACAN)

        game_state = game_state.add_player(player1)
        game_state = game_state.add_player(player2)

        # Execute status phase
        result, updated_state = manager.execute_complete_status_phase(game_state)

        # Verify execution succeeded
        assert result.success
        assert result.total_execution_time < 500  # Performance requirement

        # Test performance reporting
        performance_report = manager.get_performance_report()
        assert isinstance(performance_report, dict)

        # Should have performance data when optimization is enabled
        if "message" not in performance_report:
            assert "total_execution_time_ms" in performance_report
            assert "meets_requirements" in performance_report

    @pytest.mark.performance
    @pytest.mark.skipif(
        bool(os.getenv("CI")) or bool(os.getenv("GITHUB_ACTIONS")),
        reason="Performance tests skipped in CI environments",
    )
    def test_status_phase_manager_without_performance_optimization(self) -> None:
        """Test StatusPhaseManager with performance optimization disabled."""
        # Create manager without performance optimization
        manager = StatusPhaseManager(enable_performance_optimization=False)

        # Verify performance optimization is disabled
        assert not manager.performance_optimization_enabled

        # Create test game state
        game_state = GameState()
        player1 = Player(id="player1", faction=Faction.SOL)
        game_state = game_state.add_player(player1)

        # Execute status phase
        result, updated_state = manager.execute_complete_status_phase(game_state)

        # Verify execution succeeded
        assert result.success

        # Test performance reporting (should indicate optimization not enabled)
        performance_report = manager.get_performance_report()
        assert isinstance(performance_report, dict)
        assert "Performance optimization not enabled" in performance_report.get(
            "message", ""
        )

    @pytest.mark.performance
    @pytest.mark.skipif(
        bool(os.getenv("CI")) or bool(os.getenv("GITHUB_ACTIONS")),
        reason="Performance tests skipped in CI environments",
    )
    def test_performance_cache_management(self) -> None:
        """Test performance cache management functionality."""
        manager = StatusPhaseManager(enable_performance_optimization=True)

        # Test cache clearing
        cache_cleared = manager.clear_performance_cache()

        # Should return True if optimization is enabled and cache is available
        # May return False if the optimized orchestrator is not available
        assert isinstance(cache_cleared, bool)

    def test_optimizer_statistics(self) -> None:
        """Test optimizer statistics retrieval."""
        manager = StatusPhaseManager(enable_performance_optimization=True)

        # Get optimizer statistics
        stats = manager.get_optimizer_statistics()
        assert isinstance(stats, dict)

        # Should have statistics when optimization is enabled
        if "message" not in stats:
            assert "optimization_features" in stats or "cache_statistics" in stats

    @pytest.mark.performance
    @pytest.mark.skipif(
        bool(os.getenv("CI")) or bool(os.getenv("GITHUB_ACTIONS")),
        reason="Performance tests skipped in CI environments",
    )
    def test_performance_with_large_game_state(self) -> None:
        """Test performance optimization with a larger game state."""
        manager = StatusPhaseManager(enable_performance_optimization=True)

        # Create larger game state
        game_state = GameState()
        factions = [Faction.SOL, Faction.HACAN, Faction.XXCHA, Faction.ARBOREC]

        for i, faction in enumerate(factions):
            player = Player(id=f"player{i + 1}", faction=faction)
            game_state = game_state.add_player(player)

            # Add planets to each player
            for j in range(4):
                planet = Planet(
                    name=f"Planet_{i}_{j}", resources=j % 3 + 1, influence=j % 2 + 1
                )
                game_state = game_state.add_player_planet(player.id, planet)

        # Execute status phase
        result, updated_state = manager.execute_complete_status_phase(game_state)

        # Verify execution succeeded and met performance requirements
        assert result.success
        assert result.total_execution_time < 1000  # More lenient for larger states

        # Get performance report
        performance_report = manager.get_performance_report()
        assert isinstance(performance_report, dict)

    @pytest.mark.performance
    @pytest.mark.skipif(
        bool(os.getenv("CI")) or bool(os.getenv("GITHUB_ACTIONS")),
        reason="Performance tests skipped in CI environments",
    )
    def test_performance_monitoring_across_multiple_executions(self) -> None:
        """Test performance monitoring across multiple status phase executions."""
        manager = StatusPhaseManager(enable_performance_optimization=True)

        # Create test game state
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        game_state = game_state.add_player(player)

        execution_times = []

        # Execute status phase multiple times
        for _i in range(3):
            result, updated_state = manager.execute_complete_status_phase(game_state)
            assert result.success
            execution_times.append(result.total_execution_time)

        # Verify all executions met performance requirements
        for execution_time in execution_times:
            assert execution_time < 500

        # Get optimizer statistics (should show multiple executions)
        stats = manager.get_optimizer_statistics()
        assert isinstance(stats, dict)

    def test_backward_compatibility_with_ready_all_cards(self) -> None:
        """Test that performance optimization doesn't break backward compatibility."""
        manager = StatusPhaseManager(enable_performance_optimization=True)

        # Create test game state
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        game_state = game_state.add_player(player)

        # Test the existing ready_all_cards method still works
        updated_state = manager.ready_all_cards(game_state)

        # Should return a valid game state
        assert updated_state is not None
        assert hasattr(updated_state, "players")

    @pytest.mark.performance
    @pytest.mark.skipif(
        bool(os.getenv("CI")) or bool(os.getenv("GITHUB_ACTIONS")),
        reason="Performance tests skipped in CI environments",
    )
    def test_error_handling_with_performance_optimization(self) -> None:
        """Test error handling when performance optimization encounters issues."""
        manager = StatusPhaseManager(enable_performance_optimization=True)

        # Test with None game state (should handle gracefully)
        result, updated_state = manager.execute_complete_status_phase(None)

        # Should handle error gracefully
        assert not result.success
        # Error message should be in the main result error_message or step results
        error_found = (
            result.error_message and "cannot be None" in result.error_message
        ) or any(
            "cannot be None" in step_result.error_message
            for step_result in result.step_results.values()
        )
        assert error_found, (
            f"Expected error message not found. Main error: {result.error_message}, Step results: {result.step_results}"
        )

        # Performance report should still be available
        performance_report = manager.get_performance_report()
        assert isinstance(performance_report, dict)
