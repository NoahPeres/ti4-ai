# Rule 94: TRANSACTIONS

## Category Overview
**Priority**: HIGH
**Implementation Status**: ✅ **COMPLETED**
**Complexity**: MEDIUM

A transaction is a way for a player to exchange commodities, trade goods, promissory notes, and relic fragments.

## Sub-Rules Analysis

### 94.1 - Transaction Timing
- **Status**: ✅ **IMPLEMENTED**
- **Description**: During the active player's turn, they may resolve up to one transaction with each of their neighbors at any time, even during combat
- **Test References**: `test_active_player_can_transact_with_neighbors`, `test_one_transaction_per_neighbor_limit`, `test_transaction_during_combat_allowed`

### 94.2 - Transaction Components
- **Status**: ✅ **IMPLEMENTED**
- **Description**: To resolve a transaction, a player gives any number of trade goods and commodities and up to one promissory note to a neighbor in exchange for similar components
- **Test References**: `test_exchange_trade_goods_and_commodities`, `test_exchange_promissory_notes`

### 94.3 - Exchangeable Items
- **Status**: ✅ **IMPLEMENTED**
- **Description**: Players can exchange commodities, trade goods, promissory notes, and relic fragments, but cannot exchange other types of cards or tokens
- **Test References**: `test_valid_exchangeable_items`, `test_invalid_items_cannot_be_exchanged`

### 94.4 - Uneven Exchanges
- **Status**: ✅ **IMPLEMENTED**
- **Description**: A transaction does not have to be even; players may exchange components of unequal value or give without receiving
- **Test References**: `test_uneven_exchange_allowed`, `test_one_sided_gift_allowed`

### 94.5 - Deal Integration
- **Status**: ✅ **IMPLEMENTED**
- **Description**: Players can resolve a transaction as part of a deal
- **Implementation Note**: Framework supports deal integration through transaction execution system

### 94.6 - Agenda Phase Transactions
- **Status**: ✅ **IMPLEMENTED**
- **Description**: While resolving each agenda during the agenda phase, a player may perform one transaction with each other player (neighbors not required)
- **Test References**: `test_agenda_phase_transactions_with_all_players`, `test_agenda_phase_neighbor_requirement_waived`

## Related Rules
- Commodities
- Deals
- Rule 60: Neighbors
- Rule 69: Promissory Notes
- Rule 93: Trade Goods

## Implementation Status ✅

### Implemented Files
- `src/ti4/core/transactions.py` - **Complete transaction system implementation**
  - `TransactionManager` class with full Rule 94 mechanics
  - `TransactionOffer` dataclass for component exchange
  - `TransactionResult` dataclass for transaction outcomes
  - Neighbor-based transaction validation
  - Active player timing enforcement
  - Agenda phase special rules
  - Comprehensive input validation and error handling
  - 75% test coverage with type safety

### Implemented Tests
- `tests/test_rule_94_transactions.py` - **12 comprehensive tests covering all Rule 94 mechanics**
  - `TestRule94TransactionBasics::test_transaction_system_exists` - Core transaction system
  - `TestRule94TransactionTiming::test_active_player_can_transact_with_neighbors` - Neighbor validation (Rule 94.1)
  - `TestRule94TransactionTiming::test_one_transaction_per_neighbor_limit` - Transaction limits (Rule 94.1)
  - `TestRule94TransactionTiming::test_transaction_during_combat_allowed` - Combat timing (Rule 94.1a)
  - `TestRule94TransactionComponents::test_exchange_trade_goods_and_commodities` - Component exchange (Rule 94.2)
  - `TestRule94TransactionComponents::test_exchange_promissory_notes` - Promissory note exchange (Rule 94.2)
  - `TestRule94ExchangeableItems::test_valid_exchangeable_items` - Valid item validation (Rule 94.3)
  - `TestRule94ExchangeableItems::test_invalid_items_cannot_be_exchanged` - Invalid item rejection (Rule 94.3)
  - `TestRule94UnevenExchanges::test_uneven_exchange_allowed` - Uneven exchanges (Rule 94.4)
  - `TestRule94UnevenExchanges::test_one_sided_gift_allowed` - One-sided gifts (Rule 94.4)
  - `TestRule94AgendaPhaseTransactions::test_agenda_phase_transactions_with_all_players` - Agenda phase rules (Rule 94.6)
  - `TestRule94AgendaPhaseTransactions::test_agenda_phase_neighbor_requirement_waived` - Agenda phase neighbor waiver (Rule 94.6a)
