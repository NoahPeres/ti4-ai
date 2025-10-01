"""Integration tests for Rule 28: DEALS transaction API.

This module tests the complete integration of the transaction API with
the underlying transaction management system.

Requirements: 6.1, 7.2, 7.4
"""

from unittest.mock import Mock

from ti4.core.rule_28_deals import (
    TransactionAPI,
    TransactionStatus,
)
from ti4.core.transactions import TransactionOffer


class TestTransactionAPIIntegration:
    """Test complete integration scenarios for the transaction API."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        # Create mock dependencies
        self.mock_galaxy = Mock()
        self.mock_game_state = Mock()

        # Mock galaxy neighbor validation to return True by default
        self.mock_galaxy.are_players_neighbors.return_value = True

        # Mock game state players
        self.mock_player1 = Mock()
        self.mock_player1.id = "player1"
        self.mock_player1.get_trade_goods.return_value = 10
        self.mock_player1.get_commodities.return_value = 5
        self.mock_player1.spend_trade_goods.return_value = True
        self.mock_player1.gain_trade_goods.return_value = None

        self.mock_player2 = Mock()
        self.mock_player2.id = "player2"
        self.mock_player2.get_trade_goods.return_value = 8
        self.mock_player2.get_commodities.return_value = 3
        self.mock_player2.spend_trade_goods.return_value = True
        self.mock_player2.gain_trade_goods.return_value = None

        self.mock_game_state.players = [self.mock_player1, self.mock_player2]

        # Mock promissory note manager
        self.mock_promissory_manager = Mock()
        self.mock_promissory_manager.get_player_hand.return_value = []
        self.mock_game_state.promissory_note_manager = self.mock_promissory_manager

        # Create API instance
        self.api = TransactionAPI(self.mock_galaxy, self.mock_game_state)

    def test_complete_transaction_flow(self) -> None:
        """Test complete transaction flow from proposal to acceptance.

        Requirements: 6.1, 7.2
        """
        # Propose a transaction
        offer = TransactionOffer(trade_goods=3)
        request = TransactionOffer(commodities=2)

        result = self.api.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
        )

        # Verify proposal succeeded
        assert result.success is True
        assert result.transaction_id is not None
        assert result.transaction is not None

        transaction_id = result.transaction_id

        # Check transaction status
        status = self.api.get_transaction_status(transaction_id)
        assert status is not None
        assert status.transaction_id == transaction_id
        assert status.status == TransactionStatus.PENDING
        assert status.proposing_player == "player1"
        assert status.target_player == "player2"

        # Accept the transaction
        accept_result = self.api.accept_transaction(transaction_id)
        assert accept_result.success is True

        # Verify transaction is now completed
        final_status = self.api.get_transaction_status(transaction_id)
        assert final_status is not None
        assert final_status.status == TransactionStatus.ACCEPTED

    def test_transaction_rejection_flow(self) -> None:
        """Test transaction rejection flow.

        Requirements: 6.1
        """
        # Propose a transaction
        offer = TransactionOffer(trade_goods=1)
        request = TransactionOffer(commodities=1)

        result = self.api.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
        )

        assert result.success is True
        transaction_id = result.transaction_id

        # Reject the transaction
        reject_result = self.api.reject_transaction(transaction_id)
        assert reject_result.success is True

        # Verify transaction is now rejected
        status = self.api.get_transaction_status(transaction_id)
        assert status is not None
        assert status.status == TransactionStatus.REJECTED

    def test_transaction_history_tracking(self) -> None:
        """Test transaction history tracking.

        Requirements: 7.4
        """
        # Initially no history
        history = self.api.get_transaction_history("player1")
        assert len(history) == 0

        # Propose and complete a transaction
        offer = TransactionOffer(trade_goods=2)
        request = TransactionOffer(commodities=1)

        result = self.api.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
        )

        transaction_id = result.transaction_id
        self.api.accept_transaction(transaction_id)

        # Check history now includes the transaction
        history = self.api.get_transaction_history("player1")
        assert len(history) >= 1

        # Find our transaction in history
        our_transaction = next(
            (t for t in history if t.transaction_id == transaction_id), None
        )
        assert our_transaction is not None
        assert our_transaction.proposing_player == "player1"
        assert our_transaction.target_player == "player2"

    def test_pending_transactions_tracking(self) -> None:
        """Test pending transactions tracking."""
        # Initially no pending transactions
        pending = self.api.get_pending_transactions("player1")
        assert len(pending) == 0

        # Propose a transaction
        offer = TransactionOffer(trade_goods=1)
        request = TransactionOffer(commodities=1)

        result = self.api.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
        )

        transaction_id = result.transaction_id

        # Check pending transactions for both players
        player1_pending = self.api.get_pending_transactions("player1")
        player2_pending = self.api.get_pending_transactions("player2")

        # Transaction should appear in both players' pending lists
        assert len(player1_pending) >= 1
        assert len(player2_pending) >= 1

        # Accept the transaction
        self.api.accept_transaction(transaction_id)

        # Pending lists should be updated (transaction no longer pending)
        player1_pending_after = self.api.get_pending_transactions("player1")
        player2_pending_after = self.api.get_pending_transactions("player2")

        # The specific transaction should no longer be pending for either player
        player1_pending_ids_after = [t.transaction_id for t in player1_pending_after]
        player2_pending_ids_after = [t.transaction_id for t in player2_pending_after]
        assert transaction_id not in player1_pending_ids_after
        assert transaction_id not in player2_pending_ids_after

    def test_input_validation_errors(self) -> None:
        """Test API input validation error handling."""
        # Test empty player IDs
        result = self.api.propose_transaction(
            proposing_player="",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
        )
        assert result.success is False
        assert "Player ID cannot be empty" in result.error_message

        # Test same player transaction
        result = self.api.propose_transaction(
            proposing_player="player1",
            target_player="player1",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
        )
        assert result.success is False
        assert "cannot transact with themselves" in result.error_message

        # Test invalid transaction ID
        status = self.api.get_transaction_status("")
        assert status is None

        # Test invalid player ID for history
        history = self.api.get_transaction_history("")
        assert len(history) == 0

    def test_non_existent_transaction_handling(self) -> None:
        """Test handling of non-existent transactions."""
        # Test getting status of non-existent transaction
        status = self.api.get_transaction_status("non_existent_tx")
        assert status is None

        # Test accepting non-existent transaction
        result = self.api.accept_transaction("non_existent_tx")
        assert result.success is False
        assert result.error_message is not None

        # Test rejecting non-existent transaction
        result = self.api.reject_transaction("non_existent_tx")
        assert result.success is False
        assert result.error_message is not None

    def test_api_error_resilience(self) -> None:
        """Test API resilience to underlying system errors."""
        # Create API with broken dependencies to test error handling
        broken_galaxy = Mock()
        broken_galaxy.are_players_neighbors.side_effect = Exception("Galaxy error")

        broken_api = TransactionAPI(broken_galaxy, self.mock_game_state)

        # API should handle errors gracefully
        result = broken_api.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
        )

        # Should return error result, not raise exception
        assert result.success is False
        assert result.error_message is not None

        # History and status queries should return safe defaults
        history = broken_api.get_transaction_history("player1")
        assert isinstance(history, list)
        assert len(history) == 0

        status = broken_api.get_transaction_status("any_id")
        assert status is None
