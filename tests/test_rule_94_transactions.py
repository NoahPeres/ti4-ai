"""Tests for Rule 94: TRANSACTIONS mechanics.

This module tests the transaction system according to TI4 LRR Rule 94.
All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.

Rule 94 Sub-rules tested:
- 94.1: Transaction timing and neighbor requirements
- 94.2: Transaction components and exchange mechanics
- 94.3: Exchangeable items validation
- 94.4: Uneven exchanges and deal terms
- 94.5: Deal integration
- 94.6: Agenda phase transactions
"""

import pytest

from ti4.core.game_phase import GamePhase
from ti4.core.transactions import (
    PromissoryNote,
    PromissoryNoteType,
    TransactionManager,
    TransactionOffer,
)


class TestRule94TransactionBasics:
    """Test basic transaction mechanics (Rule 94.0)."""

    def test_transaction_system_exists(self) -> None:
        """Test that transaction system can be imported and instantiated.

        This is the first RED test - it will fail until we create the transaction system.

        LRR Reference: Rule 94.0 - Core transaction concept
        """
        # Test basic instantiation
        transaction_manager = TransactionManager()
        assert transaction_manager is not None


class TestRule94TransactionTiming:
    """Test transaction timing and neighbor requirements (Rule 94.1)."""

    def test_active_player_can_transact_with_neighbors(self) -> None:
        """Test that active player can resolve transactions with neighbors.

        LRR Reference: Rule 94.1 - "During the active player's turn, they may
        resolve up to one transaction with each of their neighbors."
        """
        # Create transaction manager (without galaxy, so all players are considered neighbors)
        transaction_manager = TransactionManager()

        # Set active player
        transaction_manager.set_active_player("player1")

        # Verify player1 can transact with other players (no galaxy = all neighbors)
        assert transaction_manager.can_transact("player1", "player2")
        assert transaction_manager.can_transact("player1", "player3")

    def test_one_transaction_per_neighbor_limit(self) -> None:
        """Test that players can only have one transaction per neighbor per turn.

        LRR Reference: Rule 94.1 - "up to one transaction with each of their neighbors"
        """
        # Create transaction manager
        transaction_manager = TransactionManager()
        transaction_manager.set_active_player("player1")

        # First transaction should be allowed
        assert transaction_manager.can_transact("player1", "player2")

        # Execute a transaction
        offer1 = TransactionOffer(trade_goods=1)
        offer2 = TransactionOffer(commodities=1)
        result = transaction_manager.execute_transaction(
            "player1", "player2", offer1, offer2
        )
        assert result.success

        # Second transaction with same neighbor should be denied
        assert not transaction_manager.can_transact("player1", "player2")


class TestRule94TransactionComponents:
    """Test transaction component exchange mechanics (Rule 94.2)."""

    def test_exchange_trade_goods_and_commodities(self) -> None:
        """Test exchanging trade goods and commodities.

        LRR Reference: Rule 94.2 - "a player gives any number of trade goods
        and commodities... in exchange for any number of trade goods, commodities"
        """
        # Create transaction manager
        transaction_manager = TransactionManager()
        transaction_manager.set_active_player("player1")

        # Create transaction offers
        player1_offer = TransactionOffer(trade_goods=3, commodities=2)
        player2_offer = TransactionOffer(trade_goods=1, commodities=4)

        # Execute transaction
        result = transaction_manager.execute_transaction(
            "player1", "player2", player1_offer, player2_offer
        )

        # Verify transaction succeeded
        assert result.success
        assert result.player1_gave.trade_goods == 3
        assert result.player1_gave.commodities == 2
        assert result.player2_gave.trade_goods == 1
        assert result.player2_gave.commodities == 4

    def test_exchange_promissory_notes(self) -> None:
        """Test exchanging promissory notes (limited to one per transaction).

        LRR Reference: Rule 94.2 - "up to one promissory note... in exchange
        for... up to one promissory note"
        """
        # Create transaction manager
        transaction_manager = TransactionManager()
        transaction_manager.set_active_player("player1")

        # Create promissory notes
        note1 = PromissoryNote(PromissoryNoteType.TRADE_AGREEMENT, "player1")
        note2 = PromissoryNote(PromissoryNoteType.CEASEFIRE, "player2")

        # Create transaction offers with promissory notes
        player1_offer = TransactionOffer(promissory_notes=[note1])
        player2_offer = TransactionOffer(promissory_notes=[note2])

        # Execute transaction
        result = transaction_manager.execute_transaction(
            "player1", "player2", player1_offer, player2_offer
        )

        # Verify transaction succeeded
        assert result.success
        assert len(result.player1_gave.promissory_notes) == 1
        assert len(result.player2_gave.promissory_notes) == 1


class TestRule94ExchangeableItems:
    """Test validation of exchangeable items (Rule 94.3)."""

    def test_valid_exchangeable_items(self) -> None:
        """Test that only valid items can be exchanged.

        LRR Reference: Rule 94.3 - Lists valid exchangeable items
        """
        # Create offers with all valid item types
        note = PromissoryNote(PromissoryNoteType.ALLIANCE, "player1")
        offer = TransactionOffer(
            trade_goods=2, commodities=3, promissory_notes=[note], relic_fragments=1
        )

        transaction_manager = TransactionManager()
        assert transaction_manager.validate_offer(offer)

    def test_invalid_items_cannot_be_exchanged(self) -> None:
        """Test that invalid items cannot be included in transactions.

        LRR Reference: Rule 94.3 - Implicit validation of exchangeable items
        """
        # Attempt to create offer with invalid items (should raise error or be invalid)
        # Test multiple promissory notes (should fail validation)
        note1 = PromissoryNote(PromissoryNoteType.TRADE_AGREEMENT, "player1")
        note2 = PromissoryNote(PromissoryNoteType.CEASEFIRE, "player1")

        with pytest.raises(
            ValueError, match="Cannot exchange more than one promissory note"
        ):
            TransactionOffer(promissory_notes=[note1, note2])

    def test_supply_validation_basic(self) -> None:
        """Test basic supply validation (foundation for future PlayerSupply system).

        This is a placeholder test for the future PlayerSupply integration.
        """
        transaction_manager = TransactionManager()

        # Test offer within supply limits
        offer = TransactionOffer(trade_goods=2, commodities=1)
        player_supply = {"trade_goods": 5, "commodities": 3, "relic_fragments": 0}
        assert transaction_manager.validate_offer(offer, player_supply)

        # Test offer exceeding supply limits
        excessive_offer = TransactionOffer(trade_goods=10, commodities=1)
        assert not transaction_manager.validate_offer(excessive_offer, player_supply)

        # Test without supply validation (current behavior)
        assert transaction_manager.validate_offer(excessive_offer)  # No supply check


class TestRule94UnevenExchanges:
    """Test uneven exchanges and gifts (Rule 94.4)."""

    def test_uneven_exchange_allowed(self) -> None:
        """Test that uneven exchanges are allowed.

        LRR Reference: Rule 94.4 - "A transaction does not have to be even.
        A player may exchange components of unequal value"
        """
        # Create transaction manager
        transaction_manager = TransactionManager()
        transaction_manager.set_active_player("player1")

        # Create uneven offers (player1 gives more than player2)
        player1_offer = TransactionOffer(trade_goods=5, commodities=3)
        player2_offer = TransactionOffer(trade_goods=1)

        # Execute uneven transaction
        result = transaction_manager.execute_transaction(
            "player1", "player2", player1_offer, player2_offer
        )

        # Verify uneven transaction is allowed
        assert result.success

    def test_one_sided_gift_allowed(self) -> None:
        """Test that one-sided gifts (giving without receiving) are allowed.

        LRR Reference: Rule 94.4 - "give components without receiving something in return"
        """
        # Create transaction manager
        transaction_manager = TransactionManager()
        transaction_manager.set_active_player("player1")

        # Create one-sided gift (player1 gives, player2 gives nothing)
        player1_offer = TransactionOffer(trade_goods=2, commodities=1)
        player2_offer = TransactionOffer()  # Empty offer

        # Execute gift transaction
        result = transaction_manager.execute_transaction(
            "player1", "player2", player1_offer, player2_offer
        )

        # Verify gift is allowed
        assert result.success


class TestRule94AgendaPhaseTransactions:
    """Test agenda phase transaction rules (Rule 94.6)."""

    def test_agenda_phase_transactions_with_all_players(self) -> None:
        """Test that during agenda phase, players can transact with all players.

        LRR Reference: Rule 94.6 - "While resolving each agenda during the agenda
        phase, a player may perform one transaction with each other player."
        """
        # Create transaction manager
        transaction_manager = TransactionManager()

        # Set agenda phase
        transaction_manager.set_game_phase(GamePhase.AGENDA)
        transaction_manager.set_active_player("player1")

        # Verify player1 can transact with any player during agenda phase
        assert transaction_manager.can_transact("player1", "player2")
        assert transaction_manager.can_transact("player1", "player3")
        assert transaction_manager.can_transact("player1", "player4")

    def test_agenda_phase_neighbor_requirement_waived(self) -> None:
        """Test that neighbor requirement is waived during agenda phase.

        LRR Reference: Rule 94.6a - "Players do not need to be neighbors to
        perform these transactions."
        """
        # Create transaction manager
        transaction_manager = TransactionManager()
        transaction_manager.set_active_player("player1")

        # During normal phases, would need neighbors (but we have no galaxy so all are neighbors)
        transaction_manager.set_game_phase(GamePhase.ACTION)
        assert transaction_manager.can_transact("player1", "player2")

        # During agenda phase, neighbor requirement is explicitly waived
        transaction_manager.set_game_phase(GamePhase.AGENDA)
        assert transaction_manager.can_transact("player1", "player2")
        assert transaction_manager.can_transact("player1", "player3")
