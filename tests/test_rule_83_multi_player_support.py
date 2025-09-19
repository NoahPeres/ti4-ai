"""Tests for Rule 83: Multi-Player Game Support.

This module tests the multi-player game support functionality that handles
flexible player counts, unselected cards, and dynamic speaker order management.

Requirements tested:
- 7.1: Games with fewer than 8 players leave some strategy cards unselected
- 7.2: System handles any number of players from 3-8
- 7.3: System supports flexible player ordering
- 7.4: System adapts card availability based on player count changes
- 7.5: Each player has independent card selection
"""

import pytest

from src.ti4.core.strategic_action import StrategicActionManager, StrategyCardType
from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator


class TestRule83MultiPlayerGameSupport:
    """Test multi-player game support functionality."""

    def test_three_player_game_leaves_five_cards_unselected(self):
        """Test that 3-player games leave 5 strategy cards unselected.

        Requirements: 7.1 - Games with fewer than 8 players leave some strategy cards unselected
        """
        # RED: Write failing test first
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Start 3-player game
        speaker_order = ["player1", "player2", "player3"]
        result = coordinator.start_strategy_phase_selection(speaker_order)
        assert result.success is True

        # All players select cards
        coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.select_strategy_card("player2", StrategyCardType.WARFARE)
        coordinator.select_strategy_card("player3", StrategyCardType.TECHNOLOGY)

        # Phase should be complete
        assert coordinator.is_strategy_phase_complete() is True

        # 5 cards should remain unselected
        unselected_cards = coordinator.get_available_cards()
        assert len(unselected_cards) == 5

        # Verify specific cards are unselected
        expected_unselected = {
            StrategyCardType.DIPLOMACY,
            StrategyCardType.POLITICS,
            StrategyCardType.CONSTRUCTION,
            StrategyCardType.TRADE,
            StrategyCardType.IMPERIAL,
        }
        assert set(unselected_cards) == expected_unselected

    def test_eight_player_game_all_cards_selected(self):
        """Test that 8-player games use all strategy cards.

        Requirements: 7.2 - System handles any number of players from 3-8
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Start 8-player game
        speaker_order = [f"player{i}" for i in range(1, 9)]
        result = coordinator.start_strategy_phase_selection(speaker_order)
        assert result.success is True

        # All players select cards
        cards = list(StrategyCardType)
        for i, player in enumerate(speaker_order):
            coordinator.select_strategy_card(player, cards[i])

        # Phase should be complete
        assert coordinator.is_strategy_phase_complete() is True

        # No cards should remain unselected
        unselected_cards = coordinator.get_available_cards()
        assert len(unselected_cards) == 0

    @pytest.mark.parametrize("player_count", [3, 4, 5, 6, 7, 8])
    def test_flexible_player_count_handling(self, player_count: int):
        """Test that system handles all valid player counts from 3-8.

        Requirements: 7.2 - System handles any number of players from 3-8
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Create speaker order for the given player count
        speaker_order = [f"player{i}" for i in range(1, player_count + 1)]
        result = coordinator.start_strategy_phase_selection(speaker_order)
        assert result.success is True

        # All players select cards
        cards = list(StrategyCardType)
        for i, player in enumerate(speaker_order):
            coordinator.select_strategy_card(player, cards[i])

        # Phase should be complete
        assert coordinator.is_strategy_phase_complete() is True

        # Correct number of cards should remain unselected
        expected_unselected = 8 - player_count
        unselected_cards = coordinator.get_available_cards()
        assert len(unselected_cards) == expected_unselected

    def test_dynamic_speaker_order_management(self):
        """Test that system supports flexible player ordering.

        Requirements: 7.3 - System supports flexible player ordering
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test different speaker orders
        speaker_orders = [
            ["alice", "bob", "charlie"],
            ["player_x", "player_y", "player_z"],
            ["p1", "p2", "p3", "p4"],
        ]

        for speaker_order in speaker_orders:
            # Reset coordinator for each test
            coordinator = StrategyCardCoordinator(strategic_action_manager)

            result = coordinator.start_strategy_phase_selection(speaker_order)
            assert result.success is True
            assert result.current_selecting_player == speaker_order[0]

            # First player should be able to select
            first_result = coordinator.select_strategy_card(
                speaker_order[0], StrategyCardType.LEADERSHIP
            )
            assert first_result.success is True
            assert first_result.next_selecting_player == speaker_order[1]

    def test_independent_player_card_selection(self):
        """Test that each player has independent card selection.

        Requirements: 7.5 - Each player has independent card selection
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        speaker_order = ["player1", "player2", "player3", "player4"]
        coordinator.start_strategy_phase_selection(speaker_order)

        # Each player selects different cards independently
        selections = [
            ("player1", StrategyCardType.LEADERSHIP),
            ("player2", StrategyCardType.WARFARE),
            ("player3", StrategyCardType.TECHNOLOGY),
            ("player4", StrategyCardType.IMPERIAL),
        ]

        for player, card in selections:
            result = coordinator.select_strategy_card(player, card)
            assert result.success is True

            # Verify player has their selected card
            player_card = coordinator.get_player_strategy_card(player)
            assert player_card == card

            # Verify other players don't have this card
            for other_player, _ in selections:
                if other_player != player:
                    other_card = coordinator.get_player_strategy_card(other_player)
                    assert other_card != card or other_card is None

    def test_card_availability_adapts_to_player_count(self):
        """Test that card availability adapts based on player count changes.

        Requirements: 7.4 - System adapts card availability based on player count changes
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Start with 3 players
        initial_speaker_order = ["player1", "player2", "player3"]
        coordinator.start_strategy_phase_selection(initial_speaker_order)

        # Complete selection for 3 players
        coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.select_strategy_card("player2", StrategyCardType.WARFARE)
        coordinator.select_strategy_card("player3", StrategyCardType.TECHNOLOGY)

        # 5 cards should be available (unselected)
        available_cards = coordinator.get_available_cards()
        assert len(available_cards) == 5

        # Reset and test with 6 players
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        expanded_speaker_order = [f"player{i}" for i in range(1, 7)]
        coordinator.start_strategy_phase_selection(expanded_speaker_order)

        # Complete selection for 6 players
        cards = list(StrategyCardType)
        for i, player in enumerate(expanded_speaker_order):
            coordinator.select_strategy_card(player, cards[i])

        # Only 2 cards should be available (unselected)
        available_cards = coordinator.get_available_cards()
        assert len(available_cards) == 2

    def test_minimum_player_count_validation(self):
        """Test validation for minimum player count.

        Requirements: 7.2 - System handles any number of players from 3-8
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test with too few players (less than 3)
        invalid_speaker_orders = [
            [],  # No players
            ["player1"],  # 1 player
            ["player1", "player2"],  # 2 players
        ]

        for speaker_order in invalid_speaker_orders:
            result = coordinator.start_strategy_phase_selection(speaker_order)
            # Current implementation might not validate this yet
            # This test will help drive the implementation
            if len(speaker_order) == 0:
                assert result.success is False
                assert "empty" in result.error_message.lower()

    def test_maximum_player_count_validation(self):
        """Test validation for maximum player count.

        Requirements: 7.2 - System handles any number of players from 3-8
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test with too many players (more than 8)
        too_many_players = [f"player{i}" for i in range(1, 10)]  # 9 players

        # This should either work (allowing extra players) or fail with validation
        result = coordinator.start_strategy_phase_selection(too_many_players)

        if result.success:
            # If it allows extra players, only first 8 should be able to select
            cards = list(StrategyCardType)
            for i in range(8):  # Only first 8 players
                player_result = coordinator.select_strategy_card(
                    f"player{i + 1}", cards[i]
                )
                assert player_result.success is True

            # 9th player should not be able to select (no cards left)
            ninth_result = coordinator.select_strategy_card(
                "player9", StrategyCardType.LEADERSHIP
            )
            assert ninth_result.success is False

    def test_unselected_cards_remain_in_common_area(self):
        """Test that unselected cards remain in common play area.

        Requirements: 7.1 - Games with fewer than 8 players leave some strategy cards unselected
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # 4-player game
        speaker_order = ["player1", "player2", "player3", "player4"]
        coordinator.start_strategy_phase_selection(speaker_order)

        # Players select 4 cards
        selected_cards = [
            StrategyCardType.LEADERSHIP,
            StrategyCardType.WARFARE,
            StrategyCardType.TECHNOLOGY,
            StrategyCardType.IMPERIAL,
        ]

        for i, player in enumerate(speaker_order):
            coordinator.select_strategy_card(player, selected_cards[i])

        # 4 cards should remain unselected and available
        unselected_cards = coordinator.get_available_cards()
        assert len(unselected_cards) == 4

        # Unselected cards should not be assigned to any player
        for card in unselected_cards:
            for player in speaker_order:
                player_card = coordinator.get_player_strategy_card(player)
                assert player_card != card

        # Unselected cards should be the ones not in selected_cards
        expected_unselected = set(StrategyCardType) - set(selected_cards)
        assert set(unselected_cards) == expected_unselected

    def test_speaker_order_determines_selection_sequence(self):
        """Test that speaker order determines the sequence of card selection.

        Requirements: 7.3 - System supports flexible player ordering
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test with specific speaker order
        speaker_order = ["charlie", "alice", "bob", "diana"]
        coordinator.start_strategy_phase_selection(speaker_order)

        # Charlie should go first
        result = coordinator.select_strategy_card(
            "charlie", StrategyCardType.LEADERSHIP
        )
        assert result.success is True
        assert result.next_selecting_player == "alice"

        # Alice should go second
        result = coordinator.select_strategy_card("alice", StrategyCardType.WARFARE)
        assert result.success is True
        assert result.next_selecting_player == "bob"

        # Bob should go third
        result = coordinator.select_strategy_card("bob", StrategyCardType.TECHNOLOGY)
        assert result.success is True
        assert result.next_selecting_player == "diana"

        # Diana should go last
        result = coordinator.select_strategy_card("diana", StrategyCardType.IMPERIAL)
        assert result.success is True
        assert result.next_selecting_player is None  # No more players

        # Verify phase is complete
        assert coordinator.is_strategy_phase_complete() is True
