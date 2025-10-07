"""Tests for ResourceManager core functionality.

Tests the ResourceManager class for Rule 26: COST, Rule 75: RESOURCES, and Rule 47: INFLUENCE.
"""

from src.ti4.core.constants import Faction
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.resource_management import (
    InfluenceSources,
    ResourceSources,
    SpendingPlan,
)


class TestResourceManagerCalculations:
    """Test ResourceManager resource and influence calculations."""

    def test_calculate_available_resources_with_planets_and_trade_goods(self) -> None:
        """Test calculating available resources from controlled planets and trade goods."""
        # This test should fail initially - ResourceManager doesn't exist yet
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planets with different resource values
        jord = Planet("Jord", resources=4, influence=2)
        muaat = Planet("Muaat", resources=2, influence=1)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)
        game_state = game_state.add_player_planet(player.id, muaat)

        # Give player some trade goods
        player.gain_trade_goods(3)

        # Create ResourceManager and test calculation
        resource_manager = ResourceManager(game_state)
        available_resources = resource_manager.calculate_available_resources(player.id)

        # Should be 4 (Jord) + 2 (Muaat) + 3 (trade goods) = 9
        assert available_resources == 9

    def test_calculate_available_resources_excludes_exhausted_planets(self) -> None:
        """Test that exhausted planets don't contribute to available resources."""
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planets
        jord = Planet("Jord", resources=4, influence=2)
        muaat = Planet("Muaat", resources=2, influence=1)

        # Exhaust one planet
        jord.exhaust()

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)
        game_state = game_state.add_player_planet(player.id, muaat)

        # Give player some trade goods
        player.gain_trade_goods(1)

        # Create ResourceManager and test calculation
        resource_manager = ResourceManager(game_state)
        available_resources = resource_manager.calculate_available_resources(player.id)

        # Should be 0 (Jord exhausted) + 2 (Muaat) + 1 (trade goods) = 3
        assert available_resources == 3

    def test_calculate_available_influence_normal_mode(self) -> None:
        """Test calculating available influence in normal mode (trade goods allowed)."""
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planets with different influence values
        mecatol = Planet("Mecatol Rex", resources=1, influence=6)
        jord = Planet("Jord", resources=4, influence=2)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, mecatol)
        game_state = game_state.add_player_planet(player.id, jord)

        # Give player some trade goods
        player.gain_trade_goods(2)

        # Create ResourceManager and test calculation
        resource_manager = ResourceManager(game_state)
        available_influence = resource_manager.calculate_available_influence(
            player.id, for_voting=False
        )

        # Should be 6 (Mecatol) + 2 (Jord) + 2 (trade goods) = 10
        assert available_influence == 10

    def test_calculate_available_influence_voting_mode_excludes_trade_goods(
        self,
    ) -> None:
        """Test that trade goods are excluded when calculating influence for voting (Rule 47.3)."""
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planets with different influence values
        mecatol = Planet("Mecatol Rex", resources=1, influence=6)
        jord = Planet("Jord", resources=4, influence=2)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, mecatol)
        game_state = game_state.add_player_planet(player.id, jord)

        # Give player some trade goods
        player.gain_trade_goods(5)

        # Create ResourceManager and test calculation
        resource_manager = ResourceManager(game_state)
        available_influence = resource_manager.calculate_available_influence(
            player.id, for_voting=True
        )

        # Should be 6 (Mecatol) + 2 (Jord) + 0 (no trade goods for voting) = 8
        assert available_influence == 8


class TestResourceManagerDetailedBreakdowns:
    """Test ResourceManager detailed source breakdown methods."""

    def test_get_resource_sources_breakdown(self) -> None:
        """Test getting detailed breakdown of resource sources."""
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planets
        jord = Planet("Jord", resources=4, influence=2)
        muaat = Planet("Muaat", resources=2, influence=1)
        exhausted_planet = Planet("Exhausted", resources=3, influence=1)
        exhausted_planet.exhaust()

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)
        game_state = game_state.add_player_planet(player.id, muaat)
        game_state = game_state.add_player_planet(player.id, exhausted_planet)

        # Give player some trade goods
        player.gain_trade_goods(3)

        # Create ResourceManager and test breakdown
        resource_manager = ResourceManager(game_state)
        sources = resource_manager.get_resource_sources(player.id)

        # Check the breakdown
        assert isinstance(sources, ResourceSources)
        assert sources.planets == {"Jord": 4, "Muaat": 2}  # Exhausted planet excluded
        assert sources.trade_goods == 3
        assert sources.total_available == 9
        assert set(sources.get_planet_names()) == {"Jord", "Muaat"}

    def test_get_influence_sources_breakdown_normal_mode(self) -> None:
        """Test getting detailed breakdown of influence sources in normal mode."""
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planets
        mecatol = Planet("Mecatol Rex", resources=1, influence=6)
        jord = Planet("Jord", resources=4, influence=2)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, mecatol)
        game_state = game_state.add_player_planet(player.id, jord)

        # Give player some trade goods
        player.gain_trade_goods(2)

        # Create ResourceManager and test breakdown
        resource_manager = ResourceManager(game_state)
        sources = resource_manager.get_influence_sources(player.id, for_voting=False)

        # Check the breakdown
        assert isinstance(sources, InfluenceSources)
        assert sources.planets == {"Mecatol Rex": 6, "Jord": 2}
        assert sources.trade_goods == 2
        assert sources.total_available == 10
        assert sources.for_voting is False
        assert set(sources.get_planet_names()) == {"Mecatol Rex", "Jord"}

    def test_get_influence_sources_breakdown_voting_mode(self) -> None:
        """Test getting detailed breakdown of influence sources in voting mode."""
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planets
        mecatol = Planet("Mecatol Rex", resources=1, influence=6)
        jord = Planet("Jord", resources=4, influence=2)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, mecatol)
        game_state = game_state.add_player_planet(player.id, jord)

        # Give player some trade goods
        player.gain_trade_goods(5)

        # Create ResourceManager and test breakdown
        resource_manager = ResourceManager(game_state)
        sources = resource_manager.get_influence_sources(player.id, for_voting=True)

        # Check the breakdown
        assert isinstance(sources, InfluenceSources)
        assert sources.planets == {"Mecatol Rex": 6, "Jord": 2}
        assert sources.trade_goods == 0  # No trade goods for voting
        assert sources.total_available == 8
        assert sources.for_voting is True


class TestResourceManagerSpendingPlans:
    """Test ResourceManager spending plan creation and validation."""

    def test_create_spending_plan_resources_only(self) -> None:
        """Test creating a spending plan for resources only."""
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planets
        jord = Planet("Jord", resources=4, influence=2)
        muaat = Planet("Muaat", resources=2, influence=1)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)
        game_state = game_state.add_player_planet(player.id, muaat)

        # Give player some trade goods
        player.gain_trade_goods(1)

        # Create ResourceManager and test spending plan
        resource_manager = ResourceManager(game_state)
        plan = resource_manager.create_spending_plan(player.id, resource_amount=5)

        # Check the plan
        assert isinstance(plan, SpendingPlan)
        assert plan.player_id == "player1"
        assert plan.total_resource_cost == 5
        assert plan.total_influence_cost == 0
        assert plan.is_valid is True
        assert plan.error_message is None

        # Check resource spending details
        # Should use planets first - when you exhaust a planet, you get all its resources
        # So we'll use both planets (4+2=6 resources) even though we only need 5
        assert plan.resource_spending.total_resources >= 5
        assert plan.resource_spending.planets_to_exhaust == {"Jord": 4, "Muaat": 2}
        assert (
            plan.resource_spending.trade_goods_to_spend == 0
        )  # Don't need trade goods

    def test_create_spending_plan_insufficient_resources(self) -> None:
        """Test creating a spending plan when resources are insufficient."""
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planet with limited resources
        small_planet = Planet("Small", resources=1, influence=1)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, small_planet)

        # No trade goods

        # Create ResourceManager and test spending plan
        resource_manager = ResourceManager(game_state)
        plan = resource_manager.create_spending_plan(player.id, resource_amount=5)

        # Check the plan
        assert isinstance(plan, SpendingPlan)
        assert plan.player_id == "player1"
        assert plan.total_resource_cost == 5
        assert plan.is_valid is False
        assert plan.error_message is not None
        assert "insufficient" in plan.error_message.lower()

    def test_can_afford_spending_check(self) -> None:
        """Test quick affordability check method."""
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planets
        jord = Planet("Jord", resources=4, influence=2)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)

        # Give player some trade goods
        player.gain_trade_goods(2)

        # Create ResourceManager and test affordability
        resource_manager = ResourceManager(game_state)

        # Should be able to afford 6 resources (4 + 2)
        assert (
            resource_manager.can_afford_spending(player.id, resource_amount=6) is True
        )

        # Should not be able to afford 7 resources
        assert (
            resource_manager.can_afford_spending(player.id, resource_amount=7) is False
        )

        # Should be able to afford 2 influence (from Jord)
        assert (
            resource_manager.can_afford_spending(player.id, influence_amount=2) is True
        )

        # Should be able to afford 4 influence in normal mode (2 + 2 trade goods)
        assert (
            resource_manager.can_afford_spending(
                player.id, influence_amount=4, for_voting=False
            )
            is True
        )

        # Should not be able to afford 4 influence in voting mode (no trade goods)
        assert (
            resource_manager.can_afford_spending(
                player.id, influence_amount=4, for_voting=True
            )
            is False
        )


class TestResourceManagerEdgeCases:
    """Test ResourceManager edge cases and error conditions."""

    def test_player_with_no_planets(self) -> None:
        """Test resource calculations for player with no controlled planets."""
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player but no planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Set up game state
        game_state = game_state.add_player(player)

        # Give player some trade goods
        player.gain_trade_goods(3)

        # Create ResourceManager and test calculations
        resource_manager = ResourceManager(game_state)

        # Should only have trade goods
        assert resource_manager.calculate_available_resources(player.id) == 3
        assert (
            resource_manager.calculate_available_influence(player.id, for_voting=False)
            == 3
        )
        assert (
            resource_manager.calculate_available_influence(player.id, for_voting=True)
            == 0
        )

        # Check sources
        resource_sources = resource_manager.get_resource_sources(player.id)
        assert resource_sources.planets == {}
        assert resource_sources.trade_goods == 3
        assert resource_sources.total_available == 3

    def test_player_with_no_trade_goods(self) -> None:
        """Test resource calculations for player with no trade goods."""
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planets
        jord = Planet("Jord", resources=4, influence=2)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)

        # No trade goods

        # Create ResourceManager and test calculations
        resource_manager = ResourceManager(game_state)

        # Should only have planet resources/influence
        assert resource_manager.calculate_available_resources(player.id) == 4
        assert (
            resource_manager.calculate_available_influence(player.id, for_voting=False)
            == 2
        )
        assert (
            resource_manager.calculate_available_influence(player.id, for_voting=True)
            == 2
        )

        # Check sources
        resource_sources = resource_manager.get_resource_sources(player.id)
        assert resource_sources.planets == {"Jord": 4}
        assert resource_sources.trade_goods == 0
        assert resource_sources.total_available == 4

    def test_nonexistent_player(self) -> None:
        """Test resource calculations for nonexistent player."""
        import pytest

        from src.ti4.core.resource_management import (
            ResourceManager,
            ResourceOperationError,
        )

        # Create empty game state
        game_state = GameState()

        # Create ResourceManager and test calculations
        resource_manager = ResourceManager(game_state)

        # Should raise ResourceOperationError for all calculations
        with pytest.raises(ResourceOperationError):
            resource_manager.calculate_available_resources("nonexistent")

        with pytest.raises(ResourceOperationError):
            resource_manager.calculate_available_influence(
                "nonexistent", for_voting=False
            )

        with pytest.raises(ResourceOperationError):
            resource_manager.calculate_available_influence(
                "nonexistent", for_voting=True
            )

        # Should raise ResourceOperationError for source queries
        with pytest.raises(ResourceOperationError):
            resource_manager.get_resource_sources("nonexistent")

        with pytest.raises(ResourceOperationError):
            resource_manager.get_influence_sources("nonexistent")

        # Should raise ResourceOperationError for affordability checks
        with pytest.raises(ResourceOperationError):
            resource_manager.can_afford_spending("nonexistent", resource_amount=1)

        with pytest.raises(ResourceOperationError):
            resource_manager.can_afford_spending("nonexistent", influence_amount=1)


class TestSpendingPlanAdvancedScenarios:
    """Test advanced spending plan scenarios and edge cases."""

    def test_create_spending_plan_influence_only(self) -> None:
        """Test creating a spending plan for influence only."""
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planets with high influence
        mecatol = Planet("Mecatol Rex", resources=1, influence=6)
        jord = Planet("Jord", resources=4, influence=2)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, mecatol)
        game_state = game_state.add_player_planet(player.id, jord)

        # Give player some trade goods
        player.gain_trade_goods(2)

        # Create ResourceManager and test spending plan
        resource_manager = ResourceManager(game_state)
        plan = resource_manager.create_spending_plan(player.id, influence_amount=7)

        # Check the plan
        assert isinstance(plan, SpendingPlan)
        assert plan.player_id == "player1"
        assert plan.total_resource_cost == 0
        assert plan.total_influence_cost == 7
        assert plan.is_valid is True
        assert plan.error_message is None

        # Check influence spending details
        # Should use planets first - when you exhaust a planet, you get all its influence
        # So we'll use both planets (6+2=8 influence) even though we only need 7
        assert plan.influence_spending.total_influence >= 7
        assert plan.influence_spending.planets_to_exhaust == {
            "Mecatol Rex": 6,
            "Jord": 2,
        }
        assert (
            plan.influence_spending.trade_goods_to_spend == 0
        )  # Don't need trade goods

    def test_create_spending_plan_both_resources_and_influence(self) -> None:
        """Test creating a spending plan for both resources and influence."""
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planets with balanced resources/influence
        balanced_planet = Planet("Balanced", resources=3, influence=3)
        resource_planet = Planet("Resource Rich", resources=5, influence=1)
        influence_planet = Planet("Influence Rich", resources=1, influence=5)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, balanced_planet)
        game_state = game_state.add_player_planet(player.id, resource_planet)
        game_state = game_state.add_player_planet(player.id, influence_planet)

        # Give player some trade goods
        player.gain_trade_goods(2)

        # Create ResourceManager and test spending plan
        resource_manager = ResourceManager(game_state)
        plan = resource_manager.create_spending_plan(
            player.id, resource_amount=4, influence_amount=4
        )

        # Check the plan
        assert isinstance(plan, SpendingPlan)
        assert plan.player_id == "player1"
        assert plan.total_resource_cost == 4
        assert plan.total_influence_cost == 4
        assert plan.is_valid is True
        assert plan.error_message is None

        # Should have sufficient resources and influence
        assert plan.resource_spending.total_resources >= 4
        assert plan.influence_spending.total_influence >= 4

    def test_create_spending_plan_voting_mode_excludes_trade_goods(self) -> None:
        """Test that voting mode spending plans exclude trade goods from influence."""
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planet with limited influence
        small_planet = Planet("Small", resources=2, influence=3)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, small_planet)

        # Give player lots of trade goods
        player.gain_trade_goods(10)

        # Create ResourceManager and test spending plan for voting
        resource_manager = ResourceManager(game_state)
        plan = resource_manager.create_spending_plan(
            player.id, influence_amount=5, for_voting=True
        )

        # Check the plan - should fail because trade goods can't be used for voting
        assert isinstance(plan, SpendingPlan)
        assert plan.player_id == "player1"
        assert plan.total_influence_cost == 5
        assert plan.is_valid is False  # Can't afford 5 influence without trade goods
        assert plan.error_message is not None
        assert "insufficient" in plan.error_message.lower()

        # Check that trade goods weren't used
        assert plan.influence_spending.trade_goods_to_spend == 0

    def test_create_spending_plan_with_trade_goods_only(self) -> None:
        """Test creating a spending plan using only trade goods."""
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player but no planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Set up game state
        game_state = game_state.add_player(player)

        # Give player trade goods
        player.gain_trade_goods(5)

        # Create ResourceManager and test spending plan
        resource_manager = ResourceManager(game_state)
        plan = resource_manager.create_spending_plan(
            player.id, resource_amount=3, influence_amount=2
        )

        # Check the plan
        assert isinstance(plan, SpendingPlan)
        assert plan.player_id == "player1"
        assert plan.total_resource_cost == 3
        assert plan.total_influence_cost == 2
        assert plan.is_valid is True
        assert plan.error_message is None

        # Should use trade goods for both
        assert plan.resource_spending.trade_goods_to_spend == 3
        assert plan.influence_spending.trade_goods_to_spend == 2
        assert plan.resource_spending.planets_to_exhaust == {}
        assert plan.influence_spending.planets_to_exhaust == {}

    def test_spending_plan_helper_methods(self) -> None:
        """Test SpendingPlan helper methods."""
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planets
        planet1 = Planet("Planet1", resources=3, influence=2)
        planet2 = Planet("Planet2", resources=2, influence=4)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet1)
        game_state = game_state.add_player_planet(player.id, planet2)

        # Give player trade goods
        player.gain_trade_goods(3)

        # Create ResourceManager and test spending plan
        resource_manager = ResourceManager(game_state)
        plan = resource_manager.create_spending_plan(
            player.id, resource_amount=4, influence_amount=3
        )

        # Test helper methods
        planets_to_exhaust = plan.get_total_planets_to_exhaust()
        trade_goods_to_spend = plan.get_total_trade_goods_to_spend()

        # Should have some planets to exhaust
        assert len(planets_to_exhaust) > 0
        assert isinstance(planets_to_exhaust, set)

        # Should have some trade goods to spend (or 0)
        assert isinstance(trade_goods_to_spend, int)
        assert trade_goods_to_spend >= 0

    def test_zero_amount_spending_plan(self) -> None:
        """Test creating a spending plan with zero amounts."""
        from src.ti4.core.resource_management import ResourceManager

        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planet
        planet = Planet("Planet", resources=3, influence=2)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet)

        # Create ResourceManager and test spending plan
        resource_manager = ResourceManager(game_state)
        plan = resource_manager.create_spending_plan(
            player.id, resource_amount=0, influence_amount=0
        )

        # Check the plan
        assert isinstance(plan, SpendingPlan)
        assert plan.player_id == "player1"
        assert plan.total_resource_cost == 0
        assert plan.total_influence_cost == 0
        assert plan.is_valid is True
        assert plan.error_message is None

        # Should not exhaust any planets or spend trade goods
        assert plan.resource_spending.planets_to_exhaust == {}
        assert plan.resource_spending.trade_goods_to_spend == 0
        assert plan.influence_spending.planets_to_exhaust == {}
        assert plan.influence_spending.trade_goods_to_spend == 0
        assert plan.get_total_planets_to_exhaust() == set()
        assert plan.get_total_trade_goods_to_spend() == 0
