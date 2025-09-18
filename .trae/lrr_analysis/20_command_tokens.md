# LRR Rule Analysis: Rule 20 - COMMAND TOKENS

## Category Overview
**Rule Category**: Core Game Mechanics - Currency System
**Priority**: CRITICAL
**Implementation Status**: PARTIALLY IMPLEMENTED
**Dependencies**: Command Sheet (Rule 19), Fleet Pool (Rule 37), Strategic Action (Rule 83), Tactical Action (Rule 89)

## Raw LRR Text

### 20 COMMAND TOKENS
Command tokens are a currency that players use to perform actions and expand their fleets.

**20.1** Each player begins the game with eight tokens on their command sheet: three in their tactic pool, three in their fleet pool, and two in their strategy pool.
- a. Command tokens in the strategy and tactic pool are placed with the faction symbol faceup.

**20.2** When a player gains a command token, they choose which of their three pools to place it in.

**20.3** A player is limited by the amount of command tokens in their reinforcements.
- a. If a player would gain a command token but has none available in their reinforcements, that player cannot gain that command token.
- b. If a game effect would place a player's command token from their reinforcements and none are available, that player must take a token from a pool on their command sheet, unless the token would be placed into a system that already contains one of their command tokens.

**20.4** During the action phase, a player can perform a tactical action by spending a command token from their tactic pool; they place the command token in a system.

**20.5** After a player performs a strategic action during the action phase, each other player can resolve the secondary ability of that strategy card by spending a command token from their strategy pool.
- a. A player does not spend a command token to resolve the secondary ability of the "Leadership" strategy card.

**20.6** If a game effect would place a player's command token in a system where they already have one, they place the token in their reinforcements instead. Any effects that resolve by placing that token are resolved as normal.

**Related Topics**: Fleet Pool, Leadership, Reinforcements, Strategic Action, Tactical Action

## Sub-Rules Analysis

### 20.1 - Starting Command Tokens
**Status**: ✅ IMPLEMENTED
**Implementation**: `constants.py` defines starting token values (3 tactic, 3 fleet, 2 strategy)
**Tests**: Multiple test files verify starting token counts
**Notes**: Well-implemented with proper constants and test coverage

### 20.2 - Token Gain Choice
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No token gain mechanics exist
**Tests**: No tests for token gain choice
**Priority**: HIGH
**Notes**: Critical for Leadership strategy card and other token-gaining effects

### 20.3 - Reinforcement Limits
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No reinforcement tracking system
**Tests**: No reinforcement limit tests
**Priority**: HIGH
**Notes**: Important constraint on token availability and management

### 20.4 - Tactical Action Token Spending
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: `TacticalAction` class exists but no token spending mechanics
**Tests**: No tactical action token spending tests
**Priority**: CRITICAL
**Notes**: Core game mechanic - tactical actions are primary player actions

### 20.5 - Strategic Action Secondary Abilities
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No secondary ability token spending system
**Tests**: No secondary ability tests
**Priority**: HIGH
**Notes**: Essential for strategy card interaction between players

### 20.6 - Duplicate Token Placement
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No system token tracking or duplicate prevention
**Tests**: No duplicate placement tests
**Priority**: MEDIUM
**Notes**: Edge case handling for token placement conflicts

## Related Topics
- **Rule 19**: COMMAND SHEET - Physical location of token pools
- **Rule 37**: FLEET POOL - Fleet supply mechanics using fleet tokens
- **Rule 52**: LEADERSHIP - Primary source of token gain
- **Rule 83**: STRATEGIC ACTION - Token spending for secondary abilities
- **Rule 89**: TACTICAL ACTION - Token spending for system activation

## Dependencies
- Command Sheet implementation (pools structure)
- Reinforcement tracking system
- System activation mechanics
- Strategy card secondary ability system
- Token placement validation

## Test References

### Existing Tests
- `test_fleet_management.py`: Fleet pool token limits (lines 84-105)
- `test_scenario_library.py`: Command token assertions
- `test_integration_with_builder.py`: Token setup and assertions
- `test_builder_utilities.py`: Command token assertions
- `test_game_scenario_builder.py`: Token setup and assertions

### Missing Tests
- Token gain and pool choice mechanics
- Reinforcement limit enforcement
- Tactical action token spending
- Strategic action secondary ability token spending
- Token placement in systems
- Duplicate token placement handling

## Implementation Files

### Existing Files
- `src/ti4/core/constants.py`: Starting token values (lines 25-30)
- `src/ti4/actions/tactical_action.py`: TacticalAction class structure
- `src/ti4/core/game_controller.py`: Basic strategic action framework

### Missing Files
- Command token management system
- Reinforcement tracking system
- Token spending validation
- System token placement tracking

## Notable Implementation Details

### Well-Implemented
- Starting token constants are properly defined
- Fleet pool token limits are enforced in fleet management
- Basic tactical action structure exists

### Implementation Gaps
- No token spending mechanics for any action type
- No reinforcement tracking or limits
- No system token placement or tracking
- No secondary ability token spending system
- No token gain mechanics or pool choice

### Critical Missing Features
- Tactical action activation (spending tactic tokens)
- Strategic action secondary abilities (spending strategy tokens)
- Token gain from Leadership and other sources
- Reinforcement limit enforcement

## Action Items

1. **Implement token spending for tactical actions** - Core game mechanic for system activation
2. **Create reinforcement tracking system** - Track available tokens and enforce limits
3. **Implement token gain mechanics** - Allow players to choose pools when gaining tokens
4. **Add strategic action secondary ability token spending** - Enable strategy card interaction
5. **Create system token placement tracking** - Track which systems have player tokens
6. **Implement duplicate token placement prevention** - Handle Rule 20.6 edge cases
7. **Add comprehensive token spending tests** - Cover all token spending scenarios
8. **Create token gain choice tests** - Verify pool selection mechanics
9. **Implement Leadership strategy card token gain** - Primary source of new tokens
10. **Add reinforcement limit validation tests** - Ensure proper constraint enforcement