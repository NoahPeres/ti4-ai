"""Tests for Rule 69: PROMISSORY NOTES mechanics.

This module tests the promissory note system according to TI4 LRR Rule 69.
All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.

Rule 69 Sub-rules tested:
- 69.1: Card resolution - following timing and ability text
- 69.2: Own card restriction - cannot play own color/faction notes
- 69.3: Card return timing - returned after abilities resolved
- 69.4: Reuse after return - returned notes can be given again
- 69.5: Transaction limits - max one per transaction (already in Rule 94)
- 69.6: Hidden information - keep hands hidden
- 69.7: Elimination effects - return matching notes when player eliminated
"""

from src.ti4.core.promissory_notes import PromissoryNoteManager
from src.ti4.core.transactions import PromissoryNote, PromissoryNoteType


class TestRule69PromissoryNoteBasics:
    """Test basic promissory note mechanics (Rule 69.0)."""

    def test_promissory_note_system_exists(self) -> None:
        """Test that promissory note system can be imported and instantiated.

        This is the first RED test - it will fail until we create the system.

        LRR Reference: Rule 69.0 - Core promissory note concept
        """
        # This will fail initially - RED phase
        manager = PromissoryNoteManager()
        assert manager is not None


class TestRule69OwnCardRestriction:
    """Test own card restriction mechanics (Rule 69.2)."""

    def test_player_cannot_play_own_color_promissory_note(self) -> None:
        """Test that players cannot play their own color's promissory notes.

        LRR Reference: Rule 69.2 - "Players cannot play their own color's
        or faction's promissory notes"
        """
        manager = PromissoryNoteManager()

        # Create a promissory note issued by player1
        note = PromissoryNote(PromissoryNoteType.TRADE_AGREEMENT, "player1")

        # Player1 should not be able to play their own note
        can_play = manager.can_player_play_note(note, "player1")
        assert can_play is False

    def test_player_can_play_other_players_promissory_notes(self) -> None:
        """Test that players can play other players' promissory notes.

        LRR Reference: Rule 69.2 - Restriction only applies to own notes
        """
        manager = PromissoryNoteManager()

        # Create a promissory note issued by player1
        note = PromissoryNote(PromissoryNoteType.TRADE_AGREEMENT, "player1")

        # Player2 should be able to play player1's note
        can_play = manager.can_player_play_note(note, "player2")
        assert can_play is True


class TestRule69HiddenInformation:
    """Test hidden information management (Rule 69.6)."""

    def test_player_can_add_promissory_note_to_hand(self) -> None:
        """Test that players can add promissory notes to their hidden hand.

        LRR Reference: Rule 69.6 - "Players should keep promissory note hands hidden"
        """
        manager = PromissoryNoteManager()

        # Create a promissory note
        note = PromissoryNote(PromissoryNoteType.TRADE_AGREEMENT, "player1")

        # Player2 should be able to add it to their hand
        manager.add_note_to_hand(note, "player2")

        # Verify the note is in player2's hand
        hand = manager.get_player_hand("player2")
        assert note in hand

    def test_player_hands_are_separate(self) -> None:
        """Test that different players have separate hidden hands.

        LRR Reference: Rule 69.6 - Each player has their own hidden hand
        """
        manager = PromissoryNoteManager()

        # Create different notes for different players
        note1 = PromissoryNote(PromissoryNoteType.TRADE_AGREEMENT, "player1")
        note2 = PromissoryNote(PromissoryNoteType.CEASEFIRE, "player2")

        # Add notes to different players' hands
        manager.add_note_to_hand(note1, "player2")
        manager.add_note_to_hand(note2, "player3")

        # Verify hands are separate
        hand2 = manager.get_player_hand("player2")
        hand3 = manager.get_player_hand("player3")

        assert note1 in hand2
        assert note1 not in hand3
        assert note2 in hand3
        assert note2 not in hand2


class TestRule69CardReturnAndReuse:
    """Test card return and reuse mechanics (Rules 69.3 and 69.4)."""

    def test_promissory_note_can_be_returned_after_use(self) -> None:
        """Test that promissory notes are returned after abilities resolved.

        LRR Reference: Rule 69.3 - "Promissory notes returned after abilities completely resolved"
        """
        manager = PromissoryNoteManager()

        # Create and add note to player's hand
        note = PromissoryNote(PromissoryNoteType.TRADE_AGREEMENT, "player1")
        manager.add_note_to_hand(note, "player2")

        # Verify note is in hand
        hand = manager.get_player_hand("player2")
        assert note in hand

        # Return the note after use
        manager.return_note_after_use(note, "player2")

        # Verify note is no longer in player's hand
        hand_after = manager.get_player_hand("player2")
        assert note not in hand_after

    def test_returned_note_can_be_given_again(self) -> None:
        """Test that returned promissory notes can be given to other players again.

        LRR Reference: Rule 69.4 - "Returned promissory notes can be given to other players again in future transactions"
        """
        manager = PromissoryNoteManager()

        # Create note and add to player2's hand
        note = PromissoryNote(PromissoryNoteType.TRADE_AGREEMENT, "player1")
        manager.add_note_to_hand(note, "player2")

        # Return the note
        manager.return_note_after_use(note, "player2")

        # Note should be available for reuse
        can_reuse = manager.is_note_available_for_transaction(note)
        assert can_reuse is True

        # Give the note to player3
        manager.add_note_to_hand(note, "player3")

        # Verify note is now in player3's hand
        hand3 = manager.get_player_hand("player3")
        assert note in hand3


class TestRule69EliminationEffects:
    """Test elimination effects on promissory notes (Rule 69.7)."""

    def test_player_elimination_returns_matching_notes(self) -> None:
        """Test that when a player is eliminated, all matching promissory notes are returned.

        LRR Reference: Rule 69.7 - "When player eliminated, all matching color/faction
        promissory notes returned to game box"
        """
        manager = PromissoryNoteManager()

        # Create notes from player1 and distribute them
        note1 = PromissoryNote(PromissoryNoteType.TRADE_AGREEMENT, "player1")
        note2 = PromissoryNote(PromissoryNoteType.CEASEFIRE, "player1")
        note3 = PromissoryNote(
            PromissoryNoteType.ALLIANCE, "player2"
        )  # Different player

        # Add notes to different players' hands
        manager.add_note_to_hand(note1, "player2")
        manager.add_note_to_hand(note2, "player3")
        manager.add_note_to_hand(note3, "player2")

        # Verify notes are in hands
        assert note1 in manager.get_player_hand("player2")
        assert note2 in manager.get_player_hand("player3")
        assert note3 in manager.get_player_hand("player2")

        # Eliminate player1
        manager.handle_player_elimination("player1")

        # Verify player1's notes are removed from all hands
        assert note1 not in manager.get_player_hand("player2")
        assert note2 not in manager.get_player_hand("player3")

        # Verify other player's notes remain
        assert note3 in manager.get_player_hand("player2")

    def test_elimination_affects_available_notes(self) -> None:
        """Test that elimination also removes notes from available pool.

        LRR Reference: Rule 69.7 - All matching notes returned to game box
        """
        manager = PromissoryNoteManager()

        # Create and return a note (making it available)
        note = PromissoryNote(PromissoryNoteType.TRADE_AGREEMENT, "player1")
        manager.add_note_to_hand(note, "player2")
        manager.return_note_after_use(note, "player2")

        # Verify note is available
        assert manager.is_note_available_for_transaction(note) is True

        # Eliminate player1
        manager.handle_player_elimination("player1")

        # Verify note is no longer available
        assert manager.is_note_available_for_transaction(note) is False


class TestRule69InputValidation:
    """Test input validation and error handling."""

    def test_empty_player_id_validation(self) -> None:
        """Test that empty player IDs are handled properly."""
        manager = PromissoryNoteManager()
        note = PromissoryNote(PromissoryNoteType.TRADE_AGREEMENT, "player1")

        # Empty player ID should not cause errors
        hand = manager.get_player_hand("")
        assert hand == []

        # Adding note with empty player ID should work (defensive programming)
        manager.add_note_to_hand(note, "")
        hand = manager.get_player_hand("")
        assert note in hand

    def test_nonexistent_player_hand_access(self) -> None:
        """Test accessing hand of player who doesn't exist."""
        manager = PromissoryNoteManager()

        # Should return empty list for nonexistent player
        hand = manager.get_player_hand("nonexistent_player")
        assert hand == []
