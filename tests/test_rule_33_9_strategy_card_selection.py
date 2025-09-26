"""Tests for Rule 33.9: Strategy Card Selection after Elimination.

This module tests the strategy card selection mechanics when player count
drops from 5+ to 4 or fewer due to elimination.

LRR Reference: Rule 33.9 - If the game drops from five or more players to four or fewer
players due to elimination, players still only select one strategy card during the strategy phase.
"""

from ti4.core.constants import Faction
from ti4.core.game_controller import GameController
from ti4.core.player import Player


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
        assert controller._initial_player_count == 5
        assert len(controller._players) == 5
        assert controller._get_cards_per_player() == 1

        # Simulate player elimination by removing a player
        controller._players = controller._players[:-1]  # Remove last player
        assert len(controller._players) == 4

        # Rule 33.9: Even with 4 players, each should still get only 1 card
        # (not 2 cards as would be normal for a 4-player game)
        assert controller._get_cards_per_player() == 1

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
        assert controller._initial_player_count == 6
        assert len(controller._players) == 6
        assert controller._get_cards_per_player() == 1

        # Simulate elimination of 2 players
        controller._players = controller._players[:-2]  # Remove last 2 players
        assert len(controller._players) == 4

        # Rule 33.9: Even with 4 players, each should still get only 1 card
        assert controller._get_cards_per_player() == 1

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
        assert controller._initial_player_count == 8
        assert len(controller._players) == 8
        assert controller._get_cards_per_player() == 1

        # Simulate elimination of 5 players
        controller._players = controller._players[:3]  # Keep only first 3 players
        assert len(controller._players) == 3

        # Rule 33.9: Even with 3 players, each should still get only 1 card
        # (not 2 cards as would be normal for a 3-player game)
        assert controller._get_cards_per_player() == 1

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
        assert controller._initial_player_count == 4
        assert len(controller._players) == 4
        assert controller._get_cards_per_player() == 2

        # Simulate elimination of 1 player
        controller._players = controller._players[:-1]  # Remove last player
        assert len(controller._players) == 3

        # Rule 33.9 does NOT apply: Game started with 4 players, so normal distribution applies
        # 3 players should get 2 cards each (8 cards / 3 players = 2 cards each, with 2 remaining)
        assert controller._get_cards_per_player() == 2

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

        # Drop to exactly 4 players
        controller._players = controller._players[:-1]
        assert len(controller._players) == 4

        # Rule 33.9 applies: Started with 5 (>= 5), now have 4 (<= 4)
        assert controller._get_cards_per_player() == 1

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

        # Drop to exactly 4 players (boundary condition)
        controller._players = controller._players[:4]
        assert len(controller._players) == 4

        # Rule 33.9 applies: Started with 6 (>= 5), now have 4 (<= 4)
        assert controller._get_cards_per_player() == 1

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

        # Drop to 5 players (still above 4)
        controller._players = controller._players[:-1]
        assert len(controller._players) == 5

        # Rule 33.9 does NOT apply: Still have more than 4 players
        # Normal distribution: 8 cards / 5 players = 1 card each
        assert controller._get_cards_per_player() == 1
