# Rule 52: LEADERSHIP (STRATEGY CARD)

## Category Overview
**Rule Type**: Strategy Card Mechanics
**Complexity**: Medium
**Implementation Priority**: High
**Dependencies**: Command Tokens, Influence, Strategy Phase, Strategic Actions

## Raw LRR Text
From `lrr.txt` section 52:

**52** LEADERSHIP (STRATEGY CARD)
The "Leadership" strategy card allows players to gain command tokens. This card's initiative value is "1."

**52.1** During the action phase, if the active player has the "Leadership" strategy card, they can perform a strategic action to resolve that card's primary ability.

**52.2** To resolve the primary ability on the "Leadership" strategy card, the active player gains three command tokens. Then, that player can spend any amount of their influence to gain one command token for every three influence they spend.

**52.3** After the active player resolves the primary ability of the "Leadership" strategy card, each other player, beginning with the player to the left of the active player and proceeding clockwise, may spend any amount of influence to gain one command token for every three influence they spend.

**52.4** When a player gains command tokens, that player places each token on their command sheet in the pool of their choice.

**Related Topics**: Command Sheet, Command Tokens, Influence, Initiative Order, Strategic Action, Strategy Card

## Sub-Rules Analysis

### 52.1 - Strategic Action Timing
- **Status**: ✅ Implemented
- **Location**: Strategy card system in game controller
- **Test Coverage**: Good - strategic action tests exist
- **Implementation Notes**: Basic strategic action framework implemented

### 52.2 - Primary Ability (3 + Influence Conversion)
- **Status**: ✅ Implemented
- **Location**: `src/ti4/core/strategy_cards/cards/leadership.py` - `execute_primary_ability`
- **Test Coverage**: Comprehensive - 12 test cases covering all aspects
- **Implementation Notes**:
  - Gains 3 base command tokens automatically
  - Allows influence spending at 3:1 ratio for additional tokens
  - Handles token distribution to player's choice of pools
  - Validates reinforcement availability per Rule 20.3a
  - Exhausts planets when spending influence

### 52.3 - Secondary Ability (Influence Conversion Only)
- **Status**: ✅ Implemented
- **Location**: `src/ti4/core/strategy_cards/cards/leadership.py` - `execute_secondary_ability`
- **Test Coverage**: Comprehensive - included in 12 test cases
- **Implementation Notes**:
  - Only influence conversion (3:1 ratio), no base tokens
  - Players can choose to participate or decline
  - No command token cost for secondary ability (per Rule 20.5a)
  - Handles token distribution to player's choice of pools

### 52.4 - Command Token Pool Choice
- **Status**: ✅ Implemented
- **Location**: Token distribution handled in both primary and secondary abilities
- **Test Coverage**: Good - tested in `test_token_pool_choice_rule_52_4`
- **Implementation Notes**: Players specify token distribution via `token_distribution` parameter

### Initiative Value "1"
- **Status**: ✅ Implemented
- **Location**: Strategy card definitions
- **Test Coverage**: Good - initiative order tests exist
- **Implementation Notes**: Leadership correctly has initiative 1 (first in turn order)

## Related Topics
- **Rule 20**: COMMAND TOKENS (token management and pools)
- **Rule 82**: STRATEGIC ACTION (strategic action resolution)
- **Rule 83**: STRATEGY CARD (strategy card mechanics)
- **Rule 84**: STRATEGY PHASE (strategy card selection)
- **Rule 44**: INFLUENCE (influence spending mechanics)
- **Rule 47**: INITIATIVE ORDER (turn order determination)

## Dependencies
- **Command Tokens**: Command token system and pool management
- **Influence**: Player influence tracking and spending
- **Strategy Cards**: Strategy card selection and execution system
- **Strategic Actions**: Strategic action resolution framework
- **Initiative Order**: Turn order based on strategy card initiative
- **Command Sheet**: Player command sheet with three pools

## Test References
### Good Test Coverage Found:
- `test_game_controller.py`: Comprehensive strategy card system testing
  - Strategy card selection and availability
  - Initiative order determination
  - Multiple strategy card handling
  - Strategic action framework
  - Turn order based on initiative

### Test Scenarios Covered:
1. **Strategy Card Selection**: Players can select Leadership card
2. **Initiative Order**: Leadership (initiative 1) determines turn order correctly
3. **Availability**: Cannot select already taken strategy cards
4. **Multiple Cards**: Players can have multiple strategy cards in smaller games
5. **Strategic Actions**: Basic strategic action framework exists

### Missing Test Scenarios:
1. **Leadership Primary Ability**: No tests for 3 command tokens + influence conversion
2. **Leadership Secondary Ability**: No tests for influence-only conversion
3. **Command Token Pool Choice**: No tests for choosing which pool to place tokens
4. **Influence Spending**: No tests for 3-influence-per-token conversion
5. **Leadership Exception**: No tests for secondary ability not requiring command token spend

## Implementation Files
### Core Implementation:
- Strategy card system in game controller
- Command token management system
- Initiative order calculation

### Supporting Files:
- Command token pool management
- Influence tracking system
- Strategic action framework

### Missing Implementation:
- Leadership-specific primary ability logic
- Leadership-specific secondary ability logic
- Influence-to-command-token conversion
- Leadership secondary ability exception (no command token cost)

## Notable Implementation Details

### Strengths:
1. **Strategy Card Framework**: Solid strategy card selection and management system
2. **Initiative Order**: Correct initiative-based turn order calculation
3. **Command Token System**: Good command token pool management
4. **Strategic Actions**: Basic strategic action framework exists
5. **Test Coverage**: Good coverage of strategy card mechanics

### Areas Needing Attention:
1. **Leadership Specifics**: No specific Leadership card implementation found
2. **Influence Conversion**: No influence-to-command-token conversion logic
3. **Secondary Exception**: Leadership secondary doesn't cost command token
4. **Pool Choice**: Command token pool selection not tested for Leadership
5. **Ability Testing**: No specific ability tests for Leadership card

### Architecture Quality:
- **Excellent**: Strategy card framework and initiative system
- **Good**: Command token management and strategic actions
- **Needs Work**: Leadership-specific implementations
- **Missing**: Influence conversion and Leadership exceptions

## Action Items

### High Priority:
1. **Implement Leadership Primary**: 3 command tokens + influence conversion (3:1 ratio)
2. **Implement Leadership Secondary**: Influence conversion only (3:1 ratio)
3. **Add Leadership Exception**: Secondary ability doesn't cost command token

### Medium Priority:
4. **Test Leadership Abilities**: Comprehensive tests for primary and secondary abilities
5. **Test Influence Conversion**: Test 3-influence-per-command-token conversion
6. **Test Pool Choice**: Test command token pool selection during Leadership resolution

### Low Priority:
7. **Leadership UI**: Visual feedback for Leadership ability resolution
8. **Influence Validation**: Ensure players have enough influence to spend
9. **Leadership Events**: Publish events when Leadership abilities are used

## Implementation Status

### Overall Status: ✅ COMPLETE
- **Primary Ability**: ✅ Fully implemented with comprehensive test coverage
- **Secondary Ability**: ✅ Fully implemented with comprehensive test coverage
- **Token Pool Choice**: ✅ Fully implemented and tested
- **Initiative Value**: ✅ Implemented (returns 1)

### Test Cases Demonstrating Implementation

The following test cases in `tests/test_rule_52_leadership.py` demonstrate complete Rule 52 implementation:

1. **`test_leadership_card_basic_properties`** - Verifies initiative value is 1
2. **`test_primary_ability_gains_three_command_tokens`** - Tests base 3 token gain (Rule 52.2)
3. **`test_primary_ability_influence_conversion`** - Tests influence spending for additional tokens (Rule 52.2)
4. **`test_primary_ability_partial_influence_spending`** - Tests partial influence spending (Rule 52.2)
5. **`test_primary_ability_no_influence_spending`** - Tests choosing not to spend influence (Rule 52.2)
6. **`test_primary_ability_insufficient_reinforcements`** - Tests reinforcement limits (Rule 20.3a)
7. **`test_secondary_ability_influence_conversion_only`** - Tests secondary ability conversion (Rule 52.3)
8. **`test_secondary_ability_no_command_token_cost`** - Tests no token cost for secondary (Rule 20.5a)
9. **`test_secondary_ability_can_decline`** - Tests optional participation (Rule 52.3)
10. **`test_token_pool_choice_rule_52_4`** - Tests token pool choice (Rule 52.4)
11. **`test_influence_three_to_one_ratio`** - Tests exact 3:1 conversion ratio
12. **`test_integration_with_coordinator`** - Tests integration with strategy card system

### Key Implementation Details

- **File**: `src/ti4/core/strategy_cards/cards/leadership.py`
- **Primary Ability**: Gains 3 base tokens + optional influence conversion (3:1 ratio)
- **Secondary Ability**: Optional influence conversion only (3:1 ratio), no base tokens
- **Token Distribution**: Players specify distribution via `token_distribution` parameter
- **Influence Spending**: Handled via `_spend_influence` helper method that exhausts planets
- **Reinforcement Validation**: Respects Rule 20.3a - cannot gain tokens without reinforcements
- **Participation**: Secondary ability allows players to decline participation

### Dependencies Satisfied
- ✅ Command Token system (Rule 20)
- ✅ Influence system (Rule 47)
- ✅ Strategy Card framework
- ✅ Planet exhaustion mechanics
- ✅ Strategic Action system

## Priority Assessment
**Overall Priority**: High - Leadership is initiative 1 and fundamental to command token economy

**Implementation Status**: Complete (100%)
- Strategy card framework: ✅ Complete
- Initiative system: ✅ Complete
- Command token system: ✅ Complete
- Leadership primary ability: ✅ Complete
- Leadership secondary ability: ✅ Complete
- Influence conversion: ✅ Complete

The Leadership strategy card is fully implemented with comprehensive test coverage. All aspects of Rule 52 are properly handled, including the 3-token base gain, influence conversion at 3:1 ratio, token pool choice, and the unique secondary ability that doesn't require command token spending. The implementation correctly integrates with the broader strategy card system and command token economy.
