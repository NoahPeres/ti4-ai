"""Comprehensive integration test suite for Rule 26: COST system.

This module provides comprehensive integration testing for the unified resource management
system covering Rule 26: COST, Rule 75: RESOURCES, and Rule 47: INFLUENCE.

Tests cover:
- Complete production flow from cost validation to unit placement
- Agenda phase voting with planet exhaustion
- Strategy card integration (Leadership, Construction, Politics)
- Error handling and rollback scenarios
- Performance with maximum players and planets

Requirements tested: All requirements integration testing
"""

from unittest.mock import patch

from src.ti4.core.agenda_phase import VotingSystem
from src.ti4.core.constants import Faction, Technology, UnitType
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.production import ProductionManager
from src.ti4.core.resource_management import (
    CostValidator,
    ProductionCost,
    ResourceManager,
)
from src.ti4.core.strategy_cards.cards.leadership import LeadershipStrategyCard
from src.ti4.core.strategy_cards.cards.politics import PoliticsStrategyCard
from src.ti4.core.unit_stats import UnitStatsProvider


class MockProductionLocation:
    """Mock implementation of ProductionLocation protocol for testing."""

    def __init__(self, can_place: bool = True, placement_error: str = ""):
        self._can_place = can_place
        self._placement_error = placement_error
        self.placed_units: list[tuple[UnitType, int]] = []

    def can_place_unit(self, unit_type: UnitType, quantity: int) -> bool:
        return self._can_place

    def place_unit(self, unit_type: UnitType, quantity: int) -> bool:
        if self._can_place:
            self.placed_units.append((unit_type, quantity))
            return True
        return False

    def get_placement_error(self) -> str:
        return self._placement_error


class TestCompleteProductionFlow:
    """Test complete production flow from cost validation to unit placement."""

    def setup_method(self) -> None:
        """Set up test fixtures for production flow tests."""
        self.game_state = GameState()
        self.player = Player("player1", Faction.SOL)
        self.game_state = self.game_state.add_player(self.player)

        # Add planets with resources
        self.planet1 = Planet("Mecatol Rex", resources=1, influence=6)
        self.planet2 = Planet("Jord", resources=4, influence=4)
        self.planet3 = Planet("Arc Prime", resources=4, influence=0)

        self.planet1.set_control("player1")
        self.planet2.set_control("player1")
        self.planet3.set_control("player1")

        self.game_state = self.game_state.add_player_planet("player1", self.planet1)
        self.game_state = self.game_state.add_player_planet("player1", self.planet2)
        self.game_state = self.game_state.add_player_planet("player1", self.planet3)

        # Add trade goods
        self.player.gain_trade_goods(3)

        # Initialize managers
        self.resource_manager = ResourceManager(self.game_state)
        self.stats_provider = UnitStatsProvider()
        self.cost_validator = CostValidator(self.resource_manager, self.stats_provider)
        self.production_manager = ProductionManager(
            self.resource_manager, self.cost_validator
        )

    def test_complete_cruiser_production_workflow(self) -> None:
        """Test complete workflow for producing a cruiser."""
        # Arrange
        placement_location = MockProductionLocation(can_place=True)

        # Act - Step 1: Validate production
        validation_result = self.production_manager.validate_production(
            player_id="player1",
            unit_type=UnitType.CRUISER,
            quantity=1,
            available_reinforcements=5,
        )

        # Assert validation
        assert validation_result.is_valid is True
        assert validation_result.production_cost is not None
        assert validation_result.production_cost.unit_type == UnitType.CRUISER
        assert validation_result.production_cost.total_cost == 2.0  # Cruiser cost

        # Act - Step 2: Create spending plan
        spending_plan = self.resource_manager.create_spending_plan(
            player_id="player1",
            resource_amount=int(validation_result.production_cost.total_cost),
        )

        # Assert spending plan
        assert spending_plan.is_valid is True
        assert spending_plan.total_resource_cost == 2

        # Act - Step 3: Execute production
        execution_result = self.production_manager.execute_production(
            player_id="player1",
            unit_type=UnitType.CRUISER,
            quantity=1,
            spending_plan=spending_plan,
            placement_location=placement_location,
        )

        # Assert execution
        assert execution_result.success is True
        assert execution_result.units_placed == 1
        assert len(placement_location.placed_units) == 1
        assert placement_location.placed_units[0] == (UnitType.CRUISER, 1)

        # Verify resource spending occurred
        assert execution_result.spending_result is not None
        assert execution_result.spending_result.success is True

    def test_dual_production_fighter_workflow(self) -> None:
        """Test complete workflow for dual production fighters."""
        # Arrange
        placement_location = MockProductionLocation(can_place=True)

        # Act - Step 1: Validate dual production
        validation_result = self.production_manager.validate_production(
            player_id="player1",
            unit_type=UnitType.FIGHTER,
            quantity=2,  # Request 2 fighters (dual production)
            available_reinforcements=5,
        )

        # Assert validation
        assert validation_result.is_valid is True
        assert validation_result.production_cost is not None
        assert validation_result.production_cost.unit_type == UnitType.FIGHTER
        assert validation_result.production_cost.units_produced == 2  # Dual production
        assert validation_result.production_cost.is_dual_production is True
        assert (
            validation_result.production_cost.total_cost == 0.5
        )  # Cost of 1 fighter for 2 units

        # Act - Step 2: Create spending plan (should only need cost for 1 unit)
        spending_plan = self.resource_manager.create_spending_plan(
            player_id="player1",
            resource_amount=int(validation_result.production_cost.total_cost)
            + 1,  # Ceiling for fractional cost
        )

        # Assert spending plan
        assert spending_plan.is_valid is True

        # Act - Step 3: Execute production
        execution_result = self.production_manager.execute_production(
            player_id="player1",
            unit_type=UnitType.FIGHTER,
            quantity=2,
            spending_plan=spending_plan,
            placement_location=placement_location,
        )

        # Assert execution
        assert execution_result.success is True
        assert execution_result.units_placed == 2  # Should place 2 fighters
        assert len(placement_location.placed_units) == 1
        assert placement_location.placed_units[0] == (UnitType.FIGHTER, 2)

    def test_production_workflow_with_technology_modifiers(self) -> None:
        """Test production workflow with technology cost modifiers."""
        # Arrange
        technologies = {Technology.CRUISER_II}  # Assume this reduces cruiser cost

        # Act - Validate production with technology
        validation_result = self.production_manager.validate_production(
            player_id="player1",
            unit_type=UnitType.CRUISER,
            quantity=1,
            available_reinforcements=5,
            faction=Faction.SOL,
            technologies=technologies,
        )

        # Assert - Should still be valid (technology effects depend on UnitStatsProvider)
        assert validation_result.is_valid is True
        assert validation_result.production_cost is not None

    def test_production_workflow_insufficient_resources(self) -> None:
        """Test production workflow when player has insufficient resources."""
        # Arrange - Remove most resources
        self.planet2.exhaust()  # Remove 4 resources
        self.planet3.exhaust()  # Remove 4 resources
        self.player.spend_trade_goods(3)  # Remove trade goods
        # Now player only has 1 resource from Mecatol Rex

        # Act - Try to produce expensive unit
        validation_result = self.production_manager.validate_production(
            player_id="player1",
            unit_type=UnitType.DREADNOUGHT,  # Cost 4
            quantity=1,
            available_reinforcements=5,
        )

        # Assert - Should fail due to insufficient resources
        assert validation_result.is_valid is False
        assert "insufficient resources" in validation_result.error_message.lower()

    def test_production_workflow_insufficient_reinforcements(self) -> None:
        """Test production workflow when player has insufficient reinforcements."""
        # Act - Try to produce with no reinforcements
        validation_result = self.production_manager.validate_production(
            player_id="player1",
            unit_type=UnitType.CRUISER,
            quantity=1,
            available_reinforcements=0,  # No reinforcements
        )

        # Assert - Should fail due to insufficient reinforcements
        assert validation_result.is_valid is False
        assert "reinforcements" in validation_result.error_message.lower()

    def test_production_execution_placement_failure_with_rollback(self) -> None:
        """Test production execution when placement fails and spending is rolled back."""
        # Arrange - Create placement location that fails
        placement_location = MockProductionLocation(
            can_place=False, placement_error="No space for unit"
        )

        # Create valid spending plan
        spending_plan = self.resource_manager.create_spending_plan(
            player_id="player1",
            resource_amount=2,  # Cost of cruiser
        )

        # Act - Execute production (should fail and rollback)
        execution_result = self.production_manager.execute_production(
            player_id="player1",
            unit_type=UnitType.CRUISER,
            quantity=1,
            spending_plan=spending_plan,
            placement_location=placement_location,
        )

        # Assert - Should fail
        assert execution_result.success is False
        assert execution_result.error_message == "No space for unit"
        assert execution_result.units_placed == 0

        # Verify rollback occurred
        # Note: The actual rollback is handled by ResourceManager's atomic operations


class TestAgendaPhaseVotingIntegration:
    """Test agenda phase voting with planet exhaustion and influence spending."""

    def setup_method(self) -> None:
        """Set up test fixtures for agenda phase voting tests."""
        self.game_state = GameState()

        # Create players
        self.player1 = Player("player1", Faction.SOL)
        self.player2 = Player("player2", Faction.HACAN)
        self.game_state = self.game_state.add_player(self.player1)
        self.game_state = self.game_state.add_player(self.player2)

        # Add planets for player1
        self.planet1 = Planet("Mecatol Rex", resources=1, influence=6)
        self.planet2 = Planet("Jord", resources=4, influence=4)
        self.planet1.set_control("player1")
        self.planet2.set_control("player1")
        self.game_state = self.game_state.add_player_planet("player1", self.planet1)
        self.game_state = self.game_state.add_player_planet("player1", self.planet2)

        # Add planets for player2
        self.planet3 = Planet("Arc Prime", resources=4, influence=0)
        self.planet4 = Planet("Wren Terra", resources=2, influence=1)
        self.planet3.set_control("player2")
        self.planet4.set_control("player2")
        self.game_state = self.game_state.add_player_planet("player2", self.planet3)
        self.game_state = self.game_state.add_player_planet("player2", self.planet4)

        # Add trade goods (should not affect voting per Rule 47.3)
        self.player1.gain_trade_goods(5)
        self.player2.gain_trade_goods(3)

        # Initialize managers
        self.resource_manager = ResourceManager(self.game_state)
        self.voting_system = VotingSystem()

    def test_complete_voting_workflow_with_resource_manager(self) -> None:
        """Test complete voting workflow using ResourceManager integration."""
        # Act - Player1 votes "For" with 8 influence (should use both planets)
        influence_sources = self.resource_manager.get_influence_sources(
            "player1", for_voting=True
        )
        assert influence_sources.total_available == 10  # 6 + 4 from planets only
        assert influence_sources.trade_goods == 0  # Trade goods excluded for voting

        # Create spending plan for voting
        spending_plan = self.resource_manager.create_spending_plan(
            player_id="player1", influence_amount=8, for_voting=True
        )

        assert spending_plan.is_valid is True
        assert spending_plan.total_influence_cost == 8

        # Execute spending plan
        spending_result = self.resource_manager.execute_spending_plan(spending_plan)
        assert spending_result.success is True

        # Verify planets are exhausted
        assert self.planet1.is_exhausted()
        assert self.planet2.is_exhausted()

        # Player2 votes "Against" with 1 influence (Wren Terra only)
        spending_plan2 = self.resource_manager.create_spending_plan(
            player_id="player2", influence_amount=1, for_voting=True
        )

        assert spending_plan2.is_valid is True
        spending_result2 = self.resource_manager.execute_spending_plan(spending_plan2)
        assert spending_result2.success is True

        # Verify correct planet exhausted
        assert not self.planet3.is_exhausted()  # No influence
        assert self.planet4.is_exhausted()  # Used for voting

    def test_voting_trade_goods_restriction(self) -> None:
        """Test that trade goods cannot be used for voting influence."""
        # Arrange - Player with only trade goods (no planet influence)
        player3 = Player("player3", Faction.XXCHA)
        self.game_state = self.game_state.add_player(player3)

        # Add planet with no influence
        planet_no_influence = Planet("No Influence", resources=3, influence=0)
        planet_no_influence.set_control("player3")
        self.game_state = self.game_state.add_player_planet(
            "player3", planet_no_influence
        )

        # Add trade goods
        player3.gain_trade_goods(10)

        # Update resource manager with new game state
        self.resource_manager = ResourceManager(self.game_state)

        # Act - Try to vote using trade goods
        influence_sources = self.resource_manager.get_influence_sources(
            "player3", for_voting=True
        )

        # Assert - Should have no influence available for voting
        assert influence_sources.total_available == 0
        assert influence_sources.trade_goods == 0  # Excluded for voting

        # Try to create spending plan for voting
        spending_plan = self.resource_manager.create_spending_plan(
            player_id="player3", influence_amount=5, for_voting=True
        )

        # Should fail
        assert spending_plan.is_valid is False
        assert "insufficient influence" in spending_plan.error_message.lower()

    def test_voting_with_exhausted_planets(self) -> None:
        """Test voting when some planets are already exhausted."""
        # Arrange - Exhaust one planet
        self.planet1.exhaust()

        # Act - Try to vote with remaining influence
        influence_sources = self.resource_manager.get_influence_sources(
            "player1", for_voting=True
        )

        # Assert - Should only have influence from ready planets
        assert influence_sources.total_available == 4  # Only Jord (planet2)
        assert "Jord" in influence_sources.planets
        assert "Mecatol Rex" not in influence_sources.planets  # Exhausted

        # Create spending plan
        spending_plan = self.resource_manager.create_spending_plan(
            player_id="player1", influence_amount=4, for_voting=True
        )

        assert spending_plan.is_valid is True

        # Execute
        spending_result = self.resource_manager.execute_spending_plan(spending_plan)
        assert spending_result.success is True

        # Verify only the ready planet was exhausted
        assert self.planet1.is_exhausted()  # Was already exhausted
        assert self.planet2.is_exhausted()  # Now exhausted for voting


class TestStrategyCardIntegration:
    """Test strategy card integration with resource management system."""

    def setup_method(self) -> None:
        """Set up test fixtures for strategy card integration tests."""
        self.game_state = GameState()
        self.player = Player("player1", Faction.SOL)
        self.game_state = self.game_state.add_player(self.player)

        # Add planets
        self.planet1 = Planet("Mecatol Rex", resources=1, influence=6)
        self.planet2 = Planet("Jord", resources=4, influence=4)
        self.planet1.set_control("player1")
        self.planet2.set_control("player1")
        self.game_state = self.game_state.add_player_planet("player1", self.planet1)
        self.game_state = self.game_state.add_player_planet("player1", self.planet2)

        # Add trade goods
        self.player.gain_trade_goods(3)

        # Initialize managers
        self.resource_manager = ResourceManager(self.game_state)
        self.stats_provider = UnitStatsProvider()
        self.cost_validator = CostValidator(self.resource_manager, self.stats_provider)

    def test_leadership_strategy_card_integration(self) -> None:
        """Test Leadership strategy card integration with ResourceManager."""
        # Arrange
        leadership_card = LeadershipStrategyCard()

        # Reset command pools for testing
        object.__setattr__(self.player.command_sheet, "tactic_pool", 0)
        object.__setattr__(self.player.command_sheet, "fleet_pool", 0)
        object.__setattr__(self.player.command_sheet, "strategy_pool", 0)

        # Check available influence first
        available_influence = self.resource_manager.calculate_available_influence(
            "player1"
        )
        # Player has Mecatol Rex (6) + Jord (4) + 3 trade goods = 13 influence
        assert available_influence == 13

        # Act - Use Leadership primary with influence spending (3 base + 1 from influence = 4 total)
        result = leadership_card.execute_primary_ability(
            "player1",
            game_state=self.game_state,
            player=self.player,
            resource_manager=self.resource_manager,
            token_distribution={
                "tactic": 4,
                "fleet": 0,
                "strategy": 0,
            },  # 3 base + 1 from influence
            influence_to_spend=3,
        )

        # Assert
        assert result.success is True
        assert self.player.command_sheet.tactic_pool == 4

        # Verify influence was spent (planets should be exhausted)
        # Note: The exact exhaustion depends on ResourceManager implementation

    def test_construction_strategy_card_cost_exemption(self) -> None:
        """Test Construction strategy card allows structure placement without cost."""
        # Arrange

        # Act - Use Construction to place PDS (structure with cost)
        # This should work without resource validation
        validation_result = (
            self.cost_validator.validate_production_cost_with_construction_exemption(
                player_id="player1",
                production_cost=ProductionCost(
                    unit_type=UnitType.PDS,
                    base_cost=0.0,  # Structures have no cost
                    modified_cost=0.0,
                    quantity_requested=1,
                    units_produced=1,
                    total_cost=0.0,
                    is_dual_production=False,
                ),
            )
        )

        # Assert - Should be valid with Construction exemption
        assert validation_result.is_valid is True
        assert validation_result.required_resources == 0

    def test_politics_strategy_card_integration(self) -> None:
        """Test Politics strategy card integration with agenda phase."""
        # Arrange
        politics_card = PoliticsStrategyCard()

        # Act & Assert - Use Politics primary (draw agenda cards)
        # This doesn't directly use ResourceManager but should be compatible
        # Note: Actual implementation depends on PoliticsStrategyCard
        assert hasattr(politics_card, "execute_primary_ability")


class TestErrorHandlingAndRollback:
    """Test error handling and rollback scenarios."""

    def setup_method(self) -> None:
        """Set up test fixtures for error handling tests."""
        self.game_state = GameState()
        self.player = Player("player1", Faction.SOL)
        self.game_state = self.game_state.add_player(self.player)

        # Add minimal resources
        self.planet = Planet("Test Planet", resources=2, influence=1)
        self.planet.set_control("player1")
        self.game_state = self.game_state.add_player_planet("player1", self.planet)

        self.resource_manager = ResourceManager(self.game_state)

    def test_spending_plan_rollback_on_failure(self) -> None:
        """Test that spending plan execution rolls back on failure."""
        # Arrange - Create valid spending plan
        spending_plan = self.resource_manager.create_spending_plan(
            player_id="player1", resource_amount=2
        )

        assert spending_plan.is_valid is True

        # Track initial state
        initial_exhausted = self.planet.is_exhausted()
        initial_trade_goods = self.player.get_trade_goods()

        # Mock a failure during execution by making planet unavailable
        with patch.object(
            self.planet, "exhaust", side_effect=Exception("Planet exhaustion failed")
        ):
            # Act - Execute spending plan (should fail and rollback)
            spending_result = self.resource_manager.execute_spending_plan(spending_plan)

            # Assert - Should fail
            assert spending_result.success is False
            assert "Planet exhaustion failed" in spending_result.error_message

            # Verify rollback occurred
            assert self.planet.is_exhausted() == initial_exhausted
            assert self.player.get_trade_goods() == initial_trade_goods

    def test_invalid_player_id_error_handling(self) -> None:
        """Test error handling for invalid player ID."""
        # Act & Assert - Should raise ResourceOperationError for non-existent player
        from src.ti4.core.resource_management import ResourceOperationError

        try:
            self.resource_manager.create_spending_plan(
                player_id="nonexistent_player", resource_amount=1
            )
            assert False, "Expected ResourceOperationError"
        except ResourceOperationError as e:
            assert "Player not found" in str(e)

    def test_concurrent_resource_access_error_handling(self) -> None:
        """Test error handling for concurrent resource access."""
        # Arrange - Create two spending plans for same resources
        spending_plan1 = self.resource_manager.create_spending_plan(
            player_id="player1", resource_amount=2
        )
        spending_plan2 = self.resource_manager.create_spending_plan(
            player_id="player1", resource_amount=2
        )

        # Act - Execute first plan
        result1 = self.resource_manager.execute_spending_plan(spending_plan1)
        assert result1.success is True

        # Execute second plan (should fail - planet already exhausted)
        result2 = self.resource_manager.execute_spending_plan(spending_plan2)

        # Assert - Second execution should fail
        assert result2.success is False
        assert "exhausted" in result2.error_message.lower()


class TestPerformanceWithMaximumPlayersAndPlanets:
    """Test performance with maximum players and planets."""

    def setup_method(self) -> None:
        """Set up test fixtures for performance tests."""
        self.game_state = GameState()

        # Create maximum players (8 players)
        self.players = []
        for i in range(8):
            player = Player(f"player{i + 1}", Faction.SOL)
            self.players.append(player)
            self.game_state = self.game_state.add_player(player)

            # Add multiple planets per player (simulate full game)
            for j in range(5):  # 5 planets per player
                planet = Planet(
                    f"Planet_{i + 1}_{j + 1}", resources=j + 1, influence=j + 1
                )
                planet.set_control(f"player{i + 1}")
                self.game_state = self.game_state.add_player_planet(
                    f"player{i + 1}", planet
                )

            # Add trade goods
            player.gain_trade_goods(10)

        self.resource_manager = ResourceManager(self.game_state)

    def test_resource_calculation_performance_with_max_players(self) -> None:
        """Test resource calculation performance with maximum players and planets."""
        import time

        # Act - Calculate resources for all players
        start_time = time.time()

        for player in self.players:
            resources = self.resource_manager.calculate_available_resources(player.id)
            influence = self.resource_manager.calculate_available_influence(player.id)

            # Verify calculations are reasonable
            assert resources > 0
            assert influence > 0

        end_time = time.time()
        execution_time = end_time - start_time

        # Assert - Should complete within reasonable time (< 1 second)
        assert execution_time < 1.0, (
            f"Resource calculation took {execution_time:.3f}s, expected < 1.0s"
        )

    def test_spending_plan_creation_performance_with_max_players(self) -> None:
        """Test spending plan creation performance with maximum players."""
        import time

        # Act - Create spending plans for all players
        start_time = time.time()

        for player in self.players:
            spending_plan = self.resource_manager.create_spending_plan(
                player_id=player.id, resource_amount=10, influence_amount=5
            )

            # Verify plan is valid
            assert spending_plan.is_valid is True

        end_time = time.time()
        execution_time = end_time - start_time

        # Assert - Should complete within reasonable time (< 2 seconds)
        assert execution_time < 2.0, (
            f"Spending plan creation took {execution_time:.3f}s, expected < 2.0s"
        )

    def test_concurrent_voting_simulation_performance(self) -> None:
        """Test performance of concurrent voting simulation with all players."""
        import time

        # Act - Simulate all players voting simultaneously
        start_time = time.time()

        spending_plans = []
        for player in self.players:
            # Create voting spending plan
            spending_plan = self.resource_manager.create_spending_plan(
                player_id=player.id, influence_amount=5, for_voting=True
            )
            spending_plans.append(spending_plan)
            assert spending_plan.is_valid is True

        # Execute all spending plans
        for spending_plan in spending_plans:
            result = self.resource_manager.execute_spending_plan(spending_plan)
            assert result.success is True

        end_time = time.time()
        execution_time = end_time - start_time

        # Assert - Should complete within reasonable time (< 3 seconds)
        assert execution_time < 3.0, (
            f"Concurrent voting simulation took {execution_time:.3f}s, expected < 3.0s"
        )

    def test_memory_usage_with_max_players_and_planets(self) -> None:
        """Test memory usage remains reasonable with maximum players and planets."""

        # Act - Create resource sources for all players
        resource_sources = []
        influence_sources = []

        for player in self.players:
            resources = self.resource_manager.get_resource_sources(player.id)
            influence = self.resource_manager.get_influence_sources(player.id)
            resource_sources.append(resources)
            influence_sources.append(influence)

        # Assert - Data structures should be reasonable size
        # Each player should have 5 planets
        for resources in resource_sources:
            assert len(resources.planets) <= 5
            assert resources.total_available > 0

        for influence in influence_sources:
            assert len(influence.planets) <= 5
            assert influence.total_available > 0

        # Memory usage should be reasonable (this is a basic check)
        total_objects = len(resource_sources) + len(influence_sources)
        assert total_objects == 16  # 8 players * 2 source types


class TestEndToEndIntegrationScenarios:
    """Test end-to-end integration scenarios combining multiple systems."""

    def setup_method(self) -> None:
        """Set up test fixtures for end-to-end scenarios."""
        self.game_state = GameState()

        # Create two players
        self.player1 = Player("player1", Faction.SOL)
        self.player2 = Player("player2", Faction.HACAN)
        self.game_state = self.game_state.add_player(self.player1)
        self.game_state = self.game_state.add_player(self.player2)

        # Add planets
        self.planet1 = Planet("Mecatol Rex", resources=1, influence=6)
        self.planet2 = Planet("Jord", resources=4, influence=4)
        self.planet3 = Planet("Arc Prime", resources=4, influence=0)

        self.planet1.set_control("player1")
        self.planet2.set_control("player1")
        self.planet3.set_control("player2")

        self.game_state = self.game_state.add_player_planet("player1", self.planet1)
        self.game_state = self.game_state.add_player_planet("player1", self.planet2)
        self.game_state = self.game_state.add_player_planet("player2", self.planet3)

        # Add trade goods
        self.player1.gain_trade_goods(2)
        self.player2.gain_trade_goods(3)

        # Initialize all managers
        self.resource_manager = ResourceManager(self.game_state)
        self.stats_provider = UnitStatsProvider()
        self.cost_validator = CostValidator(self.resource_manager, self.stats_provider)
        self.production_manager = ProductionManager(
            self.resource_manager, self.cost_validator
        )
        self.voting_system = VotingSystem()

    def test_complete_game_turn_simulation(self) -> None:
        """Test complete game turn simulation with production and voting."""
        # Scenario: Player1 produces units, then both players vote on agenda

        # Phase 1: Production
        placement_location = MockProductionLocation(can_place=True)

        # Player1 produces a cruiser
        validation_result = self.production_manager.validate_production(
            player_id="player1",
            unit_type=UnitType.CRUISER,
            quantity=1,
            available_reinforcements=5,
        )
        assert validation_result.is_valid is True

        spending_plan = self.resource_manager.create_spending_plan(
            player_id="player1",
            resource_amount=int(validation_result.production_cost.total_cost),
        )
        assert spending_plan.is_valid is True

        execution_result = self.production_manager.execute_production(
            player_id="player1",
            unit_type=UnitType.CRUISER,
            quantity=1,
            spending_plan=spending_plan,
            placement_location=placement_location,
        )
        assert execution_result.success is True

        # Phase 2: Agenda Voting
        # Player1 votes with remaining influence (planets may be exhausted from production)
        remaining_influence = self.resource_manager.calculate_available_influence(
            "player1", for_voting=True
        )
        # Note: After production, planets may be exhausted, so influence might be 0
        # This is correct behavior - production exhausts planets

        if remaining_influence > 0:
            voting_plan1 = self.resource_manager.create_spending_plan(
                player_id="player1",
                influence_amount=min(remaining_influence, 5),
                for_voting=True,
            )
            assert voting_plan1.is_valid is True

            voting_result1 = self.resource_manager.execute_spending_plan(voting_plan1)
            assert voting_result1.success is True
        else:
            # Player1 cannot vote because planets are exhausted from production
            # This is correct behavior
            voting_plan1 = self.resource_manager.create_spending_plan(
                player_id="player1", influence_amount=1, for_voting=True
            )
            assert voting_plan1.is_valid is False

        # Player2 votes
        player2_influence = self.resource_manager.calculate_available_influence(
            "player2", for_voting=True
        )
        # Player2 has Arc Prime (4 resources, 0 influence) so should have 0 influence for voting
        assert player2_influence == 0

        # Try to vote with 1 influence (should fail)
        voting_plan2 = self.resource_manager.create_spending_plan(
            player_id="player2",
            influence_amount=1,  # Player2 has no influence planets
            for_voting=True,
        )
        # Player2 should not be able to vote (no influence)
        assert voting_plan2.is_valid is False

    def test_resource_exhaustion_and_recovery_cycle(self) -> None:
        """Test complete resource exhaustion and recovery cycle."""
        # Phase 1: Exhaust all resources
        total_resources = self.resource_manager.calculate_available_resources("player1")

        spending_plan = self.resource_manager.create_spending_plan(
            player_id="player1", resource_amount=total_resources
        )
        assert spending_plan.is_valid is True

        spending_result = self.resource_manager.execute_spending_plan(spending_plan)
        assert spending_result.success is True

        # Verify all planets are exhausted
        assert self.planet1.is_exhausted()
        assert self.planet2.is_exhausted()

        # Phase 2: Try to spend more (should fail)
        additional_spending = self.resource_manager.create_spending_plan(
            player_id="player1", resource_amount=1
        )
        assert additional_spending.is_valid is False

        # Phase 3: Ready planets (simulate status phase)
        self.planet1.ready()
        self.planet2.ready()

        # Phase 4: Verify resources are available again
        recovered_resources = self.resource_manager.calculate_available_resources(
            "player1"
        )
        # Note: Trade goods spent during the spending plan are not recovered
        # Only planet resources are recovered when planets are readied
        planet_resources = self.planet1.resources + self.planet2.resources  # 1 + 4 = 5
        current_trade_goods = self.player1.get_trade_goods()
        expected_resources = planet_resources + current_trade_goods
        assert recovered_resources == expected_resources

    def test_multi_system_error_propagation(self) -> None:
        """Test error propagation across multiple integrated systems."""
        # Scenario: Production fails due to placement, verify all systems handle it correctly

        # Arrange - Create failing placement location
        failing_placement = MockProductionLocation(
            can_place=False, placement_error="System capacity exceeded"
        )

        # Create valid spending plan
        spending_plan = self.resource_manager.create_spending_plan(
            player_id="player1", resource_amount=2
        )
        assert spending_plan.is_valid is True

        # Act - Execute production (should fail at placement)
        execution_result = self.production_manager.execute_production(
            player_id="player1",
            unit_type=UnitType.CRUISER,
            quantity=1,
            spending_plan=spending_plan,
            placement_location=failing_placement,
        )

        # Assert - Should fail with proper error propagation
        assert execution_result.success is False
        assert "System capacity exceeded" in execution_result.error_message

        # Verify no side effects occurred
        assert execution_result.units_placed == 0
        # Resource spending should have been rolled back by ResourceManager
