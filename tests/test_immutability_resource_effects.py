"""Tests for immutability violations in resource effects.

This module tests that resource effects properly use deep copying to avoid
mutating original Player objects and maintain immutability.

Requirements: 3.1, 3.4
"""

from datetime import datetime

from ti4.core.constants import Faction
from ti4.core.deals import ComponentTransaction, TransactionStatus
from ti4.core.game_state import GameState
from ti4.core.player import Player
from ti4.core.transactions import TransactionOffer


class TestImmutabilityResourceEffects:
    """Test that resource effects maintain immutability.

    Requirements: 3.1, 3.4
    """

    def test_resource_effects_use_deep_copy_for_players(self) -> None:
        """Test that _apply_resource_effects uses deep copy for Player objects.

        This test verifies that when applying resource effects, the original
        Player objects are not mutated and new objects are created.

        Requirements: 3.1, 3.4
        """
        # RED: This will fail until we implement proper deep copying
        player1 = Player(id="player1", faction=Faction.SOL)
        player1.gain_trade_goods(5)

        player2 = Player(id="player2", faction=Faction.HACAN)
        player2.add_commodities(3)

        game_state = GameState(players=[player1, player2])

        # Store references to original player objects
        original_player1 = game_state.players[0]
        original_player2 = game_state.players[1]

        # Create a transaction
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

        # Apply resource effects
        new_state = game_state._apply_resource_effects(transaction)

        # CRITICAL IMMUTABILITY TEST:
        # Verify new GameState is created (identity check)
        assert new_state is not game_state, "New GameState should be a different object"

        # The new state should have different Player objects (identity check)
        new_player1 = next(p for p in new_state.players if p.id == "player1")
        new_player2 = next(p for p in new_state.players if p.id == "player2")

        # Identity checks - new objects should be created
        assert new_player1 is not original_player1, (
            "Player1 object should be a new instance"
        )
        assert new_player2 is not original_player2, (
            "Player2 object should be a new instance"
        )

        # Original players should be unchanged
        assert original_player1.get_trade_goods() == 5, (
            "Original player1 trade goods should be unchanged"
        )
        assert original_player2.get_trade_goods() == 0, (
            "Original player2 trade goods should be unchanged"
        )
        assert original_player2.get_commodities() == 3, (
            "Original player2 commodities should be unchanged"
        )

        # New players should have updated values
        assert new_player1.get_trade_goods() == 4, (
            "New player1 should have 5 - 3 + 2 = 4 trade goods"
        )
        assert new_player2.get_trade_goods() == 3, (
            "New player2 should have 0 + 3 = 3 trade goods"
        )
        assert new_player2.get_commodities() == 1, (
            "New player2 should have 3 - 2 = 1 commodities"
        )

        # Verify other players are unchanged (same object reference)
        if len(game_state.players) > 2:
            for i, original_player in enumerate(game_state.players[2:], start=2):
                new_player = new_state.players[i]
                assert new_player is original_player, (
                    f"Unchanged player {i} should be same object reference"
                )

    def test_resource_effects_preserve_original_game_state(self) -> None:
        """Test that applying resource effects doesn't mutate the original GameState.

        Requirements: 3.1, 3.4
        """
        player1 = Player(id="player1", faction=Faction.SOL)
        player1.gain_trade_goods(10)

        player2 = Player(id="player2", faction=Faction.HACAN)
        player2.add_commodities(5)

        original_game_state = GameState(players=[player1, player2])

        # Store original values
        original_player1_tg = original_game_state.players[0].get_trade_goods()
        original_player2_tg = original_game_state.players[1].get_trade_goods()
        original_player2_commodities = original_game_state.players[1].get_commodities()

        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=4),
            request=TransactionOffer(commodities=3),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # Apply resource effects
        new_game_state = original_game_state._apply_resource_effects(transaction)

        # Verify original game state is completely unchanged
        assert new_game_state is not original_game_state, (
            "New GameState should be a different object"
        )

        # Verify players list is also a new object
        assert new_game_state.players is not original_game_state.players, (
            "Players list should be a new object"
        )

        # Original players should have unchanged values
        assert original_game_state.players[0].get_trade_goods() == original_player1_tg
        assert original_game_state.players[1].get_trade_goods() == original_player2_tg
        assert (
            original_game_state.players[1].get_commodities()
            == original_player2_commodities
        )

        # New state should have updated values
        new_player1 = next(p for p in new_game_state.players if p.id == "player1")
        new_player2 = next(p for p in new_game_state.players if p.id == "player2")

        assert new_player1.get_trade_goods() == 9  # 10 - 4 + 3 = 9
        assert new_player2.get_trade_goods() == 4  # 0 + 4 = 4
        assert new_player2.get_commodities() == 2  # 5 - 3 = 2

    def test_resource_effects_with_no_changes_still_creates_new_objects(self) -> None:
        """Test that even when no resource changes occur, new Player objects are created.

        This ensures consistent behavior and prevents accidental mutations.

        Requirements: 3.1, 3.4
        """
        player1 = Player(id="player1", faction=Faction.SOL)
        player2 = Player(id="player2", faction=Faction.HACAN)
        player3 = Player(id="player3", faction=Faction.XXCHA)  # Uninvolved player

        game_state = GameState(players=[player1, player2, player3])

        # Store references to original players
        original_player1 = game_state.players[0]
        original_player2 = game_state.players[1]
        original_player3 = game_state.players[2]

        # Create a transaction with zero amounts (no actual resource transfer)
        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=0),
            request=TransactionOffer(commodities=0),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # Apply resource effects
        new_state = game_state._apply_resource_effects(transaction)

        # Verify new GameState is created (identity check)
        assert new_state is not game_state, "New GameState should be a different object"

        # Get new player objects
        new_player1 = next(p for p in new_state.players if p.id == "player1")
        new_player2 = next(p for p in new_state.players if p.id == "player2")
        new_player3 = next(p for p in new_state.players if p.id == "player3")

        # Involved players should be new objects (deep copied)
        assert new_player1 is not original_player1, (
            "Player1 should be a new object even with no changes"
        )
        assert new_player2 is not original_player2, (
            "Player2 should be a new object even with no changes"
        )

        # Uninvolved player should be the same object (no need to copy)
        assert new_player3 is original_player3, (
            "Uninvolved player should be same object reference"
        )

        # All players should have same values (no changes)
        assert new_player1.get_trade_goods() == original_player1.get_trade_goods()
        assert new_player1.get_commodities() == original_player1.get_commodities()
        assert new_player2.get_trade_goods() == original_player2.get_trade_goods()
        assert new_player2.get_commodities() == original_player2.get_commodities()

    def test_multiple_resource_effects_maintain_immutability(self) -> None:
        """Test that multiple sequential resource effects maintain immutability.

        Requirements: 3.1, 3.4
        """
        player1 = Player(id="player1", faction=Faction.SOL)
        player1.gain_trade_goods(10)

        player2 = Player(id="player2", faction=Faction.HACAN)
        player2.add_commodities(6)  # HACAN's commodity limit is 6

        game_state = GameState(players=[player1, player2])

        # First transaction
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

        # Apply first transaction
        state_after_tx1 = game_state._apply_resource_effects(transaction1)

        # Store intermediate state
        intermediate_player1 = next(
            p for p in state_after_tx1.players if p.id == "player1"
        )
        intermediate_player2 = next(
            p for p in state_after_tx1.players if p.id == "player2"
        )

        # Second transaction
        transaction2 = ComponentTransaction(
            transaction_id="tx_002",
            proposing_player="player2",
            target_player="player1",
            offer=TransactionOffer(commodities=3),
            request=TransactionOffer(trade_goods=2),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        # Apply second transaction
        final_state = state_after_tx1._apply_resource_effects(transaction2)

        # Get final players
        final_player1 = next(p for p in final_state.players if p.id == "player1")
        final_player2 = next(p for p in final_state.players if p.id == "player2")

        # Verify all states are different objects
        assert final_state is not state_after_tx1, (
            "Final state should be different from intermediate"
        )
        assert state_after_tx1 is not game_state, (
            "Intermediate state should be different from original"
        )

        # Verify all player objects are different
        assert final_player1 is not intermediate_player1, (
            "Final player1 should be different from intermediate"
        )
        assert final_player2 is not intermediate_player2, (
            "Final player2 should be different from intermediate"
        )

        # Verify original state is unchanged
        original_player1 = game_state.players[0]
        original_player2 = game_state.players[1]
        assert original_player1.get_trade_goods() == 10
        assert original_player2.get_commodities() == 6

        # Verify intermediate state is unchanged
        assert intermediate_player1.get_trade_goods() == 9  # 10 - 3 + 2 = 9
        assert intermediate_player2.get_commodities() == 4  # 6 - 2 = 4

        # Verify final state has correct values
        # Player1: 9 - 2 + 3 = 10 trade goods
        # Player2: 4 - 3 = 1 commodities, 3 + 2 = 5 trade goods
        assert final_player1.get_trade_goods() == 10
        assert final_player2.get_commodities() == 1
        assert final_player2.get_trade_goods() == 5
