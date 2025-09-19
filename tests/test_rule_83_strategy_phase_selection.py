"""Tests for Rule 83: Strategy Phase Card Selection Mechanics.

This module tests the strategy phase card selection workflow that integrates
with existing phase management and implements speaker order-based selection.

Requirements tested:
- 2.1: Players can select cards in speaker order during strategy phase
- 2.2: Selected cards move from common play area to player's play area
- 2.3: Selected cards are no longer available to other players
- 2.4: Invalid card selections are rejected
- 2.5: Strategy phase completes when all players have selected cards
"""


from src.ti4.core.strategic_action import StrategicActionManager, StrategyCardType


class TestRule83StrategyPhaseCardSelection:
    """Test strategy phase card selection mechanics."""

    def test_strategy_phase_card_selection_workflow_initialization(self):
        """Test that strategy phase card selection workflow can be initialized.

        Requirements: 2.1 - Players can select cards in speaker order during strategy phase
        """
        # This will fail initially - RED phase
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test that we can start a strategy phase card selection workflow
        result = coordinator.start_strategy_phase_selection(["player1", "player2", "player3"])

        assert result.success is True
        assert result.current_selecting_player == "player1"  # First player in speaker order
        assert len(result.available_cards) == 8  # All 8 strategy cards available initially

    def test_get_available_cards_returns_unselected_cards(self):
        """Test that available cards returns only unselected strategy cards.

        Requirements: 2.3 - Selected cards are no longer available to other players
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Initially all cards should be available
        available_cards = coordinator.get_available_cards()
        assert len(available_cards) == 8
        assert StrategyCardType.LEADERSHIP in available_cards
        assert StrategyCardType.TECHNOLOGY in available_cards

        # After assigning a card, it should no longer be available
        coordinator.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)
        available_cards = coordinator.get_available_cards()
        assert len(available_cards) == 7
        assert StrategyCardType.LEADERSHIP not in available_cards
        assert StrategyCardType.TECHNOLOGY in available_cards

    def test_select_card_in_speaker_order(self):
        """Test that cards can only be selected in speaker order.

        Requirements: 2.1 - Players can select cards in speaker order during strategy phase
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Start selection with specific speaker order
        speaker_order = ["player1", "player2", "player3"]
        coordinator.start_strategy_phase_selection(speaker_order)

        # Player 1 should be able to select (first in order)
        result = coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        assert result.success is True

        # Player 3 should not be able to select out of turn
        result = coordinator.select_strategy_card("player3", StrategyCardType.WARFARE)
        assert result.success is False
        assert "not your turn" in result.error_message.lower()

        # Player 2 should now be able to select (next in order)
        result = coordinator.select_strategy_card("player2", StrategyCardType.WARFARE)
        assert result.success is True

    def test_reject_selection_of_unavailable_card(self):
        """Test that selection of unavailable cards is rejected.

        Requirements: 2.4 - Invalid card selections are rejected
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        speaker_order = ["player1", "player2", "player3"]
        coordinator.start_strategy_phase_selection(speaker_order)

        # Player 1 selects Leadership
        result = coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        assert result.success is True

        # Player 2 tries to select the same card - should be rejected
        result = coordinator.select_strategy_card("player2", StrategyCardType.LEADERSHIP)
        assert result.success is False
        assert "not available" in result.error_message.lower()

    def test_strategy_phase_completion(self):
        """Test that strategy phase completes when all players have selected cards.

        Requirements: 2.5 - Strategy phase completes when all players have selected cards
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        speaker_order = ["player1", "player2", "player3"]
        coordinator.start_strategy_phase_selection(speaker_order)

        # Initially not complete
        assert coordinator.is_strategy_phase_complete() is False

        # After first selection, still not complete
        coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        assert coordinator.is_strategy_phase_complete() is False

        # After second selection, still not complete
        coordinator.select_strategy_card("player2", StrategyCardType.WARFARE)
        assert coordinator.is_strategy_phase_complete() is False

        # After all players have selected, should be complete
        coordinator.select_strategy_card("player3", StrategyCardType.TECHNOLOGY)
        assert coordinator.is_strategy_phase_complete() is True

    def test_card_moves_to_player_area_after_selection(self):
        """Test that selected cards move to player's play area.

        Requirements: 2.2 - Selected cards move from common play area to player's play area
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        speaker_order = ["player1", "player2", "player3"]
        coordinator.start_strategy_phase_selection(speaker_order)

        # Initially player has no card
        player_card = coordinator.get_player_strategy_card("player1")
        assert player_card is None

        # After selection, card should be in player's area
        coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        player_card = coordinator.get_player_strategy_card("player1")
        assert player_card == StrategyCardType.LEADERSHIP

    def test_multiple_player_game_support(self):
        """Test that card selection works with different player counts.

        Requirements: 7.1, 7.2 - Support games with 3-8 players, unselected cards remain
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test with 3 players (5 cards should remain unselected)
        speaker_order = ["player1", "player2", "player3"]
        coordinator.start_strategy_phase_selection(speaker_order)

        coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.select_strategy_card("player2", StrategyCardType.WARFARE)
        coordinator.select_strategy_card("player3", StrategyCardType.TECHNOLOGY)

        # Should be complete even with unselected cards
        assert coordinator.is_strategy_phase_complete() is True

        # 5 cards should remain available (unselected)
        available_cards = coordinator.get_available_cards()
        assert len(available_cards) == 5

    def test_input_validation_for_card_selection(self):
        """Test input validation for card selection operations.

        Requirements: 9.1, 9.2 - Comprehensive error handling and validation
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test empty player ID
        result = coordinator.select_strategy_card("", StrategyCardType.LEADERSHIP)
        assert result.success is False
        assert "player id" in result.error_message.lower()

        # Test None card
        result = coordinator.select_strategy_card("player1", None)
        assert result.success is False
        assert "strategy card" in result.error_message.lower()

        # Test selection without starting phase
        result = coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        assert result.success is False
        assert "strategy phase not started" in result.error_message.lower()
