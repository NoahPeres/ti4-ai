"""Tests for robust observer notification pattern.

Requirements: 9.1, 9.2, 9.3, 9.4
"""

from datetime import datetime
from unittest.mock import Mock

from ti4.core.game_state import GameState
from ti4.core.rule_28_deals import (
    ComponentTransaction,
    TransactionOffer,
    TransactionStatus,
)


class TestObserverNotificationResilience:
    """Test that observer notifications are resilient to individual observer failures."""

    def test_observer_failure_does_not_prevent_other_notifications(self) -> None:
        """Test that if one observer fails, other observers still get notified.

        Requirements: 9.1, 9.2
        """
        # RED: This will fail until we implement try-catch blocks
        game_state = GameState()

        # Create observers - one that will fail, two that will succeed
        failing_observer = Mock()
        failing_observer.on_transaction_completed.side_effect = RuntimeError(
            "Observer failed"
        )

        successful_observer1 = Mock()
        successful_observer2 = Mock()

        # Register all observers
        game_state.register_transaction_observer(failing_observer)
        game_state.register_transaction_observer(successful_observer1)
        game_state.register_transaction_observer(successful_observer2)

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

        # This should not raise an exception despite the failing observer
        game_state.apply_transaction_effects(transaction)

        # Verify that successful observers were still notified
        successful_observer1.on_transaction_completed.assert_called_once_with(
            transaction
        )
        successful_observer2.on_transaction_completed.assert_called_once_with(
            transaction
        )

        # Verify the failing observer was attempted
        failing_observer.on_transaction_completed.assert_called_once_with(transaction)

    def test_multiple_observer_failures_do_not_prevent_successful_notifications(
        self,
    ) -> None:
        """Test that multiple observer failures don't prevent successful notifications.

        Requirements: 9.1, 9.2
        """
        # RED: This will fail until we implement try-catch blocks
        game_state = GameState()

        # Create multiple failing observers and one successful
        failing_observer1 = Mock()
        failing_observer1.on_transaction_completed.side_effect = ValueError(
            "First failure"
        )

        failing_observer2 = Mock()
        failing_observer2.on_transaction_completed.side_effect = TypeError(
            "Second failure"
        )

        successful_observer = Mock()

        # Register all observers
        game_state.register_transaction_observer(failing_observer1)
        game_state.register_transaction_observer(failing_observer2)
        game_state.register_transaction_observer(successful_observer)

        transaction = ComponentTransaction(
            transaction_id="tx_002",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # This should not raise an exception despite multiple failing observers
        game_state.apply_transaction_effects(transaction)

        # Verify the successful observer was still notified
        successful_observer.on_transaction_completed.assert_called_once_with(
            transaction
        )

        # Verify the failing observers were attempted
        failing_observer1.on_transaction_completed.assert_called_once_with(transaction)
        failing_observer2.on_transaction_completed.assert_called_once_with(transaction)

    def test_observer_without_required_method_is_skipped_safely(self) -> None:
        """Test that observers without on_transaction_completed method are skipped safely.

        Requirements: 9.1, 9.2
        """
        game_state = GameState()

        # Create observer without the required method
        invalid_observer = Mock()
        del invalid_observer.on_transaction_completed  # Remove the method

        valid_observer = Mock()

        # Register both observers
        game_state.register_transaction_observer(invalid_observer)
        game_state.register_transaction_observer(valid_observer)

        transaction = ComponentTransaction(
            transaction_id="tx_003",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=2),
            request=TransactionOffer(commodities=1),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # This should not raise an exception
        game_state.apply_transaction_effects(transaction)

        # Verify the valid observer was notified
        valid_observer.on_transaction_completed.assert_called_once_with(transaction)

    def test_all_observers_fail_does_not_break_transaction_processing(self) -> None:
        """Test that transaction processing completes even if all observers fail.

        Requirements: 9.1, 9.2
        """
        # RED: This will fail until we implement try-catch blocks
        game_state = GameState()

        # Create multiple failing observers
        failing_observer1 = Mock()
        failing_observer1.on_transaction_completed.side_effect = Exception("Failure 1")

        failing_observer2 = Mock()
        failing_observer2.on_transaction_completed.side_effect = RuntimeError(
            "Failure 2"
        )

        # Register failing observers
        game_state.register_transaction_observer(failing_observer1)
        game_state.register_transaction_observer(failing_observer2)

        transaction = ComponentTransaction(
            transaction_id="tx_004",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # This should not raise an exception despite all observers failing
        result_state = game_state.apply_transaction_effects(transaction)

        # Verify transaction was still processed (new state created)
        assert result_state is not game_state

        # Verify both failing observers were attempted
        failing_observer1.on_transaction_completed.assert_called_once_with(transaction)
        failing_observer2.on_transaction_completed.assert_called_once_with(transaction)

    def test_observer_failure_logs_warning_message(self) -> None:
        """Test that observer failures are logged with appropriate warning messages.

        Requirements: 9.3
        """
        import logging
        from unittest.mock import patch

        game_state = GameState()

        # Create a failing observer
        failing_observer = Mock()
        failing_observer.on_transaction_completed.side_effect = ValueError(
            "Test failure"
        )

        game_state.register_transaction_observer(failing_observer)

        transaction = ComponentTransaction(
            transaction_id="tx_log_test",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # Capture logging output
        with patch.object(logging, "warning") as mock_warning:
            game_state.apply_transaction_effects(transaction)

            # Verify that a warning was logged
            mock_warning.assert_called_once()
            logged_message = mock_warning.call_args[0][0]
            assert "Transaction observer failed" in logged_message
            assert "Test failure" in logged_message
            assert "Continuing with remaining observers" in logged_message
