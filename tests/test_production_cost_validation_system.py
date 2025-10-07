"""Tests for comprehensive production cost validation system.

Tests the integrated production cost validation system that combines ResourceManager
and CostValidator for Rule 26: COST validation with detailed error messages and
suggested spending plans.
"""

from src.ti4.core.constants import Faction, Technology, UnitType
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.resource_management import (
    CostValidator,
    ResourceManager,
    SpendingPlan,
)
from src.ti4.core.unit_stats import UnitStatsProvider


class TestProductionCostValidationSystem:
    """Test comprehensive production cost validation system."""

    def test_validate_production_cost_with_detailed_error_messages(self) -> None:
        """Test that validation provides detailed error messages for insufficient resources."""
        # RED: Write failing test for detailed error messages
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        game_state = game_state.add_player(player)

        # Player has no resources
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Try to produce expensive unit (dreadnought costs 4)
        production_cost = cost_validator.get_production_cost(UnitType.DREADNOUGHT, 1)
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        # Should have detailed error message
        assert validation_result.is_valid is False
        assert validation_result.error_message is not None
        assert "need 4" in validation_result.error_message
        assert "have 0" in validation_result.error_message
        assert "shortfall: 4" in validation_result.error_message

    def test_validate_production_cost_suggests_spending_plan_when_valid(self) -> None:
        """Test that validation suggests spending plan when resources are sufficient."""
        # RED: Write failing test for suggested spending plan
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Give player sufficient resources
        jord = Planet("Jord", resources=4, influence=2)
        jord.set_control(player.id)
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)
        player.gain_trade_goods(2)

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Validate cruiser production (cost 2)
        production_cost = cost_validator.get_production_cost(UnitType.CRUISER, 1)
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        # Should be valid with suggested spending plan
        assert validation_result.is_valid is True
        assert validation_result.suggested_spending_plan is not None
        assert isinstance(validation_result.suggested_spending_plan, SpendingPlan)
        assert validation_result.suggested_spending_plan.is_valid is True
        assert validation_result.suggested_spending_plan.total_resource_cost == 2

    def test_validate_production_cost_no_spending_plan_when_invalid(self) -> None:
        """Test that validation doesn't suggest spending plan when resources are insufficient."""
        # RED: Write failing test for no spending plan when invalid
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        game_state = game_state.add_player(player)

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Try to produce expensive unit with no resources
        production_cost = cost_validator.get_production_cost(UnitType.DREADNOUGHT, 1)
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        # Should be invalid with no spending plan
        assert validation_result.is_valid is False
        assert validation_result.suggested_spending_plan is None

    def test_validate_production_cost_with_mixed_resource_sources(self) -> None:
        """Test validation with mixed planet and trade goods resources."""
        # RED: Write failing test for mixed resource validation
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Give player partial resources from planet and trade goods
        planet = Planet("TestPlanet", resources=2, influence=1)
        planet.set_control(player.id)
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet)
        player.gain_trade_goods(2)  # Total: 4 resources

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Validate dreadnought production (cost 4)
        production_cost = cost_validator.get_production_cost(UnitType.DREADNOUGHT, 1)
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        # Should be valid with spending plan using both sources
        assert validation_result.is_valid is True
        assert validation_result.required_resources == 4
        assert validation_result.available_resources == 4
        assert validation_result.shortfall == 0

        spending_plan = validation_result.suggested_spending_plan
        assert spending_plan is not None
        assert spending_plan.total_resource_cost == 4
        assert len(spending_plan.resource_spending.planets_to_exhaust) == 1
        assert spending_plan.resource_spending.trade_goods_to_spend == 2

    def test_validate_production_cost_with_exhausted_planets(self) -> None:
        """Test validation when some planets are already exhausted."""
        # RED: Write failing test for exhausted planet handling
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planets, one exhausted
        planet1 = Planet("Planet1", resources=3, influence=1)
        planet2 = Planet("Planet2", resources=2, influence=1)
        planet1.set_control(player.id)
        planet2.set_control(player.id)
        planet1.exhaust()  # This planet is exhausted

        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet1)
        game_state = game_state.add_player_planet(player.id, planet2)

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Validate cruiser production (cost 2)
        production_cost = cost_validator.get_production_cost(UnitType.CRUISER, 1)
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        # Should be valid using only ready planet
        assert validation_result.is_valid is True
        assert validation_result.available_resources == 2  # Only planet2

        spending_plan = validation_result.suggested_spending_plan
        assert spending_plan is not None
        assert "Planet2" in spending_plan.resource_spending.planets_to_exhaust
        assert "Planet1" not in spending_plan.resource_spending.planets_to_exhaust

    def test_validate_production_cost_with_fractional_costs(self) -> None:
        """Test validation with fractional unit costs (fighters, infantry)."""
        # RED: Write failing test for fractional cost handling
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Give player minimal resources
        player.gain_trade_goods(1)
        game_state = game_state.add_player(player)

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Validate fighter production (cost 0.5)
        production_cost = cost_validator.get_production_cost(UnitType.FIGHTER, 1)
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        # Should be valid (1 trade good >= 0.5 cost, rounded up to 1 required resource)
        assert validation_result.is_valid is True
        assert validation_result.required_resources == 1  # math.ceil(0.5) = 1
        assert validation_result.available_resources == 1

    def test_validate_production_cost_dual_production_scenarios(self) -> None:
        """Test validation for dual production scenarios."""
        # RED: Write failing test for dual production validation
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Give player minimal resources for dual production
        player.gain_trade_goods(1)
        game_state = game_state.add_player(player)

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Validate dual fighter production (2 fighters for cost of 0.5)
        production_cost = cost_validator.get_production_cost(UnitType.FIGHTER, 2)
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        # Should be valid
        assert validation_result.is_valid is True
        assert production_cost.is_dual_production is True
        assert production_cost.total_cost == 0.5
        assert production_cost.units_produced == 2

    def test_validate_production_cost_with_technology_modifiers(self) -> None:
        """Test validation with technology cost modifiers."""
        # RED: Write failing test for technology modifier validation
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Give player resources
        planet = Planet("TestPlanet", resources=3, influence=1)
        planet.set_control(player.id)
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet)

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Validate upgraded unit production with technology
        technologies = {Technology.CRUISER_II}
        production_cost = cost_validator.get_production_cost(
            UnitType.CRUISER_II, 1, technologies=technologies
        )
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        # Should be valid (assuming cruiser II still costs 2)
        assert validation_result.is_valid is True
        assert production_cost.modified_cost == 2.0  # Should be same as base cruiser

    def test_validate_production_cost_comprehensive_error_scenarios(self) -> None:
        """Test comprehensive error scenarios with detailed messages."""
        # RED: Write failing test for comprehensive error handling
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Give player insufficient resources
        planet = Planet("TestPlanet", resources=1, influence=1)
        planet.set_control(player.id)
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet)

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Try to produce multiple expensive units
        production_cost = cost_validator.get_production_cost(UnitType.CRUISER, 3)
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        # Should have detailed error
        assert validation_result.is_valid is False
        assert validation_result.required_resources == 6  # 3 cruisers * 2 cost
        assert validation_result.available_resources == 1
        assert validation_result.shortfall == 5
        assert "need 6" in validation_result.error_message
        assert "have 1" in validation_result.error_message
        assert "shortfall: 5" in validation_result.error_message


class TestProductionCostValidationWithReinforcements:
    """Test production cost validation with reinforcement checks."""

    def test_validate_production_cost_with_reinforcements_sufficient(self) -> None:
        """Test validation with sufficient reinforcements."""
        # RED: Write failing test for reinforcement validation
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Give player sufficient resources
        planet = Planet("TestPlanet", resources=4, influence=1)
        planet.set_control(player.id)
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet)

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Validate dual fighter production with sufficient reinforcements
        production_cost = cost_validator.get_production_cost(UnitType.FIGHTER, 2)
        validation_result = cost_validator.validate_production_cost_with_reinforcements(
            player.id, production_cost, available_reinforcements=5
        )

        # Should be valid
        assert validation_result.is_valid is True
        assert validation_result.reinforcement_shortfall == 0
        assert validation_result.error_message is None

    def test_validate_production_cost_with_reinforcements_insufficient(self) -> None:
        """Test validation with insufficient reinforcements."""
        # RED: Write failing test for insufficient reinforcements
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Give player sufficient resources but insufficient reinforcements
        planet = Planet("TestPlanet", resources=4, influence=1)
        planet.set_control(player.id)
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet)

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Validate dual fighter production with insufficient reinforcements
        production_cost = cost_validator.get_production_cost(UnitType.FIGHTER, 2)
        validation_result = cost_validator.validate_production_cost_with_reinforcements(
            player.id, production_cost, available_reinforcements=1
        )

        # Should be invalid due to reinforcements
        assert validation_result.is_valid is False
        assert validation_result.reinforcement_shortfall == 1
        assert "reinforcement" in validation_result.error_message.lower()
        assert "need 2" in validation_result.error_message
        assert "have 1" in validation_result.error_message

    def test_validate_production_cost_with_both_resource_and_reinforcement_issues(
        self,
    ) -> None:
        """Test validation with both resource and reinforcement shortfalls."""
        # RED: Write failing test for combined validation issues
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        game_state = game_state.add_player(player)  # No resources

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Try to produce units with no resources and no reinforcements
        production_cost = cost_validator.get_production_cost(UnitType.CRUISER, 2)
        validation_result = cost_validator.validate_production_cost_with_reinforcements(
            player.id, production_cost, available_reinforcements=1
        )

        # Should be invalid for both reasons
        assert validation_result.is_valid is False
        assert validation_result.shortfall > 0  # Resource shortfall
        assert validation_result.reinforcement_shortfall == 1  # Reinforcement shortfall
        assert "insufficient resources" in validation_result.error_message.lower()
        assert "insufficient reinforcements" in validation_result.error_message.lower()


class TestProductionCostValidationIntegration:
    """Test integration scenarios for production cost validation."""

    def test_validate_production_cost_integration_with_spending_plan_execution(
        self,
    ) -> None:
        """Test that validation integrates properly with spending plan execution."""
        # RED: Write failing test for integration with spending plan execution
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Give player exact resources needed
        planet = Planet("TestPlanet", resources=2, influence=1)
        planet.set_control(player.id)
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet)

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Validate and get spending plan
        production_cost = cost_validator.get_production_cost(UnitType.CRUISER, 1)
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        # Should be valid with executable spending plan
        assert validation_result.is_valid is True
        spending_plan = validation_result.suggested_spending_plan
        assert spending_plan is not None
        assert spending_plan.is_valid is True

        # Execute the spending plan
        execution_result = resource_manager.execute_spending_plan(spending_plan)
        assert execution_result.success is True
        assert "TestPlanet" in execution_result.planets_exhausted

    def test_validate_production_cost_with_multiple_production_requests(self) -> None:
        """Test validation for multiple production requests in sequence."""
        # RED: Write failing test for multiple production validation
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Give player resources for multiple productions
        planet1 = Planet("Planet1", resources=3, influence=1)
        planet2 = Planet("Planet2", resources=3, influence=1)
        planet1.set_control(player.id)
        planet2.set_control(player.id)
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet1)
        game_state = game_state.add_player_planet(player.id, planet2)

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # First production should be valid
        production_cost1 = cost_validator.get_production_cost(UnitType.CRUISER, 1)
        validation_result1 = cost_validator.validate_production_cost(
            player.id, production_cost1
        )
        assert validation_result1.is_valid is True

        # Execute first production
        spending_plan1 = validation_result1.suggested_spending_plan
        execution_result1 = resource_manager.execute_spending_plan(spending_plan1)
        assert execution_result1.success is True

        # Second production should still be valid with remaining resources
        production_cost2 = cost_validator.get_production_cost(UnitType.CRUISER, 1)
        validation_result2 = cost_validator.validate_production_cost(
            player.id, production_cost2
        )
        assert validation_result2.is_valid is True

        # Third production should be invalid (insufficient resources)
        production_cost3 = cost_validator.get_production_cost(UnitType.CRUISER, 2)
        validation_result3 = cost_validator.validate_production_cost(
            player.id, production_cost3
        )
        assert validation_result3.is_valid is False


class TestProductionCostValidationEdgeCases:
    """Test edge cases for production cost validation."""

    def test_validate_production_cost_zero_cost_units(self) -> None:
        """Test validation for zero-cost units (structures)."""
        # RED: Write failing test for zero-cost unit validation
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        game_state = game_state.add_player(player)  # No resources

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Validate space dock production (cost 0)
        production_cost = cost_validator.get_production_cost(UnitType.SPACE_DOCK, 1)
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        # Should be invalid - zero-cost units cannot be produced normally (Rule 26.3)
        assert validation_result.is_valid is False
        assert validation_result.required_resources == 0
        assert (
            validation_result.error_message
            == "Units without cost cannot be produced normally (Rule 26.3)"
        )

    def test_validate_production_cost_with_player_not_found(self) -> None:
        """Test validation when player doesn't exist."""
        # RED: Write failing test for missing player
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Try to validate for non-existent player
        production_cost = cost_validator.get_production_cost(UnitType.CRUISER, 1)

        # Should raise ResourceOperationError for non-existent player
        from src.ti4.core.resource_management import ResourceOperationError

        try:
            cost_validator.validate_production_cost(
                "nonexistent_player", production_cost
            )
            assert False, "Expected ResourceOperationError"
        except ResourceOperationError as e:
            assert "Player not found" in str(e)

    def test_validate_production_cost_boundary_conditions(self) -> None:
        """Test validation at boundary conditions."""
        # RED: Write failing test for boundary conditions
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Give player exactly the resources needed
        planet = Planet("TestPlanet", resources=2, influence=1)
        planet.set_control(player.id)
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet)

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test exact match
        production_cost = cost_validator.get_production_cost(UnitType.CRUISER, 1)
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )
        assert validation_result.is_valid is True
        assert validation_result.shortfall == 0

        # Test one over the limit
        production_cost = cost_validator.get_production_cost(UnitType.DREADNOUGHT, 1)
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )
        assert validation_result.is_valid is False
        assert validation_result.shortfall == 2  # Need 4, have 2
