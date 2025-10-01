"""Tests for ResourceManager class for Rule 28 deals resource management.

This module tests the ResourceManager class that handles resource transfers
between players for component transactions.

Requirements: 3.1, 3.2, 3.3, 3.4, 3.5
"""

from unittest.mock import Mock

import pytest

from ti4.core.transactions import PromissoryNote, PromissoryNoteType


class TestResourceManagerCreation:
    """Test ResourceManager class creation and initialization."""

    def test_resource_manager_creation(self) -> None:
        """Test that ResourceManager can be created with game state.

        Requirements: 3.1, 3.2
        """
        # RED: This will fail until we create ResourceManager
        from ti4.core.rule_28_deals import ResourceManager

        mock_game_state = Mock()
        resource_manager = ResourceManager(game_state=mock_game_state)

        assert resource_manager is not None
        assert resource_manager._game_state is mock_game_state


class TestResourceTracking:
    """Test resource tracking methods."""

    def test_get_trade_goods(self) -> None:
        """Test getting player's current trade goods count.

        Requirements: 3.1
        """
        from ti4.core.rule_28_deals import ResourceManager

        mock_game_state = Mock()
        mock_player = Mock()
        mock_player.id = "player1"
        mock_player.get_trade_goods.return_value = 5
        mock_game_state.players = [mock_player]

        resource_manager = ResourceManager(game_state=mock_game_state)
        trade_goods = resource_manager.get_trade_goods("player1")

        assert trade_goods == 5
        mock_player.get_trade_goods.assert_called_once()

    def test_get_commodities(self) -> None:
        """Test getting player's current commodity count.

        Requirements: 3.1
        """
        from ti4.core.rule_28_deals import ResourceManager

        mock_game_state = Mock()
        mock_player = Mock()
        mock_player.id = "player1"
        mock_player.get_commodities.return_value = 3
        mock_game_state.players = [mock_player]

        resource_manager = ResourceManager(game_state=mock_game_state)
        commodities = resource_manager.get_commodities("player1")

        assert commodities == 3
        mock_player.get_commodities.assert_called_once()

    def test_get_promissory_notes(self) -> None:
        """Test getting player's owned promissory notes.

        Requirements: 3.1
        """
        from ti4.core.rule_28_deals import ResourceManager

        mock_game_state = Mock()
        mock_promissory_manager = Mock()
        test_note = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player2"
        )
        mock_promissory_manager.get_player_hand.return_value = [test_note]
        mock_game_state.promissory_note_manager = mock_promissory_manager

        resource_manager = ResourceManager(game_state=mock_game_state)
        notes = resource_manager.get_promissory_notes("player1")

        assert notes == [test_note]
        mock_promissory_manager.get_player_hand.assert_called_once_with("player1")


class TestTradeGoodsTransfer:
    """Test trade goods transfer between players."""

    def test_transfer_trade_goods_success(self) -> None:
        """Test successful trade goods transfer between players.

        Requirements: 3.2, 3.3
        """
        from ti4.core.rule_28_deals import ResourceManager

        mock_game_state = Mock()
        mock_player1 = Mock()
        mock_player1.id = "player1"
        mock_player1.get_trade_goods.return_value = 5
        mock_player1.spend_trade_goods.return_value = True

        mock_player2 = Mock()
        mock_player2.id = "player2"

        mock_game_state.players = [mock_player1, mock_player2]

        resource_manager = ResourceManager(game_state=mock_game_state)
        resource_manager.transfer_trade_goods("player1", "player2", 3)

        mock_player1.spend_trade_goods.assert_called_once_with(3)
        mock_player2.gain_trade_goods.assert_called_once_with(3)

    def test_transfer_trade_goods_insufficient_funds(self) -> None:
        """Test trade goods transfer with insufficient funds.

        Requirements: 3.2, 3.3
        """
        from ti4.core.rule_28_deals import ResourceManager

        mock_game_state = Mock()
        mock_player1 = Mock()
        mock_player1.id = "player1"
        mock_player1.get_trade_goods.return_value = 2
        mock_player1.spend_trade_goods.return_value = False

        mock_player2 = Mock()
        mock_player2.id = "player2"

        mock_game_state.players = [mock_player1, mock_player2]

        resource_manager = ResourceManager(game_state=mock_game_state)

        with pytest.raises(ValueError, match="Insufficient trade goods"):
            resource_manager.transfer_trade_goods("player1", "player2", 5)

        mock_player1.spend_trade_goods.assert_called_once_with(5)
        mock_player2.gain_trade_goods.assert_not_called()

    def test_transfer_trade_goods_validation(self) -> None:
        """Test trade goods transfer input validation.

        Requirements: 3.2, 3.3
        """
        from ti4.core.rule_28_deals import ResourceManager

        mock_game_state = Mock()
        resource_manager = ResourceManager(game_state=mock_game_state)

        # Test empty from_player
        with pytest.raises(ValueError, match="From player ID cannot be empty"):
            resource_manager.transfer_trade_goods("", "player2", 3)

        # Test empty to_player
        with pytest.raises(ValueError, match="To player ID cannot be empty"):
            resource_manager.transfer_trade_goods("player1", "   ", 3)

        # Test same player
        with pytest.raises(ValueError, match="Cannot transfer to the same player"):
            resource_manager.transfer_trade_goods("player1", "player1", 3)

        # Test negative amount
        with pytest.raises(ValueError, match="Amount must be positive"):
            resource_manager.transfer_trade_goods("player1", "player2", -1)

        # Test zero amount
        with pytest.raises(ValueError, match="Amount must be positive"):
            resource_manager.transfer_trade_goods("player1", "player2", 0)


class TestCommodityTransfer:
    """Test commodity transfer and conversion between players."""

    def test_transfer_commodities_success(self) -> None:
        """Test successful commodity transfer with conversion to trade goods.

        Requirements: 3.4, 3.5
        """
        from ti4.core.rule_28_deals import ResourceManager

        mock_game_state = Mock()
        mock_player1 = Mock()
        mock_player1.id = "player1"
        mock_player1.get_commodities.return_value = 4

        mock_player2 = Mock()
        mock_player2.id = "player2"

        mock_game_state.players = [mock_player1, mock_player2]

        resource_manager = ResourceManager(game_state=mock_game_state)
        resource_manager.transfer_commodities("player1", "player2", 2)

        # Player1 should give commodities to player2 (which converts to trade goods)
        mock_player1.give_commodities_to_player.assert_called_once_with(mock_player2, 2)

    def test_transfer_commodities_insufficient_commodities(self) -> None:
        """Test commodity transfer with insufficient commodities.

        Requirements: 3.4, 3.5
        """
        from ti4.core.rule_28_deals import ResourceManager

        mock_game_state = Mock()
        mock_player1 = Mock()
        mock_player1.id = "player1"
        mock_player1.get_commodities.return_value = 1
        mock_player1.give_commodities_to_player.side_effect = ValueError(
            "Player only has 1 commodities, cannot give 3"
        )

        mock_player2 = Mock()
        mock_player2.id = "player2"

        mock_game_state.players = [mock_player1, mock_player2]

        resource_manager = ResourceManager(game_state=mock_game_state)

        with pytest.raises(ValueError, match="Insufficient commodities"):
            resource_manager.transfer_commodities("player1", "player2", 3)

    def test_transfer_commodities_validation(self) -> None:
        """Test commodity transfer input validation.

        Requirements: 3.4, 3.5
        """
        from ti4.core.rule_28_deals import ResourceManager

        mock_game_state = Mock()
        resource_manager = ResourceManager(game_state=mock_game_state)

        # Test empty from_player
        with pytest.raises(ValueError, match="From player ID cannot be empty"):
            resource_manager.transfer_commodities("", "player2", 2)

        # Test empty to_player
        with pytest.raises(ValueError, match="To player ID cannot be empty"):
            resource_manager.transfer_commodities("player1", "   ", 2)

        # Test same player
        with pytest.raises(ValueError, match="Cannot transfer to the same player"):
            resource_manager.transfer_commodities("player1", "player1", 2)

        # Test negative amount
        with pytest.raises(ValueError, match="Amount must be positive"):
            resource_manager.transfer_commodities("player1", "player2", -1)

        # Test zero amount
        with pytest.raises(ValueError, match="Amount must be positive"):
            resource_manager.transfer_commodities("player1", "player2", 0)


class TestPromissoryNoteTransfer:
    """Test promissory note transfer between players."""

    def test_transfer_promissory_note_success(self) -> None:
        """Test successful promissory note transfer.

        Requirements: 3.2
        """
        from ti4.core.rule_28_deals import ResourceManager

        mock_game_state = Mock()
        mock_promissory_manager = Mock()
        mock_game_state.promissory_note_manager = mock_promissory_manager

        test_note = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player2"
        )

        # Mock the player hand to contain the test note
        mock_player_hand = [test_note]
        mock_promissory_manager.get_player_hand.return_value = mock_player_hand

        resource_manager = ResourceManager(game_state=mock_game_state)
        resource_manager.transfer_promissory_note("player1", "player2", test_note)

        # Verify the note was checked in player1's hand
        mock_promissory_manager.get_player_hand.assert_called_once_with("player1")
        # Verify the note was added to player2's hand
        mock_promissory_manager.add_note_to_hand.assert_called_once_with(
            test_note, "player2"
        )

    def test_transfer_promissory_note_validation(self) -> None:
        """Test promissory note transfer input validation.

        Requirements: 3.2
        """
        from ti4.core.rule_28_deals import ResourceManager

        mock_game_state = Mock()
        resource_manager = ResourceManager(game_state=mock_game_state)

        test_note = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player2"
        )

        # Test empty from_player
        with pytest.raises(ValueError, match="From player ID cannot be empty"):
            resource_manager.transfer_promissory_note("", "player2", test_note)

        # Test empty to_player
        with pytest.raises(ValueError, match="To player ID cannot be empty"):
            resource_manager.transfer_promissory_note("player1", "   ", test_note)

        # Test same player
        with pytest.raises(ValueError, match="Cannot transfer to the same player"):
            resource_manager.transfer_promissory_note("player1", "player1", test_note)

        # Test None note
        with pytest.raises(ValueError, match="Promissory note cannot be None"):
            resource_manager.transfer_promissory_note("player1", "player2", None)

    def test_transfer_promissory_note_not_owned(self) -> None:
        """Test promissory note transfer when player doesn't own the note.

        Requirements: 3.2
        """
        from ti4.core.rule_28_deals import ResourceManager

        mock_game_state = Mock()
        mock_promissory_manager = Mock()
        mock_game_state.promissory_note_manager = mock_promissory_manager

        test_note = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player2"
        )

        # Mock the player hand to NOT contain the test note
        mock_promissory_manager.get_player_hand.return_value = []

        resource_manager = ResourceManager(game_state=mock_game_state)

        with pytest.raises(
            ValueError,
            match="Player player1 does not own the specified promissory note",
        ):
            resource_manager.transfer_promissory_note("player1", "player2", test_note)


class TestResourceManagerHelperMethods:
    """Test ResourceManager helper methods."""

    def test_find_player_success(self) -> None:
        """Test finding a player by ID.

        Requirements: 3.1
        """
        from ti4.core.rule_28_deals import ResourceManager

        mock_game_state = Mock()
        mock_player1 = Mock()
        mock_player1.id = "player1"
        mock_player2 = Mock()
        mock_player2.id = "player2"
        mock_game_state.players = [mock_player1, mock_player2]

        resource_manager = ResourceManager(game_state=mock_game_state)
        found_player = resource_manager._find_player("player2")

        assert found_player is mock_player2

    def test_find_player_not_found(self) -> None:
        """Test finding a non-existent player.

        Requirements: 3.1
        """
        from ti4.core.rule_28_deals import ResourceManager

        mock_game_state = Mock()
        mock_player1 = Mock()
        mock_player1.id = "player1"
        mock_game_state.players = [mock_player1]

        resource_manager = ResourceManager(game_state=mock_game_state)
        found_player = resource_manager._find_player("player_nonexistent")

        assert found_player is None

    def test_validate_transfer_inputs(self) -> None:
        """Test input validation for transfer operations.

        Requirements: 3.2, 3.3, 3.4, 3.5
        """
        from ti4.core.rule_28_deals import ResourceManager

        mock_game_state = Mock()
        resource_manager = ResourceManager(game_state=mock_game_state)

        # Test valid inputs
        resource_manager._validate_transfer_inputs("player1", "player2", 5)

        # Test empty from_player
        with pytest.raises(ValueError, match="From player ID cannot be empty"):
            resource_manager._validate_transfer_inputs("", "player2", 5)

        # Test empty to_player
        with pytest.raises(ValueError, match="To player ID cannot be empty"):
            resource_manager._validate_transfer_inputs("player1", "   ", 5)

        # Test same player
        with pytest.raises(ValueError, match="Cannot transfer to the same player"):
            resource_manager._validate_transfer_inputs("player1", "player1", 5)

        # Test negative amount
        with pytest.raises(ValueError, match="Amount must be positive"):
            resource_manager._validate_transfer_inputs("player1", "player2", -1)

        # Test zero amount
        with pytest.raises(ValueError, match="Amount must be positive"):
            resource_manager._validate_transfer_inputs("player1", "player2", 0)
