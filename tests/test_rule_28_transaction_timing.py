"""Tests for Rule 28: DEALS transaction timing and availability system.

This module tests the transaction timing and availability features for Rule 28 deals,
focusing on phase-independent transaction proposals, non-blocking processing,
and transaction queue management.

Requirements: 6.1, 6.2, 6.3, 6.4, 6.5
"""

from unittest.mock import Mock

from ti4.core.deals import (
    TransactionStatus,
)
from ti4.core.game_phase import GamePhase
from ti4.core.transactions import TransactionOffer


def create_mock_game_state_with_players() -> Mock:
    """Create a properly mocked game state with players for testing."""
    mock_game_state = Mock()

    # Mock players for validation
    mock_player1 = Mock()
    mock_player1.id = "player1"
    mock_player1.get_trade_goods.return_value = 10
    mock_player1.get_commodities.return_value = 5

    mock_player2 = Mock()
    mock_player2.id = "player2"
    mock_player2.get_trade_goods.return_value = 10
    mock_player2.get_commodities.return_value = 5

    mock_player3 = Mock()
    mock_player3.id = "player3"
    mock_player3.get_trade_goods.return_value = 10
    mock_player3.get_commodities.return_value = 5

    mock_player4 = Mock()
    mock_player4.id = "player4"
    mock_player4.get_trade_goods.return_value = 10
    mock_player4.get_commodities.return_value = 5

    mock_game_state.players = [mock_player1, mock_player2, mock_player3, mock_player4]
    mock_game_state.promissory_note_manager = Mock()
    mock_game_state.promissory_note_manager.get_player_hand.return_value = []

    # Set up the new GameState methods
    mock_game_state.pending_transactions = {}
    mock_game_state.transaction_history = []

    # Create Mock objects that can track calls
    mock_game_state.add_pending_transaction = Mock(return_value=mock_game_state)
    mock_game_state.apply_transaction_effects = Mock(return_value=mock_game_state)

    return mock_game_state


class TestTransactionTimingAndAvailability:
    """Test transaction timing and availability during different game phases.

    Requirements: 6.1, 6.2, 6.3, 6.4, 6.5
    """

    def test_transaction_proposal_allowed_during_any_phase(self) -> None:
        """Test that transaction proposals are allowed during any game phase.

        Requirements: 6.1
        """
        # RED: This will fail until we implement phase-independent transaction proposals
        from ti4.core.deals import EnhancedTransactionManager

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True
        mock_game_state = create_mock_game_state_with_players()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )

        # Test proposal during each game phase
        for phase in GamePhase:
            manager.set_game_phase(phase)

            result = manager.can_propose_transaction("player1", "player2")
            assert result is True, (
                f"Transaction proposal should be allowed during {phase.value} phase"
            )

    def test_non_blocking_transaction_processing_during_other_players_turns(
        self,
    ) -> None:
        """Test that transactions can be processed without interrupting game flow.

        Requirements: 6.2
        """
        # RED: This will fail until we implement non-blocking transaction processing
        from ti4.core.deals import EnhancedTransactionManager

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True
        mock_game_state = create_mock_game_state_with_players()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )

        # Set active player to player3 (different from transaction participants)
        manager.set_active_player("player3")

        # Should still allow transaction proposal between other players
        result = manager.can_propose_transaction("player1", "player2")
        assert result is True, (
            "Transaction proposal should be allowed during other players' turns"
        )

    def test_immediate_transaction_execution_upon_acceptance(self) -> None:
        """Test that transactions are executed immediately when accepted.

        Requirements: 6.3
        """
        # RED: This will fail until we implement immediate execution
        from ti4.core.deals import EnhancedTransactionManager

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True
        mock_game_state = create_mock_game_state_with_players()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )

        # Propose a transaction
        offer = TransactionOffer(trade_goods=3)
        request = TransactionOffer(commodities=2)

        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
        )

        assert transaction.status == TransactionStatus.PENDING

        # Accept the transaction
        result = manager.accept_transaction(transaction.transaction_id)

        assert result.success is True
        assert result.transaction.status == TransactionStatus.ACCEPTED
        assert result.transaction.completion_timestamp is not None

    def test_transaction_queue_management_for_multiple_pending_transactions(
        self,
    ) -> None:
        """Test that multiple pending transactions are processed in order.

        Requirements: 6.4
        """
        # RED: This will fail until we implement transaction queue management
        from ti4.core.deals import EnhancedTransactionManager

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True
        mock_game_state = create_mock_game_state_with_players()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )

        # Propose multiple transactions
        transaction1 = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
        )

        transaction2 = manager.propose_transaction(
            proposing_player="player3",
            target_player="player4",
            offer=TransactionOffer(trade_goods=2),
            request=TransactionOffer(commodities=2),
        )

        # Get pending transactions
        pending = manager.get_pending_transactions()
        assert len(pending) == 2
        assert pending[0].transaction_id == transaction1.transaction_id
        assert pending[1].transaction_id == transaction2.transaction_id

        # Accept transactions in order
        result1 = manager.accept_transaction(transaction1.transaction_id)
        result2 = manager.accept_transaction(transaction2.transaction_id)

        assert result1.success is True
        assert result2.success is True

        # Verify completion timestamps show order
        assert (
            result1.transaction.completion_timestamp
            <= result2.transaction.completion_timestamp
        )

    def test_immediate_game_state_updates_after_transaction_execution(self) -> None:
        """Test that game state is updated immediately after transaction execution.

        Requirements: 6.5
        """
        # RED: This will fail until we implement immediate game state updates
        from ti4.core.deals import EnhancedTransactionManager

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True
        mock_game_state = create_mock_game_state_with_players()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )

        # Propose and accept a transaction
        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
        )

        result = manager.accept_transaction(transaction.transaction_id)

        assert result.success is True

        # Verify that game state update methods were called
        # This will be mocked for now, but should verify actual resource transfers
        mock_game_state.apply_transaction_effects.assert_called_once()


class TestTransactionPhaseIntegration:
    """Test transaction integration with different game phases.

    Requirements: 6.1, 6.2
    """

    def test_transaction_proposal_during_setup_phase(self) -> None:
        """Test transaction proposals during setup phase.

        Requirements: 6.1
        """
        # RED: This will fail until we implement phase integration
        from ti4.core.deals import EnhancedTransactionManager

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True
        mock_game_state = create_mock_game_state_with_players()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )
        manager.set_game_phase(GamePhase.SETUP)

        result = manager.can_propose_transaction("player1", "player2")
        assert result is True

    def test_transaction_proposal_during_strategy_phase(self) -> None:
        """Test transaction proposals during strategy phase.

        Requirements: 6.1
        """
        from ti4.core.deals import EnhancedTransactionManager

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True
        mock_game_state = create_mock_game_state_with_players()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )
        manager.set_game_phase(GamePhase.STRATEGY)

        result = manager.can_propose_transaction("player1", "player2")
        assert result is True

    def test_transaction_proposal_during_action_phase(self) -> None:
        """Test transaction proposals during action phase.

        Requirements: 6.1
        """
        from ti4.core.deals import EnhancedTransactionManager

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True
        mock_game_state = create_mock_game_state_with_players()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )
        manager.set_game_phase(GamePhase.ACTION)

        result = manager.can_propose_transaction("player1", "player2")
        assert result is True

    def test_transaction_proposal_during_status_phase(self) -> None:
        """Test transaction proposals during status phase.

        Requirements: 6.1
        """
        from ti4.core.deals import EnhancedTransactionManager

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True
        mock_game_state = create_mock_game_state_with_players()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )
        manager.set_game_phase(GamePhase.STATUS)

        result = manager.can_propose_transaction("player1", "player2")
        assert result is True

    def test_transaction_proposal_during_agenda_phase(self) -> None:
        """Test transaction proposals during agenda phase.

        Requirements: 6.1
        """
        from ti4.core.deals import EnhancedTransactionManager

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True
        mock_game_state = create_mock_game_state_with_players()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )
        manager.set_game_phase(GamePhase.AGENDA)

        result = manager.can_propose_transaction("player1", "player2")
        assert result is True


class TestTransactionQueueManagement:
    """Test transaction queue management for multiple pending transactions.

    Requirements: 6.4
    """

    def test_transaction_queue_fifo_ordering(self) -> None:
        """Test that transactions are processed in first-in-first-out order.

        Requirements: 6.4
        """
        # RED: This will fail until we implement FIFO queue management
        from ti4.core.deals import EnhancedTransactionManager

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True
        mock_game_state = create_mock_game_state_with_players()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )

        # Propose transactions with slight time delays to ensure ordering
        import time

        _ = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
        )

        time.sleep(0.001)  # Small delay to ensure different timestamps

        _ = manager.propose_transaction(
            proposing_player="player3",
            target_player="player4",
            offer=TransactionOffer(trade_goods=2),
            request=TransactionOffer(commodities=2),
        )

        # Get pending transactions in order
        pending = manager.get_pending_transactions()
        assert len(pending) == 2
        assert pending[0].timestamp <= pending[1].timestamp

    def test_transaction_queue_removal_after_acceptance(self) -> None:
        """Test that transactions are removed from queue after acceptance.

        Requirements: 6.4
        """
        from ti4.core.deals import EnhancedTransactionManager

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True
        mock_game_state = create_mock_game_state_with_players()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )

        # Propose a transaction
        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
        )

        # Verify it's in the queue
        pending = manager.get_pending_transactions()
        assert len(pending) == 1

        # Accept the transaction
        manager.accept_transaction(transaction.transaction_id)

        # Verify it's removed from the queue
        pending = manager.get_pending_transactions()
        assert len(pending) == 0

    def test_transaction_queue_removal_after_rejection(self) -> None:
        """Test that transactions are removed from queue after rejection.

        Requirements: 6.4
        """
        from ti4.core.deals import EnhancedTransactionManager

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True
        mock_game_state = create_mock_game_state_with_players()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )

        # Propose a transaction
        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
        )

        # Verify it's in the queue
        pending = manager.get_pending_transactions()
        assert len(pending) == 1

        # Reject the transaction
        manager.reject_transaction(transaction.transaction_id)

        # Verify it's removed from the queue
        pending = manager.get_pending_transactions()
        assert len(pending) == 0


class TestTransactionExecutionTiming:
    """Test transaction execution timing and immediate effects.

    Requirements: 6.3, 6.5
    """

    def test_transaction_completion_timestamp_set_on_acceptance(self) -> None:
        """Test that completion timestamp is set when transaction is accepted.

        Requirements: 6.3
        """
        from ti4.core.deals import EnhancedTransactionManager

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True
        mock_game_state = create_mock_game_state_with_players()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )

        # Propose a transaction
        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
        )

        # Verify no completion timestamp initially
        assert transaction.completion_timestamp is None

        # Accept the transaction
        result = manager.accept_transaction(transaction.transaction_id)

        # Verify completion timestamp is set
        assert result.transaction.completion_timestamp is not None
        assert result.transaction.completion_timestamp >= transaction.timestamp

    def test_transaction_status_updated_immediately_on_acceptance(self) -> None:
        """Test that transaction status is updated immediately when accepted.

        Requirements: 6.3
        """
        from ti4.core.deals import EnhancedTransactionManager

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True
        mock_game_state = create_mock_game_state_with_players()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )

        # Propose a transaction
        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
        )

        # Verify initial status
        assert transaction.status == TransactionStatus.PENDING

        # Accept the transaction
        result = manager.accept_transaction(transaction.transaction_id)

        # Verify status is updated
        assert result.transaction.status == TransactionStatus.ACCEPTED

    def test_transaction_status_updated_immediately_on_rejection(self) -> None:
        """Test that transaction status is updated immediately when rejected.

        Requirements: 6.3
        """
        from ti4.core.deals import EnhancedTransactionManager

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True
        mock_game_state = create_mock_game_state_with_players()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )

        # Propose a transaction
        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
        )

        # Verify initial status
        assert transaction.status == TransactionStatus.PENDING

        # Reject the transaction
        result = manager.reject_transaction(transaction.transaction_id)

        # Verify status is updated
        assert result.transaction.status == TransactionStatus.REJECTED
