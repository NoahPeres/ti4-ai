"""Tests for transaction manager GameState synchronization.

This module tests that the transaction manager keeps its cache synchronized
with the GameState pending transactions.

Requirements: 5.1
"""

from unittest.mock import Mock

from ti4.core.constants import Faction
from ti4.core.game_state import GameState
from ti4.core.player import Player
from ti4.core.rule_28_deals import (
    EnhancedTransactionManager,
)
from ti4.core.transactions import TransactionOffer


class TestTransactionManagerGameStateSync:
    """Test transaction manager synchronization with GameState.

    Requirements: 5.1
    """

    def test_propose_transaction_syncs_with_gamestate(self) -> None:
        """Test that propose_transaction updates both manager cache and GameState.

        Requirements: 5.1
        """
        # RED: This will fail until we implement GameState synchronization

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

        # Verify transaction is in manager cache
        assert transaction.transaction_id in manager._transactions

        # Verify GameState has been updated (this will fail initially)
        assert transaction.transaction_id in manager._game_state.pending_transactions
        assert (
            manager._game_state.pending_transactions[transaction.transaction_id]
            == transaction
        )

        # Verify GameState is a new instance (immutability)
        assert manager._game_state is not game_state

    def test_propose_transaction_backward_compatibility(self) -> None:
        """Test that propose_transaction works with GameState that doesn't have add_pending_transaction.

        Requirements: 5.1
        """
        # Setup with mock GameState that doesn't have add_pending_transaction
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player1.gain_trade_goods(5)  # Give enough trade goods

        player2 = Player(id="player2", faction=Faction.BARONY)
        player2.add_commodities(2)  # Give enough commodities (within limit)

        players = [player1, player2]

        # Create a mock GameState without add_pending_transaction method
        mock_game_state = Mock(spec=[])  # Empty spec means no methods
        mock_game_state.players = players
        mock_game_state.pending_transactions = {}
        # Explicitly don't add add_pending_transaction method

        galaxy = Mock()
        galaxy.are_players_neighbors.return_value = True

        manager = EnhancedTransactionManager(galaxy, mock_game_state)

        # This should not fail even without add_pending_transaction method
        offer = TransactionOffer(trade_goods=3)
        request = TransactionOffer(commodities=2)

        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
        )

        # Should still work and store in manager cache
        assert transaction.transaction_id in manager._transactions

        # GameState should remain unchanged since it doesn't support the method
        assert manager._game_state is mock_game_state

    def test_manager_gamestate_reference_updated_after_sync(self) -> None:
        """Test that manager's _game_state reference is updated after GameState sync.

        Requirements: 5.1
        """
        # Setup
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player1.gain_trade_goods(5)  # Give enough trade goods

        player2 = Player(id="player2", faction=Faction.BARONY)
        player2.add_commodities(2)  # Give enough commodities (within limit)

        players = [player1, player2]
        original_game_state = GameState(players=players)

        galaxy = Mock()
        galaxy.are_players_neighbors.return_value = True

        manager = EnhancedTransactionManager(galaxy, original_game_state)
        original_state_ref = manager._game_state

        # Propose transaction
        offer = TransactionOffer(trade_goods=3)
        request = TransactionOffer(commodities=2)

        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
        )

        # Manager's GameState reference should be updated to new state
        assert manager._game_state is not original_state_ref
        assert manager._game_state is not original_game_state

        # New state should contain the transaction
        assert transaction.transaction_id in manager._game_state.pending_transactions
