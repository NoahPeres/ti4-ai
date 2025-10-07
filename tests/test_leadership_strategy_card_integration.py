"""Integration tests for Leadership strategy card with ResourceManager.

This module tests the complete integration between the Leadership strategy card
and the unified resource management system, ensuring proper influence spending
validation and planet exhaustion.

LRR Reference: Rule 52 - STRATEGY CARD (Leadership)
Requirements: 5.5, 10.1, 10.2
"""

from unittest.mock import Mock

from ti4.core.constants import Faction
from ti4.core.game_state import GameState
from ti4.core.player import Player
from ti4.core.resource_management import (
    InfluenceSpending,
    ResourceManager,
    ResourceSpending,
    SpendingPlan,
    SpendingResult,
)
from ti4.core.strategy_cards.cards.leadership import LeadershipStrategyCard


class TestLeadershipStrategyCardIntegration:
    """Integration test suite for Leadership strategy card with ResourceManager."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        # Create test player
        self.player = Player(id="test_player", faction=Faction.SOL)
        self.player.gain_trade_goods(5)  # Give player some trade goods

        # Reset command pools to 0 for testing Leadership card gains
        object.__setattr__(self.player.command_sheet, "tactic_pool", 0)
        object.__setattr__(self.player.command_sheet, "fleet_pool", 0)
        object.__setattr__(self.player.command_sheet, "strategy_pool", 0)

        # Create game state with players
        self.game_state = GameState(players=[self.player])

        # Create Leadership card
        self.leadership_card = LeadershipStrategyCard()

    def test_leadership_primary_with_resource_manager_integration(self) -> None:
        """Test Leadership primary ability integrates with ResourceManager for influence validation."""
        # Arrange - Mock ResourceManager to simulate successful influence spending
        mock_resource_manager = Mock(spec=ResourceManager)
        mock_resource_manager.can_afford_spending.return_value = True

        # Mock spending plan creation and execution
        mock_spending_plan = Mock(spec=SpendingPlan)
        mock_spending_plan.is_valid = True
        mock_resource_manager.create_spending_plan.return_value = mock_spending_plan

        mock_spending_result = Mock(spec=SpendingResult)
        mock_spending_result.success = True
        mock_resource_manager.execute_spending_plan.return_value = mock_spending_result

        # Act - use ResourceManager interface
        result = self.leadership_card.execute_primary_ability(
            "test_player",
            game_state=self.game_state,
            player=self.player,
            resource_manager=mock_resource_manager,
            token_distribution={
                "tactic": 4,
                "fleet": 0,
                "strategy": 0,
            },  # 3 base + 1 from influence
            influence_to_spend=3,
        )

        # Assert - should succeed and call ResourceManager methods
        assert result.success is True
        assert result.additional_data["influence_spent"] == 3
        assert self.player.command_sheet.tactic_pool == 4

        # Verify ResourceManager integration
        mock_resource_manager.can_afford_spending.assert_called_once_with(
            "test_player", influence_amount=3, for_voting=False
        )
        mock_resource_manager.create_spending_plan.assert_called_once_with(
            "test_player", influence_amount=3, for_voting=False
        )
        mock_resource_manager.execute_spending_plan.assert_called_once_with(
            mock_spending_plan
        )

    def test_leadership_primary_with_insufficient_influence_fails(self) -> None:
        """Test Leadership primary ability fails with insufficient influence."""
        # Arrange - Mock ResourceManager to indicate insufficient influence
        mock_resource_manager = Mock(spec=ResourceManager)
        mock_resource_manager.can_afford_spending.return_value = False
        mock_resource_manager.calculate_available_influence.return_value = 2

        # Act
        result = self.leadership_card.execute_primary_ability(
            "test_player",
            game_state=self.game_state,
            player=self.player,
            resource_manager=mock_resource_manager,
            token_distribution={"tactic": 5, "fleet": 0, "strategy": 0},
            influence_to_spend=6,
        )

        # Assert
        assert result.success is False
        assert "Insufficient influence" in result.error_message
        assert "need 6, have 2" in result.error_message

        # Verify no tokens were gained
        assert self.player.command_sheet.tactic_pool == 0

        # Verify ResourceManager was called for validation
        mock_resource_manager.can_afford_spending.assert_called_once_with(
            "test_player", influence_amount=6, for_voting=False
        )

    def test_leadership_secondary_with_resource_manager_integration(self) -> None:
        """Test Leadership secondary ability integrates with ResourceManager."""
        # Arrange - create another player for secondary ability
        other_player = Player(id="other_player", faction=Faction.HACAN)
        object.__setattr__(other_player.command_sheet, "tactic_pool", 0)

        # Mock ResourceManager for secondary ability
        mock_resource_manager = Mock(spec=ResourceManager)
        mock_resource_manager.can_afford_spending.return_value = True

        mock_spending_plan = Mock(spec=SpendingPlan)
        mock_spending_plan.is_valid = True
        mock_resource_manager.create_spending_plan.return_value = mock_spending_plan

        mock_spending_result = Mock(spec=SpendingResult)
        mock_spending_result.success = True
        mock_resource_manager.execute_spending_plan.return_value = mock_spending_result

        # Act - spend 3 influence for 1 token (3/3 = 1)
        result = self.leadership_card.execute_secondary_ability(
            "other_player",
            game_state=self.game_state,
            player=other_player,
            resource_manager=mock_resource_manager,
            token_distribution={"tactic": 1, "fleet": 0, "strategy": 0},
            influence_to_spend=3,
        )

        # Assert
        assert result.success is True
        assert result.additional_data["tokens_gained"] == 1
        assert result.additional_data["influence_spent"] == 3
        assert result.additional_data["participated"] is True

        # Verify token was gained
        assert other_player.command_sheet.tactic_pool == 1

        # Verify ResourceManager integration
        mock_resource_manager.can_afford_spending.assert_called_once_with(
            "other_player", influence_amount=3, for_voting=False
        )

    def test_leadership_backward_compatibility_maintained(self) -> None:
        """Test that Leadership maintains backward compatibility with old interface."""
        # Arrange - use old interface without ResourceManager

        # Act
        result = self.leadership_card.execute_primary_ability(
            "test_player",
            game_state=self.game_state,
            player=self.player,
            token_distribution={"tactic": 3, "fleet": 0, "strategy": 0},
            planets_to_exhaust=[],
            trade_goods_to_spend=0,
        )

        # Assert
        assert result.success is True
        assert result.additional_data["base_tokens_gained"] == 3
        assert result.additional_data["influence_tokens_gained"] == 0
        assert self.player.command_sheet.tactic_pool == 3

    def test_leadership_error_handling_with_invalid_spending_plan(self) -> None:
        """Test Leadership handles invalid spending plans gracefully."""
        # Arrange - Mock ResourceManager to return invalid spending plan
        mock_resource_manager = Mock(spec=ResourceManager)
        mock_resource_manager.can_afford_spending.return_value = True

        # Create invalid spending plan
        invalid_plan = SpendingPlan(
            player_id="test_player",
            resource_spending=ResourceSpending({}, 0, 0),
            influence_spending=InfluenceSpending({}, 0, 0),
            total_resource_cost=0,
            total_influence_cost=3,
            is_valid=False,
            error_message="Test error",
        )
        mock_resource_manager.create_spending_plan.return_value = invalid_plan

        # Act
        result = self.leadership_card.execute_primary_ability(
            "test_player",
            game_state=self.game_state,
            player=self.player,
            resource_manager=mock_resource_manager,
            token_distribution={"tactic": 4, "fleet": 0, "strategy": 0},
            influence_to_spend=3,
        )

        # Assert
        assert result.success is False
        assert "Test error" in result.error_message
