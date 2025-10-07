"""Tests for enhanced ProductionManager with cost integration.

This module tests the enhanced ProductionManager that integrates with
ResourceManager and CostValidator for complete production cost validation
and execution according to Rule 26: COST and Rule 67: PRODUCING UNITS.
"""

from unittest.mock import Mock

import pytest

from src.ti4.core.constants import UnitType
from src.ti4.core.production import ProductionManager
from src.ti4.core.resource_management import (
    CostValidationResult,
    CostValidator,
    InfluenceSpending,
    ProductionCost,
    ResourceManager,
    ResourceSpending,
    SpendingPlan,
    SpendingResult,
)
from src.ti4.core.unit_stats import UnitStatsProvider


class TestEnhancedProductionManagerInitialization:
    """Test enhanced ProductionManager initialization with dependencies."""

    def test_enhanced_production_manager_accepts_dependencies(self) -> None:
        """Test that ProductionManager can be initialized with ResourceManager and CostValidator."""
        # Create mock dependencies
        game_state = Mock()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # This should work - enhanced ProductionManager accepts dependencies
        production_manager = ProductionManager(resource_manager, cost_validator)

        assert production_manager is not None
        assert hasattr(production_manager, "resource_manager")
        assert hasattr(production_manager, "cost_validator")

    def test_enhanced_production_manager_maintains_backward_compatibility(self) -> None:
        """Test that ProductionManager can still be initialized without dependencies for backward compatibility."""
        # This should still work for backward compatibility
        production_manager = ProductionManager()

        assert production_manager is not None


class TestProductionValidation:
    """Test integrated production validation with cost, reinforcement, and placement checks."""

    def test_validate_production_with_sufficient_resources_and_reinforcements(
        self,
    ) -> None:
        """Test production validation when player has sufficient resources and reinforcements."""
        # Setup
        Mock()
        resource_manager = Mock(spec=ResourceManager)
        cost_validator = Mock(spec=CostValidator)

        # Mock successful cost validation
        production_cost = ProductionCost(
            unit_type=UnitType.FIGHTER,
            base_cost=1.0,
            modified_cost=1.0,
            quantity_requested=1,
            units_produced=2,  # Dual production
            total_cost=1.0,
            is_dual_production=True,
        )

        cost_validation_result = CostValidationResult(
            is_valid=True,
            required_resources=1,
            available_resources=5,
            shortfall=0,
            reinforcement_shortfall=0,
        )

        cost_validator.get_production_cost.return_value = production_cost
        cost_validator.validate_production_cost_with_reinforcements.return_value = (
            cost_validation_result
        )

        production_manager = ProductionManager(resource_manager, cost_validator)

        # Test validation
        result = production_manager.validate_production(
            player_id="player1",
            unit_type=UnitType.FIGHTER,
            quantity=1,
            available_reinforcements=3,
        )

        assert result.is_valid is True
        assert result.production_cost == production_cost
        assert result.cost_validation == cost_validation_result

    def test_validate_production_with_insufficient_resources(self) -> None:
        """Test production validation when player has insufficient resources."""
        # Setup
        Mock()
        resource_manager = Mock(spec=ResourceManager)
        cost_validator = Mock(spec=CostValidator)

        # Mock failed cost validation
        production_cost = ProductionCost(
            unit_type=UnitType.CRUISER,
            base_cost=2.0,
            modified_cost=2.0,
            quantity_requested=1,
            units_produced=1,
            total_cost=2.0,
            is_dual_production=False,
        )

        cost_validation_result = CostValidationResult(
            is_valid=False,
            required_resources=2,
            available_resources=1,
            shortfall=1,
            error_message="Insufficient resources: need 2, have 1 (shortfall: 1)",
        )

        cost_validator.get_production_cost.return_value = production_cost
        cost_validator.validate_production_cost_with_reinforcements.return_value = (
            cost_validation_result
        )

        production_manager = ProductionManager(resource_manager, cost_validator)

        # Test validation
        result = production_manager.validate_production(
            player_id="player1",
            unit_type=UnitType.CRUISER,
            quantity=1,
            available_reinforcements=5,
        )

        assert result.is_valid is False
        assert (
            result.error_message
            == "Insufficient resources: need 2, have 1 (shortfall: 1)"
        )

    def test_validate_production_with_insufficient_reinforcements(self) -> None:
        """Test production validation when player has insufficient reinforcements."""
        # Setup
        Mock()
        resource_manager = Mock(spec=ResourceManager)
        cost_validator = Mock(spec=CostValidator)

        # Mock cost validation with reinforcement shortfall
        production_cost = ProductionCost(
            unit_type=UnitType.FIGHTER,
            base_cost=1.0,
            modified_cost=1.0,
            quantity_requested=1,
            units_produced=2,  # Dual production
            total_cost=1.0,
            is_dual_production=True,
        )

        cost_validation_result = CostValidationResult(
            is_valid=False,
            required_resources=1,
            available_resources=5,
            shortfall=0,
            reinforcement_shortfall=1,
            error_message="Insufficient reinforcements: need 2, have 1 (shortfall: 1)",
        )

        cost_validator.get_production_cost.return_value = production_cost
        cost_validator.validate_production_cost_with_reinforcements.return_value = (
            cost_validation_result
        )

        production_manager = ProductionManager(resource_manager, cost_validator)

        # Test validation
        result = production_manager.validate_production(
            player_id="player1",
            unit_type=UnitType.FIGHTER,
            quantity=1,
            available_reinforcements=1,  # Not enough for dual production
        )

        assert result.is_valid is False
        assert "reinforcements" in result.error_message.lower()


class TestProductionExecution:
    """Test integrated production execution with atomic cost payment and unit placement."""

    def test_execute_production_with_successful_cost_payment(self) -> None:
        """Test production execution when cost payment succeeds."""
        # Setup
        Mock()
        resource_manager = Mock(spec=ResourceManager)
        cost_validator = Mock(spec=CostValidator)

        # Mock successful spending plan execution
        spending_plan = SpendingPlan(
            player_id="player1",
            resource_spending=ResourceSpending(
                planets_to_exhaust={"planet1": 2},
                trade_goods_to_spend=0,
                total_resources=2,
            ),
            influence_spending=InfluenceSpending(
                planets_to_exhaust={}, trade_goods_to_spend=0, total_influence=0
            ),
            total_resource_cost=2,
            total_influence_cost=0,
            is_valid=True,
        )

        spending_result = SpendingResult(
            success=True, planets_exhausted=["planet1"], trade_goods_spent=0
        )

        resource_manager.execute_spending_plan.return_value = spending_result

        production_manager = ProductionManager(resource_manager, cost_validator)

        # Mock placement location
        placement_location = Mock()
        placement_location.can_place_unit.return_value = True
        placement_location.place_unit.return_value = True

        # Test execution
        result = production_manager.execute_production(
            player_id="player1",
            unit_type=UnitType.CRUISER,
            quantity=1,
            spending_plan=spending_plan,
            placement_location=placement_location,
        )

        assert result.success is True
        assert result.units_placed == 1
        assert result.spending_result == spending_result

    def test_execute_production_with_failed_cost_payment(self) -> None:
        """Test production execution when cost payment fails."""
        # Setup
        Mock()
        resource_manager = Mock(spec=ResourceManager)
        cost_validator = Mock(spec=CostValidator)

        # Mock failed spending plan execution
        spending_plan = SpendingPlan(
            player_id="player1",
            resource_spending=ResourceSpending(
                planets_to_exhaust={"planet1": 2},
                trade_goods_to_spend=0,
                total_resources=2,
            ),
            influence_spending=InfluenceSpending(
                planets_to_exhaust={}, trade_goods_to_spend=0, total_influence=0
            ),
            total_resource_cost=2,
            total_influence_cost=0,
            is_valid=True,
        )

        spending_result = SpendingResult(
            success=False,
            planets_exhausted=[],
            trade_goods_spent=0,
            error_message="Planet planet1 is already exhausted",
        )

        resource_manager.execute_spending_plan.return_value = spending_result

        production_manager = ProductionManager(resource_manager, cost_validator)

        # Mock placement location
        placement_location = Mock()

        # Test execution
        result = production_manager.execute_production(
            player_id="player1",
            unit_type=UnitType.CRUISER,
            quantity=1,
            spending_plan=spending_plan,
            placement_location=placement_location,
        )

        assert result.success is False
        assert result.error_message == "Planet planet1 is already exhausted"
        assert result.units_placed == 0

    def test_execute_production_with_failed_unit_placement(self) -> None:
        """Test production execution when unit placement fails."""
        # Setup
        Mock()
        resource_manager = Mock(spec=ResourceManager)
        cost_validator = Mock(spec=CostValidator)

        # Mock successful spending plan execution
        spending_plan = SpendingPlan(
            player_id="player1",
            resource_spending=ResourceSpending(
                planets_to_exhaust={"planet1": 2},
                trade_goods_to_spend=0,
                total_resources=2,
            ),
            influence_spending=InfluenceSpending(
                planets_to_exhaust={}, trade_goods_to_spend=0, total_influence=0
            ),
            total_resource_cost=2,
            total_influence_cost=0,
            is_valid=True,
        )

        spending_result = SpendingResult(
            success=True, planets_exhausted=["planet1"], trade_goods_spent=0
        )

        resource_manager.execute_spending_plan.return_value = spending_result

        # Mock rollback capability (optional method)
        resource_manager.rollback_spending = Mock()

        production_manager = ProductionManager(resource_manager, cost_validator)

        # Mock placement location that fails
        placement_location = Mock()
        placement_location.can_place_unit.return_value = False
        placement_location.get_placement_error.return_value = "No space for unit"

        # Test execution
        result = production_manager.execute_production(
            player_id="player1",
            unit_type=UnitType.CRUISER,
            quantity=1,
            spending_plan=spending_plan,
            placement_location=placement_location,
        )

        assert result.success is False
        assert result.error_message == "No space for unit"
        assert result.units_placed == 0
        # Rollback is handled by ResourceManager's atomic operations
        # The ProductionManager doesn't directly call rollback methods


class TestBackwardCompatibility:
    """Test that enhanced ProductionManager maintains backward compatibility."""

    def test_existing_methods_still_work(self) -> None:
        """Test that existing ProductionManager methods continue to work."""
        production_manager = ProductionManager()

        # Test existing methods
        assert production_manager.can_afford_unit(UnitType.FIGHTER, 2) is True
        assert production_manager.get_units_produced_for_cost(UnitType.FIGHTER) == 2

        # Mock system for ship production test
        system = Mock()
        system.space_units = []
        assert production_manager.can_produce_ships_in_system(system, "player1") is True

    def test_enhanced_methods_require_dependencies(self) -> None:
        """Test that enhanced methods require dependencies to be provided."""
        production_manager = ProductionManager()

        # Enhanced methods should raise appropriate errors when dependencies not provided
        with pytest.raises(
            ValueError, match="ResourceManager and CostValidator required"
        ):
            production_manager.validate_production(
                player_id="player1",
                unit_type=UnitType.FIGHTER,
                quantity=1,
                available_reinforcements=5,
            )

        with pytest.raises(
            ValueError, match="ResourceManager and CostValidator required"
        ):
            production_manager.execute_production(
                player_id="player1",
                unit_type=UnitType.FIGHTER,
                quantity=1,
                spending_plan=Mock(),
                placement_location=Mock(),
            )
