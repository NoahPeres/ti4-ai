"""Tests for comprehensive resource management error handling.

Tests custom exception classes, detailed error messages, atomic rollback,
and logging for Rule 26: COST, Rule 75: RESOURCES, and Rule 47: INFLUENCE.
"""

from unittest.mock import Mock, patch

import pytest

from src.ti4.core.constants import Faction, UnitType
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.resource_management import (
    CostCalculationError,
    CostValidator,
    GameStateIntegrityError,
    InsufficientInfluenceError,
    InsufficientResourcesError,
    InvalidSpendingPlanError,
    PlanetExhaustionError,
    ResourceError,
    ResourceManager,
    ResourceOperationError,
)


class TestResourceExceptions:
    """Test custom exception classes for resource-related errors."""

    def test_resource_error_base_exception(self) -> None:
        """Test ResourceError base exception."""
        error = ResourceError("Base resource error")
        assert str(error) == "Base resource error"
        assert isinstance(error, Exception)

    def test_insufficient_resources_error(self) -> None:
        """Test InsufficientResourcesError with detailed information."""
        error = InsufficientResourcesError(
            required=10,
            available=5,
            shortfall=5,
            player_id="player1",
            context={"operation": "production"},
        )

        assert error.required == 10
        assert error.available == 5
        assert error.shortfall == 5
        assert error.player_id == "player1"
        assert error.context["operation"] == "production"
        assert "need 10" in str(error)
        assert "have 5" in str(error)
        assert "shortfall: 5" in str(error)

    def test_insufficient_influence_error(self) -> None:
        """Test InsufficientInfluenceError with voting context."""
        error = InsufficientInfluenceError(
            required=8,
            available=3,
            shortfall=5,
            player_id="player2",
            for_voting=True,
            context={"agenda": "Research Team"},
        )

        assert error.required == 8
        assert error.available == 3
        assert error.shortfall == 5
        assert error.player_id == "player2"
        assert error.for_voting is True
        assert error.context["agenda"] == "Research Team"
        assert "voting" in str(error)

    def test_invalid_spending_plan_error(self) -> None:
        """Test InvalidSpendingPlanError with plan details."""
        error = InvalidSpendingPlanError(
            plan_id="plan123",
            reason="Planet already exhausted",
            player_id="player1",
            context={"planet": "Jord", "operation": "resource_spending"},
        )

        assert error.plan_id == "plan123"
        assert error.reason == "Planet already exhausted"
        assert error.player_id == "player1"
        assert error.context["planet"] == "Jord"

    def test_planet_exhaustion_error(self) -> None:
        """Test PlanetExhaustionError with planet details."""
        error = PlanetExhaustionError(
            planet_name="Mecatol Rex",
            player_id="player1",
            operation="influence_spending",
            context={"current_state": "exhausted"},
        )

        assert error.planet_name == "Mecatol Rex"
        assert error.player_id == "player1"
        assert error.operation == "influence_spending"
        assert error.context["current_state"] == "exhausted"

    def test_resource_operation_error(self) -> None:
        """Test ResourceOperationError with operation context."""
        error = ResourceOperationError(
            operation="execute_spending_plan",
            player_id="player1",
            reason="Trade goods transaction failed",
            context={"trade_goods_needed": 5, "trade_goods_available": 2},
        )

        assert error.operation == "execute_spending_plan"
        assert error.player_id == "player1"
        assert error.reason == "Trade goods transaction failed"
        assert error.context["trade_goods_needed"] == 5

    def test_cost_calculation_error(self) -> None:
        """Test CostCalculationError with unit type and calculation context."""
        error = CostCalculationError(
            unit_type=UnitType.CRUISER,
            reason="Invalid cost modifier applied",
            context={
                "faction": "Sol",
                "technologies": ["Cruiser II"],
                "raw_cost": -1.5,
            },
        )

        assert error.unit_type == UnitType.CRUISER
        assert error.reason == "Invalid cost modifier applied"
        assert error.context["faction"] == "Sol"
        assert "CRUISER" in str(error)

    def test_game_state_integrity_error(self) -> None:
        """Test GameStateIntegrityError with integrity issue details."""
        error = GameStateIntegrityError(
            operation="execute_spending_plan",
            integrity_issue="Negative resource cost detected",
            context={"resource_cost": -5, "influence_cost": 3},
        )

        assert error.operation == "execute_spending_plan"
        assert error.integrity_issue == "Negative resource cost detected"
        assert error.context["resource_cost"] == -5
        assert "integrity compromised" in str(error)


class TestResourceManagerErrorHandling:
    """Test ResourceManager enhanced error handling."""

    def test_calculate_resources_with_invalid_player(self) -> None:
        """Test that calculating resources for invalid player raises proper error."""
        game_state = GameState()
        resource_manager = ResourceManager(game_state)

        with pytest.raises(ResourceOperationError) as exc_info:
            resource_manager.calculate_available_resources("nonexistent_player")

        error = exc_info.value
        assert error.operation == "calculate_available_resources"
        assert error.player_id == "nonexistent_player"
        assert "Player not found" in error.reason

    def test_create_spending_plan_insufficient_resources_detailed_error(self) -> None:
        """Test that insufficient resources creates detailed error message."""
        # Create game state with limited resources
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        planet = Planet("Poor Planet", resources=2, influence=1)

        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet)

        resource_manager = ResourceManager(game_state)

        # Try to create plan requiring more resources than available
        plan = resource_manager.create_spending_plan(player.id, resource_amount=10)

        assert plan.is_valid is False
        assert plan.error_message is not None
        assert "Insufficient resources" in plan.error_message
        assert "need 10" in plan.error_message
        assert "have 2" in plan.error_message
        assert "shortfall: 8" in plan.error_message

    def test_execute_spending_plan_with_detailed_rollback_logging(self) -> None:
        """Test that spending plan execution logs rollback operations."""
        # This test will fail initially - we need to implement logging
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        planet = Planet("Test Planet", resources=3, influence=2)

        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet)

        resource_manager = ResourceManager(game_state)

        # Create invalid plan that will trigger rollback
        from src.ti4.core.resource_management import (
            InfluenceSpending,
            ResourceSpending,
            SpendingPlan,
        )

        resource_spending = ResourceSpending(
            planets_to_exhaust={"Test Planet": 3},
            trade_goods_to_spend=10,  # More than player has
            total_resources=13,
        )
        influence_spending = InfluenceSpending(
            planets_to_exhaust={}, trade_goods_to_spend=0, total_influence=0
        )

        plan = SpendingPlan(
            player_id=player.id,
            resource_spending=resource_spending,
            influence_spending=influence_spending,
            total_resource_cost=13,
            total_influence_cost=0,
            is_valid=True,  # Force valid to test rollback
        )

        with patch("src.ti4.core.resource_management.logger") as mock_logger:
            result = resource_manager.execute_spending_plan(plan)

            # Should have logged rollback operations
            assert result.success is False
            mock_logger.warning.assert_called()
            mock_logger.info.assert_called()


class TestCostValidatorErrorHandling:
    """Test CostValidator enhanced error handling."""

    def test_cost_calculation_error_handling(self) -> None:
        """Test that cost calculation errors are properly handled."""
        game_state = GameState()
        resource_manager = ResourceManager(game_state)

        # Mock unit stats provider that returns invalid cost
        mock_stats_provider = Mock()
        mock_unit_stats = Mock()
        mock_unit_stats.cost = float("nan")  # Invalid cost
        mock_stats_provider.get_unit_stats.return_value = mock_unit_stats

        cost_validator = CostValidator(resource_manager, mock_stats_provider)

        with pytest.raises(CostCalculationError) as exc_info:
            cost_validator.get_unit_cost(UnitType.CRUISER)

        error = exc_info.value
        assert error.unit_type == UnitType.CRUISER
        assert "Invalid cost value" in error.reason
        assert "raw_cost" in error.context

    def test_cost_calculation_with_infinite_cost(self) -> None:
        """Test that infinite costs are properly handled."""
        game_state = GameState()
        resource_manager = ResourceManager(game_state)

        # Mock unit stats provider that returns infinite cost
        mock_stats_provider = Mock()
        mock_unit_stats = Mock()
        mock_unit_stats.cost = float("inf")  # Infinite cost
        mock_stats_provider.get_unit_stats.return_value = mock_unit_stats

        cost_validator = CostValidator(resource_manager, mock_stats_provider)

        with pytest.raises(CostCalculationError) as exc_info:
            cost_validator.get_unit_cost(UnitType.FIGHTER)

        error = exc_info.value
        assert error.unit_type == UnitType.FIGHTER
        assert "Invalid cost value" in error.reason

    def test_validate_production_cost_with_detailed_error_context(self) -> None:
        """Test that cost validation provides detailed error context."""
        # This test will fail initially - we need enhanced error messages
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        game_state = game_state.add_player(player)

        resource_manager = ResourceManager(game_state)

        # Mock unit stats provider
        mock_stats_provider = Mock()
        mock_stats_provider.get_unit_stats.return_value = Mock(cost=5.0)

        cost_validator = CostValidator(resource_manager, mock_stats_provider)

        # Create production cost that exceeds available resources
        production_cost = cost_validator.get_production_cost(
            UnitType.CRUISER, quantity=2
        )

        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        assert validation_result.is_valid is False
        assert validation_result.error_message is not None

        # Should include detailed context
        error_msg = validation_result.error_message
        assert "Cruiser" in error_msg or "production" in error_msg
        assert str(validation_result.required_resources) in error_msg
        assert str(validation_result.available_resources) in error_msg

    def test_validate_zero_cost_unit_production_error(self) -> None:
        """Test that zero-cost unit production raises appropriate error."""
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        game_state = game_state.add_player(player)

        resource_manager = ResourceManager(game_state)

        # Mock unit stats provider for zero-cost unit
        mock_stats_provider = Mock()
        mock_stats_provider.get_unit_stats.return_value = Mock(cost=0.0)

        cost_validator = CostValidator(resource_manager, mock_stats_provider)

        production_cost = cost_validator.get_production_cost(
            UnitType.SPACE_DOCK, quantity=1
        )

        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        assert validation_result.is_valid is False
        assert "Rule 26.3" in validation_result.error_message
        assert (
            "without cost cannot be produced normally"
            in validation_result.error_message
        )


class TestAtomicOperationRollback:
    """Test atomic operation rollback for failed spending."""

    def test_game_state_integrity_error_on_negative_costs(self) -> None:
        """Test that negative costs trigger game state integrity error."""
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        game_state = game_state.add_player(player)

        resource_manager = ResourceManager(game_state)

        # Create plan with negative costs (should trigger integrity error)
        from src.ti4.core.resource_management import (
            InfluenceSpending,
            ResourceSpending,
            SpendingPlan,
        )

        resource_spending = ResourceSpending(
            planets_to_exhaust={},
            trade_goods_to_spend=0,
            total_resources=0,
        )
        influence_spending = InfluenceSpending(
            planets_to_exhaust={},
            trade_goods_to_spend=0,
            total_influence=0,
        )

        plan = SpendingPlan(
            player_id=player.id,
            resource_spending=resource_spending,
            influence_spending=influence_spending,
            total_resource_cost=-5,  # Negative cost should trigger error
            total_influence_cost=0,
            is_valid=True,  # Force valid to test integrity check
        )

        with pytest.raises(GameStateIntegrityError) as exc_info:
            resource_manager.execute_spending_plan(plan)

        error = exc_info.value
        assert error.operation == "execute_spending_plan"
        assert "Negative costs detected" in error.integrity_issue

    def test_spending_plan_rollback_preserves_game_state(self) -> None:
        """Test that failed spending plan execution preserves original game state."""
        # Create initial game state
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        planet1 = Planet("Planet1", resources=3, influence=2)
        planet2 = Planet("Planet2", resources=2, influence=1)

        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet1)
        game_state = game_state.add_player_planet(player.id, planet2)

        player.gain_trade_goods(5)

        # Capture initial state
        initial_trade_goods = player.get_trade_goods()
        initial_planets_exhausted = [
            p.is_exhausted() for p in game_state.get_player_planets(player.id)
        ]

        resource_manager = ResourceManager(game_state)

        # Create plan that will fail (insufficient trade goods)
        from src.ti4.core.resource_management import (
            InfluenceSpending,
            ResourceSpending,
            SpendingPlan,
        )

        resource_spending = ResourceSpending(
            planets_to_exhaust={"Planet1": 3, "Planet2": 2},
            trade_goods_to_spend=10,  # More than available
            total_resources=15,
        )
        influence_spending = InfluenceSpending(
            planets_to_exhaust={}, trade_goods_to_spend=0, total_influence=0
        )

        plan = SpendingPlan(
            player_id=player.id,
            resource_spending=resource_spending,
            influence_spending=influence_spending,
            total_resource_cost=15,
            total_influence_cost=0,
            is_valid=True,  # Force valid to test rollback
        )

        # Execute plan - should fail and rollback
        result = resource_manager.execute_spending_plan(plan)

        assert result.success is False

        # Verify rollback preserved original state
        assert player.get_trade_goods() == initial_trade_goods

        current_planets_exhausted = [
            p.is_exhausted() for p in game_state.get_player_planets(player.id)
        ]
        assert current_planets_exhausted == initial_planets_exhausted

    def test_partial_planet_exhaustion_rollback(self) -> None:
        """Test rollback when some planets are exhausted before failure occurs."""
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        planet1 = Planet("Planet1", resources=3, influence=2)
        planet2 = Planet("Planet2", resources=2, influence=1)
        planet3 = Planet("Planet3", resources=1, influence=3)

        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet1)
        game_state = game_state.add_player_planet(player.id, planet2)
        game_state = game_state.add_player_planet(player.id, planet3)

        resource_manager = ResourceManager(game_state)

        # Create plan that will fail after exhausting some planets
        from src.ti4.core.resource_management import (
            InfluenceSpending,
            ResourceSpending,
            SpendingPlan,
        )

        resource_spending = ResourceSpending(
            planets_to_exhaust={"Planet1": 3, "Planet2": 2},
            trade_goods_to_spend=0,
            total_resources=5,
        )
        influence_spending = InfluenceSpending(
            planets_to_exhaust={"Planet3": 3, "NonexistentPlanet": 1},  # This will fail
            trade_goods_to_spend=0,
            total_influence=4,
        )

        plan = SpendingPlan(
            player_id=player.id,
            resource_spending=resource_spending,
            influence_spending=influence_spending,
            total_resource_cost=5,
            total_influence_cost=4,
            is_valid=True,  # Force valid to test rollback
        )

        # Execute plan - should fail and rollback all exhausted planets
        result = resource_manager.execute_spending_plan(plan)

        assert result.success is False

        # All planets should be ready (rolled back)
        for planet in game_state.get_player_planets(player.id):
            assert not planet.is_exhausted()


class TestLoggingAndDebugging:
    """Test logging and debugging support for resource operations."""

    def test_resource_operation_logging(self) -> None:
        """Test that resource operations are properly logged."""
        # This test will fail initially - we need to implement logging
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        planet = Planet("Test Planet", resources=5, influence=3)

        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet)

        resource_manager = ResourceManager(game_state)

        with patch("src.ti4.core.resource_management.logger") as mock_logger:
            # Test successful operation logging
            plan = resource_manager.create_spending_plan(player.id, resource_amount=3)
            result = resource_manager.execute_spending_plan(plan)

            # Should log operation start and success
            mock_logger.info.assert_called()
            assert result.success is True

    def test_error_context_preservation(self) -> None:
        """Test that error context is preserved through the call stack."""
        game_state = GameState()
        resource_manager = ResourceManager(game_state)

        try:
            resource_manager.calculate_available_resources("nonexistent")
        except ResourceOperationError as e:
            assert e.operation == "calculate_available_resources"
            assert e.player_id == "nonexistent"
            assert e.context is not None
            assert "timestamp" in e.context
        else:
            pytest.fail("Expected ResourceOperationError to be raised")

    def test_debug_information_in_errors(self) -> None:
        """Test that debug information is included in error messages."""
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        game_state = game_state.add_player(player)

        resource_manager = ResourceManager(game_state)

        # Try to create spending plan with no resources
        plan = resource_manager.create_spending_plan(player.id, resource_amount=10)

        assert plan.is_valid is False
        assert plan.error_message is not None

        # Error should include debug information
        error_msg = plan.error_message
        assert "player1" in error_msg or "Player" in error_msg
        assert "10" in error_msg  # Required amount
        assert "0" in error_msg  # Available amount
