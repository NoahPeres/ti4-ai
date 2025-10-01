"""Test transaction history consolidation to use GameState as single source of truth.

This module tests that all transaction history operations delegate to GameState
methods and that there is no duplicate history management.
"""

from datetime import datetime
from unittest.mock import Mock

import pytest

from ti4.core.deals import (
    ComponentTransaction,
    EnhancedTransactionManager,
    TransactionHistoryEntry,
    TransactionStatus,
)
from ti4.core.game_state import GameState
from ti4.core.transactions import TransactionOffer


class TestTransactionHistoryConsolidation:
    """Test that transaction history uses GameState as single source of truth."""

    def test_transaction_manager_delegates_history_to_gamestate(self) -> None:
        """Test that transaction manager gets history from GameState, not its own cache.

        Requirements: 11.1, 11.2
        """
        # Create a mock GameState with transaction history
        mock_game_state = Mock(spec=GameState)
        mock_game_state.transaction_history = [
            TransactionHistoryEntry(
                transaction_id="tx_001",
                proposing_player="player1",
                target_player="player2",
                offer=TransactionOffer(trade_goods=5),
                request=TransactionOffer(commodities=3),
                status=TransactionStatus.ACCEPTED,
                timestamp=datetime.now(),
                completion_timestamp=datetime.now(),
            )
        ]

        # Create mock galaxy
        mock_galaxy = Mock()

        # Create transaction manager
        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )

        # Get history should delegate to GameState, not use manager's own cache
        history = manager.get_transaction_history("player1")

        # Should get history from GameState.transaction_history, not manager cache
        assert len(history) == 1
        assert history[0].transaction_id == "tx_001"

    def test_no_duplicate_transaction_history_manager_class(self) -> None:
        """Test that TransactionHistoryManager class is removed.

        Requirements: 11.1
        """
        # TransactionHistoryManager should not exist as a separate class
        with pytest.raises(ImportError):
            from ti4.core.deals import TransactionHistoryManager  # noqa: F401

    def test_gamestate_is_single_source_of_truth(self) -> None:
        """Test that GameState is the only place transaction history is stored.

        Requirements: 11.3, 11.4
        """
        # Create real GameState
        game_state = GameState()

        # Add transaction to GameState history
        entry = TransactionHistoryEntry(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=5),
            request=TransactionOffer(commodities=3),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        new_state = game_state.add_transaction_to_history(entry)

        # Verify GameState has the history
        assert len(new_state.transaction_history) == 1
        assert new_state.transaction_history[0].transaction_id == "tx_001"

        # Create transaction manager with this GameState
        mock_galaxy = Mock()
        manager = EnhancedTransactionManager(galaxy=mock_galaxy, game_state=new_state)

        # Manager should get history from GameState
        history = manager.get_transaction_history("player1")
        assert len(history) == 1
        assert history[0].transaction_id == "tx_001"

    def test_transaction_manager_adds_to_gamestate_history(self) -> None:
        """Test that transaction manager adds completed transactions to GameState history.

        Requirements: 11.2, 11.4
        """
        # Create GameState
        game_state = GameState()

        # Create transaction manager
        mock_galaxy = Mock()
        manager = EnhancedTransactionManager(galaxy=mock_galaxy, game_state=game_state)

        # Create and accept a transaction
        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=5),
            request=TransactionOffer(commodities=3),
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        # Mock the resource manager to avoid actual transfers
        manager._resource_manager = Mock()
        manager._resource_manager.transfer_trade_goods = Mock()
        manager._resource_manager.transfer_commodities = Mock()

        # Propose and accept transaction
        manager._transactions[transaction.transaction_id] = transaction
        result = manager.accept_transaction(transaction.transaction_id)

        # Transaction should be added to GameState history
        assert result.success
        assert len(manager._game_state.transaction_history) == 1
        assert manager._game_state.transaction_history[0].transaction_id == "tx_001"
