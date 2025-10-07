"""Simple tests for Leadership strategy card integration with ResourceManager.

This module tests the basic integration between the Leadership strategy card and the
unified resource management system.
"""

from unittest.mock import Mock

from src.ti4.core.constants import Faction
from src.ti4.core.player import Player
from src.ti4.core.resource_management import (
    ResourceManager,
    SpendingPlan,
    SpendingResult,
)
from src.ti4.core.strategy_cards.cards.leadership import LeadershipStrategyCard


class TestLeadershipResourceIntegrationSimple:
    """Simple test suite for Leadership strategy card integration with ResourceManager."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.mock_game_state = Mock()
        self.leadership_card = LeadershipStrategyCard()

    def _create_test_player(self, player_id: str = "test_player") -> Player:
        """Helper to create a test player with empty command pools for testing."""
        player = Player(id=player_id, faction=Faction.SOL)
        # Reset command pools to 0 for testing Leadership card gains
        player.command_sheet.tactic_pool = 0
        player.command_sheet.fleet_pool = 0
        player.command_sheet.strategy_pool = 0
        return player

    def test_leadership_primary_accepts_resource_manager_parameters(self) -> None:
        """Test that Leadership primary ability accepts ResourceManager parameters without error."""
        # Arrange
        test_player = self._create_test_player()
        mock_resource_manager = Mock(spec=ResourceManager)

        # Mock ResourceManager to indicate insufficient influence
        mock_resource_manager.can_afford_spending.return_value = False
        mock_resource_manager.calculate_available_influence.return_value = 2

        # Act - use new interface with ResourceManager
        result = self.leadership_card.execute_primary_ability(
            "test_player",
            game_state=self.mock_game_state,
            player=test_player,
            resource_manager=mock_resource_manager,
            token_distribution={"tactic": 4, "fleet": 0, "strategy": 0},
            influence_to_spend=3,
        )

        # Assert - should fail due to insufficient influence but not crash
        assert result.success is False
        assert "Insufficient influence" in result.error_message
        # Verify ResourceManager was called
        mock_resource_manager.can_afford_spending.assert_called_once_with(
            "test_player", influence_amount=3, for_voting=False
        )
        mock_resource_manager.calculate_available_influence.assert_called_once_with(
            "test_player", for_voting=False
        )

    def test_leadership_primary_executes_spending_plan_when_valid(self) -> None:
        """Test that Leadership primary ability executes spending plan when valid."""
        # Arrange
        test_player = self._create_test_player()
        mock_resource_manager = Mock(spec=ResourceManager)

        # Mock ResourceManager to indicate sufficient influence
        mock_resource_manager.can_afford_spending.return_value = True

        # Mock spending plan creation and execution
        mock_spending_plan = Mock(spec=SpendingPlan)
        mock_spending_plan.is_valid = True
        mock_resource_manager.create_spending_plan.return_value = mock_spending_plan

        mock_spending_result = Mock(spec=SpendingResult)
        mock_spending_result.success = True
        mock_resource_manager.execute_spending_plan.return_value = mock_spending_result

        # Act - use new interface with ResourceManager
        result = self.leadership_card.execute_primary_ability(
            "test_player",
            game_state=self.mock_game_state,
            player=test_player,
            resource_manager=mock_resource_manager,
            token_distribution={
                "tactic": 4,
                "fleet": 0,
                "strategy": 0,
            },  # 3 base + 1 from influence
            influence_to_spend=3,
        )

        # Assert - should succeed
        assert result.success is True
        assert test_player.command_sheet.tactic_pool == 4

        # Verify ResourceManager methods were called
        mock_resource_manager.can_afford_spending.assert_called_once()
        mock_resource_manager.create_spending_plan.assert_called_once()
        mock_resource_manager.execute_spending_plan.assert_called_once()

    def test_leadership_secondary_accepts_resource_manager_parameters(self) -> None:
        """Test that Leadership secondary ability accepts ResourceManager parameters without error."""
        # Arrange
        other_player = self._create_test_player("other_player")
        mock_resource_manager = Mock(spec=ResourceManager)

        # Mock ResourceManager to indicate insufficient influence
        mock_resource_manager.can_afford_spending.return_value = False
        mock_resource_manager.calculate_available_influence.return_value = 1

        # Act - use new interface with ResourceManager
        result = self.leadership_card.execute_secondary_ability(
            "other_player",
            game_state=self.mock_game_state,
            player=other_player,
            resource_manager=mock_resource_manager,
            token_distribution={"tactic": 1, "fleet": 0, "strategy": 0},
            influence_to_spend=3,
        )

        # Assert - should fail due to insufficient influence but not crash
        assert result.success is False
        assert "Insufficient influence" in result.error_message
        # Verify ResourceManager was called
        mock_resource_manager.can_afford_spending.assert_called_once_with(
            "other_player", influence_amount=3, for_voting=False
        )

    def test_leadership_backward_compatibility_still_works(self) -> None:
        """Test that Leadership maintains backward compatibility with existing interface."""
        # Arrange
        test_player = self._create_test_player()

        # Act - use old interface without ResourceManager
        result = self.leadership_card.execute_primary_ability(
            "test_player",
            game_state=self.mock_game_state,
            player=test_player,
            token_distribution={
                "tactic": 3,
                "fleet": 0,
                "strategy": 0,
            },  # Just base tokens
            planets_to_exhaust=[],  # No planets
            trade_goods_to_spend=0,  # No trade goods
        )

        # Assert - should work with old interface
        assert result.success is True
        assert test_player.command_sheet.tactic_pool == 3
