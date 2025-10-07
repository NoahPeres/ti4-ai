"""Tests for Construction strategy card cost exemptions.

Tests the CostValidator integration with Construction strategy card for Rule 26.3:
- Structure placement without resource cost validation
- Validation that units without cost cannot be produced normally
- Integration with existing strategy card system
"""

from src.ti4.core.constants import UnitType
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.resource_management import (
    CostValidator,
    ResourceManager,
)
from src.ti4.core.unit_stats import UnitStatsProvider


class TestConstructionStrategyCostExemptions:
    """Test Construction strategy card cost exemptions."""

    def test_can_produce_without_cost_identifies_structures(self) -> None:
        """Test that structures (PDS, Space Dock) are identified as cost-free units."""
        # RED: Write failing test for structure identification
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # PDS should be producible without cost (has cost=0)
        assert cost_validator.can_produce_without_cost(UnitType.PDS) is True

        # Space Dock should be producible without cost (has cost=0)
        assert cost_validator.can_produce_without_cost(UnitType.SPACE_DOCK) is True

        # Regular units should NOT be producible without cost
        assert cost_validator.can_produce_without_cost(UnitType.CRUISER) is False
        assert cost_validator.can_produce_without_cost(UnitType.FIGHTER) is False
        assert cost_validator.can_produce_without_cost(UnitType.INFANTRY) is False

    def test_validate_production_cost_rejects_zero_cost_units_normally(self) -> None:
        """Test that units with zero cost cannot be produced through normal production."""
        # RED: Write failing test for zero cost unit rejection
        game_state = GameState()

        # Create a player with resources
        player = Player(id="player1", faction=None)
        player.gain_trade_goods(5)
        game_state = game_state.add_player(player)

        # Create a planet with resources
        planet = Planet(name="test_planet", resources=3, influence=2)
        planet.set_control("player1")
        game_state = game_state.add_player_planet("player1", planet)

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Try to produce PDS through normal production - should be rejected
        production_cost = cost_validator.get_production_cost(UnitType.PDS, quantity=1)
        validation_result = cost_validator.validate_production_cost(
            "player1", production_cost
        )

        # Should be invalid because zero-cost units cannot be produced normally
        assert validation_result.is_valid is False
        assert "cannot be produced normally" in validation_result.error_message

        # Same for Space Dock
        production_cost = cost_validator.get_production_cost(
            UnitType.SPACE_DOCK, quantity=1
        )
        validation_result = cost_validator.validate_production_cost(
            "player1", production_cost
        )

        assert validation_result.is_valid is False
        assert "cannot be produced normally" in validation_result.error_message

    def test_validate_production_cost_with_construction_exemption(self) -> None:
        """Test that structures can be produced when Construction strategy card exemption is active."""
        # RED: Write failing test for Construction exemption
        game_state = GameState()

        # Create a player
        player = Player(id="player1", faction=None)
        game_state = game_state.add_player(player)

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Try to produce PDS with Construction exemption - should be allowed
        production_cost = cost_validator.get_production_cost(UnitType.PDS, quantity=1)
        validation_result = (
            cost_validator.validate_production_cost_with_construction_exemption(
                "player1", production_cost
            )
        )

        # Should be valid when Construction exemption is active
        assert validation_result.is_valid is True
        assert validation_result.error_message is None

        # Same for Space Dock
        production_cost = cost_validator.get_production_cost(
            UnitType.SPACE_DOCK, quantity=1
        )
        validation_result = (
            cost_validator.validate_production_cost_with_construction_exemption(
                "player1", production_cost
            )
        )

        assert validation_result.is_valid is True
        assert validation_result.error_message is None

    def test_construction_exemption_only_applies_to_structures(self) -> None:
        """Test that Construction exemption only applies to structures, not regular units."""
        # RED: Write failing test for Construction exemption scope
        game_state = GameState()

        # Create a player with no resources
        player = Player(id="player1", faction=None)
        game_state = game_state.add_player(player)

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Try to produce regular units with Construction exemption - should still require resources
        production_cost = cost_validator.get_production_cost(
            UnitType.CRUISER, quantity=1
        )
        validation_result = (
            cost_validator.validate_production_cost_with_construction_exemption(
                "player1", production_cost
            )
        )

        # Should be invalid because regular units still require resources even with Construction
        assert validation_result.is_valid is False
        assert "Insufficient resources" in validation_result.error_message

        # Same for fighters
        production_cost = cost_validator.get_production_cost(
            UnitType.FIGHTER, quantity=1
        )
        validation_result = (
            cost_validator.validate_production_cost_with_construction_exemption(
                "player1", production_cost
            )
        )

        assert validation_result.is_valid is False
        assert "Insufficient resources" in validation_result.error_message

    def test_construction_exemption_does_not_exhaust_planets_or_trade_goods(
        self,
    ) -> None:
        """Test that Construction exemption doesn't consume resources."""
        # RED: Write failing test for resource consumption
        game_state = GameState()

        # Create a player with resources
        player = Player(id="player1", faction=None)
        player.gain_trade_goods(3)
        game_state = game_state.add_player(player)

        # Create a planet with resources
        planet = Planet(name="test_planet", resources=2, influence=1)
        planet.set_control("player1")
        game_state = game_state.add_player_planet("player1", planet)

        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Get initial resource state
        initial_trade_goods = player.get_trade_goods()
        initial_planet_exhausted = planet.is_exhausted()

        # Validate PDS production with Construction exemption
        production_cost = cost_validator.get_production_cost(UnitType.PDS, quantity=1)
        validation_result = (
            cost_validator.validate_production_cost_with_construction_exemption(
                "player1", production_cost
            )
        )

        assert validation_result.is_valid is True

        # Resources should not be consumed during validation
        assert player.get_trade_goods() == initial_trade_goods
        assert planet.is_exhausted() == initial_planet_exhausted

        # Suggested spending plan should be empty or indicate no cost
        if validation_result.suggested_spending_plan:
            assert validation_result.suggested_spending_plan.total_resource_cost == 0
            assert (
                validation_result.suggested_spending_plan.get_total_trade_goods_to_spend()
                == 0
            )
            assert (
                len(
                    validation_result.suggested_spending_plan.get_total_planets_to_exhaust()
                )
                == 0
            )
