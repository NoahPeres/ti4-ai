# Rule 28: DEALS Transaction API Guide

This guide provides comprehensive documentation for using the Rule 28 component transaction API, including examples and integration patterns.

## Overview

The Transaction API provides a clean, simplified interface for managing component-based transactions between players in TI4. It handles transaction proposals, status queries, history retrieval, and response handling while abstracting away the complexity of the underlying transaction management system.

## Key Features

- **Simple API Interface**: Clean methods for common transaction operations
- **Robust Error Handling**: Graceful handling of errors with informative messages
- **Input Validation**: Comprehensive validation of all inputs
- **Transaction History**: Complete tracking of transaction history
- **Status Queries**: Real-time transaction status information
- **Integration Ready**: Designed for easy integration with game clients

## API Classes

### TransactionAPI

The main API class that provides all transaction operations.

```python
from ti4.core.rule_28_deals import TransactionAPI
from ti4.core.transactions import TransactionOffer

# Initialize the API
api = TransactionAPI(galaxy=galaxy_instance, game_state=game_state_instance)
```

### TransactionAPIResult

Result object returned by transaction operations.

```python
@dataclass
class TransactionAPIResult:
    success: bool
    transaction_id: Optional[str] = None
    transaction: Optional[ComponentTransaction] = None
    error_message: Optional[str] = None
```

### TransactionStatusInfo

Information about a transaction's current status.

```python
@dataclass
class TransactionStatusInfo:
    transaction_id: str
    status: TransactionStatus
    proposing_player: str
    target_player: str
    offer: TransactionOffer
    request: TransactionOffer
    timestamp: datetime
    completion_timestamp: Optional[datetime] = None
```

## Basic Usage Examples

### 1. Proposing a Transaction

```python
from ti4.core.transactions import TransactionOffer

# Create transaction offers
offer = TransactionOffer(trade_goods=3, commodities=1)
request = TransactionOffer(trade_goods=2)

# Propose the transaction
result = api.propose_transaction(
    proposing_player="player1",
    target_player="player2",
    offer=offer,
    request=request
)

if result.success:
    print(f"Transaction proposed: {result.transaction_id}")
    transaction_id = result.transaction_id
else:
    print(f"Failed to propose transaction: {result.error_message}")
```

### 2. Checking Transaction Status

```python
# Get current status of a transaction
status = api.get_transaction_status(transaction_id)

if status:
    print(f"Transaction {status.transaction_id} is {status.status.value}")
    print(f"Proposed by {status.proposing_player} to {status.target_player}")
    print(f"Offer: {status.offer}")
    print(f"Request: {status.request}")
else:
    print("Transaction not found")
```

### 3. Accepting a Transaction

```python
# Accept a pending transaction
result = api.accept_transaction(transaction_id)

if result.success:
    print("Transaction accepted and executed")
    if result.transaction:
        print(f"Final status: {result.transaction.status}")
else:
    print(f"Failed to accept transaction: {result.error_message}")
```

### 4. Rejecting a Transaction

```python
# Reject a pending transaction
result = api.reject_transaction(transaction_id)

if result.success:
    print("Transaction rejected")
else:
    print(f"Failed to reject transaction: {result.error_message}")
```

### 5. Viewing Transaction History

```python
# Get transaction history for a player
history = api.get_transaction_history("player1")

print(f"Player1 has {len(history)} transactions in history:")
for transaction in history:
    print(f"  {transaction.transaction_id}: {transaction.status.value}")
    print(f"    With {transaction.target_player}")
    print(f"    Completed: {transaction.completion_timestamp}")
```

### 6. Checking Pending Transactions

```python
# Get pending transactions for a player
pending = api.get_pending_transactions("player1")

print(f"Player1 has {len(pending)} pending transactions:")
for transaction in pending:
    print(f"  {transaction.transaction_id}: waiting for response")
    print(f"    Proposed to {transaction.target_player}")
    print(f"    Offering: {transaction.offer}")
```

## Advanced Usage Examples

### Complex Transaction with Promissory Notes

```python
from ti4.core.transactions import PromissoryNote, PromissoryNoteType

# Create a promissory note
note = PromissoryNote(
    note_type=PromissoryNoteType.TRADE_AGREEMENT,
    issuing_player="player1"
)

# Create complex offers
offer = TransactionOffer(
    trade_goods=5,
    commodities=2,
    promissory_notes=[note]
)
request = TransactionOffer(trade_goods=8)

# Propose the transaction
result = api.propose_transaction(
    proposing_player="player1",
    target_player="player2",
    offer=offer,
    request=request
)
```

### Transaction Workflow Management

```python
class TransactionWorkflow:
    """Example workflow manager for transactions."""

    def __init__(self, api: TransactionAPI):
        self.api = api
        self.pending_proposals = {}

    def propose_trade(self, from_player: str, to_player: str,
                     offer: TransactionOffer, request: TransactionOffer) -> str:
        """Propose a trade and track it."""
        result = self.api.propose_transaction(from_player, to_player, offer, request)

        if result.success:
            self.pending_proposals[result.transaction_id] = {
                'from': from_player,
                'to': to_player,
                'timestamp': datetime.now()
            }
            return result.transaction_id
        else:
            raise Exception(f"Failed to propose trade: {result.error_message}")

    def process_response(self, transaction_id: str, accept: bool) -> bool:
        """Process a transaction response."""
        if accept:
            result = self.api.accept_transaction(transaction_id)
        else:
            result = self.api.reject_transaction(transaction_id)

        if result.success and transaction_id in self.pending_proposals:
            del self.pending_proposals[transaction_id]

        return result.success

    def get_player_summary(self, player_id: str) -> dict:
        """Get comprehensive transaction summary for a player."""
        return {
            'pending': self.api.get_pending_transactions(player_id),
            'history': self.api.get_transaction_history(player_id),
            'active_proposals': [
                tid for tid, info in self.pending_proposals.items()
                if info['from'] == player_id
            ]
        }

# Usage
workflow = TransactionWorkflow(api)

# Propose a trade
tx_id = workflow.propose_trade(
    "player1", "player2",
    TransactionOffer(trade_goods=3),
    TransactionOffer(commodities=2)
)

# Later, process the response
success = workflow.process_response(tx_id, accept=True)
```

### Error Handling Patterns

```python
def safe_transaction_proposal(api: TransactionAPI, proposing_player: str,
                            target_player: str, offer: TransactionOffer,
                            request: TransactionOffer) -> Optional[str]:
    """Safely propose a transaction with comprehensive error handling."""

    try:
        # Validate inputs before API call
        if not proposing_player or not target_player:
            print("Error: Player IDs cannot be empty")
            return None

        if proposing_player == target_player:
            print("Error: Players cannot trade with themselves")
            return None

        # Propose the transaction
        result = api.propose_transaction(proposing_player, target_player, offer, request)

        if result.success:
            print(f"Transaction proposed successfully: {result.transaction_id}")
            return result.transaction_id
        else:
            print(f"Transaction proposal failed: {result.error_message}")
            return None

    except Exception as e:
        print(f"Unexpected error during transaction proposal: {e}")
        return None

def monitor_transaction(api: TransactionAPI, transaction_id: str,
                       timeout_seconds: int = 300) -> TransactionStatus:
    """Monitor a transaction until completion or timeout."""

    start_time = datetime.now()

    while True:
        status = api.get_transaction_status(transaction_id)

        if not status:
            print(f"Transaction {transaction_id} not found")
            return TransactionStatus.CANCELLED

        if status.status in [TransactionStatus.ACCEPTED, TransactionStatus.REJECTED]:
            print(f"Transaction {transaction_id} completed with status: {status.status}")
            return status.status

        # Check timeout
        if (datetime.now() - start_time).seconds > timeout_seconds:
            print(f"Transaction {transaction_id} monitoring timed out")
            return TransactionStatus.EXPIRED

        # Wait before checking again
        time.sleep(5)
```

## Integration Patterns

### Game Client Integration

```python
class GameClient:
    """Example game client integration."""

    def __init__(self, player_id: str, transaction_api: TransactionAPI):
        self.player_id = player_id
        self.api = transaction_api

    def make_trade_offer(self, target_player: str, my_offer: dict,
                        their_offer: dict) -> bool:
        """Make a trade offer to another player."""

        offer = TransactionOffer(
            trade_goods=my_offer.get('trade_goods', 0),
            commodities=my_offer.get('commodities', 0),
            # Add promissory notes if provided
        )

        request = TransactionOffer(
            trade_goods=their_offer.get('trade_goods', 0),
            commodities=their_offer.get('commodities', 0),
        )

        result = self.api.propose_transaction(
            self.player_id, target_player, offer, request
        )

        return result.success

    def check_incoming_offers(self) -> list:
        """Check for incoming trade offers."""
        pending = self.api.get_pending_transactions(self.player_id)

        # Filter for offers where this player is the target
        incoming = [
            tx for tx in pending
            if tx.target_player == self.player_id
        ]

        return incoming

    def respond_to_offer(self, transaction_id: str, accept: bool) -> bool:
        """Respond to a trade offer."""
        if accept:
            result = self.api.accept_transaction(transaction_id)
        else:
            result = self.api.reject_transaction(transaction_id)

        return result.success
```

### Event-Driven Integration

```python
from typing import Callable

class TransactionEventHandler:
    """Event-driven transaction handling."""

    def __init__(self, api: TransactionAPI):
        self.api = api
        self.event_handlers = {
            'transaction_proposed': [],
            'transaction_accepted': [],
            'transaction_rejected': [],
        }

    def on_event(self, event_type: str, handler: Callable):
        """Register an event handler."""
        if event_type in self.event_handlers:
            self.event_handlers[event_type].append(handler)

    def propose_with_events(self, proposing_player: str, target_player: str,
                           offer: TransactionOffer, request: TransactionOffer):
        """Propose transaction and trigger events."""
        result = self.api.propose_transaction(proposing_player, target_player, offer, request)

        if result.success:
            # Trigger event
            for handler in self.event_handlers['transaction_proposed']:
                handler(result.transaction)

        return result

    def accept_with_events(self, transaction_id: str):
        """Accept transaction and trigger events."""
        result = self.api.accept_transaction(transaction_id)

        if result.success:
            for handler in self.event_handlers['transaction_accepted']:
                handler(result.transaction)

        return result

# Usage
handler = TransactionEventHandler(api)

# Register event handlers
handler.on_event('transaction_proposed',
                lambda tx: print(f"New proposal: {tx.transaction_id}"))
handler.on_event('transaction_accepted',
                lambda tx: print(f"Trade completed: {tx.transaction_id}"))
```

## Best Practices

### 1. Input Validation

Always validate inputs before making API calls:

```python
def validate_transaction_inputs(proposing_player: str, target_player: str,
                              offer: TransactionOffer, request: TransactionOffer) -> bool:
    """Validate transaction inputs."""

    if not proposing_player or not target_player:
        return False

    if proposing_player == target_player:
        return False

    if not isinstance(offer, TransactionOffer) or not isinstance(request, TransactionOffer):
        return False

    return True
```

### 2. Error Handling

Always check result success and handle errors appropriately:

```python
result = api.propose_transaction(player1, player2, offer, request)

if not result.success:
    # Log the error
    logger.error(f"Transaction proposal failed: {result.error_message}")

    # Handle specific error types
    if "not neighbors" in result.error_message:
        # Handle neighbor requirement error
        pass
    elif "insufficient" in result.error_message:
        # Handle resource shortage error
        pass

    return False
```

### 3. Transaction Monitoring

Implement proper monitoring for long-running transactions:

```python
def wait_for_transaction_completion(api: TransactionAPI, transaction_id: str,
                                  callback: Callable = None) -> TransactionStatus:
    """Wait for transaction completion with optional callback."""

    while True:
        status = api.get_transaction_status(transaction_id)

        if not status:
            return TransactionStatus.CANCELLED

        if status.status != TransactionStatus.PENDING:
            if callback:
                callback(status)
            return status.status

        time.sleep(1)  # Poll every second
```

### 4. Resource Management

Track resources properly to avoid failed transactions:

```python
class ResourceTracker:
    """Track player resources for transaction validation."""

    def __init__(self, api: TransactionAPI):
        self.api = api
        self.resource_cache = {}

    def can_afford_offer(self, player_id: str, offer: TransactionOffer) -> bool:
        """Check if player can afford the offer."""
        # This would integrate with actual resource tracking
        # For now, just return True as example
        return True

    def propose_if_affordable(self, proposing_player: str, target_player: str,
                            offer: TransactionOffer, request: TransactionOffer):
        """Only propose if the player can afford it."""

        if not self.can_afford_offer(proposing_player, offer):
            return TransactionAPIResult(
                success=False,
                error_message="Insufficient resources for offer"
            )

        return self.api.propose_transaction(proposing_player, target_player, offer, request)
```

## Error Reference

### Common Error Messages

- `"Player ID cannot be empty"` - Empty or None player ID provided
- `"Transaction ID cannot be empty"` - Empty or None transaction ID provided
- `"Players cannot transact with themselves"` - Same player ID for both proposer and target
- `"Offer must be a TransactionOffer instance"` - Invalid offer type
- `"Request must be a TransactionOffer instance"` - Invalid request type
- `"Transaction {id} not found"` - Transaction doesn't exist
- `"Players {p1} and {p2} are not neighbors"` - Neighbor requirement not met
- `"Insufficient trade goods"` - Player doesn't have enough trade goods
- `"Insufficient commodities"` - Player doesn't have enough commodities

### Error Handling Strategy

1. **API Level**: All API methods return result objects with success flags
2. **Validation Level**: Input validation catches common errors early
3. **System Level**: Underlying system errors are caught and converted to user-friendly messages
4. **Graceful Degradation**: Failed operations return safe defaults (empty lists, None values)

## Performance Considerations

### 1. Caching

The API doesn't implement caching internally, but you can add caching at the client level:

```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedTransactionAPI:
    """Wrapper that adds caching to the transaction API."""

    def __init__(self, api: TransactionAPI, cache_ttl: int = 30):
        self.api = api
        self.cache_ttl = cache_ttl
        self._status_cache = {}
        self._history_cache = {}

    def get_transaction_status(self, transaction_id: str):
        """Get transaction status with caching."""
        now = datetime.now()

        if transaction_id in self._status_cache:
            cached_time, cached_status = self._status_cache[transaction_id]
            if (now - cached_time).seconds < self.cache_ttl:
                return cached_status

        status = self.api.get_transaction_status(transaction_id)
        self._status_cache[transaction_id] = (now, status)
        return status
```

### 2. Batch Operations

For multiple operations, consider batching:

```python
def batch_transaction_status(api: TransactionAPI, transaction_ids: list) -> dict:
    """Get status for multiple transactions efficiently."""
    results = {}

    for tx_id in transaction_ids:
        results[tx_id] = api.get_transaction_status(tx_id)

    return results
```

## Testing

### Unit Testing

```python
import pytest
from unittest.mock import Mock

def test_transaction_proposal():
    """Test basic transaction proposal."""
    mock_galaxy = Mock()
    mock_game_state = Mock()

    api = TransactionAPI(mock_galaxy, mock_game_state)

    result = api.propose_transaction(
        "player1", "player2",
        TransactionOffer(trade_goods=1),
        TransactionOffer(commodities=1)
    )

    # Add assertions based on expected behavior
    assert result is not None
```

### Integration Testing

```python
def test_complete_transaction_flow():
    """Test complete transaction from proposal to completion."""
    # Set up real or mock dependencies
    api = TransactionAPI(galaxy, game_state)

    # Propose transaction
    result = api.propose_transaction(
        "player1", "player2",
        TransactionOffer(trade_goods=3),
        TransactionOffer(commodities=2)
    )

    assert result.success
    tx_id = result.transaction_id

    # Check status
    status = api.get_transaction_status(tx_id)
    assert status.status == TransactionStatus.PENDING

    # Accept transaction
    accept_result = api.accept_transaction(tx_id)
    assert accept_result.success

    # Verify completion
    final_status = api.get_transaction_status(tx_id)
    assert final_status.status == TransactionStatus.ACCEPTED
```

This guide provides a comprehensive overview of the Rule 28 Transaction API. For more specific use cases or advanced integration patterns, refer to the integration tests and example implementations in the codebase.
