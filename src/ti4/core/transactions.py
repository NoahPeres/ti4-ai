"""Transaction system for TI4 player trading.

This module implements Rule 94: TRANSACTIONS mechanics according to the TI4 LRR.
Handles player-to-player exchanges of commodities, trade goods, promissory notes, and relic fragments.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Optional

from .game_phase import GamePhase

if TYPE_CHECKING:
    from .galaxy import Galaxy


class PromissoryNoteType(Enum):
    """Types of promissory notes that can be exchanged in transactions."""

    # Faction-specific promissory notes
    TRADE_AGREEMENT = "trade_agreement"
    CEASEFIRE = "ceasefire"
    POLITICAL_SECRET = "political_secret"
    ALLIANCE = "alliance"

    # Generic promissory notes
    SUPPORT_FOR_THE_THRONE = "support_for_the_throne"


@dataclass(frozen=True)
class PromissoryNote:
    """Represents a promissory note that can be exchanged in transactions.

    According to LRR Rule 94.3, promissory notes are exchangeable items
    that represent agreements between players.
    """

    note_type: PromissoryNoteType
    issuing_player: str
    receiving_player: str | None = None

    def __post_init__(self) -> None:
        """Validate promissory note after initialization."""
        if not self.issuing_player:
            raise ValueError("Promissory note must have an issuing player")


@dataclass
class TransactionOffer:
    """Represents what a player offers in a transaction.

    Contains the components a player is willing to give in exchange.
    """

    trade_goods: int = 0
    commodities: int = 0
    promissory_notes: list[PromissoryNote] = field(default_factory=list)
    relic_fragments: int = 0

    def __post_init__(self) -> None:
        """Validate the transaction offer after initialization."""
        # Rule 94.2: Only up to one promissory note per transaction
        if len(self.promissory_notes) > 1:
            raise ValueError(
                "Cannot exchange more than one promissory note per transaction"
            )

        # Rule 94.3: Validate that only exchangeable items are included
        # (This validation happens in the constructor by only allowing valid fields)


@dataclass
class TransactionResult:
    """Result of a completed transaction."""

    success: bool
    player1_gave: TransactionOffer
    player2_gave: TransactionOffer
    error_message: str | None = None


class TransactionManager:
    """Manages player transactions according to Rule 94.

    Handles:
    - Transaction timing and neighbor requirements (Rule 94.1)
    - Component exchange validation (Rule 94.2, 94.3)
    - Uneven exchanges and gifts (Rule 94.4)
    - Deal integration (Rule 94.5)
    - Agenda phase special rules (Rule 94.6)
    """

    def __init__(self, galaxy: Optional["Galaxy"] = None) -> None:
        """Initialize the transaction manager.

        Args:
            galaxy: Galaxy instance for neighbor detection. If None, neighbor
                   validation will be skipped (useful for testing).
        """
        # Use existing galaxy system for neighbor detection
        self._galaxy = galaxy

        # Track active player for transaction timing
        self._active_player: str | None = None

        # Track completed transactions per turn (Rule 94.1 - one per neighbor)
        self._completed_transactions: dict[str, set[str]] = {}

        # Track current game phase for special transaction rules
        self._current_phase: GamePhase = GamePhase.SETUP

    def set_galaxy(self, galaxy: "Galaxy") -> None:
        """Set the galaxy instance for neighbor detection.

        Args:
            galaxy: Galaxy instance to use for neighbor detection
        """
        self._galaxy = galaxy

    def set_active_player(self, player_id: str) -> None:
        """Set the active player for transaction timing.

        Args:
            player_id: The player who is currently active

        Raises:
            ValueError: If invalid player ID is provided
        """
        if not player_id:
            raise ValueError("Player ID must be provided")

        self._active_player = player_id
        # Reset transaction tracking for new active player
        if player_id not in self._completed_transactions:
            self._completed_transactions[player_id] = set()

    def set_game_phase(self, phase: GamePhase) -> None:
        """Set the current game phase.

        Args:
            phase: The current game phase
        """
        self._current_phase = phase

    def can_transact(self, player1: str, player2: str) -> bool:
        """Check if two players can perform a transaction.

        Args:
            player1: The first player (usually active player)
            player2: The second player

        Returns:
            True if transaction is allowed, False otherwise
        """
        # Rule 94.1: Only active player can initiate transactions
        if player1 != self._active_player:
            return False

        # Rule 94.6: During agenda phase, can transact with any player
        if self._current_phase == GamePhase.AGENDA:
            return self._can_transact_agenda_phase(player1, player2)

        # Rule 94.1: Must be neighbors during normal play
        if not self._are_neighbors(player1, player2):
            return False

        # Rule 94.1: Only one transaction per neighbor per turn
        if player2 in self._completed_transactions.get(player1, set()):
            return False

        return True

    def execute_transaction(
        self,
        player1: str,
        player2: str,
        player1_offer: TransactionOffer,
        player2_offer: TransactionOffer,
    ) -> TransactionResult:
        """Execute a transaction between two players.

        Args:
            player1: The first player (giver)
            player2: The second player (receiver)
            player1_offer: What player1 is offering
            player2_offer: What player2 is offering

        Returns:
            TransactionResult indicating success or failure

        Raises:
            ValueError: If invalid parameters are provided
        """
        # Input validation
        if not player1 or not player2:
            raise ValueError("Both player IDs must be provided")

        if player1 == player2:
            return TransactionResult(
                success=False,
                player1_gave=TransactionOffer(),
                player2_gave=TransactionOffer(),
                error_message="Players cannot transact with themselves",
            )

        # Validate transaction is allowed
        if not self.can_transact(player1, player2):
            reason = self._get_transaction_denial_reason(player1, player2)
            return TransactionResult(
                success=False,
                player1_gave=TransactionOffer(),
                player2_gave=TransactionOffer(),
                error_message=f"Transaction not allowed: {reason}",
            )

        # Validate offers
        if not self.validate_offer(player1_offer):
            return TransactionResult(
                success=False,
                player1_gave=TransactionOffer(),
                player2_gave=TransactionOffer(),
                error_message="Invalid offer from player1",
            )

        if not self.validate_offer(player2_offer):
            return TransactionResult(
                success=False,
                player1_gave=TransactionOffer(),
                player2_gave=TransactionOffer(),
                error_message="Invalid offer from player2",
            )

        # Record transaction as completed
        if player1 not in self._completed_transactions:
            self._completed_transactions[player1] = set()
        self._completed_transactions[player1].add(player2)

        # Return successful transaction result
        return TransactionResult(
            success=True, player1_gave=player1_offer, player2_gave=player2_offer
        )

    def validate_offer(
        self, offer: TransactionOffer, player_supply: dict[str, int] | None = None
    ) -> bool:
        """Validate that a transaction offer contains only valid exchangeable items.

        Args:
            offer: The transaction offer to validate
            player_supply: Optional dict with player's available resources
                          Format: {"trade_goods": int, "commodities": int, ...}

        Returns:
            True if offer is valid, False otherwise
        """
        # Rule 94.3: Can only exchange specific item types
        # The TransactionOffer dataclass already enforces this by only having valid fields

        # Rule 94.2: Only up to one promissory note
        if len(offer.promissory_notes) > 1:
            return False

        # All values should be non-negative
        if offer.trade_goods < 0 or offer.commodities < 0 or offer.relic_fragments < 0:
            return False

        # TODO: Implement full supply validation when PlayerSupply system is ready
        # For now, just do basic validation against provided supply dict
        if player_supply is not None:
            if offer.trade_goods > player_supply.get("trade_goods", 0):
                return False
            if offer.commodities > player_supply.get("commodities", 0):
                return False
            if offer.relic_fragments > player_supply.get("relic_fragments", 0):
                return False
            # TODO: Validate promissory note ownership

        return True

    def _are_neighbors(self, player1: str, player2: str) -> bool:
        """Check if two players are neighbors using the galaxy system."""
        if self._galaxy is None:
            # If no galaxy provided, assume neighbors for testing
            return True
        return self._galaxy.are_players_neighbors(player1, player2)

    def _can_transact_agenda_phase(self, player1: str, player2: str) -> bool:
        """Check if players can transact during agenda phase."""
        # Rule 94.6: During agenda phase, can transact with any player
        # Still limited to one transaction per player per agenda
        return player2 not in self._completed_transactions.get(player1, set())

    def _get_transaction_denial_reason(self, player1: str, player2: str) -> str:
        """Get a descriptive reason why a transaction is not allowed.

        Args:
            player1: The first player
            player2: The second player

        Returns:
            Human-readable reason for transaction denial
        """
        if player1 != self._active_player:
            return f"{player1} is not the active player"

        if self._current_phase != GamePhase.AGENDA and not self._are_neighbors(
            player1, player2
        ):
            return f"{player1} and {player2} are not neighbors"

        if player2 in self._completed_transactions.get(player1, set()):
            return f"{player1} has already transacted with {player2} this turn"

        return "Unknown reason"
