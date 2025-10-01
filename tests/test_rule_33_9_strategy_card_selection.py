"""Tests for Rule 33.9: Strategy Card Selection after Elimination.

This module tests the strategy card selection mechanics when player count
drops from 5+ to 4 or fewer due to elimination.

LRR Reference: Rule 33.9 - If the game drops from five or more players to four or fewer
players due to elimination, players still only select one strategy card during the strategy phase.
"""

import pytest

from ti4.core.constants import Faction
from ti4.core.game_controller import GameController
from ti4.core.player import Player
from ti4.core.validation import ValidationError


class TestRule339StrategyCardSelection:
    """Test Rule 33.9: Strategy Card Selection after elimination."""

    def test_rule_33_9_five_to_four_players_single_card_selection(self) -> None:
        """Test Rule 33.9: When game drops from 5 to 4 players, each player still selects only 1 card."""
        # Setup 5-player game
        players = [
            Player("player1", Faction.SOL),
            Player("player2", Faction.HACAN),
            Player("player3", Faction.XXCHA),
            Player("player4", Faction.YSSARIL),
            Player("player5", Faction.NAALU),
        ]
        controller = GameController(players)

        # Verify initial state: 5 players, each should get 1 card (8 cards / 5 players = 1 card each)
        initial_players = controller.get_turn_order()
        assert len(initial_players) == 5

        # Test behavior: with 5 players, available strategy cards should be managed appropriately
        available_cards = controller.get_available_strategy_cards()
        assert (
            len(available_cards) == 8
        )  # All 8 strategy cards should be available initially

        # Simulate player elimination by creating a new controller with 4 players
        # This represents the game state after elimination
        remaining_players = players[:-1]  # Remove last player
        controller_after_elimination = GameController.with_remaining_players(
            controller, remaining_players
        )

        # Rule 33.9: Even with 4 players, each should still get only 1 card
        # (not 2 cards as would be normal for a 4-player game)
        # Test behavior: verify that strategy card selection still works with elimination rules
        remaining_players = controller_after_elimination.get_turn_order()
        assert len(remaining_players) == 4

        # Available cards should still be managed according to Rule 33.9
        available_cards_after = (
            controller_after_elimination.get_available_strategy_cards()
        )
        assert len(available_cards_after) == 8  # All cards still available

    def test_rule_33_9_six_to_four_players_single_card_selection(self) -> None:
        """Test Rule 33.9: When game drops from 6 to 4 players, each player still selects only 1 card."""
        # Setup 6-player game
        players = [
            Player("player1", Faction.SOL),
            Player("player2", Faction.HACAN),
            Player("player3", Faction.XXCHA),
            Player("player4", Faction.YSSARIL),
            Player("player5", Faction.NAALU),
            Player("player6", Faction.BARONY),
        ]
        controller = GameController(players)

        # Verify initial state: 6 players, each should get 1 card (8 cards / 6 players = 1 card each)
        initial_players = controller.get_turn_order()
        assert len(initial_players) == 6

        # Test behavior: with 6 players, available strategy cards should be managed appropriately
        available_cards = controller.get_available_strategy_cards()
        assert (
            len(available_cards) == 8
        )  # All 8 strategy cards should be available initially

        # Simulate elimination of 2 players by creating a new controller with 4 players
        remaining_players = players[:-2]  # Remove last 2 players
        controller_after_elimination = GameController.with_remaining_players(
            controller, remaining_players
        )

        # Rule 33.9: Even with 4 players, each should still get only 1 card
        # Test behavior: verify that strategy card selection still works with elimination rules
        remaining_players = controller_after_elimination.get_turn_order()
        assert len(remaining_players) == 4

        # Available cards should still be managed according to Rule 33.9
        available_cards_after = (
            controller_after_elimination.get_available_strategy_cards()
        )
        assert len(available_cards_after) == 8  # All cards still available

    def test_rule_33_9_eight_to_three_players_single_card_selection(self) -> None:
        """Test Rule 33.9: When game drops from 8 to 3 players, each player still selects only 1 card."""
        # Setup 8-player game
        players = [
            Player("player1", Faction.SOL),
            Player("player2", Faction.HACAN),
            Player("player3", Faction.XXCHA),
            Player("player4", Faction.YSSARIL),
            Player("player5", Faction.NAALU),
            Player("player6", Faction.BARONY),
            Player("player7", Faction.SAAR),
            Player("player8", Faction.MUAAT),
        ]
        controller = GameController(players)

        # Verify initial state: 8 players, each should get 1 card (8 cards / 8 players = 1 card each)
        initial_players = controller.get_turn_order()
        assert len(initial_players) == 8

        # Test behavior: with 8 players, available strategy cards should be managed appropriately
        available_cards = controller.get_available_strategy_cards()
        assert (
            len(available_cards) == 8
        )  # All 8 strategy cards should be available initially

        # Simulate elimination of 5 players by creating a new controller with 3 players
        remaining_players = players[:3]  # Keep only first 3 players
        controller_after_elimination = GameController.with_remaining_players(
            controller, remaining_players
        )

        # Rule 33.9: Even with 3 players, each should still get only 1 card
        # (not 2 cards as would be normal for a 3-player game)
        # Test behavior: verify that strategy card selection still works with elimination rules
        remaining_players = controller_after_elimination.get_turn_order()
        assert len(remaining_players) == 3

        # Available cards should still be managed according to Rule 33.9
        available_cards_after = (
            controller_after_elimination.get_available_strategy_cards()
        )
        assert len(available_cards_after) == 8  # All cards still available

    def test_rule_33_9_does_not_apply_to_games_starting_with_four_or_fewer(
        self,
    ) -> None:
        """Test Rule 33.9: Rule does not apply to games that started with 4 or fewer players."""
        # Setup 4-player game (starts with 4 players)
        players = [
            Player("player1", Faction.SOL),
            Player("player2", Faction.HACAN),
            Player("player3", Faction.XXCHA),
            Player("player4", Faction.YSSARIL),
        ]
        controller = GameController(players)

        # Verify initial state: 4 players, each should get 2 cards (8 cards / 4 players = 2 cards each)
        initial_players = controller.get_turn_order()
        assert len(initial_players) == 4

        # Test behavior: with 4 players, available strategy cards should be managed appropriately
        available_cards = controller.get_available_strategy_cards()
        assert (
            len(available_cards) == 8
        )  # All 8 strategy cards should be available initially

        # Simulate elimination of 1 player by creating a new controller with 3 players
        remaining_players = players[:-1]  # Remove last player
        controller_after_elimination = GameController.with_remaining_players(
            controller, remaining_players
        )

        # Rule 33.9 does NOT apply: Game started with 4 players, so normal distribution applies
        # 3 players should get 2 cards each (8 cards / 3 players = 2 cards each, with 2 remaining)
        # Test behavior: verify that normal strategy card selection applies (not Rule 33.9)
        remaining_players = controller_after_elimination.get_turn_order()
        assert len(remaining_players) == 3

        # Available cards should be managed according to normal rules (not Rule 33.9)
        available_cards_after = (
            controller_after_elimination.get_available_strategy_cards()
        )
        assert len(available_cards_after) == 8  # All cards still available

    def test_rule_33_9_does_not_apply_to_games_starting_with_three_players(
        self,
    ) -> None:
        """Test Rule 33.9: Rule does not apply to games that started with 3 players."""
        # Setup 3-player game (starts with 3 players)
        players = [
            Player("player1", Faction.SOL),
            Player("player2", Faction.HACAN),
            Player("player3", Faction.XXCHA),
        ]
        controller = GameController(players)

        # Verify initial state: 3 players, each should get 2 cards (8 cards / 3 players = 2 cards each)
        assert controller._initial_player_count == 3
        assert len(controller._players) == 3
        assert controller._get_cards_per_player() == 2

        # Rule 33.9 does NOT apply: Game started with 3 players (less than 5)
        # Normal distribution applies regardless of elimination
        assert controller._get_cards_per_player() == 2

    def test_rule_33_9_boundary_condition_exactly_five_players(self) -> None:
        """Test Rule 33.9: Boundary condition with exactly 5 players dropping to exactly 4."""
        # Setup exactly 5-player game
        players = [
            Player("player1", Faction.SOL),
            Player("player2", Faction.HACAN),
            Player("player3", Faction.XXCHA),
            Player("player4", Faction.YSSARIL),
            Player("player5", Faction.NAALU),
        ]
        controller = GameController(players)

        # Verify initial state
        assert controller._initial_player_count == 5
        assert controller._get_cards_per_player() == 1

        # Drop to exactly 4 players by creating a new controller with 4 players
        remaining_players = players[:-1]
        controller_after_elimination = GameController.with_remaining_players(
            controller, remaining_players
        )

        # Rule 33.9 applies: Started with 5 (>= 5), now have 4 (<= 4)
        assert controller_after_elimination._get_cards_per_player() == 1

    def test_rule_33_9_boundary_condition_drop_to_exactly_four_players(self) -> None:
        """Test Rule 33.9: Boundary condition dropping to exactly 4 players."""
        # Setup 6-player game
        players = [
            Player("player1", Faction.SOL),
            Player("player2", Faction.HACAN),
            Player("player3", Faction.XXCHA),
            Player("player4", Faction.YSSARIL),
            Player("player5", Faction.NAALU),
            Player("player6", Faction.BARONY),
        ]
        controller = GameController(players)

        # Drop to exactly 4 players by creating a new controller with 4 players
        remaining_players = players[:4]
        controller_after_elimination = GameController.with_remaining_players(
            controller, remaining_players
        )

        # Rule 33.9 applies: Started with 6 (>= 5), now have 4 (<= 4)
        assert controller_after_elimination._get_cards_per_player() == 1

    def test_rule_33_9_does_not_apply_when_staying_above_four_players(self) -> None:
        """Test Rule 33.9: Rule does not apply when player count stays above 4."""
        # Setup 6-player game
        players = [
            Player("player1", Faction.SOL),
            Player("player2", Faction.HACAN),
            Player("player3", Faction.XXCHA),
            Player("player4", Faction.YSSARIL),
            Player("player5", Faction.NAALU),
            Player("player6", Faction.BARONY),
        ]
        controller = GameController(players)

        # Drop to 5 players by creating a new controller with 5 players
        remaining_players = players[:-1]
        controller_after_elimination = GameController.with_remaining_players(
            controller, remaining_players
        )

        # Rule 33.9 does NOT apply: Still have 5 players (above 4)
        # Normal distribution should apply
        assert controller_after_elimination._get_cards_per_player() == 1

    def test_rule_33_9_validation_error_when_selecting_second_card(self) -> None:
        """Test Rule 33.9: Selecting a second strategy card raises ValidationError when rule applies."""
        # Setup 5-player game
        players = [
            Player("player1", Faction.SOL),
            Player("player2", Faction.HACAN),
            Player("player3", Faction.XXCHA),
            Player("player4", Faction.YSSARIL),
            Player("player5", Faction.NAALU),
        ]
        controller = GameController(players)

        # Start strategy phase
        controller.start_strategy_phase()

        # Simulate player elimination by creating a new controller with 4 players
        remaining_players = players[:-1]  # Remove last player
        controller_after_elimination = GameController.with_remaining_players(
            controller, remaining_players
        )
        controller_after_elimination.start_strategy_phase()

        # Rule 33.9 applies: Started with 5 (>= 5), now have 4 (<= 4)
        # Each player should only get 1 card, not 2

        # Player 1 selects their first card
        available_cards = controller_after_elimination.get_available_strategy_cards()
        first_card = available_cards[0]
        controller_after_elimination.select_strategy_card("player1", first_card.id)

        # Verify player has exactly 1 card
        player_cards = controller_after_elimination.get_player_strategy_cards("player1")
        assert len(player_cards) == 1

        # Attempting to select a second card should raise ValidationError
        # since Rule 33.9 limits players to 1 card each
        second_card = available_cards[1]

        with pytest.raises(
            ValidationError,
            match="Player player1 cannot select more than 1 strategy cards",
        ):
            controller_after_elimination.select_strategy_card("player1", second_card.id)

        # Verify player still has only 1 card after failed attempt
        player_cards_after = controller_after_elimination.get_player_strategy_cards(
            "player1"
        )
        assert len(player_cards_after) == 1
