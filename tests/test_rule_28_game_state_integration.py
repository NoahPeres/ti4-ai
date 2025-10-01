"""Tests for Rule 28 game state integration.

This module tests the integration between Rule 28 component transactions
and the existing game state management system.

Requirements: 8.1, 8.2, 8.3, 8.4, 8.5
"""

from datetime import datetime
from unittest.mock import Mock

from ti4.core.constants import Faction
from ti4.core.deals import (
    ComponentTransaction,
    TransactionStatus,
)
from ti4.core.game_state import GameState
from ti4.core.player import Player
from ti4.core.transactions import PromissoryNote, PromissoryNoteType, TransactionOffer


class TestGameStateTransactionTracking:
    """Test game state tracking of pending and completed transactions.

    Requirements: 8.1
    """

    def test_duplicate_transaction_id_prevention(self) -> None:
        """Test that duplicate transaction IDs are prevented.

        Requirements: 1.1, 1.2, 1.3
        """
        # RED: This will fail until we implement duplicate ID validation
        game_state = GameState()

        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        # Add first transaction
        new_state = game_state.add_pending_transaction(transaction)
        assert new_state is not game_state  # Immutability check
        assert len(new_state.pending_transactions) == 1

        # Attempt to add duplicate transaction ID
        duplicate_transaction = ComponentTransaction(
            transaction_id="tx_001",  # Same ID
            proposing_player="player2",
            target_player="player3",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        # Should raise ValueError with descriptive message including transaction ID
        try:
            new_state.add_pending_transaction(duplicate_transaction)
            assert False, "Should have raised ValueError for duplicate transaction ID"
        except ValueError as e:
            error_message = str(e)
            assert "tx_001" in error_message, (
                f"Error message should include transaction ID: {error_message}"
            )
            assert "already exists" in error_message.lower(), (
                f"Error message should indicate duplication: {error_message}"
            )
            assert "pending transaction" in error_message.lower(), (
                f"Error message should specify pending transaction: {error_message}"
            )

    def test_game_state_tracks_pending_transactions(self) -> None:
        """Test that game state can track pending transactions.

        Requirements: 8.1
        """
        # RED: This will fail until we implement pending transaction tracking
        game_state = GameState()

        # Should have a field to track pending transactions
        assert hasattr(game_state, "pending_transactions")
        assert isinstance(game_state.pending_transactions, dict)

        # Should be able to add pending transactions
        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        new_state = game_state.add_pending_transaction(transaction)
        assert len(new_state.pending_transactions) == 1
        assert "tx_001" in new_state.pending_transactions

    def test_game_state_removes_completed_transactions_from_pending(self) -> None:
        """Test that completed transactions are removed from pending list.

        Requirements: 8.1
        """
        # RED: This will fail until we implement transaction completion handling
        game_state = GameState()

        # Add a pending transaction
        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        state_with_pending = game_state.add_pending_transaction(transaction)
        assert len(state_with_pending.pending_transactions) == 1

        # Complete the transaction
        completed_transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.ACCEPTED,
            timestamp=transaction.timestamp,
            completion_timestamp=datetime.now(),
        )

        final_state = state_with_pending.complete_transaction(completed_transaction)
        assert len(final_state.pending_transactions) == 0
        assert len(final_state.transaction_history) == 1

    def test_game_state_tracks_multiple_pending_transactions(self) -> None:
        """Test that game state can track multiple pending transactions.

        Requirements: 8.1
        """
        # RED: This will fail until we implement multiple transaction tracking
        game_state = GameState()

        transaction1 = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        transaction2 = ComponentTransaction(
            transaction_id="tx_002",
            proposing_player="player2",
            target_player="player3",
            offer=TransactionOffer(commodities=1),
            request=TransactionOffer(trade_goods=1),
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        state_with_tx1 = game_state.add_pending_transaction(transaction1)
        state_with_both = state_with_tx1.add_pending_transaction(transaction2)

        assert len(state_with_both.pending_transactions) == 2
        assert "tx_001" in state_with_both.pending_transactions
        assert "tx_002" in state_with_both.pending_transactions


class TestGameStateResourceConsistency:
    """Test that transaction effects properly update all relevant game systems.

    Requirements: 8.2
    """

    def test_transaction_updates_player_resources(self) -> None:
        """Test that completed transactions update player resource pools.

        Requirements: 8.2
        """
        # RED: This will fail until we implement resource consistency updates
        player1 = Player(id="player1", faction=Faction.SOL)
        player1.gain_trade_goods(5)

        player2 = Player(id="player2", faction=Faction.HACAN)
        player2.add_commodities(3)

        game_state = GameState(players=[player1, player2])

        # Execute a transaction
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

        new_state = game_state.apply_transaction_effects(transaction)

        # Verify resource updates
        updated_player1 = next(p for p in new_state.players if p.id == "player1")
        updated_player2 = next(p for p in new_state.players if p.id == "player2")

        assert (
            updated_player1.get_trade_goods() == 4
        )  # 5 - 3 + 2 (commodities converted)
        assert updated_player2.get_trade_goods() == 3  # 0 + 3
        assert updated_player2.get_commodities() == 1  # 3 - 2

    def test_transaction_updates_promissory_note_ownership(self) -> None:
        """Test that promissory note exchanges update ownership records.

        Requirements: 8.2
        """
        # RED: This will fail until we implement promissory note consistency
        player1 = Player(id="player1", faction=Faction.SOL)
        player2 = Player(id="player2", faction=Faction.SOL)

        # Give player2 some trade goods so they can pay for the promissory note
        player2.gain_trade_goods(5)

        game_state = GameState(players=[player1, player2])

        # Add a promissory note to player1
        note = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player1"
        )
        game_state.promissory_note_manager.add_note_to_hand(note, "player1")

        # Execute transaction with promissory note
        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(promissory_notes=[note]),
            request=TransactionOffer(trade_goods=2),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        new_state = game_state.apply_transaction_effects(transaction)

        # Verify promissory note ownership transfer
        player1_notes = new_state.promissory_note_manager.get_player_hand("player1")
        player2_notes = new_state.promissory_note_manager.get_player_hand("player2")

        assert note not in player1_notes
        assert note in player2_notes


class TestTransactionSystemConsistency:
    """Test transaction consistency with resource-dependent systems.

    Requirements: 8.3
    """

    def test_transaction_maintains_fleet_supply_consistency(self) -> None:
        """Test that transactions maintain consistency with fleet supply limits.

        Requirements: 8.3
        """
        # RED: This will fail until we implement fleet supply consistency
        player1 = Player(id="player1", faction=Faction.SOL)
        player1.gain_trade_goods(5)

        player2 = Player(id="player2", faction=Faction.SOL)
        player2.add_commodities(3)

        game_state = GameState(players=[player1, player2])

        # Set up a scenario where transaction affects fleet supply
        # This is a placeholder - actual implementation depends on fleet supply system
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

        new_state = game_state.apply_transaction_effects(transaction)

        # Verify fleet supply consistency is maintained
        assert new_state.is_fleet_supply_consistent()

    def test_transaction_maintains_production_system_consistency(self) -> None:
        """Test that transactions maintain consistency with production systems.

        Requirements: 8.3
        """
        # RED: This will fail until we implement production consistency
        player1 = Player(id="player1", faction=Faction.SOL)
        player1.gain_trade_goods(8)

        player2 = Player(id="player2", faction=Faction.SOL)
        player2.add_commodities(4)

        game_state = GameState(players=[player1, player2])

        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=5),
            request=TransactionOffer(commodities=3),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        new_state = game_state.apply_transaction_effects(transaction)

        # Verify production system consistency
        assert new_state.is_production_system_consistent()


class TestTransactionNotifications:
    """Test transaction notifications to game components.

    Requirements: 8.4
    """

    def test_transaction_notifies_relevant_game_components(self) -> None:
        """Test that completed transactions notify relevant game components.

        Requirements: 8.4
        """
        # RED: This will fail until we implement notification system
        game_state = GameState()

        # Mock game components that should be notified
        mock_resource_manager = Mock()
        mock_fleet_manager = Mock()
        mock_production_manager = Mock()

        game_state.register_transaction_observer(mock_resource_manager)
        game_state.register_transaction_observer(mock_fleet_manager)
        game_state.register_transaction_observer(mock_production_manager)

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

        game_state.apply_transaction_effects(transaction)

        # Verify all observers were notified
        mock_resource_manager.on_transaction_completed.assert_called_once_with(
            transaction
        )
        mock_fleet_manager.on_transaction_completed.assert_called_once_with(transaction)
        mock_production_manager.on_transaction_completed.assert_called_once_with(
            transaction
        )

    def test_transaction_notification_includes_relevant_data(self) -> None:
        """Test that transaction notifications include all relevant data.

        Requirements: 8.4
        """
        # RED: This will fail until we implement detailed notifications
        game_state = GameState()

        mock_observer = Mock()
        game_state.register_transaction_observer(mock_observer)

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

        game_state.apply_transaction_effects(transaction)

        # Verify notification includes transaction details
        call_args = mock_observer.on_transaction_completed.call_args[0][0]
        assert call_args.transaction_id == "tx_001"
        assert call_args.proposing_player == "player1"
        assert call_args.target_player == "player2"
        assert call_args.offer.trade_goods == 3
        assert call_args.request.commodities == 2


class TestGameStateConsistencyValidation:
    """Test integration tests for game state consistency.

    Requirements: 8.5
    """

    def test_complete_transaction_flow_maintains_game_state_consistency(self) -> None:
        """Test that complete transaction flow maintains game state consistency.

        Requirements: 8.5
        """
        # RED: This will fail until we implement full consistency validation
        player1 = Player(id="player1", faction=Faction.SOL)
        player1.gain_trade_goods(10)

        player2 = Player(id="player2", faction=Faction.SOL)
        player2.add_commodities(4)

        game_state = GameState(players=[player1, player2])

        # Verify initial state is consistent
        assert game_state.is_valid()

        # Execute multiple transactions
        transaction1 = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        state_after_tx1 = game_state.apply_transaction_effects(transaction1)
        assert state_after_tx1.is_valid()

        transaction2 = ComponentTransaction(
            transaction_id="tx_002",
            proposing_player="player2",
            target_player="player1",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(trade_goods=2),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        final_state = state_after_tx1.apply_transaction_effects(transaction2)
        assert final_state.is_valid()

        # Verify transaction history is maintained
        assert len(final_state.transaction_history) == 2

    def test_concurrent_transactions_maintain_consistency(self) -> None:
        """Test that concurrent transactions maintain game state consistency.

        Requirements: 8.5
        """
        # RED: This will fail until we implement concurrent transaction handling
        player1 = Player(id="player1", faction=Faction.SOL)
        player1.gain_trade_goods(10)

        player2 = Player(id="player2", faction=Faction.SOL)
        player2.add_commodities(4)

        player3 = Player(id="player3", faction=Faction.SOL)
        player3.gain_trade_goods(8)

        game_state = GameState(players=[player1, player2, player3])

        # Simulate concurrent transactions
        transaction1 = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=3),
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        transaction2 = ComponentTransaction(
            transaction_id="tx_002",
            proposing_player="player3",
            target_player="player1",
            offer=TransactionOffer(trade_goods=2),
            request=TransactionOffer(trade_goods=1),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # Apply both transactions
        final_state = game_state.apply_concurrent_transaction_effects(
            [transaction1, transaction2]
        )

        # Verify consistency is maintained
        assert final_state.is_valid()
        assert len(final_state.transaction_history) == 2

    def test_transaction_rollback_maintains_consistency(self) -> None:
        """Test that transaction rollback maintains game state consistency.

        Requirements: 8.5
        """
        # RED: This will fail until we implement rollback consistency
        player1 = Player(id="player1", faction=Faction.SOL)
        player1.gain_trade_goods(5)

        player2 = Player(id="player2", faction=Faction.SOL)
        player2.add_commodities(3)

        game_state = GameState(players=[player1, player2])
        original_state = game_state

        # Attempt a transaction that should fail and rollback
        invalid_transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=10),  # More than player has
            request=TransactionOffer(commodities=2),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # This should fail and rollback
        try:
            game_state.apply_transaction_effects(invalid_transaction)
            assert False, "Transaction should have failed"
        except ValueError:
            # Expected failure
            pass

        # Verify state is unchanged after rollback
        assert game_state.is_valid()
        assert game_state == original_state
