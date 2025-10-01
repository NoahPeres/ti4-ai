"""Tests for Rule 28: DEALS component transaction system.

This module tests the enhanced component transaction system for Rule 28 deals.
All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.

Rule 28 focuses on component-based transactions that can be objectively validated
and enforced by the game system.
"""

from datetime import datetime
from unittest.mock import Mock

import pytest

from ti4.core.rule_28_deals import (
    ComponentTransaction,
    TransactionStatus,
    ValidationResult,
)
from ti4.core.transactions import TransactionOffer


class TestComponentTransactionEntity:
    """Test ComponentTransaction dataclass and lifecycle management."""

    def test_component_transaction_creation(self) -> None:
        """Test that ComponentTransaction can be created with required fields.

        Requirements: 1.1, 1.4, 1.5
        """
        # This will fail until we create ComponentTransaction
        offer = TransactionOffer(trade_goods=3)
        request = TransactionOffer(commodities=2)

        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        assert transaction.transaction_id == "tx_001"
        assert transaction.proposing_player == "player1"
        assert transaction.target_player == "player2"
        assert transaction.offer == offer
        assert transaction.request == request
        assert transaction.status == TransactionStatus.PENDING
        assert transaction.timestamp is not None

    def test_component_transaction_is_pending(self) -> None:
        """Test ComponentTransaction.is_pending() method.

        Requirements: 1.4, 1.5
        """
        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        assert transaction.is_pending() is True

        # Test non-pending status
        completed_transaction = ComponentTransaction(
            transaction_id="tx_002",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        assert completed_transaction.is_pending() is False

    def test_component_transaction_is_completed(self) -> None:
        """Test ComponentTransaction.is_completed() method.

        Requirements: 1.4, 1.5
        """
        pending_transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        assert pending_transaction.is_completed() is False

        # Test completed status
        completed_transaction = ComponentTransaction(
            transaction_id="tx_002",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
            status=TransactionStatus.ACCEPTED,
            timestamp=datetime.now(),
            completion_timestamp=datetime.now(),
        )

        assert completed_transaction.is_completed() is True

    def test_component_transaction_get_net_exchange(self) -> None:
        """Test ComponentTransaction.get_net_exchange() method.

        Requirements: 1.1, 1.4
        """
        offer = TransactionOffer(trade_goods=3, commodities=1)
        request = TransactionOffer(trade_goods=1, commodities=2)

        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        # Proposing player gives offer, receives request
        proposer_net = transaction.get_net_exchange("player1")
        assert proposer_net.trade_goods == -2  # gives 3, receives 1
        assert proposer_net.commodities == 1  # gives 1, receives 2

        # Target player receives offer, gives request
        target_net = transaction.get_net_exchange("player2")
        assert target_net.trade_goods == 2  # receives 3, gives 1
        assert target_net.commodities == -1  # receives 1, gives 2


class TestTransactionStatusEnum:
    """Test TransactionStatus enum for tracking transaction states."""

    def test_transaction_status_enum_values(self) -> None:
        """Test that TransactionStatus enum has all required values.

        Requirements: 1.4, 1.5
        """
        # This will fail until we create TransactionStatus enum
        assert TransactionStatus.PENDING.value == "pending"
        assert TransactionStatus.ACCEPTED.value == "accepted"
        assert TransactionStatus.REJECTED.value == "rejected"
        assert TransactionStatus.EXPIRED.value == "expired"
        assert TransactionStatus.CANCELLED.value == "cancelled"

    def test_transaction_status_enum_completeness(self) -> None:
        """Test that TransactionStatus enum has all expected states.

        Requirements: 1.4, 1.5
        """
        expected_statuses = {"pending", "accepted", "rejected", "expired", "cancelled"}
        actual_statuses = {status.value for status in TransactionStatus}
        assert actual_statuses == expected_statuses


class TestValidationResultDataclass:
    """Test ValidationResult dataclass for validation feedback."""

    def test_validation_result_creation(self) -> None:
        """Test that ValidationResult can be created with validation feedback.

        Requirements: 1.1, 1.4, 1.5
        """
        # This will fail until we create ValidationResult
        result = ValidationResult(
            is_valid=True, error_messages=["Error 1", "Error 2"], warnings=["Warning 1"]
        )

        assert result.is_valid is True
        assert result.error_messages == ["Error 1", "Error 2"]
        assert result.warnings == ["Warning 1"]

    def test_validation_result_default_values(self) -> None:
        """Test ValidationResult default values for optional fields.

        Requirements: 1.4, 1.5
        """
        result = ValidationResult(is_valid=False)

        assert result.is_valid is False
        assert result.error_messages == []
        assert result.warnings == []

    def test_validation_result_add_error(self) -> None:
        """Test ValidationResult.add_error() method.

        Requirements: 1.4, 1.5
        """
        result = ValidationResult(is_valid=True)
        result.add_error("New error message")

        assert "New error message" in result.error_messages
        assert result.is_valid is False  # Should become invalid when error added

    def test_validation_result_add_warning(self) -> None:
        """Test ValidationResult.add_warning() method.

        Requirements: 1.4, 1.5
        """
        result = ValidationResult(is_valid=True)
        result.add_warning("New warning message")

        assert "New warning message" in result.warnings
        assert result.is_valid is True  # Should remain valid when warning added

    def test_validation_result_enhanced_methods(self) -> None:
        """Test enhanced ValidationResult methods.

        Requirements: 1.4, 1.5
        """
        result = ValidationResult(is_valid=True)

        # Test has_errors and has_warnings
        assert not result.has_errors()
        assert not result.has_warnings()

        result.add_warning("Test warning")
        assert not result.has_errors()
        assert result.has_warnings()

        result.add_error("Test error")
        assert result.has_errors()
        assert result.has_warnings()

        # Test get_summary
        summary = result.get_summary()
        assert "1 error(s)" in summary
        assert "1 warning(s)" in summary

    def test_validation_result_input_validation(self) -> None:
        """Test ValidationResult input validation.

        Requirements: 1.4, 1.5
        """
        result = ValidationResult(is_valid=True)

        # Test empty error message
        with pytest.raises(ValueError, match="Error message cannot be empty"):
            result.add_error("")

        with pytest.raises(ValueError, match="Error message cannot be empty"):
            result.add_error("   ")

        # Test empty warning message
        with pytest.raises(ValueError, match="Warning message cannot be empty"):
            result.add_warning("")

        with pytest.raises(ValueError, match="Warning message cannot be empty"):
            result.add_warning("   ")


class TestTransactionEntityValidation:
    """Test validation and error handling for transaction entities."""

    def test_component_transaction_immutability(self) -> None:
        """Test that ComponentTransaction is immutable (frozen dataclass).

        Requirements: 1.1, 1.4
        """
        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=TransactionOffer(trade_goods=1),
            request=TransactionOffer(commodities=1),
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        # Should not be able to modify frozen dataclass
        with pytest.raises(AttributeError):
            transaction.status = TransactionStatus.ACCEPTED

    def test_component_transaction_validation(self) -> None:
        """Test ComponentTransaction input validation.

        Requirements: 1.1, 1.4, 1.5
        """
        # Test invalid transaction_id
        with pytest.raises(ValueError, match="Transaction ID cannot be empty"):
            ComponentTransaction(
                transaction_id="",
                proposing_player="player1",
                target_player="player2",
                offer=TransactionOffer(trade_goods=1),
                request=TransactionOffer(commodities=1),
                status=TransactionStatus.PENDING,
                timestamp=datetime.now(),
            )

        # Test invalid transaction ID format
        with pytest.raises(
            ValueError, match="Transaction ID must contain only alphanumeric"
        ):
            ComponentTransaction(
                transaction_id="tx@001!",
                proposing_player="player1",
                target_player="player2",
                offer=TransactionOffer(trade_goods=1),
                request=TransactionOffer(commodities=1),
                status=TransactionStatus.PENDING,
                timestamp=datetime.now(),
            )

        # Test invalid proposing player ID
        with pytest.raises(ValueError, match="Proposing player ID cannot be empty"):
            ComponentTransaction(
                transaction_id="tx_001",
                proposing_player="",
                target_player="player2",
                offer=TransactionOffer(trade_goods=1),
                request=TransactionOffer(commodities=1),
                status=TransactionStatus.PENDING,
                timestamp=datetime.now(),
            )

        # Test invalid target player ID
        with pytest.raises(ValueError, match="Target player ID cannot be empty"):
            ComponentTransaction(
                transaction_id="tx_001",
                proposing_player="player1",
                target_player="   ",
                offer=TransactionOffer(trade_goods=1),
                request=TransactionOffer(commodities=1),
                status=TransactionStatus.PENDING,
                timestamp=datetime.now(),
            )

        # Test same player transaction
        with pytest.raises(ValueError, match="Players cannot transact with themselves"):
            ComponentTransaction(
                transaction_id="tx_001",
                proposing_player="player1",
                target_player="player1",
                offer=TransactionOffer(trade_goods=1),
                request=TransactionOffer(commodities=1),
                status=TransactionStatus.PENDING,
                timestamp=datetime.now(),
            )

    def test_component_transaction_timestamp_validation(self) -> None:
        """Test ComponentTransaction timestamp validation.

        Requirements: 1.1, 1.4, 1.5
        """
        from datetime import timedelta

        now = datetime.now()
        earlier = now - timedelta(seconds=1)  # Ensure earlier is actually before now

        # Test invalid completion timestamp (before transaction timestamp)
        with pytest.raises(
            ValueError,
            match="Completion timestamp cannot be before transaction timestamp",
        ):
            ComponentTransaction(
                transaction_id="tx_001",
                proposing_player="player1",
                target_player="player2",
                offer=TransactionOffer(trade_goods=1),
                request=TransactionOffer(commodities=1),
                status=TransactionStatus.ACCEPTED,
                timestamp=now,
                completion_timestamp=earlier,
            )


class TestComponentValidator:
    """Test ComponentValidator class for neighbor requirement and resource validation.

    Requirements: 2.1, 2.2, 2.3, 2.4, 2.5
    """

    def test_component_validator_creation(self) -> None:
        """Test that ComponentValidator can be created with required dependencies.

        Requirements: 2.1, 2.2, 2.3, 2.4, 2.5
        """
        # RED: This will fail until we create ComponentValidator
        from ti4.core.rule_28_deals import ComponentValidator

        mock_galaxy = Mock()
        mock_game_state = Mock()

        validator = ComponentValidator(galaxy=mock_galaxy, game_state=mock_game_state)

        assert validator is not None
        assert validator._galaxy is mock_galaxy
        assert validator._game_state is mock_game_state

    def test_validate_neighbor_requirement_success(self) -> None:
        """Test neighbor validation when players are neighbors.

        Requirements: 2.1, 2.2
        """
        from ti4.core.rule_28_deals import ComponentValidator

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True
        mock_game_state = Mock()

        validator = ComponentValidator(galaxy=mock_galaxy, game_state=mock_game_state)

        result = validator.validate_neighbor_requirement("player1", "player2")

        assert result is True
        mock_galaxy.are_players_neighbors.assert_called_once_with("player1", "player2")

    def test_validate_neighbor_requirement_failure(self) -> None:
        """Test neighbor validation when players are not neighbors.

        Requirements: 2.1, 2.2
        """
        from ti4.core.rule_28_deals import ComponentValidator

        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = False
        mock_game_state = Mock()

        validator = ComponentValidator(galaxy=mock_galaxy, game_state=mock_game_state)

        result = validator.validate_neighbor_requirement("player1", "player3")

        assert result is False
        mock_galaxy.are_players_neighbors.assert_called_once_with("player1", "player3")

    def test_validate_trade_goods_availability_success(self) -> None:
        """Test trade goods validation when player has sufficient trade goods.

        Requirements: 2.3
        """
        from ti4.core.rule_28_deals import ComponentValidator

        mock_galaxy = Mock()
        mock_game_state = Mock()
        mock_player = Mock()
        mock_player.id = "player1"
        mock_player.get_trade_goods.return_value = 5
        mock_game_state.players = [mock_player]

        validator = ComponentValidator(galaxy=mock_galaxy, game_state=mock_game_state)

        result = validator.validate_trade_goods_availability("player1", 3)

        assert result is True
        mock_player.get_trade_goods.assert_called_once()

    def test_validate_trade_goods_availability_failure(self) -> None:
        """Test trade goods validation when player has insufficient trade goods.

        Requirements: 2.3
        """
        from ti4.core.rule_28_deals import ComponentValidator

        mock_galaxy = Mock()
        mock_game_state = Mock()
        mock_player = Mock()
        mock_player.id = "player1"
        mock_player.get_trade_goods.return_value = 2
        mock_game_state.players = [mock_player]

        validator = ComponentValidator(galaxy=mock_galaxy, game_state=mock_game_state)

        result = validator.validate_trade_goods_availability("player1", 5)

        assert result is False
        mock_player.get_trade_goods.assert_called_once()

    def test_validate_commodity_availability_success(self) -> None:
        """Test commodity validation when player has sufficient commodities.

        Requirements: 2.4
        """
        from ti4.core.rule_28_deals import ComponentValidator

        mock_galaxy = Mock()
        mock_game_state = Mock()
        mock_player = Mock()
        mock_player.id = "player1"
        mock_player.get_commodities.return_value = 4
        mock_game_state.players = [mock_player]

        validator = ComponentValidator(galaxy=mock_galaxy, game_state=mock_game_state)

        result = validator.validate_commodity_availability("player1", 2)

        assert result is True
        mock_player.get_commodities.assert_called_once()

    def test_validate_commodity_availability_failure(self) -> None:
        """Test commodity validation when player has insufficient commodities.

        Requirements: 2.4
        """
        from ti4.core.rule_28_deals import ComponentValidator

        mock_galaxy = Mock()
        mock_game_state = Mock()
        mock_player = Mock()
        mock_player.id = "player1"
        mock_player.get_commodities.return_value = 1
        mock_game_state.players = [mock_player]

        validator = ComponentValidator(galaxy=mock_galaxy, game_state=mock_game_state)

        result = validator.validate_commodity_availability("player1", 3)

        assert result is False
        mock_player.get_commodities.assert_called_once()

    def test_validate_promissory_note_availability_success(self) -> None:
        """Test promissory note validation when player owns the note.

        Requirements: 2.5
        """
        from ti4.core.rule_28_deals import ComponentValidator
        from ti4.core.transactions import PromissoryNote, PromissoryNoteType

        mock_galaxy = Mock()
        mock_game_state = Mock()
        mock_promissory_manager = Mock()

        test_note = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player2"
        )

        mock_promissory_manager.get_player_hand.return_value = [test_note]
        mock_game_state.promissory_note_manager = mock_promissory_manager

        validator = ComponentValidator(galaxy=mock_galaxy, game_state=mock_game_state)

        result = validator.validate_promissory_note_availability("player1", test_note)

        assert result is True
        mock_promissory_manager.get_player_hand.assert_called_once_with("player1")

    def test_validate_promissory_note_availability_failure(self) -> None:
        """Test promissory note validation when player doesn't own the note.

        Requirements: 2.5
        """
        from ti4.core.rule_28_deals import ComponentValidator
        from ti4.core.transactions import PromissoryNote, PromissoryNoteType

        mock_galaxy = Mock()
        mock_game_state = Mock()
        mock_promissory_manager = Mock()

        test_note = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player2"
        )

        other_note = PromissoryNote(
            note_type=PromissoryNoteType.CEASEFIRE, issuing_player="player3"
        )

        mock_promissory_manager.get_player_hand.return_value = [other_note]
        mock_game_state.promissory_note_manager = mock_promissory_manager

        validator = ComponentValidator(galaxy=mock_galaxy, game_state=mock_game_state)

        result = validator.validate_promissory_note_availability("player1", test_note)

        assert result is False
        mock_promissory_manager.get_player_hand.assert_called_once_with("player1")

    def test_validate_transaction_comprehensive(self) -> None:
        """Test comprehensive transaction validation with all components.

        Requirements: 2.1, 2.2, 2.3, 2.4, 2.5
        """
        from ti4.core.rule_28_deals import ComponentValidator
        from ti4.core.transactions import PromissoryNote, PromissoryNoteType

        # Setup mocks for successful validation
        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = True

        mock_game_state = Mock()
        mock_player1 = Mock()
        mock_player1.id = "player1"
        mock_player1.get_trade_goods.return_value = 5
        mock_player1.get_commodities.return_value = 3

        mock_player2 = Mock()
        mock_player2.id = "player2"
        mock_player2.get_trade_goods.return_value = 2
        mock_player2.get_commodities.return_value = 1

        mock_game_state.players = [mock_player1, mock_player2]

        test_note = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player2"
        )

        mock_promissory_manager = Mock()
        mock_promissory_manager.get_player_hand.return_value = [test_note]
        mock_game_state.promissory_note_manager = mock_promissory_manager

        # Create transaction
        offer = TransactionOffer(trade_goods=3, promissory_notes=[test_note])
        request = TransactionOffer(commodities=1)

        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        validator = ComponentValidator(galaxy=mock_galaxy, game_state=mock_game_state)

        result = validator.validate_transaction(transaction)

        assert result.is_valid is True
        assert len(result.error_messages) == 0
        assert len(result.warnings) == 0

    def test_validate_transaction_with_errors(self) -> None:
        """Test comprehensive transaction validation with multiple errors.

        Requirements: 2.1, 2.2, 2.3, 2.4, 2.5
        """
        from ti4.core.rule_28_deals import ComponentValidator
        from ti4.core.transactions import PromissoryNote, PromissoryNoteType

        # Setup mocks for failed validation
        mock_galaxy = Mock()
        mock_galaxy.are_players_neighbors.return_value = False  # Not neighbors

        mock_game_state = Mock()
        mock_player1 = Mock()
        mock_player1.id = "player1"
        mock_player1.get_trade_goods.return_value = 1  # Insufficient trade goods
        mock_player1.get_commodities.return_value = 0  # No commodities

        mock_player2 = Mock()
        mock_player2.id = "player2"
        mock_player2.get_trade_goods.return_value = 0  # No trade goods
        mock_player2.get_commodities.return_value = 0  # No commodities

        mock_game_state.players = [mock_player1, mock_player2]

        test_note = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player2"
        )

        mock_promissory_manager = Mock()
        mock_promissory_manager.get_player_hand.return_value = []  # Player doesn't have the note
        mock_game_state.promissory_note_manager = mock_promissory_manager

        # Create transaction with invalid offers
        offer = TransactionOffer(
            trade_goods=5, promissory_notes=[test_note]
        )  # Too many trade goods
        request = TransactionOffer(commodities=2)  # Player2 doesn't have commodities

        transaction = ComponentTransaction(
            transaction_id="tx_001",
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        validator = ComponentValidator(galaxy=mock_galaxy, game_state=mock_game_state)

        result = validator.validate_transaction(transaction)

        assert result.is_valid is False
        assert len(result.error_messages) > 0
        # Should have errors for: not neighbors, insufficient trade goods, missing promissory note, insufficient commodities
        assert any("neighbor" in msg.lower() for msg in result.error_messages)
        assert any("trade goods" in msg.lower() for msg in result.error_messages)
        assert any("promissory note" in msg.lower() for msg in result.error_messages)
        assert any("commodities" in msg.lower() for msg in result.error_messages)

    def test_input_validation_for_neighbor_requirement(self) -> None:
        """Test input validation for neighbor requirement validation.

        Requirements: 2.1, 2.2 - Defensive programming
        """
        from ti4.core.rule_28_deals import ComponentValidator

        mock_galaxy = Mock()
        mock_game_state = Mock()

        validator = ComponentValidator(galaxy=mock_galaxy, game_state=mock_game_state)

        # Test empty player1 ID
        with pytest.raises(ValueError, match="Player1 ID cannot be empty"):
            validator.validate_neighbor_requirement("", "player2")

        # Test empty player2 ID
        with pytest.raises(ValueError, match="Player2 ID cannot be empty"):
            validator.validate_neighbor_requirement("player1", "   ")

        # Test same player IDs
        with pytest.raises(ValueError, match="Players cannot be the same"):
            validator.validate_neighbor_requirement("player1", "player1")

    def test_input_validation_for_resource_availability(self) -> None:
        """Test input validation for resource availability checks.

        Requirements: 2.3, 2.4 - Defensive programming
        """
        from ti4.core.rule_28_deals import ComponentValidator

        mock_galaxy = Mock()
        mock_game_state = Mock()

        validator = ComponentValidator(galaxy=mock_galaxy, game_state=mock_game_state)

        # Test empty player ID for trade goods
        with pytest.raises(ValueError, match="Player ID cannot be empty"):
            validator.validate_trade_goods_availability("", 5)

        # Test negative amount for trade goods
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            validator.validate_trade_goods_availability("player1", -1)

        # Test empty player ID for commodities
        with pytest.raises(ValueError, match="Player ID cannot be empty"):
            validator.validate_commodity_availability("   ", 3)

        # Test negative amount for commodities
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            validator.validate_commodity_availability("player1", -5)

    def test_input_validation_for_promissory_note_availability(self) -> None:
        """Test input validation for promissory note availability checks.

        Requirements: 2.5 - Defensive programming
        """
        from ti4.core.rule_28_deals import ComponentValidator
        from ti4.core.transactions import PromissoryNote, PromissoryNoteType

        mock_galaxy = Mock()
        mock_game_state = Mock()

        validator = ComponentValidator(galaxy=mock_galaxy, game_state=mock_game_state)

        test_note = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player2"
        )

        # Test empty player ID
        with pytest.raises(ValueError, match="Player ID cannot be empty"):
            validator.validate_promissory_note_availability("", test_note)

        # Test None promissory note
        with pytest.raises(ValueError, match="Promissory note cannot be None"):
            validator.validate_promissory_note_availability("player1", None)


class TestPromissoryNoteExchangeSystem:
    """Test promissory note exchange system for Rule 28 deals.

    Requirements: 4.1, 4.2, 4.3, 4.4, 4.5
    """

    def test_promissory_note_immediate_effect_activation(self) -> None:
        """Test that immediate effects are activated when promissory notes are exchanged.

        Requirements: 4.4, 4.5
        """
        # RED: This will fail until we implement immediate effect activation
        from ti4.core.rule_28_deals import PromissoryNoteExchangeHandler
        from ti4.core.transactions import PromissoryNote, PromissoryNoteType

        # Setup proper mocks
        mock_game_state = Mock()
        mock_promissory_manager = Mock()
        mock_player = Mock()
        mock_player.id = "player2"

        note = PromissoryNote(
            note_type=PromissoryNoteType.SUPPORT_FOR_THE_THRONE,
            issuing_player="player1",
        )

        # Mock that player1 owns the note
        mock_promissory_manager.get_player_hand.return_value = [note]
        mock_game_state.promissory_note_manager = mock_promissory_manager
        mock_game_state.players = [mock_player]

        # Mock game state methods for victory points
        mock_game_state.get_victory_points.return_value = 5
        mock_game_state.victory_points_to_win = 10

        handler = PromissoryNoteExchangeHandler(game_state=mock_game_state)

        # Exchange the note and check if immediate effects are activated
        result = handler.exchange_promissory_note(
            from_player="player1", to_player="player2", note=note
        )

        assert result.success is True
        assert result.immediate_effects_activated is True
        assert "Support for the Throne" in result.activated_effects

    def test_promissory_note_exchange_without_immediate_effects(self) -> None:
        """Test promissory note exchange for notes without immediate effects.

        Requirements: 4.1, 4.2, 4.3
        """
        # RED: This will fail until we implement the exchange handler
        from ti4.core.rule_28_deals import PromissoryNoteExchangeHandler
        from ti4.core.transactions import PromissoryNote, PromissoryNoteType

        # Setup proper mocks
        mock_game_state = Mock()
        mock_promissory_manager = Mock()

        note = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player1"
        )

        # Mock that player1 owns the note
        mock_promissory_manager.get_player_hand.return_value = [note]
        mock_game_state.promissory_note_manager = mock_promissory_manager

        handler = PromissoryNoteExchangeHandler(game_state=mock_game_state)

        # Exchange the note
        result = handler.exchange_promissory_note(
            from_player="player1", to_player="player2", note=note
        )

        assert result.success is True
        assert result.immediate_effects_activated is False
        assert len(result.activated_effects) == 0

    def test_promissory_note_exchange_validation_failure(self) -> None:
        """Test promissory note exchange when validation fails.

        Requirements: 4.2, 4.3
        """
        # RED: This will fail until we implement validation
        from ti4.core.rule_28_deals import PromissoryNoteExchangeHandler
        from ti4.core.transactions import PromissoryNote, PromissoryNoteType

        mock_game_state = Mock()
        mock_promissory_manager = Mock()
        mock_promissory_manager.get_player_hand.return_value = []  # Player doesn't own the note
        mock_game_state.promissory_note_manager = mock_promissory_manager

        handler = PromissoryNoteExchangeHandler(game_state=mock_game_state)

        note = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player2"
        )

        # Try to exchange a note the player doesn't own
        result = handler.exchange_promissory_note(
            from_player="player1", to_player="player2", note=note
        )

        assert result.success is False
        assert "does not own" in result.error_message
        assert result.immediate_effects_activated is False

    def test_support_for_throne_immediate_effect(self) -> None:
        """Test Support for the Throne immediate effect activation.

        Requirements: 4.4, 4.5
        """
        # RED: This will fail until we implement specific immediate effects
        from ti4.core.rule_28_deals import PromissoryNoteExchangeHandler
        from ti4.core.transactions import PromissoryNote, PromissoryNoteType

        # Setup proper mocks
        mock_game_state = Mock()
        mock_promissory_manager = Mock()
        mock_player = Mock()
        mock_player.id = "player2"

        note = PromissoryNote(
            note_type=PromissoryNoteType.SUPPORT_FOR_THE_THRONE,
            issuing_player="player1",
        )

        # Mock that player1 owns the note
        mock_promissory_manager.get_player_hand.return_value = [note]
        mock_game_state.promissory_note_manager = mock_promissory_manager
        mock_game_state.players = [mock_player]

        # Mock game state methods for victory points
        mock_game_state.get_victory_points.return_value = 5
        mock_game_state.victory_points_to_win = 10

        handler = PromissoryNoteExchangeHandler(game_state=mock_game_state)

        # Exchange Support for the Throne
        result = handler.exchange_promissory_note(
            from_player="player1", to_player="player2", note=note
        )

        assert result.success is True
        assert result.immediate_effects_activated is True
        # Verify that the Support for the Throne effect was activated
        assert "Support for the Throne" in result.activated_effects

    def test_promissory_note_exchange_integration_with_resource_manager(self) -> None:
        """Test that promissory note exchange integrates with existing ResourceManager.

        Requirements: 4.1, 4.2, 4.3
        """
        # This tests integration with existing functionality
        from ti4.core.rule_28_deals import (
            PromissoryNoteExchangeHandler,
        )
        from ti4.core.transactions import PromissoryNote, PromissoryNoteType

        mock_game_state = Mock()
        mock_promissory_manager = Mock()

        note = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player2"
        )

        mock_promissory_manager.get_player_hand.return_value = [note]
        mock_game_state.promissory_note_manager = mock_promissory_manager

        handler = PromissoryNoteExchangeHandler(game_state=mock_game_state)

        # Exchange should use ResourceManager internally
        result = handler.exchange_promissory_note(
            from_player="player1", to_player="player2", note=note
        )

        assert result.success is True
        # Verify the note was transferred using the promissory note manager
        mock_promissory_manager.add_note_to_hand.assert_called_once_with(
            note, "player2"
        )

    def test_promissory_note_exchange_input_validation(self) -> None:
        """Test input validation for promissory note exchange.

        Requirements: 4.1, 4.2, 4.3 - Defensive programming
        """
        from ti4.core.rule_28_deals import PromissoryNoteExchangeHandler
        from ti4.core.transactions import PromissoryNote, PromissoryNoteType

        mock_game_state = Mock()
        handler = PromissoryNoteExchangeHandler(game_state=mock_game_state)

        note = PromissoryNote(
            note_type=PromissoryNoteType.TRADE_AGREEMENT, issuing_player="player1"
        )

        # Test empty from_player
        result = handler.exchange_promissory_note("", "player2", note)
        assert result.success is False
        assert "From player ID cannot be empty" in result.error_message

        # Test empty to_player
        result = handler.exchange_promissory_note("player1", "   ", note)
        assert result.success is False
        assert "To player ID cannot be empty" in result.error_message

        # Test same player
        result = handler.exchange_promissory_note("player1", "player1", note)
        assert result.success is False
        assert (
            "Cannot exchange promissory note with the same player"
            in result.error_message
        )

        # Test None note
        result = handler.exchange_promissory_note("player1", "player2", None)
        assert result.success is False
        assert "Promissory note cannot be None" in result.error_message

    def test_promissory_note_immediate_effects_edge_cases(self) -> None:
        """Test edge cases for immediate effects system.

        Requirements: 4.4, 4.5 - Defensive programming
        """
        from ti4.core.rule_28_deals import PromissoryNoteImmediateEffects
        from ti4.core.transactions import PromissoryNote, PromissoryNoteType

        mock_game_state = Mock()
        mock_game_state.players = []  # No players

        effects_handler = PromissoryNoteImmediateEffects(game_state=mock_game_state)

        # Test with None note
        effects = effects_handler.get_immediate_effects(None, "player1")
        assert effects == []

        # Test activation with empty effects list
        activated = effects_handler.activate_immediate_effects(
            PromissoryNote(PromissoryNoteType.TRADE_AGREEMENT, "player1"), "player2", []
        )
        assert activated == []

        # Test activation with empty receiving player
        activated = effects_handler.activate_immediate_effects(
            PromissoryNote(PromissoryNoteType.SUPPORT_FOR_THE_THRONE, "player1"),
            "",
            ["Support for the Throne"],
        )
        assert activated == []

        # Test activation when player not found
        activated = effects_handler.activate_immediate_effects(
            PromissoryNote(PromissoryNoteType.SUPPORT_FOR_THE_THRONE, "player1"),
            "nonexistent_player",
            ["Support for the Throne"],
        )
        assert activated == []


class TestEnhancedTransactionManager:
    """Test enhanced TransactionManager for Rule 28 component deals.

    Requirements: 1.1, 1.2, 1.3, 1.4, 1.5
    """

    def test_enhanced_transaction_manager_creation(self) -> None:
        """Test that enhanced TransactionManager can be created with component support.

        Requirements: 1.1, 1.4, 1.5
        """
        from ti4.core.rule_28_deals import EnhancedTransactionManager

        mock_galaxy = Mock()
        mock_game_state = Mock()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )

        assert manager is not None
        assert manager._galaxy is mock_galaxy
        assert manager._game_state is mock_game_state

    def test_propose_transaction_success(self) -> None:
        """Test successful transaction proposal with validation.

        Requirements: 1.1, 1.2, 1.4, 1.5
        """
        from ti4.core.rule_28_deals import EnhancedTransactionManager

        # Setup mocks for successful validation
        mock_galaxy = Mock()
        mock_game_state = Mock()
        mock_validator = Mock()
        mock_validator.validate_transaction.return_value = ValidationResult(
            is_valid=True
        )

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )
        manager._validator = mock_validator

        offer = TransactionOffer(trade_goods=3)
        request = TransactionOffer(commodities=2)

        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
        )

        assert transaction is not None
        assert transaction.proposing_player == "player1"
        assert transaction.target_player == "player2"
        assert transaction.offer == offer
        assert transaction.request == request
        assert transaction.status == TransactionStatus.PENDING
        assert transaction.transaction_id is not None

    def test_propose_transaction_validation_failure(self) -> None:
        """Test transaction proposal with validation failure.

        Requirements: 1.1, 1.2, 1.4, 1.5
        """
        from ti4.core.rule_28_deals import (
            EnhancedTransactionManager,
            TransactionValidationError,
        )

        # Setup mocks for failed validation
        mock_galaxy = Mock()
        mock_game_state = Mock()
        mock_validator = Mock()
        validation_result = ValidationResult(is_valid=False)
        validation_result.add_error("Players are not neighbors")
        mock_validator.validate_transaction.return_value = validation_result

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )
        manager._validator = mock_validator

        offer = TransactionOffer(trade_goods=3)
        request = TransactionOffer(commodities=2)

        with pytest.raises(
            TransactionValidationError, match="Players are not neighbors"
        ):
            manager.propose_transaction(
                proposing_player="player1",
                target_player="player2",
                offer=offer,
                request=request,
            )

    def test_accept_transaction_success(self) -> None:
        """Test successful transaction acceptance with immediate execution.

        Requirements: 1.2, 1.3, 1.4, 1.5
        """
        from ti4.core.rule_28_deals import EnhancedTransactionManager

        # Setup mocks
        mock_galaxy = Mock()
        mock_game_state = Mock()
        mock_validator = Mock()
        mock_validator.validate_transaction.return_value = ValidationResult(
            is_valid=True
        )
        mock_resource_manager = Mock()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )
        manager._validator = mock_validator
        manager._resource_manager = mock_resource_manager

        # Create a pending transaction
        offer = TransactionOffer(trade_goods=3)
        request = TransactionOffer(commodities=2)

        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
        )

        # Accept the transaction
        result = manager.accept_transaction(transaction.transaction_id)

        assert result.success is True
        assert result.transaction.status == TransactionStatus.ACCEPTED
        assert result.transaction.completion_timestamp is not None

        # Verify resource transfers were called
        mock_resource_manager.transfer_trade_goods.assert_called_once_with(
            "player1", "player2", 3
        )
        mock_resource_manager.transfer_commodities.assert_called_once_with(
            "player2", "player1", 2
        )

    def test_accept_transaction_not_found(self) -> None:
        """Test accepting non-existent transaction.

        Requirements: 1.2, 1.3, 1.4, 1.5
        """
        from ti4.core.rule_28_deals import (
            EnhancedTransactionManager,
            TransactionNotFoundError,
        )

        mock_galaxy = Mock()
        mock_game_state = Mock()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )

        with pytest.raises(TransactionNotFoundError, match="Transaction .* not found"):
            manager.accept_transaction("nonexistent_tx")

    def test_reject_transaction_success(self) -> None:
        """Test successful transaction rejection.

        Requirements: 1.2, 1.3, 1.4, 1.5
        """
        from ti4.core.rule_28_deals import EnhancedTransactionManager

        # Setup mocks
        mock_galaxy = Mock()
        mock_game_state = Mock()
        mock_validator = Mock()
        mock_validator.validate_transaction.return_value = ValidationResult(
            is_valid=True
        )

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )
        manager._validator = mock_validator

        # Create a pending transaction
        offer = TransactionOffer(trade_goods=3)
        request = TransactionOffer(commodities=2)

        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
        )

        # Reject the transaction
        manager.reject_transaction(transaction.transaction_id)

        # Verify transaction status changed
        updated_transaction = manager.get_transaction(transaction.transaction_id)
        assert updated_transaction.status == TransactionStatus.REJECTED

    def test_cancel_transaction_success(self) -> None:
        """Test successful transaction cancellation by proposing player.

        Requirements: 1.2, 1.3, 1.4, 1.5
        """
        from ti4.core.rule_28_deals import EnhancedTransactionManager

        # Setup mocks
        mock_galaxy = Mock()
        mock_game_state = Mock()
        mock_validator = Mock()
        mock_validator.validate_transaction.return_value = ValidationResult(
            is_valid=True
        )

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )
        manager._validator = mock_validator

        # Create a pending transaction
        offer = TransactionOffer(trade_goods=3)
        request = TransactionOffer(commodities=2)

        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
        )

        # Cancel the transaction
        manager.cancel_transaction(transaction.transaction_id, "player1")

        # Verify transaction status changed
        updated_transaction = manager.get_transaction(transaction.transaction_id)
        assert updated_transaction.status == TransactionStatus.CANCELLED

    def test_get_pending_transactions_for_player(self) -> None:
        """Test getting pending transactions for a specific player.

        Requirements: 1.4, 1.5
        """
        from ti4.core.rule_28_deals import EnhancedTransactionManager

        # Setup mocks
        mock_galaxy = Mock()
        mock_game_state = Mock()
        mock_validator = Mock()
        mock_validator.validate_transaction.return_value = ValidationResult(
            is_valid=True
        )

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )
        manager._validator = mock_validator

        # Create transactions
        offer1 = TransactionOffer(trade_goods=3)
        request1 = TransactionOffer(commodities=2)

        transaction1 = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=offer1,
            request=request1,
        )

        offer2 = TransactionOffer(trade_goods=1)
        request2 = TransactionOffer(commodities=1)

        transaction2 = manager.propose_transaction(
            proposing_player="player3",
            target_player="player2",
            offer=offer2,
            request=request2,
        )

        # Get pending transactions for player2 (target)
        pending = manager.get_pending_transactions("player2")

        assert len(pending) == 2
        assert transaction1 in pending
        assert transaction2 in pending

        # Get pending transactions for player1 (proposer)
        pending_player1 = manager.get_pending_transactions("player1")

        assert len(pending_player1) == 1
        assert transaction1 in pending_player1

    def test_get_transaction_history_for_player(self) -> None:
        """Test getting transaction history for a specific player.

        Requirements: 1.4, 1.5
        """
        from ti4.core.rule_28_deals import EnhancedTransactionManager

        # Setup mocks
        mock_galaxy = Mock()
        mock_game_state = Mock()
        mock_validator = Mock()
        mock_validator.validate_transaction.return_value = ValidationResult(
            is_valid=True
        )
        mock_resource_manager = Mock()

        manager = EnhancedTransactionManager(
            galaxy=mock_galaxy, game_state=mock_game_state
        )
        manager._validator = mock_validator
        manager._resource_manager = mock_resource_manager

        # Create and accept a transaction
        offer = TransactionOffer(trade_goods=3)
        request = TransactionOffer(commodities=2)

        transaction = manager.propose_transaction(
            proposing_player="player1",
            target_player="player2",
            offer=offer,
            request=request,
        )

        manager.accept_transaction(transaction.transaction_id)

        # Get transaction history
        history = manager.get_transaction_history("player1")

        assert len(history) == 1
        assert history[0].status == TransactionStatus.ACCEPTED
        assert history[0].completion_timestamp is not None
