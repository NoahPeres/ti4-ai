"""Tests for PromissoryNoteManager cloning in promissory note effects.

This module tests that promissory note effects properly clone the PromissoryNoteManager
to preserve both player hands and available notes.

Requirements: 3.2, 3.3, 3.4
"""

from datetime import datetime

from ti4.core.constants import Faction
from ti4.core.deals import ComponentTransaction, TransactionStatus
from ti4.core.game_state import GameState
from ti4.core.player import Player
from ti4.core.transactions import PromissoryNote, PromissoryNoteType, TransactionOffer


class TestPromissoryNoteManagerCloning:
    """Test that PromissoryNoteManager cloning preserves complete state.

    Requirements: 3.2, 3.3, 3.4
    """

    def test_clone_promissory_note_manager_preserves_player_hands(self) -> None:
        """Test that cloning preserves player hands.

        Requirements: 3.2, 3.3
        """
        player1 = Player(id="player1", faction=Faction.SOL)
        player2 = Player(id="player2", faction=Faction.HACAN)

        # Create a game state with promissory notes in player hands
        game_state = GameState(players=[player1, player2])

        # Add some promissory notes to player hands
        note1 = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player1"
        )
        note2 = PromissoryNote(
            note_type=PromissoryNoteType.SUPPORT_FOR_THE_THRONE,
            issuing_player="player2",
        )

        game_state.promissory_note_manager.add_note_to_hand(note1, "player2")
        game_state.promissory_note_manager.add_note_to_hand(note2, "player1")

        # Clone the manager
        cloned_manager = game_state._clone_promissory_note_manager()

        # Verify cloned manager is a different object
        assert cloned_manager is not game_state.promissory_note_manager, (
            "Cloned manager should be a different object"
        )

        # Verify player hands are preserved
        original_player1_hand = game_state.promissory_note_manager.get_player_hand(
            "player1"
        )
        original_player2_hand = game_state.promissory_note_manager.get_player_hand(
            "player2"
        )

        cloned_player1_hand = cloned_manager.get_player_hand("player1")
        cloned_player2_hand = cloned_manager.get_player_hand("player2")

        # Hands should have same content but be different objects
        assert cloned_player1_hand is not original_player1_hand, (
            "Cloned player1 hand should be different object"
        )
        assert cloned_player2_hand is not original_player2_hand, (
            "Cloned player2 hand should be different object"
        )

        assert len(cloned_player1_hand) == len(original_player1_hand), (
            "Player1 hand size should be preserved"
        )
        assert len(cloned_player2_hand) == len(original_player2_hand), (
            "Player2 hand size should be preserved"
        )

        assert note2 in cloned_player1_hand, (
            "Player1 should have note2 in cloned manager"
        )
        assert note1 in cloned_player2_hand, (
            "Player2 should have note1 in cloned manager"
        )

    def test_clone_promissory_note_manager_preserves_available_notes(self) -> None:
        """Test that cloning preserves available notes.

        Requirements: 3.2, 3.3
        """
        player1 = Player(id="player1", faction=Faction.SOL)
        game_state = GameState(players=[player1])

        # Add some notes to available notes
        note1 = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player1"
        )
        note2 = PromissoryNote(
            note_type=PromissoryNoteType.SUPPORT_FOR_THE_THRONE,
            issuing_player="player1",
        )

        # Simulate notes being returned to available pool
        game_state.promissory_note_manager._available_notes.add(note1)
        game_state.promissory_note_manager._available_notes.add(note2)

        # Clone the manager
        cloned_manager = game_state._clone_promissory_note_manager()

        # Verify available notes are preserved but in different set object
        assert (
            cloned_manager._available_notes
            is not game_state.promissory_note_manager._available_notes
        ), "Available notes should be different set object"

        assert len(cloned_manager._available_notes) == len(
            game_state.promissory_note_manager._available_notes
        ), "Available notes size should be preserved"

        assert note1 in cloned_manager._available_notes, (
            "Note1 should be in cloned available notes"
        )
        assert note2 in cloned_manager._available_notes, (
            "Note2 should be in cloned available notes"
        )

    def test_promissory_note_effects_use_proper_cloning(self) -> None:
        """Test that _apply_promissory_note_effects uses proper cloning.

        Requirements: 3.2, 3.3, 3.4
        """
        player1 = Player(id="player1", faction=Faction.SOL)
        player2 = Player(id="player2", faction=Faction.HACAN)

        game_state = GameState(players=[player1, player2])

        # Set up initial state with promissory notes
        note1 = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player1"
        )
        note2 = PromissoryNote(
            note_type=PromissoryNoteType.SUPPORT_FOR_THE_THRONE,
            issuing_player="player2",
        )

        # Player1 has note2, player2 has note1
        game_state.promissory_note_manager.add_note_to_hand(note2, "player1")
        game_state.promissory_note_manager.add_note_to_hand(note1, "player2")

        # Add some available notes
        available_note = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="other"
        )
        game_state.promissory_note_manager._available_notes.add(available_note)

        # Store original state
        original_manager = game_state.promissory_note_manager
        original_player1_hand_size = len(original_manager.get_player_hand("player1"))
        original_player2_hand_size = len(original_manager.get_player_hand("player2"))
        original_available_size = len(original_manager._available_notes)

        # Create transaction to transfer note1 from player2 to player1
        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(),  # No offer
            request=TransactionOffer(promissory_notes=[note1]),  # Request note1
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # Apply promissory note effects
        new_state = game_state._apply_promissory_note_effects(transaction)

        # Verify new state has different manager
        assert new_state.promissory_note_manager is not original_manager, (
            "New state should have different PromissoryNoteManager"
        )

        # Verify original state is unchanged
        assert (
            len(original_manager.get_player_hand("player1"))
            == original_player1_hand_size
        ), "Original player1 hand should be unchanged"
        assert (
            len(original_manager.get_player_hand("player2"))
            == original_player2_hand_size
        ), "Original player2 hand should be unchanged"
        assert len(original_manager._available_notes) == original_available_size, (
            "Original available notes should be unchanged"
        )

        assert note2 in original_manager.get_player_hand("player1"), (
            "Original player1 should still have note2"
        )
        assert note1 in original_manager.get_player_hand("player2"), (
            "Original player2 should still have note1"
        )

        # Verify new state has correct transfers
        new_manager = new_state.promissory_note_manager
        assert note2 in new_manager.get_player_hand("player1"), (
            "New player1 should still have note2"
        )
        assert note1 in new_manager.get_player_hand("player1"), (
            "New player1 should now have note1"
        )
        assert note1 not in new_manager.get_player_hand("player2"), (
            "New player2 should no longer have note1"
        )

        # Verify available notes are preserved
        assert available_note in new_manager._available_notes, (
            "Available notes should be preserved in new manager"
        )

    def test_promissory_note_effects_immutability_with_complex_state(self) -> None:
        """Test immutability with complex promissory note state.

        Requirements: 3.2, 3.3, 3.4
        """
        player1 = Player(id="player1", faction=Faction.SOL)
        player2 = Player(id="player2", faction=Faction.HACAN)
        player3 = Player(id="player3", faction=Faction.XXCHA)

        game_state = GameState(players=[player1, player2, player3])

        # Create complex initial state
        notes = [
            PromissoryNote(
                note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player1"
            ),
            PromissoryNote(
                note_type=PromissoryNoteType.SUPPORT_FOR_THE_THRONE,
                issuing_player="player2",
            ),
            PromissoryNote(
                note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player3"
            ),
        ]

        # Distribute notes among players
        game_state.promissory_note_manager.add_note_to_hand(notes[0], "player2")
        game_state.promissory_note_manager.add_note_to_hand(notes[1], "player3")
        game_state.promissory_note_manager.add_note_to_hand(notes[2], "player1")

        # Add available notes
        available_notes = [
            PromissoryNote(
                note_type=PromissoryNoteType.TRADE_AGREEMENT,
                issuing_player="available1",
            ),
            PromissoryNote(
                note_type=PromissoryNoteType.SUPPORT_FOR_THE_THRONE,
                issuing_player="available2",
            ),
        ]
        for note in available_notes:
            game_state.promissory_note_manager._available_notes.add(note)

        # Store original state references
        original_manager = game_state.promissory_note_manager
        original_player_hands = {
            pid: original_manager.get_player_hand(pid).copy()
            for pid in ["player1", "player2", "player3"]
        }
        original_available = original_manager._available_notes.copy()

        # Create transaction
        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(
                promissory_notes=[notes[2]]
            ),  # Player1 gives notes[2]
            request=TransactionOffer(
                promissory_notes=[notes[0]]
            ),  # Player1 gets notes[0]
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # Apply effects
        new_state = game_state._apply_promissory_note_effects(transaction)

        # Verify complete immutability of original state
        for pid in ["player1", "player2", "player3"]:
            current_hand = original_manager.get_player_hand(pid)
            expected_hand = original_player_hands[pid]
            assert current_hand == expected_hand, (
                f"Original {pid} hand should be unchanged"
            )
            assert (
                current_hand
                is not new_state.promissory_note_manager.get_player_hand(pid)
            ), f"Original {pid} hand should be different object from new state"

        assert original_manager._available_notes == original_available, (
            "Original available notes should be unchanged"
        )
        assert (
            original_manager._available_notes
            is not new_state.promissory_note_manager._available_notes
        ), "Original available notes should be different object from new state"

        # Verify new state has correct transfers
        new_manager = new_state.promissory_note_manager
        assert notes[0] in new_manager.get_player_hand("player1"), (
            "Player1 should have received notes[0]"
        )
        assert notes[2] in new_manager.get_player_hand("player2"), (
            "Player2 should have received notes[2]"
        )
        assert notes[1] in new_manager.get_player_hand("player3"), (
            "Player3 should still have notes[1]"
        )

        # Verify available notes preserved
        for note in available_notes:
            assert note in new_manager._available_notes, (
                f"Available note {note} should be preserved"
            )
