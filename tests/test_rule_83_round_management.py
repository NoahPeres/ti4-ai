"""Tests for Rule 83: STRATEGY CARD round management and card reset functionality.

This module tests the round lifecycle management, card redistribution to common play area,
and proper cleanup and state reset between rounds.

Requirements: 10.1, 10.2, 10.3, 10.4, 10.5
"""

from src.ti4.core.strategic_action import StrategicActionManager, StrategyCardType
from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator


class TestRoundManagement:
    """Test round management and card reset functionality."""

    def test_reset_round_returns_all_cards_to_common_play_area(self):
        """Test that round reset returns all strategy cards to common play area.

        Requirements: 10.1 - When a new round begins, all strategy cards SHALL be returned to the common play area
        """
        # Arrange
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Set up a game with assigned cards
        speaker_order = ["player1", "player2", "player3"]
        coordinator.start_strategy_phase_selection(speaker_order)

        # Players select cards
        coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.select_strategy_card("player2", StrategyCardType.DIPLOMACY)
        coordinator.select_strategy_card("player3", StrategyCardType.POLITICS)

        # Verify cards are assigned
        assert (
            coordinator.get_player_strategy_card("player1")
            == StrategyCardType.LEADERSHIP
        )
        assert (
            coordinator.get_player_strategy_card("player2")
            == StrategyCardType.DIPLOMACY
        )
        assert (
            coordinator.get_player_strategy_card("player3") == StrategyCardType.POLITICS
        )
        assert (
            len(coordinator.get_available_cards()) == 5
        )  # 8 total - 3 assigned = 5 available

        # Act
        coordinator.reset_round()

        # Assert
        # All cards should be returned to common play area
        assert len(coordinator.get_available_cards()) == 8  # All 8 cards available
        assert coordinator.get_player_strategy_card("player1") is None
        assert coordinator.get_player_strategy_card("player2") is None
        assert coordinator.get_player_strategy_card("player3") is None

    def test_reset_round_readies_all_cards_for_selection(self):
        """Test that round reset readies all cards and makes them available for selection.

        Requirements: 10.2 - When cards are reset, all cards SHALL be readied and available for selection
        """
        # Arrange
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Set up a game with assigned and exhausted cards
        speaker_order = ["player1", "player2", "player3"]
        coordinator.start_strategy_phase_selection(speaker_order)

        # Players select cards
        coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.select_strategy_card("player2", StrategyCardType.DIPLOMACY)
        coordinator.select_strategy_card("player3", StrategyCardType.POLITICS)

        # Exhaust the cards
        coordinator.exhaust_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.exhaust_strategy_card("player2", StrategyCardType.DIPLOMACY)

        # Verify cards are exhausted
        assert coordinator.is_strategy_card_exhausted(
            "player1", StrategyCardType.LEADERSHIP
        )
        assert coordinator.is_strategy_card_exhausted(
            "player2", StrategyCardType.DIPLOMACY
        )

        # Act
        coordinator.reset_round()

        # Assert
        # All cards should be available for selection in new round
        available_cards = coordinator.get_available_cards()
        assert len(available_cards) == 8  # All 8 cards available
        assert StrategyCardType.LEADERSHIP in available_cards
        assert StrategyCardType.DIPLOMACY in available_cards
        assert StrategyCardType.POLITICS in available_cards

    def test_reset_round_clears_player_assignments(self):
        """Test that round reset clears player assignments appropriately.

        Requirements: 10.3 - When round transitions occur, player assignments SHALL be cleared appropriately
        """
        # Arrange
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Set up a game with assigned cards
        speaker_order = ["player1", "player2", "player3"]
        coordinator.start_strategy_phase_selection(speaker_order)

        # Players select cards
        coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.select_strategy_card("player2", StrategyCardType.DIPLOMACY)
        coordinator.select_strategy_card("player3", StrategyCardType.POLITICS)

        # Verify assignments exist
        assignments = coordinator.get_player_strategy_card_assignments()
        assert len(assignments) == 3
        assert assignments["player1"] == StrategyCardType.LEADERSHIP
        assert assignments["player2"] == StrategyCardType.DIPLOMACY
        assert assignments["player3"] == StrategyCardType.POLITICS

        # Act
        coordinator.reset_round()

        # Assert
        # All player assignments should be cleared
        assignments_after_reset = coordinator.get_player_strategy_card_assignments()
        assert len(assignments_after_reset) == 0
        assert coordinator.get_player_strategy_card("player1") is None
        assert coordinator.get_player_strategy_card("player2") is None
        assert coordinator.get_player_strategy_card("player3") is None

    def test_reset_round_restores_initial_card_state(self):
        """Test that round reset restores initial card state.

        Requirements: 10.4 - If a round reset is requested, the system SHALL restore initial card state
        """
        # Arrange
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Set up a game with assigned cards and secondary ability participation
        speaker_order = ["player1", "player2", "player3"]
        coordinator.start_strategy_phase_selection(speaker_order)

        # Players select cards
        coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.select_strategy_card("player2", StrategyCardType.DIPLOMACY)
        coordinator.select_strategy_card("player3", StrategyCardType.POLITICS)

        # Exhaust some cards and use secondary abilities
        coordinator.exhaust_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.use_secondary_ability("player2", StrategyCardType.LEADERSHIP)
        coordinator.use_secondary_ability("player3", StrategyCardType.LEADERSHIP)

        # Verify state before reset
        assert coordinator.is_strategy_card_exhausted(
            "player1", StrategyCardType.LEADERSHIP
        )
        participants = coordinator.get_secondary_ability_participants(
            StrategyCardType.LEADERSHIP
        )
        assert len(participants) == 2
        assert "player2" in participants
        assert "player3" in participants

        # Act
        coordinator.reset_round()

        # Assert
        # All state should be restored to initial conditions
        # No cards should be assigned
        assert len(coordinator.get_available_cards()) == 8

        # No secondary ability participants should remain
        participants_after_reset = coordinator.get_secondary_ability_participants(
            StrategyCardType.LEADERSHIP
        )
        assert len(participants_after_reset) == 0

    def test_reset_round_maintains_proper_card_lifecycle_management(self):
        """Test that round reset maintains proper card lifecycle management.

        Requirements: 10.5 - When managing rounds, the system SHALL maintain proper card lifecycle management
        """
        # Arrange
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Set up initial game state
        speaker_order = ["player1", "player2", "player3"]
        coordinator.start_strategy_phase_selection(speaker_order)

        # Complete a full round cycle
        coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.select_strategy_card("player2", StrategyCardType.DIPLOMACY)
        coordinator.select_strategy_card("player3", StrategyCardType.POLITICS)

        # Use cards during the round
        coordinator.exhaust_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.use_secondary_ability("player2", StrategyCardType.LEADERSHIP)

        # Verify round is complete
        assert coordinator.is_strategy_phase_complete()

        # Act - Reset for new round
        coordinator.reset_round()

        # Assert - System should be ready for new round
        # Strategy phase should be inactive (ready to start new selection)
        assert not coordinator._strategy_phase_active

        # All cards should be available for new selection
        available_cards = coordinator.get_available_cards()
        assert len(available_cards) == 8

        # Should be able to start a new strategy phase
        new_round_result = coordinator.start_strategy_phase_selection(speaker_order)
        assert new_round_result.success

        # Should be able to select cards again
        selection_result = coordinator.select_strategy_card(
            "player1", StrategyCardType.TECHNOLOGY
        )
        assert selection_result.success
        assert (
            coordinator.get_player_strategy_card("player1")
            == StrategyCardType.TECHNOLOGY
        )
