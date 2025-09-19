"""Tests for Rule 83: Player Count Validation and Enhanced Multi-Player Support.

This module tests enhanced player count validation and multi-player game support
functionality that ensures proper handling of edge cases and validation.

Requirements tested:
- 7.2: System handles any number of players from 3-8
- 7.4: System adapts card availability based on player count changes
- 9.1, 9.2: Comprehensive error handling and validation
"""

from src.ti4.core.strategic_action import StrategicActionManager, StrategyCardType
from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator


class TestRule83PlayerCountValidation:
    """Test player count validation and enhanced multi-player support."""

    def test_reject_empty_speaker_order(self):
        """Test that empty speaker order is rejected.

        Requirements: 7.2, 9.1 - System validates player count, provides error messages
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Empty speaker order should be rejected
        result = coordinator.start_strategy_phase_selection([])
        assert result.success is False
        assert "empty" in result.error_message.lower()

    def test_reject_single_player_game(self):
        """Test that single player games are rejected.

        Requirements: 7.2 - System handles any number of players from 3-8 (minimum 3)
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Single player should be rejected
        result = coordinator.start_strategy_phase_selection(["player1"])
        assert result.success is False
        assert "minimum" in result.error_message.lower() or "3" in result.error_message

    def test_reject_two_player_game(self):
        """Test that two player games are rejected.

        Requirements: 7.2 - System handles any number of players from 3-8 (minimum 3)
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Two players should be rejected
        result = coordinator.start_strategy_phase_selection(["player1", "player2"])
        assert result.success is False
        assert "minimum" in result.error_message.lower() or "3" in result.error_message

    def test_reject_nine_player_game(self):
        """Test that games with more than 8 players are rejected.

        Requirements: 7.2 - System handles any number of players from 3-8 (maximum 8)
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Nine players should be rejected
        nine_players = [f"player{i}" for i in range(1, 10)]
        result = coordinator.start_strategy_phase_selection(nine_players)
        assert result.success is False
        assert "maximum" in result.error_message.lower() or "8" in result.error_message

    def test_duplicate_player_ids_rejected(self):
        """Test that duplicate player IDs in speaker order are rejected.

        Requirements: 7.5, 9.1 - Each player has independent selection, input validation
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Duplicate player IDs should be rejected
        duplicate_players = ["player1", "player2", "player1", "player3"]
        result = coordinator.start_strategy_phase_selection(duplicate_players)
        assert result.success is False
        assert "duplicate" in result.error_message.lower()

    def test_empty_player_id_in_speaker_order_rejected(self):
        """Test that empty player IDs in speaker order are rejected.

        Requirements: 9.1 - Comprehensive input validation
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Empty player ID should be rejected
        invalid_players = ["player1", "", "player3"]
        result = coordinator.start_strategy_phase_selection(invalid_players)
        assert result.success is False
        assert (
            "empty" in result.error_message.lower()
            or "invalid" in result.error_message.lower()
        )

    def test_none_player_id_in_speaker_order_rejected(self):
        """Test that None player IDs in speaker order are rejected.

        Requirements: 9.1 - Comprehensive input validation
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # None player ID should be rejected
        invalid_players = ["player1", None, "player3"]
        result = coordinator.start_strategy_phase_selection(invalid_players)
        assert result.success is False
        assert (
            "invalid" in result.error_message.lower()
            or "none" in result.error_message.lower()
        )

    def test_get_player_count_information(self):
        """Test that coordinator provides player count information.

        Requirements: 7.4 - System adapts card availability based on player count
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Start with 5 players
        speaker_order = [f"player{i}" for i in range(1, 6)]
        result = coordinator.start_strategy_phase_selection(speaker_order)
        assert result.success is True

        # Should be able to get player count
        player_count = coordinator.get_player_count()
        assert player_count == 5

        # Should be able to get expected unselected cards count
        expected_unselected = coordinator.get_expected_unselected_cards_count()
        assert expected_unselected == 3  # 8 - 5 = 3

    def test_get_speaker_order_information(self):
        """Test that coordinator provides speaker order information.

        Requirements: 7.3 - System supports flexible player ordering
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Start with specific speaker order
        original_order = ["alice", "bob", "charlie", "diana"]
        result = coordinator.start_strategy_phase_selection(original_order)
        assert result.success is True

        # Should be able to retrieve speaker order
        retrieved_order = coordinator.get_speaker_order()
        assert retrieved_order == original_order

        # Should be able to get current selecting player
        current_player = coordinator.get_current_selecting_player()
        assert current_player == "alice"

    def test_reset_strategy_phase_for_new_game(self):
        """Test that strategy phase can be reset for a new game with different player count.

        Requirements: 7.4 - System adapts card availability based on player count changes
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Start first game with 4 players
        first_order = ["p1", "p2", "p3", "p4"]
        coordinator.start_strategy_phase_selection(first_order)
        coordinator.select_strategy_card("p1", StrategyCardType.LEADERSHIP)
        coordinator.select_strategy_card("p2", StrategyCardType.WARFARE)

        # Reset and start new game with 6 players
        coordinator.reset_strategy_phase()
        second_order = [f"player{i}" for i in range(1, 7)]
        result = coordinator.start_strategy_phase_selection(second_order)
        assert result.success is True

        # Should have all cards available again
        available_cards = coordinator.get_available_cards()
        assert len(available_cards) == 8

        # Should have new player count
        assert coordinator.get_player_count() == 6

    def test_validate_player_count_bounds(self):
        """Test explicit player count validation methods.

        Requirements: 7.2 - System handles any number of players from 3-8
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test validation methods
        assert coordinator.is_valid_player_count(3) is True
        assert coordinator.is_valid_player_count(4) is True
        assert coordinator.is_valid_player_count(5) is True
        assert coordinator.is_valid_player_count(6) is True
        assert coordinator.is_valid_player_count(7) is True
        assert coordinator.is_valid_player_count(8) is True

        # Invalid counts
        assert coordinator.is_valid_player_count(0) is False
        assert coordinator.is_valid_player_count(1) is False
        assert coordinator.is_valid_player_count(2) is False
        assert coordinator.is_valid_player_count(9) is False
        assert coordinator.is_valid_player_count(10) is False

    def test_get_minimum_maximum_player_counts(self):
        """Test that coordinator provides min/max player count constants.

        Requirements: 7.2 - System handles any number of players from 3-8
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Should provide constants
        assert coordinator.get_minimum_player_count() == 3
        assert coordinator.get_maximum_player_count() == 8
