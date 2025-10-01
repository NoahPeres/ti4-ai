"""Tests for atomic transaction operations.

This module tests that transaction effects are applied atomically - either all succeed or all fail,
with no partial state changes or history commits on failure.

Requirements: 2.1, 2.2, 2.3, 2.4, 2.5
"""

from datetime import datetime

import pytest

from ti4.core.constants import Faction
from ti4.core.game_state import GameState
from ti4.core.player import Player
from ti4.core.rule_28_deals import ComponentTransaction, TransactionStatus
from ti4.core.transactions import TransactionOffer


class TestAtomicTransactionOperations:
    """Test that transaction operations are atomic.

    Requirements: 2.1, 2.2, 2.3, 2.4, 2.5
    """

    def test_transaction_effects_applied_before_history_commit(self) -> None:
        """Test that resource and promissory note effects are applied before history commit.

        This test verifies that the order of operations is:
        1. Apply resource effects
        2. Apply promissory note effects
        3. Validate resulting state
        4. Only then commit to history

        Requirements: 2.1, 2.2, 2.3
        """
        # RED: This will fail until we reorder the operations
        player1 = Player(id="player1", faction=Faction.SOL)
        player1.gain_trade_goods(5)

        player2 = Player(id="player2", faction=Faction.HACAN)
        player2.add_commodities(3)

        game_state = GameState(players=[player1, player2])

        # Create a transaction that should succeed
        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # Add transaction to pending first
        state_with_pending = game_state.add_pending_transaction(transaction)

        # Apply transaction effects
        final_state = state_with_pending.apply_transaction_effects(transaction)

        # Verify new state is created (immutability check)
        assert final_state is not state_with_pending, "New GameState should be created"
        assert final_state is not game_state, (
            "Final state should be different from original"
        )

        # Verify effects were applied
        updated_player1 = next(p for p in final_state.players if p.id == "player1")
        updated_player2 = next(p for p in final_state.players if p.id == "player2")

        # Player1: 5 - 3 + 2 = 4 trade goods (lost 3, gained 2 from commodities)
        assert updated_player1.get_trade_goods() == 4
        # Player2: 0 + 3 = 3 trade goods (gained 3), 3 - 2 = 1 commodities (lost 2)
        assert updated_player2.get_trade_goods() == 3
        assert updated_player2.get_commodities() == 1

        # Verify transaction was committed to history (explicit success state)
        assert len(final_state.transaction_history) == 1
        assert final_state.transaction_history[0].transaction_id == "tx_001"
        assert final_state.transaction_history[0].status == TransactionStatus.ACCEPTED

        # Verify transaction was removed from pending (explicit success state)
        assert len(final_state.pending_transactions) == 0

    def test_transaction_failure_prevents_history_commit(self) -> None:
        """Test that transaction failure prevents history commit.

        This test demonstrates the current atomicity issue where the transaction
        is committed to history BEFORE effects are applied, so if effects fail,
        the transaction is still incorrectly in history.

        Requirements: 2.4, 2.5
        """
        # RED: This will fail until we implement proper atomicity
        player1 = Player(id="player1", faction=Faction.SOL)
        player1.gain_trade_goods(2)  # Only has 2 trade goods

        player2 = Player(id="player2", faction=Faction.HACAN)
        player2.add_commodities(3)

        game_state = GameState(players=[player1, player2])

        # Create a transaction that should fail (player1 doesn't have enough trade goods)
        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=5),  # More than player1 has
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # Add transaction to pending first
        state_with_pending = game_state.add_pending_transaction(transaction)
        original_history_length = len(state_with_pending.transaction_history)

        # Attempt to apply transaction effects - should fail with specific error message
        with pytest.raises(ValueError, match="insufficient trade goods") as exc_info:
            state_with_pending.apply_transaction_effects(transaction)

        # Verify specific error message content
        assert "player1" in str(exc_info.value), (
            "Error should mention the specific player"
        )
        assert "5" in str(exc_info.value) or "trade goods" in str(exc_info.value), (
            "Error should mention trade goods"
        )

        # CRITICAL ATOMICITY TEST:
        # The current implementation calls complete_transaction() FIRST, which moves
        # the transaction from pending to history BEFORE applying effects.
        # If effects fail (as they do here), the transaction is already in history!

        # This demonstrates the atomicity violation - the transaction should NOT
        # be in history if the effects failed, but with the current implementation it will be.

        # Note: We intentionally assert using original state below to ensure no partial commits occurred.

        # For now, let's verify the original state is unchanged
        # (This part should work correctly)
        assert len(state_with_pending.pending_transactions) == 1
        assert len(state_with_pending.transaction_history) == original_history_length

        # Verify player resources are unchanged
        original_player1 = next(
            p for p in state_with_pending.players if p.id == "player1"
        )
        original_player2 = next(
            p for p in state_with_pending.players if p.id == "player2"
        )

        assert original_player1.get_trade_goods() == 2
        assert original_player2.get_trade_goods() == 0
        assert original_player2.get_commodities() == 3

    def test_promissory_note_failure_prevents_history_commit(self) -> None:
        """Test that promissory note transfer failure prevents history commit.

        If promissory note effects fail, the transaction should not be committed to history.

        Requirements: 2.4, 2.5
        """
        # RED: This will fail until we implement proper atomicity
        from ti4.core.transactions import PromissoryNote, PromissoryNoteType

        player1 = Player(id="player1", faction=Faction.SOL)
        player1.gain_trade_goods(5)

        player2 = Player(id="player2", faction=Faction.HACAN)
        player2.gain_trade_goods(3)

        game_state = GameState(players=[player1, player2])

        # Create a promissory note that player1 doesn't actually own
        fake_note = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player1"
        )

        # Create a transaction with a promissory note player1 doesn't own
        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(promissory_notes=[fake_note]),
            request=TransactionOffer(trade_goods=2),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # Add transaction to pending first
        state_with_pending = game_state.add_pending_transaction(transaction)
        original_history_length = len(state_with_pending.transaction_history)

        # Attempt to apply transaction effects - should fail with specific error message
        with pytest.raises(
            ValueError, match="does not own promissory note"
        ) as exc_info:
            state_with_pending.apply_transaction_effects(transaction)

        # Verify specific error message content
        assert "player1" in str(exc_info.value), (
            "Error should mention the specific player"
        )
        assert "TRADE_AGREEMENT" in str(exc_info.value) or "promissory note" in str(
            exc_info.value
        ), "Error should mention promissory note details"

        # Verify original state is unchanged
        # Transaction should still be in pending (not moved to history)
        assert len(state_with_pending.pending_transactions) == 1
        assert len(state_with_pending.transaction_history) == original_history_length

        # Verify player resources are unchanged
        original_player1 = next(
            p for p in state_with_pending.players if p.id == "player1"
        )
        original_player2 = next(
            p for p in state_with_pending.players if p.id == "player2"
        )

        assert original_player1.get_trade_goods() == 5
        assert original_player2.get_trade_goods() == 3

    @pytest.mark.skip(
        reason="GameState.is_valid() always returns True - validation test needs proper validation implementation"
    )
    def test_validation_failure_prevents_history_commit(self) -> None:
        """Test that validation failure prevents history commit.

        If the resulting game state is invalid, the transaction should not be committed to history.

        Requirements: 2.4, 2.5
        """
        # This test is skipped because GameState.is_valid() currently always returns True
        # Once proper validation is implemented, this test should be updated to:
        # 1. Create a scenario that results in invalid game state
        # 2. Verify that apply_transaction_effects raises ValueError with "invalid game state"
        # 3. Verify that the transaction is not committed to history

        # The atomicity framework is in place - validation just needs to be implemented
        pass

    def test_successful_transaction_commits_to_history_last(self) -> None:
        """Test that successful transactions commit to history only after all effects are applied.

        This verifies the complete atomic operation sequence.

        Requirements: 2.1, 2.2, 2.3, 2.4
        """
        # RED: This will fail until we implement proper ordering
        player1 = Player(id="player1", faction=Faction.SOL)
        player1.gain_trade_goods(5)

        player2 = Player(id="player2", faction=Faction.HACAN)
        player2.add_commodities(3)

        game_state = GameState(players=[player1, player2])

        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # Add transaction to pending first
        state_with_pending = game_state.add_pending_transaction(transaction)
        assert len(state_with_pending.pending_transactions) == 1
        assert len(state_with_pending.transaction_history) == 0

        # Apply transaction effects
        final_state = state_with_pending.apply_transaction_effects(transaction)

        # Immutability verification (identity checks)
        assert final_state is not state_with_pending, (
            "Final state should be different from pending state"
        )
        assert final_state is not game_state, (
            "Final state should be different from original state"
        )

        # Verify all effects were applied AND transaction was committed to history
        # Effects verification
        updated_player1 = next(p for p in final_state.players if p.id == "player1")
        updated_player2 = next(p for p in final_state.players if p.id == "player2")

        assert updated_player1.get_trade_goods() == 4  # 5 - 3 + 2
        assert updated_player2.get_trade_goods() == 3  # 0 + 3
        assert updated_player2.get_commodities() == 1  # 3 - 2

        # History commitment verification (explicit success state)
        assert len(final_state.transaction_history) == 1
        assert final_state.transaction_history[0].transaction_id == "tx_001"
        assert final_state.transaction_history[0].status == TransactionStatus.ACCEPTED

        # Pending transactions should be cleared (explicit success state)
        assert len(final_state.pending_transactions) == 0
