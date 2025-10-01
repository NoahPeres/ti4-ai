"""Tests for reject and cancel transaction GameState synchronization.

This module tests that reject and cancel operations properly synchronize
with GameState pending transactions.

Requirements: 5.3, 5.4
"""

from unittest.mock import Mock

from ti4.core.constants import Faction
from ti4.core.game_state import GameState
from ti4.core.player import Player
from ti4.core.rule_28_deals import (
    EnhancedTransactionManager,
    TransactionStatus,
)
from ti4.core.transactions import TransactionOffer


class TestRejectCancelGameStateSync:
    """Test reject and cancel operations synchronization with GameState.

    Requirements: 5.3, 5.4
    """

    def test_reject_transaction_removes_from_gamestate(self) -> None:
        """Test that reject_transaction removes transaction from GameState pending_transactions.

        Requirements: 5.3
        """
        # RED: This will fail until we implement GameState synchronization for reject

        # Setup
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player1.gain_trade_goods(5)  # Give enough trade goods

        player2 = Player(id="player2", faction=Faction.BARONY)
        player2.add_commodities(2)  # Give enough commodities (within limit)

        players = [player1, player2]
        game_state = GameState(players=players)

        # Mock galaxy for neighbor validation
        galaxy = Mock()
        galaxy.are_players_neighbors.return_value = True

        # Create transaction manager
        manager = EnhancedTransactionManager(galaxy, game_state)

        # Propose transaction
        offer = TransactionOffer(trade_goods=3)
        request = TransactionOffer(commodities=2)

        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
        )

        # Verify transaction is in both manager cache and GameState
        assert transaction.transaction_id in manager._transactions
        assert transaction.transaction_id in manager._game_state.pending_transactions

        # Reject the transaction
        result = manager.reject_transaction(transaction.transaction_id)

        # Verify transaction is removed from GameState pending_transactions
        assert (
            transaction.transaction_id not in manager._game_state.pending_transactions
        )

        # Verify transaction status is updated in manager cache
        assert result.success
        assert result.transaction.status == TransactionStatus.REJECTED

        # Verify manager still has the transaction (for history)
        assert transaction.transaction_id in manager._transactions
        updated_transaction = manager.get_transaction(transaction.transaction_id)
        assert updated_transaction.status == TransactionStatus.REJECTED

    def test_cancel_transaction_removes_from_gamestate(self) -> None:
        """Test that cancel_transaction removes transaction from GameState pending_transactions.

        Requirements: 5.4
        """
        # RED: This will fail until we implement GameState synchronization for cancel

        # Setup
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player1.gain_trade_goods(5)  # Give enough trade goods

        player2 = Player(id="player2", faction=Faction.BARONY)
        player2.add_commodities(2)  # Give enough commodities (within limit)

        players = [player1, player2]
        game_state = GameState(players=players)

        # Mock galaxy for neighbor validation
        galaxy = Mock()
        galaxy.are_players_neighbors.return_value = True

        # Create transaction manager
        manager = EnhancedTransactionManager(galaxy, game_state)

        # Propose transaction
        offer = TransactionOffer(trade_goods=3)
        request = TransactionOffer(commodities=2)

        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
        )

        # Verify transaction is in both manager cache and GameState
        assert transaction.transaction_id in manager._transactions
        assert transaction.transaction_id in manager._game_state.pending_transactions

        # Cancel the transaction
        manager.cancel_transaction(transaction.transaction_id, "player1")

        # Verify transaction is removed from GameState pending_transactions
        assert (
            transaction.transaction_id not in manager._game_state.pending_transactions
        )

        # Verify manager still has the transaction (for history)
        assert transaction.transaction_id in manager._transactions
        updated_transaction = manager.get_transaction(transaction.transaction_id)
        assert updated_transaction.status == TransactionStatus.CANCELLED

    def test_reject_transaction_safe_removal_with_copy_and_pop(self) -> None:
        """Test that reject uses safe removal with copy() and pop() with default.

        Requirements: 5.3
        """
        # Setup
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player1.gain_trade_goods(5)

        player2 = Player(id="player2", faction=Faction.BARONY)
        player2.add_commodities(2)

        players = [player1, player2]
        game_state = GameState(players=players)

        galaxy = Mock()
        galaxy.are_players_neighbors.return_value = True

        manager = EnhancedTransactionManager(galaxy, game_state)

        # Propose transaction
        offer = TransactionOffer(trade_goods=3)
        request = TransactionOffer(commodities=2)

        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
        )

        original_pending = manager._game_state.pending_transactions

        # Reject the transaction
        manager.reject_transaction(transaction.transaction_id)

        # Verify original pending_transactions dict was not mutated
        assert transaction.transaction_id in original_pending  # Original unchanged
        assert (
            transaction.transaction_id not in manager._game_state.pending_transactions
        )  # New state updated

    def test_cancel_transaction_safe_removal_with_copy_and_pop(self) -> None:
        """Test that cancel uses safe removal with copy() and pop() with default.

        Requirements: 5.4
        """
        # Setup
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player1.gain_trade_goods(5)

        player2 = Player(id="player2", faction=Faction.BARONY)
        player2.add_commodities(2)

        players = [player1, player2]
        game_state = GameState(players=players)

        galaxy = Mock()
        galaxy.are_players_neighbors.return_value = True

        manager = EnhancedTransactionManager(galaxy, game_state)

        # Propose transaction
        offer = TransactionOffer(trade_goods=3)
        request = TransactionOffer(commodities=2)

        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
        )

        original_pending = manager._game_state.pending_transactions

        # Cancel the transaction
        manager.cancel_transaction(transaction.transaction_id, "player1")

        # Verify original pending_transactions dict was not mutated
        assert transaction.transaction_id in original_pending  # Original unchanged
        assert (
            transaction.transaction_id not in manager._game_state.pending_transactions
        )  # New state updated

    def test_reject_nonexistent_transaction_from_gamestate(self) -> None:
        """Test rejecting a transaction that doesn't exist in GameState but exists in manager.

        This tests the safe removal behavior when GameState and manager cache are out of sync.

        Requirements: 5.3
        """
        # Setup
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)
        players = [player1, player2]
        game_state = GameState(players=players)

        galaxy = Mock()
        manager = EnhancedTransactionManager(galaxy, game_state)

        # Manually add transaction to manager cache but not GameState
        from datetime import datetime

        from ti4.core.rule_28_deals import ComponentTransaction

        transaction = ComponentTransaction(
            transaction_id="manual_tx",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        manager._transactions["manual_tx"] = transaction

        # Verify transaction is NOT in GameState
        assert "manual_tx" not in manager._game_state.pending_transactions

        # Reject should work without error (safe removal)
        result = manager.reject_transaction("manual_tx")
        assert result.success
        assert result.transaction.status == TransactionStatus.REJECTED

        # GameState should remain unchanged
        assert "manual_tx" not in manager._game_state.pending_transactions

    def test_cancel_nonexistent_transaction_from_gamestate(self) -> None:
        """Test cancelling a transaction that doesn't exist in GameState but exists in manager.

        This tests the safe removal behavior when GameState and manager cache are out of sync.

        Requirements: 5.4
        """
        # Setup
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)
        players = [player1, player2]
        game_state = GameState(players=players)

        galaxy = Mock()
        manager = EnhancedTransactionManager(galaxy, game_state)

        # Manually add transaction to manager cache but not GameState
        from datetime import datetime

        from ti4.core.rule_28_deals import ComponentTransaction

        transaction = ComponentTransaction(
            transaction_id="manual_tx",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        manager._transactions["manual_tx"] = transaction

        # Verify transaction is NOT in GameState
        assert "manual_tx" not in manager._game_state.pending_transactions

        # Cancel should work without error (safe removal)
        manager.cancel_transaction("manual_tx", "player1")

        # Verify transaction status updated in manager
        updated_transaction = manager.get_transaction("manual_tx")
        assert updated_transaction.status == TransactionStatus.CANCELLED

        # GameState should remain unchanged
        assert "manual_tx" not in manager._game_state.pending_transactions
