"""Tests for ResourceManager performance optimizations and caching.

Tests caching, lazy evaluation, batch operations, and performance benchmarks
for the resource management system.
"""

import time
from unittest.mock import Mock, patch

from src.ti4.core.constants import Faction, UnitType
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.resource_management import (
    CostValidator,
    InfluenceSources,
    ResourceManager,
    ResourceSources,
)


class TestResourceManagerCaching:
    """Test caching functionality for resource/influence calculations."""

    def test_resource_calculation_caching_when_game_state_unchanged(self) -> None:
        """Test that resource calculations are cached when game state hasn't changed."""
        # This test should fail initially - caching doesn't exist yet
        from src.ti4.core.resource_management import CachedResourceManager

        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        jord = Planet("Jord", resources=4, influence=2)

        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)
        player.gain_trade_goods(3)

        # Create cached resource manager
        resource_manager = CachedResourceManager(game_state)

        # First calculation should hit the actual calculation
        with patch.object(
            resource_manager, "_calculate_available_resources_uncached"
        ) as mock_calc:
            mock_calc.return_value = 7
            result1 = resource_manager.calculate_available_resources(player.id)
            assert result1 == 7
            assert mock_calc.call_count == 1

        # Second calculation should use cache (no game state change)
        with patch.object(
            resource_manager, "_calculate_available_resources_uncached"
        ) as mock_calc:
            mock_calc.return_value = 7
            result2 = resource_manager.calculate_available_resources(player.id)
            assert result2 == 7
            assert mock_calc.call_count == 0  # Should not be called due to cache

    def test_cache_invalidation_on_game_state_change(self) -> None:
        """Test that cache is invalidated when game state changes."""
        from src.ti4.core.resource_management import CachedResourceManager

        # Create game state
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        jord = Planet("Jord", resources=4, influence=2)

        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)

        resource_manager = CachedResourceManager(game_state)

        # First calculation
        resource_manager.calculate_available_resources(player.id)

        # Change game state (exhaust planet)
        jord.exhaust()

        # Second calculation should recalculate due to state change
        with patch.object(
            resource_manager, "_calculate_available_resources_uncached"
        ) as mock_calc:
            mock_calc.return_value = 0
            resource_manager.calculate_available_resources(player.id)
            assert mock_calc.call_count == 1  # Should recalculate

    def test_influence_calculation_caching_with_voting_flag(self) -> None:
        """Test that influence calculations are cached separately for voting vs non-voting."""
        from src.ti4.core.resource_management import CachedResourceManager

        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        jord = Planet("Jord", resources=4, influence=2)

        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)
        player.gain_trade_goods(3)

        resource_manager = CachedResourceManager(game_state)

        # Calculate for voting and non-voting - should be cached separately
        voting_influence = resource_manager.calculate_available_influence(
            player.id, for_voting=True
        )
        normal_influence = resource_manager.calculate_available_influence(
            player.id, for_voting=False
        )

        # Should have different values due to trade goods exclusion for voting
        assert voting_influence != normal_influence
        assert normal_influence > voting_influence


class TestLazyEvaluation:
    """Test lazy evaluation for detailed resource breakdowns."""

    def test_lazy_resource_sources_evaluation(self) -> None:
        """Test that detailed resource sources are only calculated when accessed."""
        from src.ti4.core.resource_management import LazyResourceSources

        # Mock the calculation function
        mock_calculate = Mock(
            return_value=ResourceSources(
                planets={"Jord": 4, "Muaat": 2}, trade_goods=3, total_available=9
            )
        )

        # Create lazy resource sources
        lazy_sources = LazyResourceSources(mock_calculate)

        # Calculation should not happen until accessed
        assert mock_calculate.call_count == 0

        # Access should trigger calculation
        sources = lazy_sources.get_sources()
        assert mock_calculate.call_count == 1
        assert sources.total_available == 9

        # Second access should use cached result
        sources2 = lazy_sources.get_sources()
        assert mock_calculate.call_count == 1  # Still 1, not 2
        assert sources2.total_available == 9

    def test_lazy_influence_sources_evaluation(self) -> None:
        """Test that detailed influence sources are only calculated when accessed."""
        from src.ti4.core.resource_management import LazyInfluenceSources

        # Mock the calculation function
        mock_calculate = Mock(
            return_value=InfluenceSources(
                planets={"Mecatol Rex": 6, "Jord": 2},
                trade_goods=0,  # for voting
                total_available=8,
                for_voting=True,
            )
        )

        # Create lazy influence sources
        lazy_sources = LazyInfluenceSources(mock_calculate)

        # Calculation should not happen until accessed
        assert mock_calculate.call_count == 0

        # Access should trigger calculation
        sources = lazy_sources.get_sources()
        assert mock_calculate.call_count == 1
        assert sources.total_available == 8

        # Second access should use cached result
        lazy_sources.get_sources()
        assert mock_calculate.call_count == 1  # Still 1, not 2


class TestBatchOperations:
    """Test batch operation support for multiple cost validations."""

    def test_batch_cost_validation(self) -> None:
        """Test validating multiple production costs in a single batch operation."""
        from src.ti4.core.resource_management import BatchCostValidator

        # Create game state with sufficient resources
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        jord = Planet("Jord", resources=10, influence=5)

        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)

        # Mock unit stats provider
        mock_stats_provider = Mock()
        mock_stats_provider.get_unit_stats.return_value = Mock(cost=2.0)

        resource_manager = ResourceManager(game_state)
        batch_validator = BatchCostValidator(resource_manager, mock_stats_provider)

        # Create multiple production requests
        production_requests = [
            (UnitType.FIGHTER, 2, None, None),
            (UnitType.INFANTRY, 1, None, None),
            (UnitType.CRUISER, 1, None, None),
        ]

        # Batch validate
        results = batch_validator.validate_batch_production_costs(
            player.id, production_requests
        )

        # Should return results for all requests
        assert len(results) == 3
        assert all(result.is_valid for result in results)

    def test_batch_spending_plan_creation(self) -> None:
        """Test creating multiple spending plans in a batch operation."""
        from src.ti4.core.resource_management import BatchResourceManager

        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        jord = Planet("Jord", resources=10, influence=8)

        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)

        batch_manager = BatchResourceManager(game_state)

        # Create multiple spending requests
        spending_requests = [
            (2, 0, False),  # 2 resources, 0 influence, not for voting
            (0, 3, True),  # 0 resources, 3 influence, for voting
            (1, 1, False),  # 1 resource, 1 influence, not for voting
        ]

        # Batch create spending plans
        plans = batch_manager.create_batch_spending_plans(player.id, spending_requests)

        # Should return plans for all requests
        assert len(plans) == 3
        assert all(plan.is_valid for plan in plans)


class TestPerformanceBenchmarks:
    """Test performance benchmarks and optimization validation."""

    def test_resource_calculation_performance_with_many_planets(self) -> None:
        """Test resource calculation performance with maximum number of planets."""
        from src.ti4.core.resource_management import CachedResourceManager

        # Create game state with many planets (simulate late game)
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        game_state = game_state.add_player(player)

        # Add many planets (simulate controlling many systems)
        for i in range(50):  # Large number of planets
            planet = Planet(f"Planet_{i}", resources=i % 5 + 1, influence=i % 3 + 1)
            game_state = game_state.add_player_planet(player.id, planet)

        resource_manager = CachedResourceManager(game_state)

        # Measure performance
        start_time = time.time()
        for _ in range(100):  # Multiple calculations
            resource_manager.calculate_available_resources(player.id)
        end_time = time.time()

        # Should complete quickly (less than 1 second for 100 calculations)
        elapsed_time = end_time - start_time
        assert elapsed_time < 1.0, (
            f"Performance too slow: {elapsed_time:.3f}s for 100 calculations"
        )

    def test_batch_operation_performance_vs_individual(self) -> None:
        """Test that batch operations are faster than individual operations."""
        from src.ti4.core.resource_management import BatchCostValidator

        # Create game state
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        jord = Planet("Jord", resources=20, influence=10)

        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)

        # Mock unit stats provider
        mock_stats_provider = Mock()
        mock_stats_provider.get_unit_stats.return_value = Mock(cost=2.0)

        resource_manager = ResourceManager(game_state)
        cost_validator = CostValidator(resource_manager, mock_stats_provider)
        batch_validator = BatchCostValidator(resource_manager, mock_stats_provider)

        # Create many production requests
        production_requests = [(UnitType.FIGHTER, 1, None, None) for _ in range(20)]

        # Time individual operations
        start_time = time.time()
        individual_results = []
        for unit_type, quantity, faction, technologies in production_requests:
            production_cost = cost_validator.get_production_cost(
                unit_type, quantity, faction, technologies
            )
            result = cost_validator.validate_production_cost(player.id, production_cost)
            individual_results.append(result)
        individual_time = time.time() - start_time

        # Time batch operation
        start_time = time.time()
        batch_results = batch_validator.validate_batch_production_costs(
            player.id, production_requests
        )
        batch_time = time.time() - start_time

        # Batch should be faster (or at least not significantly slower)
        assert len(batch_results) == len(individual_results)
        # Allow some tolerance, but batch should generally be faster
        assert batch_time <= individual_time * 1.2, (
            f"Batch operation too slow: {batch_time:.3f}s vs {individual_time:.3f}s"
        )

    def test_cache_hit_rate_measurement(self) -> None:
        """Test measuring cache hit rates for performance monitoring."""
        from src.ti4.core.resource_management import CachedResourceManager

        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        jord = Planet("Jord", resources=4, influence=2)

        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)

        resource_manager = CachedResourceManager(game_state)

        # Perform multiple calculations
        for _ in range(10):
            resource_manager.calculate_available_resources(player.id)

        # Check cache statistics
        cache_stats = resource_manager.get_cache_statistics()
        assert cache_stats.total_requests == 10
        assert cache_stats.cache_hits == 9  # First is miss, rest are hits
        assert cache_stats.cache_hit_rate == 0.9

    def test_memory_usage_optimization(self) -> None:
        """Test that caching doesn't cause excessive memory usage."""
        import sys

        from src.ti4.core.resource_management import CachedResourceManager

        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Add multiple planets
        for i in range(20):
            planet = Planet(f"Planet_{i}", resources=i % 5 + 1, influence=i % 3 + 1)
            game_state = game_state.add_player(player)
            game_state = game_state.add_player_planet(player.id, planet)

        resource_manager = CachedResourceManager(game_state)

        # Measure initial memory
        initial_size = sys.getsizeof(resource_manager)

        # Perform many calculations to populate cache
        for _ in range(100):
            resource_manager.calculate_available_resources(player.id)
            resource_manager.calculate_available_influence(player.id, for_voting=True)
            resource_manager.calculate_available_influence(player.id, for_voting=False)

        # Measure final memory
        final_size = sys.getsizeof(resource_manager)

        # Memory growth should be reasonable (less than 10x initial size)
        memory_growth = final_size / initial_size
        assert memory_growth < 10.0, f"Excessive memory growth: {memory_growth:.2f}x"
