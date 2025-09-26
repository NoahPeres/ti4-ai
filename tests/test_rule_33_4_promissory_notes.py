"""Test Rule 33.4: Promissory note handling on player elimination."""

from ti4.core.game_state import GameState
from ti4.core.player import Player
from ti4.core.transactions import PromissoryNote, PromissoryNoteType
from ti4.core.constants import Faction


class TestRule334PromissoryNoteElimination:
    """Test Rule 33.4: Return other players' promissory notes on elimination."""

    def test_promissory_notes_returned_on_elimination(self) -> None:
        """Test that promissory notes are properly handled when a player is eliminated.

        LRR Reference: Rule 33.4 - When a player becomes eliminated, each promissory
        note they have that matches another player's faction or color is returned to
        that player.
        """
        # Create game state with players
        players = [
            Player("player1", Faction.HACAN),
            Player("player2", Faction.SOL),
            Player("player3", Faction.BARONY),
        ]
        game_state = GameState(players=players)

        # Set up promissory notes - player1 has notes from other players
        note_from_player2 = PromissoryNote(
            PromissoryNoteType.TRADE_AGREEMENT, "player2"
        )
        note_from_player3 = PromissoryNote(
            PromissoryNoteType.SUPPORT_FOR_THE_THRONE, "player3"
        )
        note_from_player1 = PromissoryNote(PromissoryNoteType.CEASEFIRE, "player1")

        # Add notes to player1's hand
        game_state.promissory_note_manager.add_note_to_hand(
            note_from_player2, "player1"
        )
        game_state.promissory_note_manager.add_note_to_hand(
            note_from_player3, "player1"
        )
        game_state.promissory_note_manager.add_note_to_hand(
            note_from_player1, "player2"
        )

        # Verify initial state
        player1_hand = game_state.promissory_note_manager.get_player_hand("player1")
        assert note_from_player2 in player1_hand
        assert note_from_player3 in player1_hand

        player2_hand = game_state.promissory_note_manager.get_player_hand("player2")
        assert note_from_player1 in player2_hand

        # Eliminate player1
        new_game_state = game_state.eliminate_player("player1")

        # Verify player1 is eliminated
        assert len(new_game_state.players) == 2
        assert not any(p.id == "player1" for p in new_game_state.players)

        # Verify promissory notes issued by player1 are removed from all hands
        player2_hand_after = new_game_state.promissory_note_manager.get_player_hand(
            "player2"
        )
        assert note_from_player1 not in player2_hand_after

        # Verify player1's hand is empty (player eliminated)
        player1_hand_after = new_game_state.promissory_note_manager.get_player_hand(
            "player1"
        )
        assert len(player1_hand_after) == 0

    def test_promissory_notes_removed_from_available_pool(self) -> None:
        """Test that eliminated player's promissory notes are removed from available pool.

        LRR Reference: Rule 33.4 combined with Rule 69.7 - All matching notes
        returned to game box.
        """
        # Create game state with players
        players = [
            Player("player1", Faction.HACAN),
            Player("player2", Faction.SOL),
        ]
        game_state = GameState(players=players)

        # Create and use a note (making it available)
        note = PromissoryNote(PromissoryNoteType.TRADE_AGREEMENT, "player1")
        game_state.promissory_note_manager.add_note_to_hand(note, "player2")
        game_state.promissory_note_manager.return_note_after_use(note, "player2")

        # Verify note is available
        assert (
            game_state.promissory_note_manager.is_note_available_for_transaction(note)
            is True
        )

        # Eliminate player1
        new_game_state = game_state.eliminate_player("player1")

        # Verify note is no longer available
        assert (
            new_game_state.promissory_note_manager.is_note_available_for_transaction(
                note
            )
            is False
        )

    def test_elimination_with_no_promissory_notes(self) -> None:
        """Test that elimination works correctly when no promissory notes are involved."""
        # Create game state with players
        players = [
            Player("player1", Faction.HACAN),
            Player("player2", Faction.SOL),
        ]
        game_state = GameState(players=players)

        # Eliminate player1 (no promissory notes involved)
        new_game_state = game_state.eliminate_player("player1")

        # Verify player1 is eliminated
        assert len(new_game_state.players) == 1
        assert not any(p.id == "player1" for p in new_game_state.players)

        # Verify promissory note manager is still functional
        assert new_game_state.promissory_note_manager is not None
        assert (
            len(new_game_state.promissory_note_manager.get_player_hand("player1")) == 0
        )
        assert (
            len(new_game_state.promissory_note_manager.get_player_hand("player2")) == 0
        )
