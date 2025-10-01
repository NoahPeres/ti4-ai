"""Tests for Rule 28: DEALS transaction API interface.

This module tests the clean API interface for transaction operations,
including status queries, history retrieval, and client integration points.

Requirements: 6.1, 7.2, 7.4
"""

from unittest.mock import Mock

from ti4.core.transactions import TransactionOffer


class TestTransactionAPI:
    """Test the clean API interface for transaction operations."""

    def test_transaction_api_creation(self) -> None:
        """Test that TransactionAPI can be created with required dependencies.

        RED: This test will fail until we create the TransactionAPI class.
        Requirements: 6.1
        """
        # Import will fail initially
        from ti4.core.deals import TransactionAPI

        # Mock dependencies
        mock_galaxy = Mock()
        mock_game_state = Mock()

        api = TransactionAPI(galaxy=mock_galaxy, game_state=mock_game_state)

        assert api is not None
        assert api._galaxy == mock_galaxy
        assert api._game_state == mock_game_state

    def test_propose_transaction_api(self) -> None:
        """Test API method for proposing transactions.

        RED: This test will fail until we implement propose_transaction method.
        Requirements: 6.1
        """
        from ti4.core.deals import TransactionAPI

        # Mock dependencies
        mock_galaxy = Mock()
        mock_game_state = Mock()

        api = TransactionAPI(galaxy=mock_galaxy, game_state=mock_game_state)

        # Test proposing a transaction
        result = api.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
        )

        assert result is not None
        assert hasattr(result, "success")
        assert hasattr(result, "transaction_id")

    def test_get_transaction_status_api(self) -> None:
        """Test API method for querying transaction status.

        RED: This test will fail until we implement get_transaction_status method.
        Requirements: 7.2
        """
        from ti4.core.deals import TransactionAPI

        # Mock dependencies
        mock_galaxy = Mock()
        mock_game_state = Mock()

        api = TransactionAPI(galaxy=mock_galaxy, game_state=mock_game_state)

        # Test getting transaction status for non-existent transaction
        status = api.get_transaction_status("tx_001")

        # Should return None for non-existent transaction
        assert status is None

        # Test that the method returns the correct type when transaction exists
        # (This will be tested in integration tests with real transactions)

    def test_get_transaction_history_api(self) -> None:
        """Test API method for retrieving transaction history.

        RED: This test will fail until we implement get_transaction_history method.
        Requirements: 7.4
        """
        from ti4.core.deals import TransactionAPI

        # Mock dependencies
        mock_galaxy = Mock()
        mock_game_state = Mock()

        api = TransactionAPI(galaxy=mock_galaxy, game_state=mock_game_state)

        # Test getting transaction history
        history = api.get_transaction_history("player1")

        assert isinstance(history, list)
        # Should return empty list initially
        assert len(history) == 0

    def test_accept_transaction_api(self) -> None:
        """Test API method for accepting transactions.

        RED: This test will fail until we implement accept_transaction method.
        Requirements: 6.1
        """
        from ti4.core.deals import TransactionAPI

        # Mock dependencies
        mock_galaxy = Mock()
        mock_game_state = Mock()

        api = TransactionAPI(galaxy=mock_galaxy, game_state=mock_game_state)

        # Test accepting a transaction
        result = api.accept_transaction("tx_001")

        assert result is not None
        assert hasattr(result, "success")
        assert hasattr(result, "transaction")

    def test_reject_transaction_api(self) -> None:
        """Test API method for rejecting transactions.

        RED: This test will fail until we implement reject_transaction method.
        Requirements: 6.1
        """
        from ti4.core.deals import TransactionAPI

        # Mock dependencies
        mock_galaxy = Mock()
        mock_game_state = Mock()

        api = TransactionAPI(galaxy=mock_galaxy, game_state=mock_game_state)

        # Test rejecting a transaction
        result = api.reject_transaction("tx_001")

        assert result is not None
        assert hasattr(result, "success")
        assert hasattr(result, "transaction_id")
