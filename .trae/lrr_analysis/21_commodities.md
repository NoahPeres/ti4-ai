# LRR Rule Analysis: Rule 21 - COMMODITIES

## Category Overview
**Rule Category**: Economic System - Resource Management
**Priority**: HIGH
**Implementation Status**: PARTIALLY IMPLEMENTED
**Dependencies**: Trade Goods (Rule 93), Transactions (Rule 94), Trade Strategy Card (Rule 92), Faction Sheets

## Raw LRR Text

### 21 COMMODITIES
Commodities represent goods that are plentiful for their own faction and are desired by other factions. A commodity has no inherent game effects, but converts into a trade good if given to or received from another player.

**21.1** Commodities and trade goods are represented by opposite sides of the same token.

**21.2** The commodity value on a player's faction sheet indicates the maximum number of commodities that player can have.

**21.3** When an effect instructs a player to replenish commodities, that player takes the number of commodity tokens necessary so that the amount of commodities that player has equals the commodity value on their faction sheet. Then, those tokens are placed faceup in the commodity area of that player's faction sheet.

**21.4** When a player replenishes commodities, that player takes the commodity tokens from the supply.

**21.5** Players can trade commodities following the rules for transactions. When a player receives a commodity from another player, the player who received that token converts it into a trade good by placing it in the trade good area of their command sheet with the trade good side faceup.
- a. That token is no longer a commodity token; it is a trade good token.
- b. A player can trade commodity tokens before resolving a game effect that allows them to replenish commodities.
- c. If a game effect instructs a player to convert a number of their own commodities to trade goods, those trade goods are not treated as being gained for the purpose of triggering other abilities.

**21.6** Any game effect that instructs a player to give a commodity to another player causes that commodity to be converted into a trade good.

**21.7** A player cannot spend commodities unless otherwise specified; a player can only trade them during a transaction.

**21.8** Commodity tokens come in values of one and three. A player can swap between these tokens as necessary.

**Related Topics**: Deals, Trade Goods, Transactions

## Sub-Rules Analysis

### 21.1 - Token Representation
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No commodity/trade good token system exists
**Tests**: No token representation tests
**Priority**: HIGH
**Notes**: Fundamental token system for economic mechanics

### 21.2 - Commodity Value Limits
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No faction sheet commodity values or limits
**Tests**: No commodity limit tests
**Priority**: HIGH
**Notes**: Each faction has different commodity values (0-4 typically)

### 21.3 - Commodity Replenishment
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No replenishment mechanics exist
**Tests**: No replenishment tests
**Priority**: HIGH
**Notes**: Core mechanic for Trade strategy card and other effects

### 21.4 - Supply Management
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No supply tracking for commodity tokens
**Tests**: No supply management tests
**Priority**: MEDIUM
**Notes**: Token availability constraint

### 21.5 - Commodity Trading and Conversion
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No commodity trading or conversion system
**Tests**: Basic transaction tests exist but no commodity-specific logic
**Priority**: HIGH
**Notes**: Core economic interaction between players

### 21.6 - Automatic Conversion
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No automatic conversion for game effects
**Tests**: No automatic conversion tests
**Priority**: MEDIUM
**Notes**: Edge case for certain abilities and effects

### 21.7 - Spending Restrictions
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No commodity spending restrictions
**Tests**: No spending restriction tests
**Priority**: MEDIUM
**Notes**: Important constraint - commodities can't be spent like trade goods

### 21.8 - Token Values
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No token value system (1 and 3 denominations)
**Tests**: No token value tests
**Priority**: LOW
**Notes**: Quality of life feature for token management

## Related Topics
- **Rule 92**: TRADE (STRATEGY CARD) - Primary source of commodity replenishment
- **Rule 93**: TRADE GOODS - Converted form of commodities
- **Rule 94**: TRANSACTIONS - Trading mechanism for commodities
- **Faction Sheets**: Commodity values vary by faction

## Dependencies
- Faction sheet implementation with commodity values
- Token supply management system
- Transaction system with commodity support
- Trade strategy card implementation
- Command sheet trade good area

## Test References

### Existing Tests
- `test_action.py`: Basic transaction description (lines 54-61)
- `test_builder_utilities.py`: Trade goods setup (line 23)
- `test_game_scenario_builder.py`: Trade goods resource setup (lines 122-135)
- `test_integration_with_builder.py`: Trade goods resource setup (lines 129-141)
- `test_scenario_library.py`: Trade goods assertions (lines 36-176)

### Missing Tests
- Commodity replenishment mechanics
- Commodity value limits per faction
- Commodity to trade good conversion
- Commodity trading in transactions
- Automatic conversion for game effects
- Spending restriction enforcement
- Token value management (1 and 3 denominations)

## Implementation Files

### Existing Files
- Basic trade goods tracking in test scenarios
- Transaction framework exists but lacks commodity support

### Missing Files
- Commodity management system
- Faction sheet commodity values
- Commodity replenishment mechanics
- Commodity/trade good token system
- Supply management for tokens

## Notable Implementation Details

### Well-Implemented
- Basic trade goods tracking exists in test scenarios
- Transaction framework provides foundation for commodity trading

### Implementation Gaps
- No commodity system exists at all
- No faction-specific commodity values
- No replenishment mechanics
- No conversion system between commodities and trade goods
- No spending restrictions for commodities

### Critical Missing Features
- Commodity replenishment (Trade strategy card primary ability)
- Commodity trading and conversion in transactions
- Faction sheet commodity values
- Token supply management

## Action Items

1. **Implement faction sheet commodity values** - Each faction needs different commodity limits
2. **Create commodity replenishment system** - Core mechanic for Trade strategy card
3. **Add commodity to trade good conversion** - Automatic conversion when traded
4. **Implement commodity trading in transactions** - Allow commodity exchange between players
5. **Create commodity/trade good token system** - Dual-sided token representation
6. **Add commodity spending restrictions** - Prevent spending commodities like trade goods
7. **Implement automatic conversion for game effects** - Handle Rule 21.6 scenarios
8. **Create comprehensive commodity tests** - Cover all commodity mechanics
9. **Add token supply management** - Track available commodity tokens
10. **Implement token value system** - Support 1 and 3 denomination tokens