"""Tests for spending plan execution functionality.

Tests the execute_spending_plan() method and related error handling for
Rule 26: COST, Rule 75: RESOURCES, and Rule 47: INFLUENCE.
"""

from src.ti4.core.constants import Faction
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.resource_management import ResourceManager, SpendingResult


class TestSpendingPlanExecution:
    """Test spending plan execution with atomic planet exhaustion."""

    def test_execute_spending_plan_resources_only(self) -> None:
        """Test executing a spending plan for resources only."""
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
        player.gain_trade_goods(3)

        # Create ResourceManager and spending plan
        resource_manager = ResourceManager(game_state)
        plan = resource_manager.create_spending_plan(player.id, resource_amount=5)

        # Verify plan is valid
        assert plan.is_valid is True

        # Execute the spending plan - this should fail initially
        result = resource_manager.execute_spending_plan(plan)

        # Check that execution was successful
        assert isinstance(result, SpendingResult)
        assert result.success is True
        assert result.error_message is None

        # Check that planets were exhausted
        updated_planets = game_state.get_player_planets(player.id)
        exhausted_planets = [p for p in updated_planets if p.is_exhausted()]
        assert len(exhausted_planets) > 0

        # Check that trade goods were spent if needed
        if plan.resource_spending.trade_goods_to_spend > 0:
            assert (
                player.get_trade_goods()
                == 3 - plan.resource_spending.trade_goods_to_spend
            )

    def test_execute_spending_plan_with_rollback_on_failure(self) -> None:
        """Test that spending plan execution rolls back on failure."""
        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planet
        jord = Planet("Jord", resources=4, influence=2)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)

        # Give player insufficient trade goods
        player.gain_trade_goods(1)

        # Create ResourceManager and create an invalid spending plan
        resource_manager = ResourceManager(game_state)
        plan = resource_manager.create_spending_plan(player.id, resource_amount=10)

        # Verify plan is invalid
        assert plan.is_valid is False

        # Execute the spending plan - should fail
        result = resource_manager.execute_spending_plan(plan)

        # Check that execution failed
        assert isinstance(result, SpendingResult)
        assert result.success is False
        assert result.error_message is not None

        # Check that no planets were exhausted (rollback)
        updated_planets = game_state.get_player_planets(player.id)
        exhausted_planets = [p for p in updated_planets if p.is_exhausted()]
        assert len(exhausted_planets) == 0

        # Check that no trade goods were spent (rollback)
        assert player.get_trade_goods() == 1

    def test_execute_spending_plan_influence_only(self) -> None:
        """Test executing a spending plan for influence only."""
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

        # Create ResourceManager and spending plan
        resource_manager = ResourceManager(game_state)
        plan = resource_manager.create_spending_plan(player.id, influence_amount=7)

        # Verify plan is valid
        assert plan.is_valid is True

        # Execute the spending plan
        result = resource_manager.execute_spending_plan(plan)

        # Check that execution was successful
        assert isinstance(result, SpendingResult)
        assert result.success is True
        assert result.error_message is None

        # Check that planets were exhausted
        updated_planets = game_state.get_player_planets(player.id)
        exhausted_planets = [p for p in updated_planets if p.is_exhausted()]
        assert len(exhausted_planets) > 0

        # Check that trade goods were spent if needed
        if plan.influence_spending.trade_goods_to_spend > 0:
            assert (
                player.get_trade_goods()
                == 2 - plan.influence_spending.trade_goods_to_spend
            )

    def test_execute_spending_plan_both_resources_and_influence(self) -> None:
        """Test executing a spending plan for both resources and influence."""
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

        # Create ResourceManager and spending plan
        resource_manager = ResourceManager(game_state)
        plan = resource_manager.create_spending_plan(
            player.id, resource_amount=4, influence_amount=4
        )

        # Verify plan is valid
        assert plan.is_valid is True

        # Execute the spending plan
        result = resource_manager.execute_spending_plan(plan)

        # Check that execution was successful
        assert isinstance(result, SpendingResult)
        assert result.success is True
        assert result.error_message is None

        # Check that planets were exhausted
        updated_planets = game_state.get_player_planets(player.id)
        exhausted_planets = [p for p in updated_planets if p.is_exhausted()]
        assert len(exhausted_planets) > 0

    def test_execute_spending_plan_with_trade_goods_only(self) -> None:
        """Test executing a spending plan using only trade goods."""
        # Create game state with player but no planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Set up game state
        game_state = game_state.add_player(player)

        # Give player trade goods
        player.gain_trade_goods(10)

        # Create ResourceManager and spending plan
        resource_manager = ResourceManager(game_state)
        plan = resource_manager.create_spending_plan(
            player.id, resource_amount=3, influence_amount=2
        )

        # Verify plan is valid
        assert plan.is_valid is True

        # Execute the spending plan
        result = resource_manager.execute_spending_plan(plan)

        # Check that execution was successful
        assert isinstance(result, SpendingResult)
        assert result.success is True
        assert result.error_message is None

        # Check that no planets were exhausted (none to exhaust)
        assert result.planets_exhausted == []

        # Check that trade goods were spent
        assert result.trade_goods_spent == 5  # 3 for resources + 2 for influence
        assert player.get_trade_goods() == 5  # 10 - 5 = 5

    def test_execute_spending_plan_insufficient_trade_goods(self) -> None:
        """Test that spending plan execution fails when trade goods are insufficient."""
        # Create game state with player but no planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Set up game state
        game_state = game_state.add_player(player)

        # Give player insufficient trade goods
        player.gain_trade_goods(2)

        # Create ResourceManager and try to create a plan that needs more trade goods
        resource_manager = ResourceManager(game_state)
        plan = resource_manager.create_spending_plan(
            player.id, resource_amount=5, influence_amount=3
        )

        # Plan should be invalid
        assert plan.is_valid is False

        # Execute the spending plan - should fail
        result = resource_manager.execute_spending_plan(plan)

        # Check that execution failed
        assert isinstance(result, SpendingResult)
        assert result.success is False
        assert result.error_message is not None

        # Check that no trade goods were spent (rollback)
        assert player.get_trade_goods() == 2

    def test_execute_spending_plan_planet_already_exhausted(self) -> None:
        """Test that spending plan execution fails when a planet is already exhausted."""
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

        # Create ResourceManager and spending plan that would use the exhausted planet
        resource_manager = ResourceManager(game_state)

        # Force create a plan that includes the exhausted planet by manually creating it
        from src.ti4.core.resource_management import (
            InfluenceSpending,
            ResourceSpending,
            SpendingPlan,
        )

        resource_spending = ResourceSpending(
            planets_to_exhaust={"Jord": 4, "Muaat": 2},  # Includes exhausted Jord
            trade_goods_to_spend=0,
            total_resources=6,
        )
        influence_spending = InfluenceSpending(
            planets_to_exhaust={}, trade_goods_to_spend=0, total_influence=0
        )

        plan = SpendingPlan(
            player_id=player.id,
            resource_spending=resource_spending,
            influence_spending=influence_spending,
            total_resource_cost=5,
            total_influence_cost=0,
            is_valid=True,  # Force valid for this test
        )

        # Execute the spending plan - should fail due to exhausted planet
        result = resource_manager.execute_spending_plan(plan)

        # Check that execution failed
        assert isinstance(result, SpendingResult)
        assert result.success is False
        assert result.error_message is not None
        assert "already exhausted" in result.error_message

        # Check that Muaat was not exhausted (rollback)
        updated_planets = game_state.get_player_planets(player.id)
        muaat_planet = next(p for p in updated_planets if p.name == "Muaat")
        assert not muaat_planet.is_exhausted()

    def test_execute_spending_plan_nonexistent_player(self) -> None:
        """Test that spending plan execution fails for nonexistent player."""
        # Create empty game state
        game_state = GameState()

        # Create ResourceManager
        resource_manager = ResourceManager(game_state)

        # Create a fake spending plan for nonexistent player
        from src.ti4.core.resource_management import (
            InfluenceSpending,
            ResourceSpending,
            SpendingPlan,
        )

        resource_spending = ResourceSpending(
            planets_to_exhaust={}, trade_goods_to_spend=1, total_resources=1
        )
        influence_spending = InfluenceSpending(
            planets_to_exhaust={}, trade_goods_to_spend=0, total_influence=0
        )

        plan = SpendingPlan(
            player_id="nonexistent",
            resource_spending=resource_spending,
            influence_spending=influence_spending,
            total_resource_cost=1,
            total_influence_cost=0,
            is_valid=True,  # Force valid for this test
        )

        # Execute the spending plan - should fail
        result = resource_manager.execute_spending_plan(plan)

        # Check that execution failed
        assert isinstance(result, SpendingResult)
        assert result.success is False
        assert result.error_message is not None
        assert "not found" in result.error_message

    def test_execute_spending_plan_zero_amounts(self) -> None:
        """Test executing a spending plan with zero amounts."""
        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planet
        planet = Planet("Planet", resources=3, influence=2)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet)

        # Create ResourceManager and spending plan
        resource_manager = ResourceManager(game_state)
        plan = resource_manager.create_spending_plan(
            player.id, resource_amount=0, influence_amount=0
        )

        # Verify plan is valid
        assert plan.is_valid is True

        # Execute the spending plan
        result = resource_manager.execute_spending_plan(plan)

        # Check that execution was successful
        assert isinstance(result, SpendingResult)
        assert result.success is True
        assert result.error_message is None

        # Check that no planets were exhausted
        assert result.planets_exhausted == []

        # Check that no trade goods were spent
        assert result.trade_goods_spent == 0

        # Check that planet is still ready
        updated_planets = game_state.get_player_planets(player.id)
        planet_updated = updated_planets[0]
        assert not planet_updated.is_exhausted()


class TestSpendingPlanExecutionEdgeCases:
    """Test edge cases and error conditions for spending plan execution."""

    def test_execute_spending_plan_same_planet_for_resources_and_influence(
        self,
    ) -> None:
        """Test executing a plan where the same planet is used for both resources and influence."""
        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planet with both resources and influence
        balanced_planet = Planet("Balanced", resources=3, influence=3)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, balanced_planet)

        # Create ResourceManager
        resource_manager = ResourceManager(game_state)

        # Create a plan that uses the same planet for both resources and influence
        from src.ti4.core.resource_management import (
            InfluenceSpending,
            ResourceSpending,
            SpendingPlan,
        )

        resource_spending = ResourceSpending(
            planets_to_exhaust={"Balanced": 3},
            trade_goods_to_spend=0,
            total_resources=3,
        )
        influence_spending = InfluenceSpending(
            planets_to_exhaust={"Balanced": 3},  # Same planet
            trade_goods_to_spend=0,
            total_influence=3,
        )

        plan = SpendingPlan(
            player_id=player.id,
            resource_spending=resource_spending,
            influence_spending=influence_spending,
            total_resource_cost=3,
            total_influence_cost=3,
            is_valid=True,
        )

        # Execute the spending plan
        result = resource_manager.execute_spending_plan(plan)

        # Check that execution was successful
        assert isinstance(result, SpendingResult)
        assert result.success is True
        assert result.error_message is None

        # Check that the planet was only exhausted once
        assert result.planets_exhausted == ["Balanced"]

        # Check that planet is exhausted
        updated_planets = game_state.get_player_planets(player.id)
        planet_updated = updated_planets[0]
        assert planet_updated.is_exhausted()

    def test_execute_spending_plan_rollback_partial_exhaustion(self) -> None:
        """Test that rollback works correctly when some planets are exhausted before failure."""
        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planets
        planet1 = Planet("Planet1", resources=3, influence=2)
        planet2 = Planet("Planet2", resources=2, influence=1)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet1)
        game_state = game_state.add_player_planet(player.id, planet2)

        # Give player insufficient trade goods to cause failure
        player.gain_trade_goods(1)

        # Create ResourceManager
        resource_manager = ResourceManager(game_state)

        # Create a plan that will fail on trade goods but after exhausting planets
        from src.ti4.core.resource_management import (
            InfluenceSpending,
            ResourceSpending,
            SpendingPlan,
        )

        resource_spending = ResourceSpending(
            planets_to_exhaust={"Planet1": 3, "Planet2": 2},
            trade_goods_to_spend=5,  # More than available (1)
            total_resources=10,
        )
        influence_spending = InfluenceSpending(
            planets_to_exhaust={}, trade_goods_to_spend=0, total_influence=0
        )

        plan = SpendingPlan(
            player_id=player.id,
            resource_spending=resource_spending,
            influence_spending=influence_spending,
            total_resource_cost=10,
            total_influence_cost=0,
            is_valid=True,  # Force valid for this test
        )

        # Execute the spending plan - should fail on trade goods
        result = resource_manager.execute_spending_plan(plan)

        # Check that execution failed
        assert isinstance(result, SpendingResult)
        assert result.success is False
        assert result.error_message is not None

        # Check that all planets were rolled back (not exhausted)
        updated_planets = game_state.get_player_planets(player.id)
        for planet in updated_planets:
            assert not planet.is_exhausted()

        # Check that trade goods were not spent
        assert player.get_trade_goods() == 1
