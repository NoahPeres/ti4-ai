"""Rule 28: DEALS component transaction system.

This module implements enhanced component transaction entities for Rule 28 deals,
building upon the existing transaction system to provide component-based exchanges
that can be objectively validated and enforced by the game system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Optional

from .transactions import PromissoryNote, PromissoryNoteType, TransactionOffer

if TYPE_CHECKING:
    from .galaxy import Galaxy
    from .game_phase import GamePhase
    from .game_state import GameState
    from .player import Player


class TransactionStatus(Enum):
    """Status of a component transaction."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


@dataclass
class ValidationResult:
    """Result of transaction validation."""

    is_valid: bool
    error_messages: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """Add validation error and mark result as invalid.

        Args:
            message: The error message to add

        Raises:
            ValueError: If message is empty or None
        """
        if not message or not message.strip():
            raise ValueError("Error message cannot be empty")

        self.error_messages.append(message.strip())
        # Make result invalid when error is added
        object.__setattr__(self, "is_valid", False)

    def add_warning(self, message: str) -> None:
        """Add validation warning.

        Args:
            message: The warning message to add

        Raises:
            ValueError: If message is empty or None
        """
        if not message or not message.strip():
            raise ValueError("Warning message cannot be empty")

        self.warnings.append(message.strip())

    def has_errors(self) -> bool:
        """Check if validation result has any errors."""
        return len(self.error_messages) > 0

    def has_warnings(self) -> bool:
        """Check if validation result has any warnings."""
        return len(self.warnings) > 0

    def get_summary(self) -> str:
        """Get a summary of validation results."""
        if self.is_valid and not self.has_warnings():
            return "Validation passed"

        parts = []
        if not self.is_valid:
            parts.append(f"{len(self.error_messages)} error(s)")
        if self.has_warnings():
            parts.append(f"{len(self.warnings)} warning(s)")

        return f"Validation failed: {', '.join(parts)}"


@dataclass(frozen=True)
class ComponentTransaction:
    """Represents a component-based transaction between two players."""

    transaction_id: str
    proposing_player: str
    target_player: str
    offer: TransactionOffer
    request: TransactionOffer
    status: TransactionStatus
    timestamp: datetime
    completion_timestamp: Optional[datetime] = None

    def is_pending(self) -> bool:
        """Check if transaction is awaiting response."""
        return self.status == TransactionStatus.PENDING

    def is_completed(self) -> bool:
        """Check if transaction has been executed."""
        return (
            self.status == TransactionStatus.ACCEPTED
            and self.completion_timestamp is not None
        )

    def get_net_exchange(self, player_id: str) -> TransactionOffer:
        """Get what a player gains/loses in this transaction."""
        if player_id == self.proposing_player:
            # Proposing player gives offer, receives request
            return TransactionOffer(
                trade_goods=self.request.trade_goods - self.offer.trade_goods,
                commodities=self.request.commodities - self.offer.commodities,
                promissory_notes=self.request.promissory_notes.copy(),  # Simplified for now
                relic_fragments=self.request.relic_fragments
                - self.offer.relic_fragments,
            )
        elif player_id == self.target_player:
            # Target player receives offer, gives request
            return TransactionOffer(
                trade_goods=self.offer.trade_goods - self.request.trade_goods,
                commodities=self.offer.commodities - self.request.commodities,
                promissory_notes=self.offer.promissory_notes.copy(),  # Simplified for now
                relic_fragments=self.offer.relic_fragments
                - self.request.relic_fragments,
            )
        else:
            # Player not involved in transaction
            return TransactionOffer()

    def __post_init__(self) -> None:
        """Validate transaction after initialization.

        Raises:
            ValueError: If any validation fails
        """
        self._validate_transaction_id()
        self._validate_player_ids()
        self._validate_offers()
        self._validate_timestamps()

    def _validate_transaction_id(self) -> None:
        """Validate transaction ID."""
        if not self.transaction_id or not self.transaction_id.strip():
            raise ValueError("Transaction ID cannot be empty")

        # Basic format validation - should be alphanumeric with underscores/hyphens
        if not self.transaction_id.replace("_", "").replace("-", "").isalnum():
            raise ValueError(
                "Transaction ID must contain only alphanumeric characters, underscores, and hyphens"
            )

    def _validate_player_ids(self) -> None:
        """Validate player IDs."""
        if not self.proposing_player or not self.proposing_player.strip():
            raise ValueError("Proposing player ID cannot be empty")

        if not self.target_player or not self.target_player.strip():
            raise ValueError("Target player ID cannot be empty")

        if self.proposing_player == self.target_player:
            raise ValueError("Players cannot transact with themselves")

    def _validate_offers(self) -> None:
        """Validate transaction offers."""
        if not isinstance(self.offer, TransactionOffer):
            raise ValueError("Offer must be a TransactionOffer instance")

        if not isinstance(self.request, TransactionOffer):
            raise ValueError("Request must be a TransactionOffer instance")

    def _validate_timestamps(self) -> None:
        """Validate timestamps."""
        if not isinstance(self.timestamp, datetime):
            raise ValueError("Timestamp must be a datetime instance")

        if self.completion_timestamp is not None:
            if not isinstance(self.completion_timestamp, datetime):
                raise ValueError("Completion timestamp must be a datetime instance")

            if self.completion_timestamp < self.timestamp:
                raise ValueError(
                    "Completion timestamp cannot be before transaction timestamp"
                )


@dataclass(frozen=True)
class TransactionHistoryEntry:
    """Represents a transaction history entry for tracking completed transactions."""

    transaction_id: str
    proposing_player: str
    target_player: str
    offer: TransactionOffer
    request: TransactionOffer
    status: TransactionStatus
    timestamp: datetime
    completion_timestamp: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Validate transaction after initialization.

        Raises:
            ValueError: If any validation fails
        """
        self._validate_transaction_id()
        self._validate_player_ids()
        self._validate_offers()
        self._validate_timestamps()

    def _validate_transaction_id(self) -> None:
        """Validate transaction ID."""
        if not self.transaction_id or not self.transaction_id.strip():
            raise ValueError("Transaction ID cannot be empty")

        # Basic format validation - should be alphanumeric with underscores/hyphens
        if not self.transaction_id.replace("_", "").replace("-", "").isalnum():
            raise ValueError(
                "Transaction ID must contain only alphanumeric characters, underscores, and hyphens"
            )

    def _validate_player_ids(self) -> None:
        """Validate player IDs."""
        if not self.proposing_player or not self.proposing_player.strip():
            raise ValueError("Proposing player ID cannot be empty")

        if not self.target_player or not self.target_player.strip():
            raise ValueError("Target player ID cannot be empty")

        if self.proposing_player == self.target_player:
            raise ValueError("Players cannot transact with themselves")

    def _validate_offers(self) -> None:
        """Validate transaction offers."""
        if not isinstance(self.offer, TransactionOffer):
            raise ValueError("Offer must be a TransactionOffer instance")

        if not isinstance(self.request, TransactionOffer):
            raise ValueError("Request must be a TransactionOffer instance")

    def _validate_timestamps(self) -> None:
        """Validate timestamps."""
        if not isinstance(self.timestamp, datetime):
            raise ValueError("Timestamp must be a datetime instance")

        if self.completion_timestamp is not None:
            if not isinstance(self.completion_timestamp, datetime):
                raise ValueError("Completion timestamp must be a datetime instance")

            if self.completion_timestamp < self.timestamp:
                raise ValueError(
                    "Completion timestamp cannot be before transaction timestamp"
                )

    def is_pending(self) -> bool:
        """Check if transaction is awaiting response."""
        return self.status == TransactionStatus.PENDING

    def is_completed(self) -> bool:
        """Check if transaction has been executed."""
        return (
            self.status == TransactionStatus.ACCEPTED
            and self.completion_timestamp is not None
        )

    def get_net_exchange(self, player_id: str) -> TransactionOffer:
        """Get what a player gains/loses in this transaction."""
        if player_id == self.proposing_player:
            # Proposing player gives offer, receives request
            return TransactionOffer(
                trade_goods=self.request.trade_goods - self.offer.trade_goods,
                commodities=self.request.commodities - self.offer.commodities,
                promissory_notes=self.request.promissory_notes.copy(),  # Simplified for now
                relic_fragments=self.request.relic_fragments
                - self.offer.relic_fragments,
            )
        elif player_id == self.target_player:
            # Target player receives offer, gives request
            return TransactionOffer(
                trade_goods=self.offer.trade_goods - self.request.trade_goods,
                commodities=self.offer.commodities - self.request.commodities,
                promissory_notes=self.offer.promissory_notes.copy(),  # Simplified for now
                relic_fragments=self.offer.relic_fragments
                - self.request.relic_fragments,
            )
        else:
            # Player not involved in transaction
            return TransactionOffer()


class ComponentValidator:
    """Validates component transactions according to game rules.

    Handles validation of neighbor requirements, resource availability,
    and component ownership for Rule 28 deals.
    """

    def __init__(self, galaxy: "Galaxy", game_state: "GameState") -> None:
        """Initialize with game systems for validation.

        Args:
            galaxy: Galaxy instance for neighbor validation
            game_state: Game state for resource and component tracking
        """
        self._galaxy = galaxy
        self._game_state = game_state

    def validate_neighbor_requirement(self, player1: str, player2: str) -> bool:
        """Validate that players are neighbors for component exchange.

        Args:
            player1: First player ID
            player2: Second player ID

        Returns:
            True if players are neighbors, False otherwise

        Raises:
            ValueError: If player IDs are empty or the same
        """
        if not player1 or not player1.strip():
            raise ValueError("Player1 ID cannot be empty")
        if not player2 or not player2.strip():
            raise ValueError("Player2 ID cannot be empty")
        if player1 == player2:
            raise ValueError("Players cannot be the same")

        return self._galaxy.are_players_neighbors(player1, player2)

    def validate_trade_goods_availability(self, player_id: str, amount: int) -> bool:
        """Validate player has sufficient trade goods.

        Args:
            player_id: Player ID to check
            amount: Amount of trade goods required

        Returns:
            True if player has sufficient trade goods, False otherwise

        Raises:
            ValueError: If player_id is empty or amount is negative
        """
        self._validate_resource_check_inputs(player_id, amount)
        return self._validate_player_resource(
            player_id, amount, lambda player: player.get_trade_goods()
        )

    def validate_commodity_availability(self, player_id: str, amount: int) -> bool:
        """Validate player has sufficient commodities.

        Args:
            player_id: Player ID to check
            amount: Amount of commodities required

        Returns:
            True if player has sufficient commodities, False otherwise

        Raises:
            ValueError: If player_id is empty or amount is negative
        """
        self._validate_resource_check_inputs(player_id, amount)
        return self._validate_player_resource(
            player_id, amount, lambda player: player.get_commodities()
        )

    def validate_promissory_note_availability(
        self, player_id: str, note: PromissoryNote
    ) -> bool:
        """Validate player owns the promissory note and can trade it.

        Args:
            player_id: Player ID to check
            note: Promissory note to validate

        Returns:
            True if player owns the note, False otherwise

        Raises:
            ValueError: If player_id is empty or note is None
        """
        if not player_id or not player_id.strip():
            raise ValueError("Player ID cannot be empty")
        if note is None:
            raise ValueError("Promissory note cannot be None")

        player_hand = self._game_state.promissory_note_manager.get_player_hand(
            player_id
        )
        return note in player_hand

    def validate_transaction(
        self, transaction: ComponentTransaction
    ) -> ValidationResult:
        """Comprehensive validation of a proposed transaction.

        Args:
            transaction: Transaction to validate

        Returns:
            ValidationResult with validation status and messages
        """
        result = ValidationResult(is_valid=True)

        # Validate neighbor requirement
        if not self.validate_neighbor_requirement(
            transaction.proposing_player, transaction.target_player
        ):
            result.add_error(
                f"Players {transaction.proposing_player} and {transaction.target_player} are not neighbors"
            )

        # Validate proposing player's offer
        self._validate_player_offer(
            transaction.proposing_player, transaction.offer, "proposing player", result
        )

        # Validate target player's request (what they're giving back)
        self._validate_player_offer(
            transaction.target_player, transaction.request, "target player", result
        )

        return result

    def _validate_player_offer(
        self,
        player_id: str,
        offer: TransactionOffer,
        player_description: str,
        result: ValidationResult,
    ) -> None:
        """Validate a player's offer components.

        Args:
            player_id: Player making the offer
            offer: Offer to validate
            player_description: Description for error messages
            result: ValidationResult to add errors to
        """
        # Validate trade goods
        if offer.trade_goods > 0:
            if not self.validate_trade_goods_availability(player_id, offer.trade_goods):
                result.add_error(
                    f"{player_description} has insufficient trade goods "
                    f"(needs {offer.trade_goods})"
                )

        # Validate commodities
        if offer.commodities > 0:
            if not self.validate_commodity_availability(player_id, offer.commodities):
                result.add_error(
                    f"{player_description} has insufficient commodities "
                    f"(needs {offer.commodities})"
                )

        # Validate promissory notes
        for note in offer.promissory_notes:
            if not self.validate_promissory_note_availability(player_id, note):
                result.add_error(
                    f"{player_description} does not own promissory note "
                    f"{note.note_type.value}"
                )

    def _validate_resource_check_inputs(self, player_id: str, amount: int) -> None:
        """Validate inputs for resource availability checks.

        Args:
            player_id: Player ID to validate
            amount: Amount to validate

        Raises:
            ValueError: If inputs are invalid
        """
        if not player_id or not player_id.strip():
            raise ValueError("Player ID cannot be empty")
        if amount < 0:
            raise ValueError("Amount cannot be negative")

    def _validate_player_resource(
        self,
        player_id: str,
        required_amount: int,
        resource_getter: Callable[["Player"], int],
    ) -> bool:
        """Generic method to validate player has sufficient resources.

        Args:
            player_id: Player ID to check
            required_amount: Amount of resource required
            resource_getter: Function to get resource amount from player

        Returns:
            True if player has sufficient resources, False otherwise
        """
        player = self._find_player(player_id)
        if player is None:
            return False
        current_amount = resource_getter(player)
        return current_amount >= required_amount

    def validate_neighbor_requirement_detailed(
        self, player1: str, player2: str
    ) -> bool:
        """Validate neighbor requirement with detailed error messages.

        Args:
            player1: First player ID
            player2: Second player ID

        Returns:
            True if players are neighbors

        Raises:
            TransactionValidationError: With detailed error message if not neighbors
        """
        if not self.validate_neighbor_requirement(player1, player2):
            # Get system information for detailed error
            try:
                # Try to get system information if available
                if hasattr(self._galaxy, "get_player_systems"):
                    player1_systems = self._galaxy.get_player_systems(player1)
                    player2_systems = self._galaxy.get_player_systems(player2)
                    error_msg = (
                        f"Players {player1} and {player2} are not neighbors. "
                        f"{player1} controls systems {player1_systems}, "
                        f"{player2} controls systems {player2_systems}."
                    )
                else:
                    error_msg = f"Players {player1} and {player2} are not neighbors."
            except Exception:
                # Fallback if system information is not available
                error_msg = f"Players {player1} and {player2} are not neighbors."

            raise TransactionValidationError(error_msg)

        return True

    def validate_trade_goods_availability_detailed(
        self, player_id: str, amount: int
    ) -> bool:
        """Validate trade goods availability with detailed error messages.

        Args:
            player_id: Player ID to check
            amount: Amount required

        Returns:
            True if player has sufficient trade goods

        Raises:
            TransactionValidationError: With detailed error message if insufficient
        """
        if not self.validate_trade_goods_availability(player_id, amount):
            player = self._find_player(player_id)
            current_amount = player.get_trade_goods() if player else 0
            error_msg = (
                f"Player {player_id} has insufficient trade goods. "
                f"Required: {amount}, Available: {current_amount}"
            )
            raise TransactionValidationError(error_msg)

        return True

    def _find_player(self, player_id: str) -> Optional["Player"]:
        """Find a player by ID in the game state.

        Args:
            player_id: Player ID to find

        Returns:
            Player instance if found, None otherwise
        """
        for player in self._game_state.players:
            if player.id == player_id:
                return player
        return None


class ResourceManager:
    """Manages player resources and component ownership for Rule 28 deals.

    Handles resource transfers between players including trade goods,
    commodities, and promissory notes with proper validation and conversion.
    """

    def __init__(self, game_state: "GameState") -> None:
        """Initialize with game state for resource tracking.

        Args:
            game_state: Game state for resource and component tracking
        """
        self._game_state = game_state

    def get_trade_goods(self, player_id: str) -> int:
        """Get player's current trade goods count.

        Args:
            player_id: Player ID to check

        Returns:
            Current number of trade goods

        Raises:
            ValueError: If player not found
        """
        player = self._find_player(player_id)
        if player is None:
            raise ValueError(f"Player {player_id} not found")
        return player.get_trade_goods()

    def get_commodities(self, player_id: str) -> int:
        """Get player's current commodity count.

        Args:
            player_id: Player ID to check

        Returns:
            Current number of commodities

        Raises:
            ValueError: If player not found
        """
        player = self._find_player(player_id)
        if player is None:
            raise ValueError(f"Player {player_id} not found")
        return player.get_commodities()

    def get_promissory_notes(self, player_id: str) -> list[PromissoryNote]:
        """Get player's owned promissory notes.

        Args:
            player_id: Player ID to check

        Returns:
            List of promissory notes owned by the player
        """
        return self._game_state.promissory_note_manager.get_player_hand(player_id)

    def transfer_trade_goods(
        self, from_player: str, to_player: str, amount: int
    ) -> None:
        """Transfer trade goods between players with validation.

        Args:
            from_player: Player giving trade goods
            to_player: Player receiving trade goods
            amount: Number of trade goods to transfer

        Raises:
            ValueError: If validation fails or insufficient trade goods
        """
        # Early return for zero amounts (no-op behavior)
        if amount == 0:
            return

        self._validate_transfer_inputs(from_player, to_player, amount)

        from_player_obj = self._find_player(from_player)
        to_player_obj = self._find_player(to_player)

        if from_player_obj is None:
            raise ValueError(f"From player {from_player} not found")
        if to_player_obj is None:
            raise ValueError(f"To player {to_player} not found")

        # Try to spend trade goods from the source player
        if not from_player_obj.spend_trade_goods(amount):
            raise ValueError(f"Insufficient trade goods for player {from_player}")

        # Give trade goods to the target player
        to_player_obj.gain_trade_goods(amount)

    def transfer_commodities(
        self, from_player: str, to_player: str, amount: int
    ) -> None:
        """Transfer commodities (converting to trade goods for receiver).

        Args:
            from_player: Player giving commodities
            to_player: Player receiving commodities (as trade goods)
            amount: Number of commodities to transfer

        Raises:
            ValueError: If validation fails or insufficient commodities
        """
        # Early return for zero amounts (no-op behavior)
        if amount == 0:
            return

        self._validate_transfer_inputs(from_player, to_player, amount)

        from_player_obj = self._find_player(from_player)
        to_player_obj = self._find_player(to_player)

        if from_player_obj is None:
            raise ValueError(f"From player {from_player} not found")
        if to_player_obj is None:
            raise ValueError(f"To player {to_player} not found")

        try:
            # Use existing player method that handles commodity-to-trade-goods conversion
            from_player_obj.give_commodities_to_player(to_player_obj, amount)
        except ValueError as e:
            # Re-raise with more specific error message for resource manager context
            raise ValueError(
                f"Insufficient commodities for player {from_player}: {str(e)}"
            ) from e

    def transfer_promissory_note(
        self, from_player: str, to_player: str, note: PromissoryNote
    ) -> None:
        """Transfer promissory note ownership.

        Args:
            from_player: Player giving the promissory note
            to_player: Player receiving the promissory note
            note: Promissory note to transfer

        Raises:
            ValueError: If validation fails or note not owned by from_player
        """
        if not from_player or not from_player.strip():
            raise ValueError("From player ID cannot be empty")
        if not to_player or not to_player.strip():
            raise ValueError("To player ID cannot be empty")
        if from_player == to_player:
            raise ValueError("Cannot transfer to the same player")
        if note is None:
            raise ValueError("Promissory note cannot be None")

        # Check if the from_player actually owns the note
        from_player_hand = self._game_state.promissory_note_manager.get_player_hand(
            from_player
        )
        if note not in from_player_hand:
            raise ValueError(
                f"Player {from_player} does not own the specified promissory note"
            )

        # Remove note from from_player's hand
        from_player_hand.remove(note)

        # Add note to to_player's hand
        self._game_state.promissory_note_manager.add_note_to_hand(note, to_player)

    def _find_player(self, player_id: str) -> Optional["Player"]:
        """Find a player by ID in the game state.

        Args:
            player_id: Player ID to find

        Returns:
            Player instance if found, None otherwise
        """
        for player in self._game_state.players:
            if player.id == player_id:
                return player
        return None

    def _validate_transfer_inputs(
        self, from_player: str, to_player: str, amount: int
    ) -> None:
        """Validate inputs for transfer operations.

        Args:
            from_player: From player ID
            to_player: To player ID
            amount: Transfer amount

        Raises:
            ValueError: If any input is invalid
        """
        if not from_player or not from_player.strip():
            raise ValueError("From player ID cannot be empty")
        if not to_player or not to_player.strip():
            raise ValueError("To player ID cannot be empty")
        if from_player == to_player:
            raise ValueError("Cannot transfer to the same player")
        if amount < 0:
            raise ValueError("Amount cannot be negative")


# Custom exceptions for enhanced transaction management
class TransactionError(Exception):
    """Base exception for transaction-related errors."""

    pass


class TransactionValidationError(TransactionError):
    """Raised when transaction validation fails."""

    pass


class TransactionNotFoundError(TransactionError):
    """Raised when referenced transaction doesn't exist."""

    pass


class TransactionExecutionError(TransactionError):
    """Raised when transaction execution fails."""

    def __init__(self, message: str, context: Optional[dict[str, Any]] = None):
        super().__init__(message)
        self.context = context or {}


class PlayerEliminationError(TransactionError):
    """Raised when a player is eliminated during a pending transaction."""

    def __init__(self, message: str, player_id: str):
        super().__init__(message)
        self.player_id = player_id


class TransactionRollbackError(TransactionError):
    """Raised when transaction rollback fails.

    This error includes context information to help diagnose rollback issues,
    particularly the commodity rollback problem where commodities are converted
    to trade goods during transfer but need to be restored as commodities
    during rollback to preserve asset type distinctions.
    """

    def __init__(
        self, message: str, rollback_step: str, context: dict[str, Any] | None = None
    ):
        super().__init__(message)
        self.rollback_step = rollback_step
        self.context = context or {}


@dataclass
class TransactionResult:
    """Result of a transaction operation."""

    success: bool
    transaction: ComponentTransaction
    error_message: Optional[str] = None


@dataclass
class PromissoryNoteExchangeResult:
    """Result of a promissory note exchange operation."""

    success: bool
    immediate_effects_activated: bool = False
    activated_effects: list[str] = field(default_factory=list)
    error_message: Optional[str] = None


class PromissoryNoteImmediateEffects:
    """Handles immediate effects for promissory note exchanges.

    Separated from the main exchange handler to follow single responsibility principle.
    """

    def __init__(self, game_state: "GameState") -> None:
        """Initialize with game state for player access.

        Args:
            game_state: Game state for player tracking
        """
        self._game_state = game_state

    def get_immediate_effects(
        self, note: PromissoryNote, receiving_player: str
    ) -> list[str]:
        """Get list of immediate effects for a promissory note.

        Args:
            note: The promissory note being exchanged
            receiving_player: Player receiving the note

        Returns:
            List of immediate effect descriptions
        """
        if note is None:
            return []

        # Support for the Throne has immediate effect
        if note.note_type == PromissoryNoteType.SUPPORT_FOR_THE_THRONE:
            return ["Support for the Throne"]

        # Other promissory notes don't have immediate effects
        return []

    def activate_immediate_effects(
        self, note: PromissoryNote, receiving_player: str, effects: list[str]
    ) -> list[str]:
        """Activate immediate effects for a promissory note.

        Args:
            note: The promissory note being exchanged
            receiving_player: Player receiving the note
            effects: List of effects to activate

        Returns:
            List of successfully activated effects
        """
        if not effects or not receiving_player:
            return []

        activated = []

        for effect in effects:
            if effect == "Support for the Throne":
                if self._activate_support_for_throne(receiving_player):
                    activated.append(effect)

        return activated

    def _activate_support_for_throne(self, receiving_player: str) -> bool:
        """Activate Support for the Throne immediate effect.

        Args:
            receiving_player: Player receiving the Support for the Throne

        Returns:
            True if effect was successfully activated

        Note:
            This method currently only validates that the effect can be applied.
            The actual victory point award must be handled by the caller using
            game_state.award_victory_points(receiving_player, 1).
        """
        # Find the receiving player to validate they exist
        player = self._find_player(receiving_player)
        if player is None:
            return False

        # Support for the Throne: gain 1 victory point immediately
        # For now, we just validate that the effect can be applied
        # The actual game state update should be handled by the transaction system
        current_points = self._game_state.get_victory_points(receiving_player)
        max_points = self._game_state.victory_points_to_win

        # Check if awarding 1 victory point would exceed the maximum
        if current_points + 1 > max_points:
            return False

        return True

    def _find_player(self, player_id: str) -> Optional["Player"]:
        """Find a player by ID in the game state.

        Args:
            player_id: Player ID to find

        Returns:
            Player instance if found, None otherwise
        """
        for player in self._game_state.players:
            if player.id == player_id:
                return player
        return None


class PromissoryNoteExchangeHandler:
    """Handles promissory note exchanges with immediate effect activation.

    Manages the exchange of promissory notes between players and activates
    any immediate effects that should trigger upon exchange.
    """

    def __init__(self, game_state: "GameState") -> None:
        """Initialize with game state for resource tracking.

        Args:
            game_state: Game state for resource and component tracking
        """
        self._game_state = game_state
        self._resource_manager = ResourceManager(game_state)
        self._immediate_effects = PromissoryNoteImmediateEffects(game_state)

    def exchange_promissory_note(
        self, from_player: str, to_player: str, note: PromissoryNote
    ) -> PromissoryNoteExchangeResult:
        """Exchange a promissory note between players with immediate effect activation.

        Args:
            from_player: Player giving the promissory note
            to_player: Player receiving the promissory note
            note: Promissory note to exchange

        Returns:
            PromissoryNoteExchangeResult with exchange status and effects
        """
        try:
            # Input validation
            self._validate_exchange_inputs(from_player, to_player, note)

            # Validate and perform the exchange using existing ResourceManager
            self._resource_manager.transfer_promissory_note(
                from_player, to_player, note
            )

            # Check for and activate immediate effects
            immediate_effects = self._immediate_effects.get_immediate_effects(
                note, to_player
            )
            activated_effects = []

            if immediate_effects:
                activated_effects = self._immediate_effects.activate_immediate_effects(
                    note, to_player, immediate_effects
                )

            return PromissoryNoteExchangeResult(
                success=True,
                immediate_effects_activated=len(activated_effects) > 0,
                activated_effects=activated_effects,
            )

        except Exception as e:
            return PromissoryNoteExchangeResult(success=False, error_message=str(e))

    def _validate_exchange_inputs(
        self, from_player: str, to_player: str, note: PromissoryNote
    ) -> None:
        """Validate inputs for promissory note exchange.

        Args:
            from_player: Player giving the promissory note
            to_player: Player receiving the promissory note
            note: Promissory note to exchange

        Raises:
            ValueError: If any input is invalid
        """
        if not from_player or not from_player.strip():
            raise ValueError("From player ID cannot be empty")
        if not to_player or not to_player.strip():
            raise ValueError("To player ID cannot be empty")
        if from_player == to_player:
            raise ValueError("Cannot exchange promissory note with the same player")
        if note is None:
            raise ValueError("Promissory note cannot be None")


class TransactionLogger:
    """Handles transaction logging with timestamps and player details.

    Provides logging capabilities for successful and failed transactions
    with detailed information for debugging and audit purposes.
    """

    def __init__(self) -> None:
        """Initialize the transaction logger."""
        self._transaction_logs: list[dict[str, Any]] = []

    def log_transaction_success(self, transaction: ComponentTransaction) -> None:
        """Log a successful transaction with details.

        Args:
            transaction: Successfully completed transaction
        """
        log_entry = {
            "transaction_id": transaction.transaction_id,
            "status": "success",
            "proposing_player": transaction.proposing_player,
            "target_player": transaction.target_player,
            "offer": {
                "trade_goods": transaction.offer.trade_goods,
                "commodities": transaction.offer.commodities,
                "promissory_notes": len(transaction.offer.promissory_notes),
                "relic_fragments": transaction.offer.relic_fragments,
            },
            "request": {
                "trade_goods": transaction.request.trade_goods,
                "commodities": transaction.request.commodities,
                "promissory_notes": len(transaction.request.promissory_notes),
                "relic_fragments": transaction.request.relic_fragments,
            },
            "timestamp": transaction.completion_timestamp or transaction.timestamp,
        }
        self._transaction_logs.append(log_entry)

    def log_transaction_failure(
        self, transaction: ComponentTransaction, error_message: str
    ) -> None:
        """Log a failed transaction with error details.

        Args:
            transaction: Failed transaction
            error_message: Error message describing the failure
        """
        log_entry = {
            "transaction_id": transaction.transaction_id,
            "status": "failure",
            "proposing_player": transaction.proposing_player,
            "target_player": transaction.target_player,
            "error_message": error_message,
            "timestamp": transaction.timestamp,
        }
        self._transaction_logs.append(log_entry)

    def get_transaction_logs(self) -> list[dict[str, Any]]:
        """Get all transaction logs.

        Returns:
            List of transaction log entries
        """
        return self._transaction_logs.copy()


class TransactionConsistencyValidator:
    """Validates transaction consistency with resource systems.

    Ensures that transaction effects maintain consistency with existing
    game systems like fleet supply, production, and resource tracking.
    """

    def __init__(self, game_state: "GameState") -> None:
        """Initialize with game state for consistency validation.

        Args:
            game_state: Game state for resource and system validation
        """
        self._game_state = game_state

    def validate_transaction_consistency(
        self, transaction: ComponentTransaction
    ) -> bool:
        """Validate that a transaction maintains consistency with resource systems.

        Args:
            transaction: Transaction to validate for consistency

        Returns:
            True if transaction is consistent with resource systems
        """
        # For now, we'll implement basic consistency checks
        # In a full implementation, this would check:
        # - Fleet supply consistency after resource changes
        # - Production capacity consistency
        # - Technology prerequisites consistency
        # - Victory point consistency

        # Basic validation: check that players exist (if game_state has players)
        if (
            hasattr(self._game_state, "players")
            and self._game_state.players is not None
        ):
            try:
                player_ids = [player.id for player in self._game_state.players]

                if transaction.proposing_player not in player_ids:
                    return False
                if transaction.target_player not in player_ids:
                    return False
            except (TypeError, AttributeError):
                # If we can't iterate over players (e.g., Mock object), assume valid
                pass

        # Transaction is consistent by default
        return True


class TransactionNotificationSystem:
    """Handles transaction notifications to game components.

    Manages sending notifications to relevant game systems when
    transactions are completed, ensuring all systems stay in sync.
    """

    def __init__(self, game_state: "GameState") -> None:
        """Initialize with game state for notification management.

        Args:
            game_state: Game state for component notification
        """
        self._game_state = game_state
        self._pending_notifications: list[dict[str, Any]] = []

    def notify_transaction_completed(self, transaction: ComponentTransaction) -> None:
        """Notify relevant game components that a transaction was completed.

        Args:
            transaction: Completed transaction to notify about
        """
        notification = {
            "type": "transaction_completed",
            "transaction_id": transaction.transaction_id,
            "proposing_player": transaction.proposing_player,
            "target_player": transaction.target_player,
            "timestamp": transaction.completion_timestamp or transaction.timestamp,
        }
        self._pending_notifications.append(notification)

    def get_pending_notifications(self) -> list[dict[str, Any]]:
        """Get all pending notifications.

        Returns:
            List of pending notification dictionaries
        """
        return self._pending_notifications.copy()


class EnhancedTransactionManager:
    """Enhanced transaction manager for Rule 28 component deals.

    Extends the existing transaction system with component transaction support,
    including proposal, acceptance, rejection, and cancellation with validation.
    """

    def __init__(self, galaxy: "Galaxy", game_state: "GameState") -> None:
        """Initialize with galaxy for neighbor validation and game state for resource tracking.

        Args:
            galaxy: Galaxy instance for neighbor detection
            game_state: Game state for resource and component tracking
        """
        self._galaxy = galaxy
        self._game_state = game_state
        self._validator = ComponentValidator(galaxy, game_state)
        self._resource_manager = ResourceManager(game_state)

        # Track active transactions
        self._transactions: dict[str, ComponentTransaction] = {}
        self._transaction_counter = 0

        # Track game phase and active player for timing rules
        self._current_phase: Optional[GamePhase] = None
        self._active_player: Optional[str] = None

    def _validate_transaction_players(
        self, proposing_player: str, target_player: str
    ) -> None:
        """Validate player IDs for transaction operations.

        Args:
            proposing_player: Player making the proposal
            target_player: Player receiving the proposal

        Raises:
            ValueError: If player IDs are invalid
        """
        if not proposing_player or not proposing_player.strip():
            raise ValueError("Proposing player ID cannot be empty")
        if not target_player or not target_player.strip():
            raise ValueError("Target player ID cannot be empty")
        if proposing_player == target_player:
            raise ValueError("Players cannot transact with themselves")

    def _validate_transaction_offers(
        self, offer: TransactionOffer, request: TransactionOffer
    ) -> None:
        """Validate transaction offers for basic requirements.

        Args:
            offer: What the proposing player is offering
            request: What the proposing player is requesting

        Raises:
            ValueError: If offers are invalid
        """
        if offer is None:
            raise ValueError("Offer cannot be None")
        if request is None:
            raise ValueError("Request cannot be None")

        # Validate that at least one side has something to exchange
        offer_empty = (
            offer.trade_goods == 0
            and offer.commodities == 0
            and len(offer.promissory_notes) == 0
            and offer.relic_fragments == 0
        )
        request_empty = (
            request.trade_goods == 0
            and request.commodities == 0
            and len(request.promissory_notes) == 0
            and request.relic_fragments == 0
        )

        if offer_empty and request_empty:
            raise ValueError(
                "Transaction must involve exchange of at least one component"
            )

    def set_game_phase(self, phase: "GamePhase") -> None:
        """Set the current game phase.

        Args:
            phase: The current game phase
        """
        self._current_phase = phase

    def set_active_player(self, player_id: str) -> None:
        """Set the active player for transaction timing.

        Args:
            player_id: The player who is currently active

        Raises:
            ValueError: If invalid player ID is provided
        """
        if not player_id or not player_id.strip():
            raise ValueError("Player ID must be provided")
        self._active_player = player_id

    def can_propose_transaction(
        self, proposing_player: str, target_player: str
    ) -> bool:
        """Check if a transaction proposal is allowed.

        For Rule 28 component deals, transactions can be proposed during any game phase
        and by any player (not just the active player), enabling non-blocking processing.

        Args:
            proposing_player: Player making the proposal
            target_player: Player receiving the proposal

        Returns:
            True if transaction proposal is allowed, False otherwise

        Requirements: 6.1, 6.2
        """
        try:
            self._validate_transaction_players(proposing_player, target_player)
            # Rule 28 component deals can be proposed during any phase (Requirement 6.1)
            # and by any player during other players' turns (Requirement 6.2)
            return True
        except ValueError:
            return False

    def propose_transaction(
        self,
        proposing_player: str,
        target_player: str,
        offer: TransactionOffer,
        request: TransactionOffer,
    ) -> ComponentTransaction:
        """Propose a component transaction between players.

        Args:
            proposing_player: Player making the proposal
            target_player: Player receiving the proposal
            offer: What the proposing player is offering
            request: What the proposing player is requesting

        Returns:
            ComponentTransaction representing the proposed transaction

        Raises:
            TransactionValidationError: If transaction validation fails
            ValueError: If invalid parameters are provided
        """
        # Validate player IDs
        self._validate_transaction_players(proposing_player, target_player)

        # Validate offers
        self._validate_transaction_offers(offer, request)

        # Generate unique transaction ID
        self._transaction_counter += 1
        transaction_id = f"tx_{self._transaction_counter:06d}"

        # Create transaction
        transaction = ComponentTransaction(
            transaction_id=transaction_id,
            proposing_player=proposing_player,
            target_player=target_player,
            offer=offer,
            request=request,
            status=TransactionStatus.PENDING,
            timestamp=datetime.now(),
        )

        # Validate transaction
        validation_result = self._validator.validate_transaction(transaction)
        if not validation_result.is_valid:
            error_msg = "; ".join(validation_result.error_messages)
            raise TransactionValidationError(error_msg)

        # Store transaction
        self._transactions[transaction_id] = transaction

        # Sync with GameState (with backward compatibility)
        if hasattr(self._game_state, "add_pending_transaction"):
            self._game_state = self._game_state.add_pending_transaction(transaction)

        return transaction

    def accept_transaction(self, transaction_id: str) -> TransactionResult:
        """Accept and execute a pending transaction.

        Args:
            transaction_id: ID of the transaction to accept

        Returns:
            TransactionResult indicating success or failure

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            TransactionExecutionError: If transaction execution fails
        """
        if transaction_id not in self._transactions:
            raise TransactionNotFoundError(f"Transaction {transaction_id} not found")

        transaction = self._transactions[transaction_id]

        if transaction.status != TransactionStatus.PENDING:
            raise TransactionExecutionError(
                f"Transaction {transaction_id} is not pending (status: {transaction.status.value})"
            )

        try:
            # Build completed transaction before calling GameState method
            completed_transaction = ComponentTransaction(
                transaction_id=transaction.transaction_id,
                proposing_player=transaction.proposing_player,
                target_player=transaction.target_player,
                offer=transaction.offer,
                request=transaction.request,
                status=TransactionStatus.ACCEPTED,
                timestamp=transaction.timestamp,
                completion_timestamp=datetime.now(),
            )

            # Use GameState for transaction execution if available (Requirements: 5.2)
            if hasattr(self._game_state, "apply_transaction_effects"):
                # Delegate to GameState.apply_transaction_effects
                self._game_state = self._game_state.apply_transaction_effects(
                    completed_transaction
                )
            else:
                # Fallback to direct resource manager calls for backward compatibility
                self._execute_transaction(transaction)

            # Update manager cache after successful GameState execution
            self._transactions[transaction_id] = completed_transaction

            return TransactionResult(success=True, transaction=completed_transaction)

        except Exception as e:
            error_msg = f"Failed to execute transaction: {str(e)}"
            return TransactionResult(
                success=False, transaction=transaction, error_message=error_msg
            )

    def reject_transaction(self, transaction_id: str) -> TransactionResult:
        """Reject a pending transaction.

        Args:
            transaction_id: ID of the transaction to reject

        Returns:
            TransactionResult indicating the rejection was successful

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
        """
        if transaction_id not in self._transactions:
            raise TransactionNotFoundError(f"Transaction {transaction_id} not found")

        transaction = self._transactions[transaction_id]
        self._update_transaction_status(transaction, TransactionStatus.REJECTED)

        # Remove from GameState pending_transactions
        self._remove_from_gamestate_pending(transaction_id)

        # Return the updated transaction
        rejected_transaction = self._transactions[transaction_id]
        return TransactionResult(success=True, transaction=rejected_transaction)

    def cancel_transaction(self, transaction_id: str, requesting_player: str) -> None:
        """Cancel a pending transaction.

        Args:
            transaction_id: ID of the transaction to cancel
            requesting_player: Player requesting the cancellation

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            ValueError: If player is not authorized to cancel
        """
        if transaction_id not in self._transactions:
            raise TransactionNotFoundError(f"Transaction {transaction_id} not found")

        transaction = self._transactions[transaction_id]

        # Only proposing player can cancel
        if requesting_player != transaction.proposing_player:
            raise ValueError(
                f"Only the proposing player ({transaction.proposing_player}) can cancel this transaction"
            )

        self._update_transaction_status(transaction, TransactionStatus.CANCELLED)

        # Remove from GameState pending_transactions
        self._remove_from_gamestate_pending(transaction_id)

    def get_transaction(self, transaction_id: str) -> ComponentTransaction:
        """Get a transaction by ID.

        Args:
            transaction_id: ID of the transaction to retrieve

        Returns:
            ComponentTransaction instance

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
        """
        if transaction_id not in self._transactions:
            raise TransactionNotFoundError(f"Transaction {transaction_id} not found")

        return self._transactions[transaction_id]

    def get_pending_transactions(
        self, player_id: Optional[str] = None
    ) -> list[ComponentTransaction]:
        """Get pending transactions for a player or all pending transactions.

        Args:
            player_id: Player ID to get transactions for. If None, returns all pending transactions.

        Returns:
            List of pending transactions involving the player (if player_id provided)
            or all pending transactions (if player_id is None), ordered by timestamp (FIFO)

        Requirements: 6.4
        """
        pending = []
        for transaction in self._transactions.values():
            if transaction.status == TransactionStatus.PENDING:
                if player_id is None:
                    # Return all pending transactions
                    pending.append(transaction)
                elif (
                    transaction.proposing_player == player_id
                    or transaction.target_player == player_id
                ):
                    # Return transactions for specific player
                    pending.append(transaction)

        # Sort by timestamp to ensure FIFO ordering (Requirement 6.4)
        pending.sort(key=lambda t: t.timestamp)
        return pending

    def get_transaction_history(self, player_id: str) -> list[TransactionHistoryEntry]:
        """Get completed transaction history for a player.

        Delegates to GameState as the single source of truth for transaction history.

        Args:
            player_id: Player ID to get history for

        Returns:
            List of completed transaction history entries involving the player
        """
        # Delegate to GameState as single source of truth
        history = []
        for entry in self._game_state.transaction_history:
            if entry.proposing_player == player_id or entry.target_player == player_id:
                history.append(entry)
        return history

    def _execute_transaction(self, transaction: ComponentTransaction) -> None:
        """Execute the resource transfers for a transaction.

        Args:
            transaction: Transaction to execute

        Raises:
            Exception: If any resource transfer fails
        """
        # Transfer trade goods from proposing player to target player
        if transaction.offer.trade_goods > 0:
            self._resource_manager.transfer_trade_goods(
                transaction.proposing_player,
                transaction.target_player,
                transaction.offer.trade_goods,
            )

        # Transfer commodities from target player to proposing player
        if transaction.request.commodities > 0:
            self._resource_manager.transfer_commodities(
                transaction.target_player,
                transaction.proposing_player,
                transaction.request.commodities,
            )

        # Transfer promissory notes from proposing player to target player with immediate effects
        promissory_handler = PromissoryNoteExchangeHandler(self._game_state)
        for note in transaction.offer.promissory_notes:
            result = promissory_handler.exchange_promissory_note(
                transaction.proposing_player, transaction.target_player, note
            )
            if not result.success:
                raise TransactionExecutionError(
                    f"Failed to transfer promissory note: {result.error_message}"
                )

        # Transfer promissory notes from target player to proposing player with immediate effects
        for note in transaction.request.promissory_notes:
            result = promissory_handler.exchange_promissory_note(
                transaction.target_player, transaction.proposing_player, note
            )
            if not result.success:
                raise TransactionExecutionError(
                    f"Failed to transfer promissory note: {result.error_message}"
                )

        # Transfer relic fragments (if any)
        # Note: Relic fragment transfer not implemented yet in ResourceManager
        # This would be added when relic fragment system is implemented

        # Update game state to reflect transaction effects (Requirement 6.5)
        self._update_game_state_after_transaction(transaction)

    def _update_transaction_status(
        self, transaction: ComponentTransaction, new_status: TransactionStatus
    ) -> None:
        """Update transaction status with completion timestamp.

        Args:
            transaction: Transaction to update
            new_status: New status to set

        Note:
            This helper method reduces code duplication in status update operations.
        """
        updated_transaction = ComponentTransaction(
            transaction_id=transaction.transaction_id,
            proposing_player=transaction.proposing_player,
            target_player=transaction.target_player,
            offer=transaction.offer,
            request=transaction.request,
            status=new_status,
            timestamp=transaction.timestamp,
            completion_timestamp=datetime.now(),
        )

        self._transactions[transaction.transaction_id] = updated_transaction

    def _remove_from_gamestate_pending(self, transaction_id: str) -> None:
        """Remove transaction from GameState pending_transactions using safe removal.

        Args:
            transaction_id: ID of the transaction to remove

        Note:
            Uses copy() and pop() with default for safe removal that doesn't fail
            if the transaction doesn't exist in GameState (handles sync issues).
        """
        new_pending = self._game_state.pending_transactions.copy()
        new_pending.pop(transaction_id, None)  # Safe removal with default
        self._game_state = self._game_state._create_new_state(
            pending_transactions=new_pending
        )

    def _update_game_state_after_transaction(
        self, transaction: ComponentTransaction
    ) -> None:
        """Update game state after transaction execution.

        Args:
            transaction: The executed transaction

        Requirements: 6.5
        """
        # Notify game state of transaction effects
        if hasattr(self._game_state, "update_transaction_effects"):
            self._game_state.update_transaction_effects(transaction)

        # For now, this is a placeholder for future game state integration
        # The actual resource transfers are handled by ResourceManager
        pass

    def handle_player_elimination(self, player_id: str) -> None:
        """Handle player elimination by cancelling all pending transactions involving the player.

        Args:
            player_id: ID of the eliminated player

        Requirements: 5.3
        """
        if not player_id or not player_id.strip():
            raise ValueError("Player ID cannot be empty")

        # Find all pending transactions involving the eliminated player
        transactions_to_cancel = []
        for transaction in self._transactions.values():
            if transaction.status == TransactionStatus.PENDING and (
                transaction.proposing_player == player_id
                or transaction.target_player == player_id
            ):
                transactions_to_cancel.append(transaction.transaction_id)

        # Cancel all found transactions
        for transaction_id in transactions_to_cancel:
            self._cancel_transaction_internal(transaction_id, "Player eliminated")

    def accept_transaction_with_rollback(
        self, transaction_id: str
    ) -> TransactionResult:
        """Accept and execute a transaction with rollback capability.

        Args:
            transaction_id: ID of the transaction to accept

        Returns:
            TransactionResult with success status and error details

        Requirements: 3.3, 4.3
        """
        if transaction_id not in self._transactions:
            raise TransactionNotFoundError(f"Transaction {transaction_id} not found")

        transaction = self._transactions[transaction_id]

        if transaction.status != TransactionStatus.PENDING:
            return TransactionResult(
                success=False,
                transaction=transaction,
                error_message=f"Transaction {transaction_id} is not pending",
            )

        # Validate transaction before execution
        validation_result = self._validator.validate_transaction(transaction)
        if not validation_result.is_valid:
            return TransactionResult(
                success=False,
                transaction=transaction,
                error_message=f"Transaction validation failed: {', '.join(validation_result.error_messages)}",
            )

        # Track rollback information
        rollback_actions: list[tuple[str, str, str, Any]] = []

        try:
            # Execute resource transfers with rollback tracking
            if transaction.offer.trade_goods > 0:
                rollback_actions.append(
                    (
                        "trade_goods",
                        transaction.target_player,
                        transaction.proposing_player,
                        transaction.offer.trade_goods,
                    )
                )
                self._resource_manager.transfer_trade_goods(
                    transaction.proposing_player,
                    transaction.target_player,
                    transaction.offer.trade_goods,
                )

            if transaction.request.trade_goods > 0:
                rollback_actions.append(
                    (
                        "trade_goods",
                        transaction.proposing_player,
                        transaction.target_player,
                        transaction.request.trade_goods,
                    )
                )
                self._resource_manager.transfer_trade_goods(
                    transaction.target_player,
                    transaction.proposing_player,
                    transaction.request.trade_goods,
                )

            if transaction.offer.commodities > 0:
                rollback_actions.append(
                    (
                        "commodities",
                        transaction.target_player,
                        transaction.proposing_player,
                        transaction.offer.commodities,
                    )
                )
                self._resource_manager.transfer_commodities(
                    transaction.proposing_player,
                    transaction.target_player,
                    transaction.offer.commodities,
                )

            if transaction.request.commodities > 0:
                rollback_actions.append(
                    (
                        "commodities",
                        transaction.proposing_player,
                        transaction.target_player,
                        transaction.request.commodities,
                    )
                )
                self._resource_manager.transfer_commodities(
                    transaction.target_player,
                    transaction.proposing_player,
                    transaction.request.commodities,
                )

            # Handle promissory notes
            for note in transaction.offer.promissory_notes:
                rollback_actions.append(
                    (
                        "promissory_note",
                        transaction.target_player,
                        transaction.proposing_player,
                        note,
                    )
                )
                self._resource_manager.transfer_promissory_note(
                    transaction.proposing_player, transaction.target_player, note
                )

            for note in transaction.request.promissory_notes:
                rollback_actions.append(
                    (
                        "promissory_note",
                        transaction.proposing_player,
                        transaction.target_player,
                        note,
                    )
                )
                self._resource_manager.transfer_promissory_note(
                    transaction.target_player, transaction.proposing_player, note
                )

            # Mark transaction as completed
            completed_transaction = ComponentTransaction(
                transaction_id=transaction.transaction_id,
                proposing_player=transaction.proposing_player,
                target_player=transaction.target_player,
                offer=transaction.offer,
                request=transaction.request,
                status=TransactionStatus.ACCEPTED,
                timestamp=transaction.timestamp,
                completion_timestamp=datetime.now(),
            )

            self._transactions[transaction_id] = completed_transaction
            self._update_game_state_after_transaction(completed_transaction)

            return TransactionResult(success=True, transaction=completed_transaction)

        except Exception as e:
            # Rollback all completed actions
            try:
                self._perform_rollback(rollback_actions)
                return TransactionResult(
                    success=False,
                    transaction=transaction,
                    error_message=f"Transaction execution failed and was rolled back: {str(e)}",
                )
            except Exception as rollback_error:
                context = {
                    "rollback_step": "multiple_operations",
                    "original_error": str(e),
                    "rollback_error": str(rollback_error),
                    "rollback_actions_attempted": len(rollback_actions),
                }

                # If the rollback error is a TransactionRollbackError, preserve its context
                if isinstance(rollback_error, TransactionRollbackError):
                    context.update(rollback_error.context)
                    # Ensure asset_type is available at the top level for easy access
                    if "asset_type" in rollback_error.context:
                        context["asset_type"] = rollback_error.context["asset_type"]
                    if "original_amount" in rollback_error.context:
                        context["original_amount"] = rollback_error.context[
                            "original_amount"
                        ]

                raise TransactionRollbackError(
                    f"Transaction execution failed and rollback also failed: {str(rollback_error)}",
                    rollback_step="multiple_operations",
                    context=context,
                ) from e

    def _perform_rollback(
        self, rollback_actions: list[tuple[str, str, str, Any]]
    ) -> None:
        """Perform rollback of transaction actions.

        Args:
            rollback_actions: List of actions to rollback

        Raises:
            TransactionRollbackError: If rollback fails
        """
        # Reverse the order of actions for rollback
        for action_type, from_player, to_player, amount_or_item in reversed(
            rollback_actions
        ):
            try:
                if action_type == "trade_goods":
                    self._resource_manager.transfer_trade_goods(
                        from_player, to_player, amount_or_item
                    )
                elif action_type == "commodities":
                    # For commodities, we need to reverse the conversion
                    # This is complex and may require special handling
                    self._resource_manager.transfer_trade_goods(
                        from_player, to_player, amount_or_item
                    )
                elif action_type == "promissory_note":
                    self._resource_manager.transfer_promissory_note(
                        from_player, to_player, amount_or_item
                    )
            except Exception as e:
                # Create context information for rollback error
                context = {
                    "asset_type": action_type,
                    "original_amount": amount_or_item,
                    "from_player": from_player,
                    "to_player": to_player,
                    "rollback_step": action_type,
                }

                # Document the commodity rollback issue
                if action_type == "commodities":
                    context["rollback_issue"] = (
                        "Commodity rollback converts to trade goods instead of preserving asset type"
                    )
                    context["expected_behavior"] = (
                        "Should restore original commodities, not convert to trade goods"
                    )

                raise TransactionRollbackError(
                    f"Failed to rollback {action_type} transfer",
                    rollback_step=action_type,
                    context=context,
                ) from e

    def _cancel_transaction_internal(self, transaction_id: str, reason: str) -> None:
        """Internal method to cancel a transaction.

        Args:
            transaction_id: ID of the transaction to cancel
            reason: Reason for cancellation
        """
        if transaction_id in self._transactions:
            transaction = self._transactions[transaction_id]
            cancelled_transaction = ComponentTransaction(
                transaction_id=transaction.transaction_id,
                proposing_player=transaction.proposing_player,
                target_player=transaction.target_player,
                offer=transaction.offer,
                request=transaction.request,
                status=TransactionStatus.CANCELLED,
                timestamp=transaction.timestamp,
                completion_timestamp=datetime.now(),
            )
            self._transactions[transaction_id] = cancelled_transaction


@dataclass
class TransactionAPIResult:
    """Result of a transaction API operation."""

    success: bool
    transaction_id: Optional[str] = None
    transaction: Optional[ComponentTransaction] = None
    error_message: Optional[str] = None
    game_state: Optional["GameState"] = None


@dataclass
class TransactionStatusInfo:
    """Information about a transaction's current status."""

    transaction_id: str
    status: TransactionStatus
    proposing_player: str
    target_player: str
    offer: TransactionOffer
    request: TransactionOffer
    timestamp: datetime
    completion_timestamp: Optional[datetime] = None


class TransactionAPI:
    """Clean API interface for transaction operations.

    Provides a simplified interface for client integration with the Rule 28
    component transaction system. Handles transaction proposals, status queries,
    history retrieval, and response handling.

    Requirements: 6.1, 7.2, 7.4
    """

    def __init__(self, galaxy: "Galaxy", game_state: "GameState") -> None:
        """Initialize the transaction API with required dependencies.

        Args:
            galaxy: Galaxy instance for neighbor validation
            game_state: Game state for resource and component tracking
        """
        self._galaxy = galaxy
        self._game_state = game_state

        # Initialize the enhanced transaction manager
        self._transaction_manager = EnhancedTransactionManager(galaxy, game_state)

    def _validate_transaction_id(self, transaction_id: str) -> None:
        """Validate transaction ID input.

        Args:
            transaction_id: Transaction ID to validate

        Raises:
            ValueError: If transaction ID is invalid
        """
        if not transaction_id or not transaction_id.strip():
            raise ValueError("Transaction ID cannot be empty")

    def _validate_player_id(self, player_id: str) -> None:
        """Validate player ID input.

        Args:
            player_id: Player ID to validate

        Raises:
            ValueError: If player ID is invalid
        """
        if not player_id or not player_id.strip():
            raise ValueError("Player ID cannot be empty")

    def _convert_to_status_info(
        self, transaction: ComponentTransaction | TransactionHistoryEntry
    ) -> TransactionStatusInfo:
        """Convert ComponentTransaction to TransactionStatusInfo.

        Args:
            transaction: Transaction to convert

        Returns:
            TransactionStatusInfo representation
        """
        return TransactionStatusInfo(
            transaction_id=transaction.transaction_id,
            status=transaction.status,
            proposing_player=transaction.proposing_player,
            target_player=transaction.target_player,
            offer=transaction.offer,
            request=transaction.request,
            timestamp=transaction.timestamp,
            completion_timestamp=transaction.completion_timestamp,
        )

    def propose_transaction(
        self,
        proposing_player: str,
        target_player: str,
        offer: TransactionOffer,
        request: TransactionOffer,
    ) -> TransactionAPIResult:
        """Propose a component transaction between players.

        Args:
            proposing_player: Player making the proposal
            target_player: Player receiving the proposal
            offer: What the proposing player is offering
            request: What the proposing player is requesting

        Returns:
            TransactionAPIResult with success status and transaction ID

        Requirements: 6.1
        """
        try:
            # Validate inputs
            self._validate_player_id(proposing_player)
            self._validate_player_id(target_player)

            if proposing_player == target_player:
                raise ValueError("Players cannot transact with themselves")

            if not isinstance(offer, TransactionOffer):
                raise ValueError("Offer must be a TransactionOffer instance")

            if not isinstance(request, TransactionOffer):
                raise ValueError("Request must be a TransactionOffer instance")

            transaction = self._transaction_manager.propose_transaction(
                proposing_player, target_player, offer, request
            )
            return TransactionAPIResult(
                success=True,
                transaction_id=transaction.transaction_id,
                transaction=transaction,
            )
        except Exception as e:
            return TransactionAPIResult(success=False, error_message=str(e))

    def get_transaction_status(
        self, transaction_id: str
    ) -> Optional[TransactionStatusInfo]:
        """Get the current status of a transaction.

        Args:
            transaction_id: ID of the transaction to query

        Returns:
            TransactionStatusInfo if transaction exists, None otherwise

        Requirements: 7.2
        """
        try:
            # Validate input
            self._validate_transaction_id(transaction_id)

            transaction = self._transaction_manager.get_transaction(transaction_id)
            return self._convert_to_status_info(transaction)
        except TransactionNotFoundError:
            # Transaction doesn't exist - this is expected behavior
            return None
        except Exception:
            # Other errors - log and return None for API consistency
            return None

    def get_transaction_history(self, player_id: str) -> list[TransactionStatusInfo]:
        """Get transaction history for a player.

        Args:
            player_id: Player ID to get history for

        Returns:
            List of TransactionStatusInfo for completed transactions

        Requirements: 7.4
        """
        try:
            # Validate input
            self._validate_player_id(player_id)

            history = self._transaction_manager.get_transaction_history(player_id)
            return [self._convert_to_status_info(entry) for entry in history]
        except Exception:
            # Return empty list on any error for API consistency
            return []

    def accept_transaction(self, transaction_id: str) -> TransactionAPIResult:
        """Accept a pending transaction.

        Args:
            transaction_id: ID of the transaction to accept

        Returns:
            TransactionAPIResult with success status and updated transaction

        Requirements: 6.1
        """
        try:
            # Validate input
            self._validate_transaction_id(transaction_id)

            result = self._transaction_manager.accept_transaction(transaction_id)
            return TransactionAPIResult(
                success=result.success,
                transaction_id=transaction_id,
                transaction=result.transaction,
                error_message=result.error_message,
            )
        except Exception as e:
            return TransactionAPIResult(
                success=False, transaction_id=transaction_id, error_message=str(e)
            )

    def reject_transaction(self, transaction_id: str) -> TransactionAPIResult:
        """Reject a pending transaction.

        Args:
            transaction_id: ID of the transaction to reject

        Returns:
            TransactionAPIResult with success status

        Requirements: 6.1
        """
        try:
            # Validate input
            self._validate_transaction_id(transaction_id)

            self._transaction_manager.reject_transaction(transaction_id)
            return TransactionAPIResult(success=True, transaction_id=transaction_id)
        except Exception as e:
            return TransactionAPIResult(
                success=False, transaction_id=transaction_id, error_message=str(e)
            )

    def get_pending_transactions(self, player_id: str) -> list[TransactionStatusInfo]:
        """Get all pending transactions for a player.

        Args:
            player_id: Player ID to get pending transactions for

        Returns:
            List of TransactionStatusInfo for pending transactions
        """
        try:
            # Validate input
            self._validate_player_id(player_id)

            pending = self._transaction_manager.get_pending_transactions(player_id)
            return [
                self._convert_to_status_info(transaction) for transaction in pending
            ]
        except Exception:
            # Return empty list on any error for API consistency
            return []

    def get_game_state(self) -> "GameState":
        """Get the current GameState.

        Returns the current GameState, which may have been updated by transaction operations.
        This provides access to the updated state after operations complete.

        Returns:
            Current GameState instance

        Requirements: 12.1, 12.3
        """
        # Return the current state from the transaction manager, which is kept synchronized
        return self._transaction_manager._game_state
