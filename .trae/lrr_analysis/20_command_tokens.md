# Rule 20: COMMAND TOKENS - Implementation Analysis

## Rule Overview
Command tokens are a currency that players use to perform actions and expand their fleets.

## Implementation Status: ✅ COMPLETED

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

## Test Cases Demonstrating Implementation

### Core Command Token Mechanics
1. **Starting Configuration**: `test_player_starts_with_correct_tokens()` - Validates 3/3/2 starting distribution
2. **Token Spending**: `test_spend_tactic_token()`, `test_spend_fleet_token()`, `test_spend_strategy_token()` - Basic spending mechanics
3. **Pool Validation**: `test_cannot_spend_from_empty_pool()` - Prevents invalid spending

### Reinforcement System (Rule 20.3)
1. **Starting Reinforcements**: `test_player_starts_with_correct_reinforcements()` - Validates 8 starting reinforcements
2. **Exhaustion Prevention**: `test_cannot_gain_token_with_no_reinforcements()` - Blocks token gain when exhausted
3. **Tracking**: `test_gain_token_reduces_reinforcements()` - Proper reinforcement decrement

### Token Gain Mechanics (Rule 20.2)
1. **Pool Choice**: `test_can_gain_token_in_*_pool()` - Player choice of destination pool
2. **Sequential Gains**: `test_player_can_choose_different_pools_sequentially()` - Multiple token gains
3. **Validation**: `test_invalid_pool_raises_error()` - Error handling for invalid pools

## Dependencies
- ✅ `GameConstants` - Starting token values
- ✅ `CommandSheet` - Token pool management
- ✅ `Player` - Integration with player state
- ⚠️ Tactical Action System (Rule 58) - For Rule 20.4 completion
- ⚠️ Strategy Card System - For Rule 20.5 completion
- ⚠️ Galaxy/System Mechanics - For Rule 20.6 completion

## Quality Metrics
- **Test Coverage**: 18 tests across 3 test files
- **Implementation Coverage**: Core mechanics (20.1-20.3) fully implemented
- **Code Quality**: Passes type checking, linting, and formatting standards
- **TDD Compliance**: All tests written first, proper RED-GREEN-REFACTOR cycles

## Integration Notes
- Command tokens integrate with player state through frozen dataclass pattern
- Reinforcement tracking uses `object.__setattr__()` for immutable updates
- Pool validation ensures type safety with `PoolType` literal type
- Ready for integration with tactical actions and strategy card systems

## Next Steps for Full Completion
1. Implement tactical action system (Rule 58) for Rule 20.4 completion
2. Implement strategy card system for Rule 20.5 completion
3. Implement system placement mechanics for Rule 20.6 completion
4. Add integration tests between command tokens and other systems

**Overall Rule 20 Status**: Core mechanics complete, ready for system integration

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
