# Rule 28: DEALS - Analysis

## Category Overview
**Rule Type**: Player Interaction/Trading System  
**Priority**: MEDIUM-HIGH  
**Complexity**: MEDIUM  
**Dependencies**: Transactions, Trade Goods, Promissory Notes, Neighbors  

## Raw LRR Text
```
28 DEALS	
A deal is an agreement between two players that may or may not include a transaction that involves physical components.

28.1 Players can make deals with each other at any time, even if they are not neighbors. However, deals that include a transaction must follow the rules for transactions, including that the players be neighbors.

28.2 Deals are binding or non-binding according to the conditions of the deal.

28.3 If the terms of a deal can be resolved immediately, it is a binding deal. When a deal is binding, a player must adhere to the terms of the agreement and whatever transactions, if any, were agreed upon.
a	The results of playing an action card, including the act of successfully resolving a card, are not instantaneous and cannot be guaranteed. They cannot be part of a binding deal.

28.4 If the terms of a deal cannot be resolved immediately, it is a non-binding deal. When a deal is non-binding, a player does not have to adhere to any part of the agreement.

RELATED TOPICS: Promissory Notes, Trade Goods
```

## Sub-Rules Analysis

### 28.1 Deal Timing and Transaction Requirements
**Status**: ⚠️ PARTIAL  
**Implementation**: Basic transaction system exists but no deal framework  
**Tests**: Transaction tests exist but no deal validation  
**Notes**: Neighbor requirement for transactions exists but no deal system to enforce it  

### 28.2 Binding vs Non-Binding Classification
**Status**: ❌ NOT IMPLEMENTED  
**Implementation**: No deal classification system or binding enforcement  
**Tests**: No tests for deal binding mechanics  
**Notes**: Core mechanic for determining deal enforceability missing  

### 28.3 Binding Deal Requirements and Enforcement
**Status**: ❌ NOT IMPLEMENTED  
**Implementation**: No immediate resolution validation or binding enforcement  
**Tests**: No tests for binding deal adherence  
**Notes**: Critical for ensuring players honor immediate agreements  

### 28.3a Action Card Exclusion from Binding Deals
**Status**: ❌ NOT IMPLEMENTED  
**Implementation**: No action card result validation in deal system  
**Tests**: No tests for action card exclusion from binding deals  
**Notes**: Important limitation preventing guaranteed action card outcomes  

### 28.4 Non-Binding Deal Flexibility
**Status**: ❌ NOT IMPLEMENTED  
**Implementation**: No non-binding deal system or adherence flexibility  
**Tests**: No tests for non-binding deal behavior  
**Notes**: Allows future promises without enforcement  

## Related Topics
- **Transactions** (Rule 94): Physical component exchange system
- **Trade Goods** (Rule 93): Currency for deals and transactions
- **Promissory Notes** (Rule 69): Tradeable cards for future benefits
- **Neighbors** (Rule 59): Adjacency requirement for transactions
- **Action Cards** (Rule 2): Cards excluded from binding deals
- **Commodities** (Rule 21): Tradeable resources

## Dependencies
- **Transaction System**: ⚠️ Partial (basic trading exists)
- **Trade Goods**: ✅ Implemented (resource management exists)
- **Neighbor System**: ⚠️ Partial (adjacency checking exists)
- **Promissory Notes**: ❌ Missing (tradeable cards system)
- **Action Cards**: ✅ Implemented (card system exists)
- **Player Communication**: ❌ Missing (deal negotiation interface)

## Test References

### Existing Tests
- `test_action.py`: Basic transaction class with trade commodities description
- `test_game_scenario_builder.py`: Trade goods resource management
- `test_scenario_library.py`: Trade goods allocation and verification
- `test_integration_with_builder.py`: Multi-player trade goods setup
- `test_builder_utilities.py`: Basic trade goods assignment

### Missing Tests
- Deal creation and validation
- Binding vs non-binding deal classification
- Deal enforcement and adherence checking
- Transaction neighbor requirement validation
- Action card exclusion from binding deals
- Deal resolution timing validation
- Multi-player deal negotiation scenarios

## Implementation Files

### Core Implementation
- Trade goods system: ✅ Exists in game state and resource management
- Basic transaction framework: ⚠️ Partial implementation exists
- Player resource management: ✅ Comprehensive system exists

### Missing Implementation
- Deal entity and management system
- Binding/non-binding classification logic
- Deal enforcement and validation
- Player communication interface for deals
- Transaction-deal integration
- Promissory note trading system

## Notable Implementation Details

### Well-Implemented
- **Trade Goods System**: Comprehensive resource management with proper allocation
- **Resource Management**: Players can have and manage trade goods effectively
- **Basic Transaction Framework**: Foundation exists for component exchange
- **Game State Integration**: Trade goods properly integrated into game state

### Implementation Gaps
- **Deal System**: No formal deal entity or management system
- **Binding Enforcement**: No mechanism to enforce binding deal adherence
- **Player Communication**: No interface for deal negotiation
- **Transaction Validation**: No neighbor requirement enforcement for deals
- **Promissory Notes**: Missing tradeable card system for future benefits
- **Deal Classification**: No logic to determine binding vs non-binding status

## Action Items

1. **Create deal entity system** - Implement deal objects with terms and classification
2. **Add binding/non-binding classification** - Logic to determine deal enforceability
3. **Implement deal enforcement** - System to ensure binding deal adherence
4. **Add transaction-deal integration** - Connect physical trades to deal framework
5. **Create neighbor validation** - Enforce neighbor requirement for transaction deals
6. **Implement promissory note system** - Tradeable cards for future benefits
7. **Add action card exclusion logic** - Prevent action card results in binding deals
8. **Create player communication interface** - UI/API for deal negotiation
9. **Add deal resolution timing** - Validate immediate vs future resolution
10. **Create comprehensive deal tests** - Cover all deal scenarios and edge cases

## Priority Assessment
**MEDIUM-HIGH** - Deals are a fundamental diplomatic and economic mechanic in TI4. While basic trade goods exist, the formal deal system with binding/non-binding classification and enforcement is completely missing. This affects player interaction and strategic depth significantly.