"""Tests for TransactionAPI GameState access functionality.

This module tests that the TransactionAPI provides access to updated GameState
after transaction operations, as required by Requirement 12.

Requirements: 12.1, 12.2, 12.3, 12.4
"""

from unittest.mock import Mock

from ti4.core.rule_28_deals import TransactionAPI, TransactionAPIResult
from ti4.core.transactions import TransactionOffer


class TestTransactionAPIGameStateAccess:
    """Test GameState access functionality in TransactionAPI."""

    def test_get_game_state_method_exists(self) -> None:
        """Test that TransactionAPI has a get_game_state method.

        RED: This test will fail until we add the get_game_state method.
        Requirements: 12.1, 12.3
        """
        # Mock dependencies
        mock_galaxy = Mock()
        mock_game_state = Mock()

        api = TransactionAPI(galaxy=mock_galaxy, game_state=mock_game_state)

        # Test that get_game_state method exists
        assert hasattr(api, "get_game_state")
        assert callable(api.get_game_state)

    def test_get_game_state_returns_current_state(self) -> None:
        """Test that get_game_state returns the current GameState.

        RED: This test will fail until we implement get_game_state properly.
        Requirements: 12.1, 12.3
        """
        # Mock dependencies
        mock_galaxy = Mock()
        mock_game_state = Mock()

        api = TransactionAPI(galaxy=mock_galaxy, game_state=mock_game_state)

        # Test that get_game_state returns the current state
        current_state = api.get_game_state()
        assert current_state is mock_game_state

    def test_game_state_updated_after_transaction_operations(self) -> None:
        """Test that GameState is updated after transaction operations.

        RED: This test will fail until we ensure GameState is properly updated.
        Requirements: 12.1, 12.4
        """
        # Mock dependencies
        mock_galaxy = Mock()
        initial_game_state = Mock()
        updated_game_state = Mock()

        # Mock the transaction manager to return updated state
        mock_transaction_manager = Mock()
        mock_transaction_manager._game_state = updated_game_state

        api = TransactionAPI(galaxy=mock_galaxy, game_state=initial_game_state)
        api._transaction_manager = mock_transaction_manager

        # After operations, get_game_state should return updated state
        current_state = api.get_game_state()
        assert current_state is updated_game_state

    def test_transaction_api_result_includes_game_state_access(self) -> None:
        """Test that TransactionAPIResult provides access to GameState.

        RED: This test will fail until we add GameState access to results.
        Requirements: 12.2
        """
        # Create a result with game_state access
        mock_game_state = Mock()

        result = TransactionAPIResult(
            success=True, transaction_id="tx_001", game_state=mock_game_state
        )

        # Test that result has game_state attribute
        assert hasattr(result, "game_state")
        assert result.game_state is mock_game_state

    def test_propose_transaction_provides_updated_state_access(self) -> None:
        """Test that propose_transaction result provides access to updated state.

        RED: This test will fail until we include GameState in results.
        Requirements: 12.1, 12.2, 12.4
        """
        # Mock dependencies
        mock_galaxy = Mock()
        mock_game_state = Mock()
        updated_game_state = Mock()

        # Mock transaction manager to simulate state update
        mock_transaction_manager = Mock()
        mock_transaction_manager.propose_transaction.return_value = Mock(
            transaction_id="tx_001"
        )
        mock_transaction_manager._game_state = updated_game_state

        api = TransactionAPI(galaxy=mock_galaxy, game_state=mock_game_state)
        api._transaction_manager = mock_transaction_manager

        # Propose a transaction
        result = api.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
        )

        # Result should provide access to updated GameState
        assert result.success is True
        # Either through direct attribute or through API method
        current_state = api.get_game_state()
        assert current_state is updated_game_state

    def test_accept_transaction_provides_updated_state_access(self) -> None:
        """Test that accept_transaction result provides access to updated state.

        RED: This test will fail until we include GameState in results.
        Requirements: 12.1, 12.2, 12.4
        """
        # Mock dependencies
        mock_galaxy = Mock()
        mock_game_state = Mock()
        updated_game_state = Mock()

        # Mock transaction manager to simulate state update
        mock_transaction_manager = Mock()
        mock_result = Mock()
        mock_result.success = True
        mock_result.transaction = Mock()
        mock_result.error_message = None
        mock_transaction_manager.accept_transaction.return_value = mock_result
        mock_transaction_manager._game_state = updated_game_state

        api = TransactionAPI(galaxy=mock_galaxy, game_state=mock_game_state)
        api._transaction_manager = mock_transaction_manager

        # Accept a transaction
        result = api.accept_transaction("tx_001")

        # Result should provide access to updated GameState
        assert result.success is True
        # Either through direct attribute or through API method
        current_state = api.get_game_state()
        assert current_state is updated_game_state

    def test_api_maintains_state_consistency_across_operations(self) -> None:
        """Test that API maintains GameState consistency across multiple operations.

        RED: This test will fail until we ensure proper state synchronization.
        Requirements: 12.3, 12.4
        """
        # Mock dependencies
        mock_galaxy = Mock()
        initial_game_state = Mock()

        api = TransactionAPI(galaxy=mock_galaxy, game_state=initial_game_state)

        # Initial state should be accessible
        assert api.get_game_state() is initial_game_state

        # After any operation that modifies state, get_game_state should return updated state
        # This will be tested with real operations in integration tests
        # For now, just verify the method exists and returns consistently
        state1 = api.get_game_state()
        state2 = api.get_game_state()
        assert state1 is state2  # Should return same reference consistently
