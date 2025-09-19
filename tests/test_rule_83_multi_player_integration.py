"""Integration tests for Rule 83: Multi-Player Game Support.

This module tests the complete multi-player workflow integration to ensure
all components work together seamlessly.

Requirements tested:
- 7.1: Games with fewer than 8 players leave some strategy cards unselected
- 7.2: System handles any number of players from 3-8
- 7.3: System supports flexible player ordering
- 7.4: System adapts card availability based on player count changes
- 7.5: Each player has independent card selection
"""

from src.ti4.core.strategic_action import StrategicActionManager, StrategyCardType
from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator


class TestRule83MultiPlayerIntegration:
    """Integration tests for complete multi-player workflow."""

    def test_complete_four_player_game_workflow(self):
        """Test complete workflow for a 4-player game.

        Requirements: 7.1, 7.2, 7.3, 7.5 - Complete multi-player support
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Setup 4-player game
        speaker_order = ["alice", "bob", "charlie", "diana"]

        # Verify player count validation
        assert coordinator.is_valid_player_count(4) is True
        assert coordinator.get_minimum_player_count() == 3
        assert coordinator.get_maximum_player_count() == 8

        # Start strategy phase
        result = coordinator.start_strategy_phase_selection(speaker_order)
        assert result.success is True
        assert result.current_selecting_player == "alice"
        assert len(result.available_cards) == 8

        # Verify initial state
        assert coordinator.get_player_count() == 4
        assert coordinator.get_expected_unselected_cards_count() == 4
        assert coordinator.get_speaker_order() == speaker_order
        assert coordinator.get_current_selecting_player() == "alice"

        # Complete card selection workflow
        selections = [
            ("alice", StrategyCardType.LEADERSHIP),
            ("bob", StrategyCardType.WARFARE),
            ("charlie", StrategyCardType.TECHNOLOGY),
            ("diana", StrategyCardType.IMPERIAL),
        ]

        for i, (player, card) in enumerate(selections):
            # Verify it's the correct player's turn
            assert coordinator.get_current_selecting_player() == player

            # Select card
            result = coordinator.select_strategy_card(player, card)
            assert result.success is True
            assert result.player_id == player
            assert result.strategy_card == card

            # Verify card is assigned to player
            assert coordinator.get_player_strategy_card(player) == card

            # Verify next player (if not last)
            if i < len(selections) - 1:
                next_player = selections[i + 1][0]
                assert result.next_selecting_player == next_player
            else:
                assert result.next_selecting_player is None

        # Verify phase completion
        assert coordinator.is_strategy_phase_complete() is True
        assert coordinator.get_current_selecting_player() is None

        # Verify unselected cards
        unselected_cards = coordinator.get_available_cards()
        assert len(unselected_cards) == 4
        selected_cards = {card for _, card in selections}
        assert set(unselected_cards).isdisjoint(selected_cards)

        # Verify initiative order
        initiative_order = coordinator.get_action_phase_initiative_order()
        expected_order = [
            "alice",
            "bob",
            "charlie",
            "diana",
        ]  # Based on card initiative numbers: 1, 6, 7, 8
        assert initiative_order == expected_order

    def test_game_reset_and_different_player_count(self):
        """Test resetting game and starting with different player count.

        Requirements: 7.4 - System adapts card availability based on player count changes
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # First game: 3 players
        first_order = ["p1", "p2", "p3"]
        coordinator.start_strategy_phase_selection(first_order)
        coordinator.select_strategy_card("p1", StrategyCardType.LEADERSHIP)
        coordinator.select_strategy_card("p2", StrategyCardType.WARFARE)
        coordinator.select_strategy_card("p3", StrategyCardType.TECHNOLOGY)

        # Verify first game state
        assert coordinator.get_player_count() == 3
        assert len(coordinator.get_available_cards()) == 5
        assert coordinator.is_strategy_phase_complete() is True

        # Reset for new game
        coordinator.reset_strategy_phase()

        # Verify reset state
        assert coordinator.get_player_count() == 0
        assert len(coordinator.get_available_cards()) == 8
        assert coordinator.is_strategy_phase_complete() is False
        assert coordinator.get_current_selecting_player() is None

        # Second game: 6 players
        second_order = [f"player{i}" for i in range(1, 7)]
        result = coordinator.start_strategy_phase_selection(second_order)
        assert result.success is True

        # Verify new game state
        assert coordinator.get_player_count() == 6
        assert coordinator.get_expected_unselected_cards_count() == 2
        assert coordinator.get_speaker_order() == second_order

        # Complete second game
        cards = list(StrategyCardType)
        for i, player in enumerate(second_order):
            coordinator.select_strategy_card(player, cards[i])

        # Verify second game completion
        assert coordinator.is_strategy_phase_complete() is True
        assert len(coordinator.get_available_cards()) == 2

    def test_edge_case_maximum_players(self):
        """Test edge case with maximum number of players (8).

        Requirements: 7.2 - System handles any number of players from 3-8
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # 8-player game (maximum)
        max_players = [f"player{i}" for i in range(1, 9)]
        result = coordinator.start_strategy_phase_selection(max_players)
        assert result.success is True

        # Verify maximum player state
        assert coordinator.get_player_count() == 8
        assert coordinator.get_expected_unselected_cards_count() == 0

        # All players select cards
        cards = list(StrategyCardType)
        for i, player in enumerate(max_players):
            result = coordinator.select_strategy_card(player, cards[i])
            assert result.success is True

        # Verify all cards are selected
        assert coordinator.is_strategy_phase_complete() is True
        assert len(coordinator.get_available_cards()) == 0

        # Verify initiative order includes all players
        initiative_order = coordinator.get_action_phase_initiative_order()
        assert len(initiative_order) == 8
        assert set(initiative_order) == set(max_players)

    def test_edge_case_minimum_players(self):
        """Test edge case with minimum number of players (3).

        Requirements: 7.2 - System handles any number of players from 3-8
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # 3-player game (minimum)
        min_players = ["alpha", "beta", "gamma"]
        result = coordinator.start_strategy_phase_selection(min_players)
        assert result.success is True

        # Verify minimum player state
        assert coordinator.get_player_count() == 3
        assert coordinator.get_expected_unselected_cards_count() == 5

        # All players select cards
        selected_cards = [
            StrategyCardType.LEADERSHIP,
            StrategyCardType.WARFARE,
            StrategyCardType.TECHNOLOGY,
        ]
        for i, player in enumerate(min_players):
            result = coordinator.select_strategy_card(player, selected_cards[i])
            assert result.success is True

        # Verify 5 cards remain unselected
        assert coordinator.is_strategy_phase_complete() is True
        assert len(coordinator.get_available_cards()) == 5

        # Verify initiative order includes all players
        initiative_order = coordinator.get_action_phase_initiative_order()
        assert len(initiative_order) == 3
        assert set(initiative_order) == set(min_players)

    def test_flexible_speaker_order_with_initiative_calculation(self):
        """Test that flexible speaker order works correctly with initiative calculation.

        Requirements: 7.3 - System supports flexible player ordering
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Use non-alphabetical speaker order
        speaker_order = ["zulu", "alpha", "yankee", "bravo", "charlie"]
        result = coordinator.start_strategy_phase_selection(speaker_order)
        assert result.success is True

        # Players select cards in speaker order
        selections = [
            ("zulu", StrategyCardType.IMPERIAL),  # Initiative 8
            ("alpha", StrategyCardType.LEADERSHIP),  # Initiative 1
            ("yankee", StrategyCardType.WARFARE),  # Initiative 6
            ("bravo", StrategyCardType.DIPLOMACY),  # Initiative 2
            ("charlie", StrategyCardType.POLITICS),  # Initiative 3
        ]

        for player, card in selections:
            result = coordinator.select_strategy_card(player, card)
            assert result.success is True

        # Verify initiative order is based on card numbers, not speaker order
        initiative_order = coordinator.get_action_phase_initiative_order()
        expected_initiative_order = ["alpha", "bravo", "charlie", "yankee", "zulu"]
        assert initiative_order == expected_initiative_order

        # Verify speaker order is preserved separately
        assert coordinator.get_speaker_order() == speaker_order

    def test_independent_player_selection_validation(self):
        """Test that each player's selection is truly independent.

        Requirements: 7.5 - Each player has independent card selection
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # 5-player game
        players = ["p1", "p2", "p3", "p4", "p5"]
        coordinator.start_strategy_phase_selection(players)

        # Each player selects different cards
        selections = [
            ("p1", StrategyCardType.LEADERSHIP),
            ("p2", StrategyCardType.DIPLOMACY),
            ("p3", StrategyCardType.POLITICS),
            ("p4", StrategyCardType.CONSTRUCTION),
            ("p5", StrategyCardType.TRADE),
        ]

        for player, card in selections:
            coordinator.select_strategy_card(player, card)

        # Verify each player has their own card
        for player, expected_card in selections:
            actual_card = coordinator.get_player_strategy_card(player)
            assert actual_card == expected_card

            # Verify no other player has this card
            for other_player, _ in selections:
                if other_player != player:
                    other_card = coordinator.get_player_strategy_card(other_player)
                    assert other_card != expected_card

        # Verify 3 cards remain unselected
        unselected_cards = coordinator.get_available_cards()
        assert len(unselected_cards) == 3
        expected_unselected = {
            StrategyCardType.WARFARE,
            StrategyCardType.TECHNOLOGY,
            StrategyCardType.IMPERIAL,
        }
        assert set(unselected_cards) == expected_unselected
