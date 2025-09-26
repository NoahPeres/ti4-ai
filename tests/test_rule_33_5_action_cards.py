"""Test Rule 33.5: Action card handling on player elimination.

LRR Reference: Rule 33.5 - Action cards in the eliminated player's hand are discarded.
"""

import pytest

from ti4.core.constants import Faction
from ti4.core.game_state import GameState
from ti4.core.player import Player


class TestRule335ActionCardElimination:
    """Test Rule 33.5: Action cards are discarded on elimination."""

    def test_action_cards_discarded_on_elimination(self) -> None:
        """Test that action cards in eliminated player's hand are discarded."""
        # Setup game state with two players
        player1 = Player("player1", Faction.SOL)
        player2 = Player("player2", Faction.HACAN)
        game_state = GameState().add_player(player1).add_player(player2)
        
        # Give player1 some action cards
        action_cards = ["Direct Hit", "Sabotage", "Skilled Retreat"]
        game_state = game_state._create_new_state(
            players=game_state.players,
            player_action_cards={
                "player1": action_cards,
                "player2": ["Morale Boost"]
            },
            action_card_discard_pile=[]
        )
        
        # Verify initial state
        assert game_state.player_action_cards["player1"] == action_cards
        assert game_state.player_action_cards["player2"] == ["Morale Boost"]
        assert len(game_state.action_card_discard_pile) == 0
        
        # Eliminate player1
        new_game_state = game_state.eliminate_player("player1")
        
        # Verify player1's action cards are discarded
        assert "player1" not in new_game_state.player_action_cards
        assert new_game_state.player_action_cards["player2"] == ["Morale Boost"]
        assert set(new_game_state.action_card_discard_pile) == set(action_cards)

    def test_elimination_with_no_action_cards(self) -> None:
        """Test that elimination works correctly when player has no action cards."""
        # Setup game state with player
        player = Player("player1", Faction.SOL)
        game_state = GameState().add_player(player)
        
        # Ensure player has no action cards
        game_state = game_state._create_new_state(
            players=game_state.players,
            player_action_cards={"player1": []},
            action_card_discard_pile=[]
        )
        
        # Verify initial state
        assert game_state.player_action_cards["player1"] == []
        assert len(game_state.action_card_discard_pile) == 0
        
        # Eliminate player
        new_game_state = game_state.eliminate_player("player1")
        
        # Verify no action cards were discarded
        assert "player1" not in new_game_state.player_action_cards
        assert len(new_game_state.action_card_discard_pile) == 0

    def test_elimination_preserves_other_players_action_cards(self) -> None:
        """Test that eliminating a player doesn't affect other players' action cards."""
        # Setup game state with three players
        player1 = Player("player1", Faction.SOL)
        player2 = Player("player2", Faction.HACAN)
        player3 = Player("player3", Faction.ARBOREC)
        game_state = GameState().add_player(player1).add_player(player2).add_player(player3)
        
        # Give each player different action cards
        game_state = game_state._create_new_state(
            players=game_state.players,
            player_action_cards={
                "player1": ["Direct Hit", "Sabotage"],
                "player2": ["Morale Boost", "Skilled Retreat"],
                "player3": ["Emergency Repairs"]
            },
            action_card_discard_pile=["Ancient Burial Sites"]
        )
        
        # Eliminate player2
        new_game_state = game_state.eliminate_player("player2")
        
        # Verify player1 and player3 still have their action cards
        assert new_game_state.player_action_cards["player1"] == ["Direct Hit", "Sabotage"]
        assert new_game_state.player_action_cards["player3"] == ["Emergency Repairs"]
        assert "player2" not in new_game_state.player_action_cards
        
        # Verify player2's cards were added to discard pile
        expected_discard = ["Ancient Burial Sites", "Morale Boost", "Skilled Retreat"]
        assert set(new_game_state.action_card_discard_pile) == set(expected_discard)

    def test_elimination_adds_to_existing_discard_pile(self) -> None:
        """Test that eliminated player's action cards are added to existing discard pile."""
        # Setup game state with player
        player = Player("player1", Faction.SOL)
        game_state = GameState().add_player(player)
        
        # Setup with existing discard pile and player action cards
        existing_discard = ["Ancient Burial Sites", "Diplomacy"]
        player_cards = ["Direct Hit", "Sabotage"]
        
        game_state = game_state._create_new_state(
            players=game_state.players,
            player_action_cards={"player1": player_cards},
            action_card_discard_pile=existing_discard
        )
        
        # Eliminate player
        new_game_state = game_state.eliminate_player("player1")
        
        # Verify all cards are in discard pile
        expected_discard = existing_discard + player_cards
        assert set(new_game_state.action_card_discard_pile) == set(expected_discard)
        assert len(new_game_state.action_card_discard_pile) == 4