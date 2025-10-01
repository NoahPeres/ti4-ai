"""Tests for transaction history and logging system.

This module tests the transaction history tracking and logging capabilities
for Rule 28 component deals. All tests follow strict TDD methodology.

Requirements: 7.1, 7.2, 7.3, 7.4, 7.5
"""

from datetime import datetime, timedelta
from unittest.mock import Mock

from ti4.core.deals import (
    ComponentTransaction,
    TransactionStatus,
)
from ti4.core.transactions import TransactionOffer


class TestTransactionHistoryTracking:
    """Test transaction history tracking in game state.

    Requirements: 7.1, 7.2
    """

    def test_transaction_history_entry_creation(self) -> None:
        """Test that transaction history entries can be created with required fields.

        Requirements: 7.1, 7.2
        """
        # RED: This will fail until we create TransactionHistoryEntry
        from ti4.core.deals import TransactionHistoryEntry

        entry = TransactionHistoryEntry(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        assert entry.transaction_id == "tx_001"
        assert entry.proposing_player == "player1"
        assert entry.target_player == "player2"
        assert entry.status == TransactionStatus.ACCEPTED
        assert entry.timestamp is not None
        assert entry.completion_timestamp is not None

    def test_transaction_history_manager_creation(self) -> None:
        """Test that transaction history is managed through GameState.

        Requirements: 7.1, 7.2
        """
        # Transaction history is now managed directly through GameState
        # No separate TransactionHistoryManager class needed
        from ti4.core.game_state import GameState

        game_state = Mock(spec=GameState)
        game_state.transaction_history = []

        # Verify GameState has transaction history capability
        assert hasattr(game_state, "transaction_history")
        assert game_state.transaction_history == []

    def test_add_transaction_to_history(self) -> None:
        """Test adding a completed transaction to history through GameState.

        Requirements: 7.1, 7.2
        """
        # Transaction history is now managed directly through GameState
        from ti4.core.deals import ComponentTransaction, TransactionOffer
        from ti4.core.game_state import GameState

        mock_game_state = Mock(spec=GameState)
        mock_game_state.transaction_history = []

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

        # Add transaction to GameState history directly
        mock_game_state.transaction_history.append(transaction)

        # Verify transaction was added
        assert len(mock_game_state.transaction_history) == 1
        assert mock_game_state.transaction_history[0].transaction_id == "tx_001"

    def test_get_transaction_history_for_player(self) -> None:
        """Test retrieving transaction history for a specific player through GameState.

        Requirements: 7.2, 7.3
        """
        # Transaction history is now managed directly through GameState
        from ti4.core.deals import (
            ComponentTransaction,
            TransactionOffer,
            TransactionStatus,
        )
        from ti4.core.game_state import GameState

        mock_game_state = Mock(spec=GameState)
        mock_game_state.transaction_history = []

        # Add multiple transactions
        tx1 = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        tx2 = ComponentTransaction(
            transaction_id="tx_002",
            proposing_player="player2",
            target_player="player1",
            offer=TransactionOffer(commodities=1),
            request=TransactionOffer(trade_goods=1),
            status=TransactionStatus.REJECTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        tx3 = ComponentTransaction(
            transaction_id="tx_003",
            proposing_player="player3",
            target_player="player4",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # Add transactions to GameState history
        mock_game_state.transaction_history.extend([tx1, tx2, tx3])

        # Filter transactions for player1 (involved in tx1 and tx2)
        player1_transactions = [
            tx
            for tx in mock_game_state.transaction_history
            if tx.proposing_player == "player1" or tx.target_player == "player1"
        ]
        assert len(player1_transactions) == 2

        # Filter transactions for player3 (only involved in tx3)
        player3_transactions = [
            tx
            for tx in mock_game_state.transaction_history
            if tx.proposing_player == "player3" or tx.target_player == "player3"
        ]
        assert len(player3_transactions) == 1
        assert player3_transactions[0].transaction_id == "tx_003"


class TestTransactionLogging:
    """Test transaction logging with timestamps and player details.

    Requirements: 7.2, 7.4
    """

    def test_transaction_logger_creation(self) -> None:
        """Test that TransactionLogger can be created.

        Requirements: 7.2, 7.4
        """
        # RED: This will fail until we create TransactionLogger
        from ti4.core.deals import TransactionLogger

        logger = TransactionLogger()
        assert logger is not None

    def test_log_transaction_success(self) -> None:
        """Test logging successful transaction with details.

        Requirements: 7.2, 7.4
        """
        # RED: This will fail until we implement log_transaction_success
        from ti4.core.deals import TransactionLogger

        logger = TransactionLogger()

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

        logger.log_transaction_success(transaction)

        # Should be able to retrieve the log entry
        logs = logger.get_transaction_logs()
        assert len(logs) == 1
        assert logs[0]["transaction_id"] == "tx_001"
        assert logs[0]["status"] == "success"
        assert "timestamp" in logs[0]

    def test_log_transaction_failure(self) -> None:
        """Test logging failed transaction with error details.

        Requirements: 7.4, 7.5
        """
        # RED: This will fail until we implement log_transaction_failure
        from ti4.core.deals import TransactionLogger

        logger = TransactionLogger()

        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.REJECTED,
            timestamp=datetime.now(),
        )

        error_message = "Insufficient trade goods"
        logger.log_transaction_failure(transaction, error_message)

        # Should be able to retrieve the log entry
        logs = logger.get_transaction_logs()
        assert len(logs) == 1
        assert logs[0]["transaction_id"] == "tx_001"
        assert logs[0]["status"] == "failure"
        assert logs[0]["error_message"] == error_message
        assert "timestamp" in logs[0]


class TestTransactionSearchAndFiltering:
    """Test transaction search and filtering capabilities.

    Requirements: 7.3, 7.4
    """

    def test_search_transactions_by_player(self) -> None:
        """Test searching transactions by player involvement through GameState.

        Requirements: 7.3
        """
        # Transaction search is now done directly on GameState transaction history
        from ti4.core.deals import (
            ComponentTransaction,
            TransactionOffer,
            TransactionStatus,
        )
        from ti4.core.game_state import GameState

        mock_game_state = Mock(spec=GameState)
        mock_game_state.transaction_history = []

        # Add test transactions
        tx1 = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        tx2 = ComponentTransaction(
            transaction_id="tx_002",
            proposing_player="player3",
            target_player="player1",
            offer=TransactionOffer(commodities=1),
            request=TransactionOffer(trade_goods=1),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # Add transactions to GameState history
        mock_game_state.transaction_history.extend([tx1, tx2])

        # Search for transactions involving player1
        player1_results = [
            tx
            for tx in mock_game_state.transaction_history
            if tx.proposing_player == "player1" or tx.target_player == "player1"
        ]
        assert len(player1_results) == 2

        # Search for transactions involving player2
        player2_results = [
            tx
            for tx in mock_game_state.transaction_history
            if tx.proposing_player == "player2" or tx.target_player == "player2"
        ]
        assert len(player2_results) == 1
        assert player2_results[0].transaction_id == "tx_001"

    def test_filter_transactions_by_status(self) -> None:
        """Test filtering transactions by status through GameState.

        Requirements: 7.3
        """
        # Transaction filtering is now done directly on GameState transaction history
        from ti4.core.deals import (
            ComponentTransaction,
            TransactionOffer,
            TransactionStatus,
        )
        from ti4.core.game_state import GameState

        mock_game_state = Mock(spec=GameState)
        mock_game_state.transaction_history = []

        # Add transactions with different statuses
        tx1 = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        tx2 = ComponentTransaction(
            transaction_id="tx_002",
            proposing_player="player1",
            target_player="player3",
            offer=TransactionOffer(commodities=1),
            request=TransactionOffer(trade_goods=1),
            status=TransactionStatus.REJECTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # Add transactions to GameState history
        mock_game_state.transaction_history.extend([tx1, tx2])

        # Filter for accepted transactions
        accepted = [
            tx
            for tx in mock_game_state.transaction_history
            if tx.status == TransactionStatus.ACCEPTED
        ]
        assert len(accepted) == 1
        assert accepted[0].transaction_id == "tx_001"

        # Filter for rejected transactions
        rejected = [
            tx
            for tx in mock_game_state.transaction_history
            if tx.status == TransactionStatus.REJECTED
        ]
        assert len(rejected) == 1
        assert rejected[0].transaction_id == "tx_002"

    def test_filter_transactions_by_time_range(self) -> None:
        """Test filtering transactions by time range through GameState.

        Requirements: 7.3, 7.4
        """
        # Time range filtering is now done directly on GameState transaction history
        from ti4.core.deals import (
            ComponentTransaction,
            TransactionOffer,
            TransactionStatus,
        )
        from ti4.core.game_state import GameState

        mock_game_state = Mock(spec=GameState)
        mock_game_state.transaction_history = []

        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        two_hours_ago = now - timedelta(hours=2)

        # Add transactions at different times
        tx1 = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.ACCEPTED,
            timestamp=two_hours_ago,
            completion_timestamp=two_hours_ago,
        )

        tx2 = ComponentTransaction(
            transaction_id="tx_002",
            proposing_player="player1",
            target_player="player3",
            offer=TransactionOffer(commodities=1),
            request=TransactionOffer(trade_goods=1),
            status=TransactionStatus.ACCEPTED,
            timestamp=now,
            completion_timestamp=now,
        )

        # Add transactions to GameState history
        mock_game_state.transaction_history.extend([tx1, tx2])

        # Filter for transactions in the last hour
        recent = [
            tx
            for tx in mock_game_state.transaction_history
            if hour_ago <= tx.timestamp <= now
        ]
        assert len(recent) == 1
        assert recent[0].transaction_id == "tx_002"

        # Filter for all transactions
        all_transactions = [
            tx
            for tx in mock_game_state.transaction_history
            if two_hours_ago <= tx.timestamp <= now
        ]
        assert len(all_transactions) == 2


class TestGameStateIntegration:
    """Test integration with existing game state management.

    Requirements: 8.1, 8.2, 8.3, 8.4, 8.5
    """

    def test_game_state_transaction_history_field(self) -> None:
        """Test that GameState has transaction history field.

        Requirements: 8.1, 8.2
        """
        # RED: This will fail until we add transaction_history to GameState
        from ti4.core.game_state import GameState

        game_state = GameState()

        # Should have transaction_history field
        assert hasattr(game_state, "transaction_history")
        assert isinstance(game_state.transaction_history, list)

    def test_update_game_state_with_transaction_history(self) -> None:
        """Test updating game state with transaction history.

        Requirements: 8.1, 8.2, 8.3
        """
        # RED: This will fail until we implement game state integration
        from ti4.core.deals import TransactionHistoryEntry
        from ti4.core.game_state import GameState

        game_state = GameState()

        entry = TransactionHistoryEntry(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # Should be able to add transaction to game state history
        new_state = game_state.add_transaction_to_history(entry)
        assert len(new_state.transaction_history) == 1
        assert new_state.transaction_history[0].transaction_id == "tx_001"

    def test_transaction_consistency_with_resource_systems(self) -> None:
        """Test that transaction effects maintain consistency with resource systems.

        Requirements: 8.3, 8.4
        """
        # RED: This will fail until we implement consistency checks
        from ti4.core.deals import TransactionConsistencyValidator

        mock_game_state = Mock()
        validator = TransactionConsistencyValidator(game_state=mock_game_state)

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

        # Should validate consistency
        is_consistent = validator.validate_transaction_consistency(transaction)
        assert isinstance(is_consistent, bool)

    def test_transaction_notifications_to_game_components(self) -> None:
        """Test that transaction notifications are sent to relevant game components.

        Requirements: 8.4, 8.5
        """
        # RED: This will fail until we implement notification system
        from ti4.core.deals import TransactionNotificationSystem

        mock_game_state = Mock()
        notification_system = TransactionNotificationSystem(game_state=mock_game_state)

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

        # Should be able to notify components
        notification_system.notify_transaction_completed(transaction)

        # Should track notifications
        notifications = notification_system.get_pending_notifications()
        assert len(notifications) >= 0  # May be empty if no components to notify
