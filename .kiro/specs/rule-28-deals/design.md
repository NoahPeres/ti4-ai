# Design Document

## Overview

This document outlines the design for implementing Rule 28: DEALS component transaction system in the TI4 AI system. The design focuses on immediate component exchanges between neighboring players, building upon existing systems for transactions, promissory notes, and galaxy adjacency.

The system will provide a clean API for component-based transactions while integrating seamlessly with existing game state management, resource tracking, and adjacency validation.

## Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Game Client   │    │  Transaction    │    │   Game State    │
│                 │───▶│    Manager      │───▶│   Management    │
│ - Propose Trade │    │                 │    │                 │
│ - Accept Trade  │    │ - Validate      │    │ - Update        │
│ - View History  │    │ - Execute       │    │ - Persist       │
└─────────────────┘    │ - Log           │    │ - Notify        │
                       └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Validation    │
                       │    Services     │
                       │                 │
                       │ - Neighbor      │
                       │ - Resources     │
                       │ - Components    │
                       └─────────────────┘
```

### Core Components

1. **ComponentTransaction**: Represents a proposed or completed component exchange
2. **TransactionManager**: Enhanced to handle Rule 28 deals (builds on existing implementation)
3. **ComponentValidator**: Validates component availability and neighbor requirements
4. **TransactionHistory**: Tracks completed transactions for audit and reference
5. **ResourceManager**: Manages trade goods, commodities, and promissory note ownership

## Components and Interfaces

### ComponentTransaction Entity

```python
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

    def is_completed(self) -> bool:
        """Check if transaction has been executed."""

    def get_net_exchange(self, player_id: str) -> TransactionOffer:
        """Get what a player gains/loses in this transaction."""
```

### Enhanced TransactionManager

Building on the existing `TransactionManager` class:

```python
class TransactionManager:
    """Enhanced transaction manager for Rule 28 component deals."""

    def __init__(self, galaxy: Galaxy, game_state: GameState):
        """Initialize with galaxy for neighbor validation and game state for resource tracking."""

    def propose_transaction(
        self,
        proposing_player: str,
        target_player: str,
        offer: TransactionOffer,
        request: TransactionOffer
    ) -> ComponentTransaction:
        """Propose a component transaction between players."""

    def accept_transaction(self, transaction_id: str) -> TransactionResult:
        """Accept and execute a pending transaction."""

    def reject_transaction(self, transaction_id: str) -> None:
        """Reject a pending transaction."""

    def get_pending_transactions(self, player_id: str) -> list[ComponentTransaction]:
        """Get all pending transactions for a player."""

    def get_transaction_history(self, player_id: str) -> list[ComponentTransaction]:
        """Get completed transaction history for a player."""
```

### ComponentValidator Service

```python
class ComponentValidator:
    """Validates component transactions according to game rules."""

    def __init__(self, galaxy: Galaxy, game_state: GameState):
        """Initialize with game systems for validation."""

    def validate_neighbor_requirement(self, player1: str, player2: str) -> bool:
        """Validate that players are neighbors for component exchange."""

    def validate_trade_goods_availability(self, player_id: str, amount: int) -> bool:
        """Validate player has sufficient trade goods."""

    def validate_commodity_availability(self, player_id: str, amount: int) -> bool:
        """Validate player has sufficient commodities."""

    def validate_promissory_note_availability(
        self,
        player_id: str,
        note: PromissoryNote
    ) -> bool:
        """Validate player owns the promissory note and can trade it."""

    def validate_transaction(self, transaction: ComponentTransaction) -> ValidationResult:
        """Comprehensive validation of a proposed transaction."""
```

### ResourceManager Integration

```python
class ResourceManager:
    """Manages player resources and component ownership."""

    def __init__(self, game_state: GameState):
        """Initialize with game state for resource tracking."""

    def get_trade_goods(self, player_id: str) -> int:
        """Get player's current trade goods count."""

    def get_commodities(self, player_id: str) -> int:
        """Get player's current commodity count."""

    def get_promissory_notes(self, player_id: str) -> list[PromissoryNote]:
        """Get player's owned promissory notes."""

    def transfer_trade_goods(self, from_player: str, to_player: str, amount: int) -> None:
        """Transfer trade goods between players."""

    def transfer_commodities(self, from_player: str, to_player: str, amount: int) -> None:
        """Transfer commodities (converting to trade goods for receiver)."""

    def transfer_promissory_note(
        self,
        from_player: str,
        to_player: str,
        note: PromissoryNote
    ) -> None:
        """Transfer promissory note ownership."""
```

## Data Models

### Enhanced TransactionOffer

Building on the existing `TransactionOffer` class:

```python
@dataclass
class TransactionOffer:
    """Enhanced transaction offer with validation."""

    trade_goods: int = 0
    commodities: int = 0
    promissory_notes: list[PromissoryNote] = field(default_factory=list)
    relic_fragments: int = 0

    def is_empty(self) -> bool:
        """Check if offer contains no components."""

    def get_total_value(self) -> int:
        """Get approximate total value of offer."""

    def validate_amounts(self) -> None:
        """Validate all amounts are non-negative."""
```

### TransactionStatus Enum

```python
class TransactionStatus(Enum):
    """Status of a component transaction."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
```

### ValidationResult

```python
@dataclass(frozen=True)
class ValidationResult:
    """Result of transaction validation."""

    is_valid: bool
    error_messages: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """Add validation error."""

    def add_warning(self, message: str) -> None:
        """Add validation warning."""
```

## Error Handling

### Custom Exceptions

```python
class TransactionError(Exception):
    """Base exception for transaction-related errors."""
    pass

class NeighborRequirementError(TransactionError):
    """Raised when players are not neighbors for component exchange."""
    pass

class InsufficientResourcesError(TransactionError):
    """Raised when player lacks required components."""
    pass

class InvalidTransactionError(TransactionError):
    """Raised when transaction violates game rules."""
    pass

class TransactionNotFoundError(TransactionError):
    """Raised when referenced transaction doesn't exist."""
    pass
```

### Error Handling Strategy

1. **Validation Errors**: Return `ValidationResult` with error messages for user feedback
2. **System Errors**: Raise appropriate exceptions with detailed error messages
3. **Logging**: Log all transaction attempts, successes, and failures for debugging
4. **Recovery**: Provide clear error messages and suggested corrections

## Testing Strategy

### Unit Tests

1. **ComponentTransaction Tests**
   - Transaction creation and validation
   - Status transitions and lifecycle
   - Net exchange calculations

2. **TransactionManager Tests**
   - Transaction proposal and acceptance
   - Neighbor validation integration
   - Resource availability checking
   - Transaction history management

3. **ComponentValidator Tests**
   - Neighbor requirement validation
   - Resource availability validation
   - Promissory note ownership validation
   - Comprehensive transaction validation

4. **ResourceManager Tests**
   - Resource tracking and updates
   - Component transfers between players
   - Integration with game state

### Integration Tests

1. **End-to-End Transaction Flow**
   - Complete transaction from proposal to execution
   - Multi-player transaction scenarios
   - Error handling and recovery

2. **Game State Integration**
   - Transaction effects on game state
   - Resource consistency after transactions
   - Integration with existing systems

3. **Adjacency Integration**
   - Galaxy system integration for neighbor detection
   - Dynamic adjacency changes during game
   - Wormhole adjacency handling

### Edge Case Tests

1. **Boundary Conditions**
   - Zero-amount transactions
   - Maximum resource transfers
   - Empty offers and requests

2. **Error Scenarios**
   - Non-neighboring players
   - Insufficient resources
   - Invalid promissory notes
   - Concurrent transaction conflicts

3. **Game State Changes**
   - Adjacency changes during pending transactions
   - Resource changes during pending transactions
   - Player elimination effects

## Integration Points

### Existing Systems Integration

1. **Galaxy System**: Use existing `are_systems_adjacent()` for neighbor validation
2. **Game State**: Integrate with existing player resource tracking
3. **Promissory Notes**: Build on existing `PromissoryNoteManager` and `PromissoryNote` classes
4. **Transaction Framework**: Enhance existing `TransactionManager` and `TransactionOffer` classes

### New System Dependencies

1. **Player Resource Tracking**: Extend player model to track trade goods and commodities
2. **Transaction History**: Add transaction logging to game state
3. **Validation Services**: Create comprehensive validation layer
4. **Event System**: Integrate with game events for transaction notifications

### API Integration

```python
# Example API usage
transaction_manager = TransactionManager(galaxy, game_state)

# Propose a trade
transaction = transaction_manager.propose_transaction(
    proposing_player="player1",
    target_player="player2",
    offer=TransactionOffer(trade_goods=3),
    request=TransactionOffer(commodities=2)
)

# Accept the trade
result = transaction_manager.accept_transaction(transaction.transaction_id)

# View history
history = transaction_manager.get_transaction_history("player1")
```

This design provides a robust, testable, and extensible foundation for implementing Rule 28 component transactions while building on existing TI4 AI system architecture.
