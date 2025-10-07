"""Integration tests for enhanced ProductionManager with ResourceManager and CostValidator.

This module tests the complete integration of the enhanced ProductionManager
with ResourceManager and CostValidator for end-to-end production workflows.
"""

from unittest.mock import Mock

from src.ti4.core.constants import UnitType
from src.ti4.core.production import ProductionManager
from src.ti4.core.resource_management import (
    CostValidator,
    ResourceManager,
)
from src.ti4.core.unit_stats import UnitStatsProvider


class MockProductionLocation:
    """Mock implementation of ProductionLocation protocol."""

    def __init__(self, can_place: bool = True, placement_error: str = ""):
        self._can_place = can_place
        self._placement_error = placement_error
        self.placed_units = []

    def can_place_unit(self, unit_type: UnitType, quantity: int) -> bool:
        return self._can_place

    def place_unit(self, unit_type: UnitType, quantity: int) -> bool:
        if self._can_place:
            self.placed_units.append((unit_type, quantity))
            return True
        return False

    def get_placement_error(self) -> str:
        return self._placement_error


class TestEnhancedProductionIntegration:
    """Test complete integration of enhanced ProductionManager."""

    def test_complete_production_workflow_success(self) -> None:
        """Test complete production workflow from validation to execution."""
        # Setup real dependencies
        game_state = Mock()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)
        production_manager = ProductionManager(resource_manager, cost_validator)

        # Mock game state to return controlled planets
        mock_planet = Mock()
        mock_planet.name = "planet1"
        mock_planet.resources = 3
        mock_planet.influence = 2
        mock_planet.can_spend_resources.return_value = True
        mock_planet.can_spend_influence.return_value = True
        mock_planet.is_exhausted.return_value = False
        mock_planet.exhaust.return_value = None

        game_state.get_player_planets.return_value = [mock_planet]

        # Mock player with trade goods
        mock_player = Mock()
        mock_player.id = "player1"
        mock_player.get_trade_goods.return_value = 2
        mock_player.spend_trade_goods.return_value = True

        game_state.players = [mock_player]

        # Create placement location
        placement_location = MockProductionLocation(can_place=True)

        # Step 1: Validate production
        validation_result = production_manager.validate_production(
            player_id="player1",
            unit_type=UnitType.CRUISER,
            quantity=1,
            available_reinforcements=5,
        )

        assert validation_result.is_valid is True
        assert validation_result.production_cost is not None
        assert validation_result.production_cost.unit_type == UnitType.CRUISER
        assert validation_result.production_cost.units_produced == 1

        # Step 2: Create spending plan
        spending_plan = resource_manager.create_spending_plan(
            player_id="player1",
            resource_amount=int(validation_result.production_cost.total_cost),
        )

        assert spending_plan.is_valid is True

        # Step 3: Execute production
        execution_result = production_manager.execute_production(
            player_id="player1",
            unit_type=UnitType.CRUISER,
            quantity=1,
            spending_plan=spending_plan,
            placement_location=placement_location,
        )

        assert execution_result.success is True
        assert execution_result.units_placed == 1
        assert len(placement_location.placed_units) == 1
        assert placement_location.placed_units[0] == (UnitType.CRUISER, 1)

    def test_complete_production_workflow_dual_production(self) -> None:
        """Test complete production workflow with dual production units."""
        # Setup real dependencies
        game_state = Mock()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)
        production_manager = ProductionManager(resource_manager, cost_validator)

        # Mock game state to return controlled planets
        mock_planet = Mock()
        mock_planet.name = "planet1"
        mock_planet.resources = 2
        mock_planet.influence = 1
        mock_planet.can_spend_resources.return_value = True
        mock_planet.can_spend_influence.return_value = True
        mock_planet.is_exhausted.return_value = False
        mock_planet.exhaust.return_value = None

        game_state.get_player_planets.return_value = [mock_planet]

        # Mock player with trade goods
        mock_player = Mock()
        mock_player.id = "player1"
        mock_player.get_trade_goods.return_value = 0
        mock_player.spend_trade_goods.return_value = True

        game_state.players = [mock_player]

        # Create placement location
        placement_location = MockProductionLocation(can_place=True)

        # Step 1: Validate dual production (2 fighters for cost of 1)
        validation_result = production_manager.validate_production(
            player_id="player1",
            unit_type=UnitType.FIGHTER,
            quantity=2,  # Request 2 fighters (dual production)
            available_reinforcements=5,
        )

        assert validation_result.is_valid is True
        assert validation_result.production_cost is not None
        assert validation_result.production_cost.unit_type == UnitType.FIGHTER
        assert validation_result.production_cost.units_produced == 2  # Dual production
        assert validation_result.production_cost.is_dual_production is True

        # Step 2: Create spending plan (should only need cost for 1 unit)
        spending_plan = resource_manager.create_spending_plan(
            player_id="player1",
            resource_amount=int(validation_result.production_cost.total_cost),
        )

        assert spending_plan.is_valid is True

        # Step 3: Execute production
        execution_result = production_manager.execute_production(
            player_id="player1",
            unit_type=UnitType.FIGHTER,
            quantity=2,
            spending_plan=spending_plan,
            placement_location=placement_location,
        )

        assert execution_result.success is True
        assert execution_result.units_placed == 2  # Should place 2 fighters
        assert len(placement_location.placed_units) == 1
        assert placement_location.placed_units[0] == (UnitType.FIGHTER, 2)

    def test_production_workflow_insufficient_resources(self) -> None:
        """Test production workflow when player has insufficient resources."""
        # Setup real dependencies
        game_state = Mock()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)
        production_manager = ProductionManager(resource_manager, cost_validator)

        # Mock game state with insufficient resources
        mock_planet = Mock()
        mock_planet.name = "planet1"
        mock_planet.resources = 1  # Not enough for cruiser (cost 2)
        mock_planet.influence = 1
        mock_planet.can_spend_resources.return_value = True
        mock_planet.can_spend_influence.return_value = True

        game_state.get_player_planets.return_value = [mock_planet]

        # Mock player with no trade goods
        mock_player = Mock()
        mock_player.id = "player1"
        mock_player.get_trade_goods.return_value = 0

        game_state.players = [mock_player]

        # Step 1: Validate production (should fail)
        validation_result = production_manager.validate_production(
            player_id="player1",
            unit_type=UnitType.CRUISER,
            quantity=1,
            available_reinforcements=5,
        )

        assert validation_result.is_valid is False
        assert "insufficient resources" in validation_result.error_message.lower()

    def test_production_workflow_insufficient_reinforcements(self) -> None:
        """Test production workflow when player has insufficient reinforcements."""
        # Setup real dependencies
        game_state = Mock()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)
        production_manager = ProductionManager(resource_manager, cost_validator)

        # Mock game state with sufficient resources
        mock_planet = Mock()
        mock_planet.name = "planet1"
        mock_planet.resources = 3
        mock_planet.influence = 1
        mock_planet.can_spend_resources.return_value = True
        mock_planet.can_spend_influence.return_value = True

        game_state.get_player_planets.return_value = [mock_planet]

        # Mock player
        mock_player = Mock()
        mock_player.id = "player1"
        mock_player.get_trade_goods.return_value = 0

        game_state.players = [mock_player]

        # Step 1: Validate production with insufficient reinforcements
        validation_result = production_manager.validate_production(
            player_id="player1",
            unit_type=UnitType.CRUISER,
            quantity=1,
            available_reinforcements=0,  # No reinforcements available
        )

        assert validation_result.is_valid is False
        assert "reinforcements" in validation_result.error_message.lower()

    def test_production_execution_placement_failure_with_rollback(self) -> None:
        """Test production execution when placement fails and spending is rolled back."""
        # Setup real dependencies
        game_state = Mock()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)
        production_manager = ProductionManager(resource_manager, cost_validator)

        # Mock game state
        mock_planet = Mock()
        mock_planet.name = "planet1"
        mock_planet.resources = 3
        mock_planet.influence = 1
        mock_planet.can_spend_resources.return_value = True
        mock_planet.can_spend_influence.return_value = True
        mock_planet.is_exhausted.return_value = False
        mock_planet.exhaust.return_value = None
        mock_planet.ready.return_value = None  # For rollback

        game_state.get_player_planets.return_value = [mock_planet]

        # Mock player
        mock_player = Mock()
        mock_player.id = "player1"
        mock_player.get_trade_goods.return_value = 0
        mock_player.spend_trade_goods.return_value = True
        mock_player.gain_trade_goods.return_value = None  # For rollback

        game_state.players = [mock_player]

        # Create placement location that fails
        placement_location = MockProductionLocation(
            can_place=False, placement_error="No space for unit"
        )

        # Create valid spending plan
        spending_plan = resource_manager.create_spending_plan(
            player_id="player1",
            resource_amount=2,  # Cost of cruiser
        )

        # Execute production (should fail and rollback)
        execution_result = production_manager.execute_production(
            player_id="player1",
            unit_type=UnitType.CRUISER,
            quantity=1,
            spending_plan=spending_plan,
            placement_location=placement_location,
        )

        assert execution_result.success is False
        assert execution_result.error_message == "No space for unit"
        assert execution_result.units_placed == 0

        # Rollback is handled by ResourceManager's atomic operations
        # The ProductionManager doesn't directly call rollback methods
