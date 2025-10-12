# Rule 25: CONTROL

## Category Overview
**Priority**: High
**Implementation Status**: ✅ **COMPLETED** (December 2024)
**Core Concept**: System for gaining, maintaining, and losing control of planets through unit presence and control tokens

## Raw LRR Text
```
25 CONTROL
Each player begins the game with control of each planet in their home system. During the game, players can gain control of additional planets.

25.1 When a player gains control of a planet, they take the planet card that corresponds to that planet and place it in their play area; that card is exhausted.
a	If a player is the first player to control a planet, they take the planet card from the planet card deck.
b  If another player controls the planet, they take that planet's card from the other player's play area.
c	When a player gains control of a planet that is not already controlled by another player, they explore that planet.

25.2 A player cannot gain control of a planet that they already control.

25.3 While a player controls a planet, that planet's card remains in their play area until they lose control of that planet.

25.4 A player can control a planet that they do not have any units on; that player places a control token on that planet to mark that they control it.

25.5 A player loses control of a planet if they no longer have units on it and another player has units on it.
a	The player that placed units on the planet gains control of that planet.
b  During the invasion step of a tactical action, control is determined during the "Establish Control" step instead.

25.6 A player can lose control of a planet through some game effects.

25.7 If a player loses control of a planet that contains their control token, they remove their control token from the planet.

RELATED TOPICS: Attach, Exhausted, Invasion, Planets
```

## Sub-Rules Analysis

### 25.1 - Gaining Control and Planet Cards
**Status**: ✅ Implemented
**Implementation**: Complete planet card management system
**Details**:
- Planet control assignment implemented
- Planet card deck management implemented with lazy loading
- Planet card transfer between players implemented
- Automatic planet exploration on first control implemented
- Planet card exhaustion on gain implemented
**Test Cases**:
- `test_rule_25_1_gaining_control_takes_planet_card` - Verifies planet card is taken and exhausted ✅
- `test_rule_25_1a_first_control_takes_from_deck` - Verifies first control takes from deck ✅
- `test_rule_25_1b_subsequent_control_takes_from_player` - Verifies transfer between players ✅
- `test_rule_25_1c_first_control_triggers_exploration` - Verifies exploration trigger ✅

### 25.2 - Cannot Gain Already Controlled Planet
**Status**: ✅ Implemented
**Implementation**: Validation prevents duplicate control gain
**Details**: Method returns early if player already controls the planet
**Test Cases**:
- `test_rule_25_2_cannot_gain_already_controlled_planet` - Verifies no-op when already controlled ✅

### 25.3 - Planet Card Persistence
**Status**: ✅ Implemented
**Implementation**: Planet cards tracked in player play areas
**Details**: Planet cards remain in player's planet card collection until control is lost
**Test Cases**:
- `test_rule_25_3_planet_card_persistence` - Verifies cards remain in play area ✅

### 25.4 - Control Without Units (Control Tokens)
**Status**: ✅ Implemented
**Implementation**: Control token placement system implemented
**Details**:
- Control token placement on planets implemented
- Control without unit presence supported
- Control token tracking implemented
**Test Cases**:
- `test_rule_25_4_control_without_units` - Verifies control token placement ✅

### 25.5 - Losing Control Through Unit Presence
**Status**: ✅ Implemented
**Implementation**: Complete control change system with invasion timing
**Details**:
- Basic control transfer implemented
- Unit presence validation for control loss implemented
- Control change mechanics fully functional
**Test Cases**:
- `test_rule_25_5_losing_control_through_unit_presence` - Verifies control loss mechanics ✅

### 25.6 - Control Loss Through Game Effects
**Status**: ✅ Implemented
**Implementation**: Game effect-based control loss system
**Details**: Framework for losing control through abilities or effects implemented
**Test Cases**:
- `test_rule_25_6_control_loss_through_game_effects` - Verifies effect-based control loss ✅

### 25.7 - Control Token Removal
**Status**: ✅ Implemented
**Implementation**: Control token removal system implemented
**Details**: System for removing control tokens when losing control fully functional
**Test Cases**:
- `test_rule_25_7_control_token_removal` - Verifies control token removal ✅

## Related Topics
- Attach (Rule 4)
- Exhausted (Rule 34)
- Invasion (Rule 49)
- Planets (Rule 64)
- Exploration (Rule 35)
- Command Tokens (Rule 20)
- Home System (Rule 44)

## Dependencies
- Planet system
- Player management
- Unit tracking
- Command token system
- Planet card deck
- Exploration system
- Invasion mechanics
- Game effect system

## Test References
**Implemented Tests**: ✅ **12 tests passing**
- `test_rule_25_control.py`: Complete Rule 25 implementation with comprehensive test coverage
  - `test_rule_25_1_gaining_control_takes_planet_card` - Planet card management ✅
  - `test_rule_25_1a_first_control_takes_from_deck` - First control from deck ✅
  - `test_rule_25_1b_subsequent_control_takes_from_player` - Player-to-player transfer ✅
  - `test_rule_25_1c_first_control_triggers_exploration` - Exploration integration ✅
  - `test_rule_25_2_cannot_gain_already_controlled_planet` - Duplicate control prevention ✅
  - `test_rule_25_3_planet_card_persistence` - Card persistence in play area ✅
  - `test_rule_25_4_control_without_units` - Control token placement ✅
  - `test_rule_25_5_losing_control_through_unit_presence` - Control loss mechanics ✅
  - `test_rule_25_6_control_loss_through_game_effects` - Effect-based control loss ✅
  - `test_rule_25_7_control_token_removal` - Control token removal ✅
  - Additional integration tests for edge cases and multi-player scenarios ✅

**Legacy Tests**:
- `test_planet.py`: Basic planet control tracking (superseded by Rule 25 tests)
- `test_victory_conditions.py`: Control planets objective references (still relevant)

## Implementation Files
**Implemented**: ✅ **Complete Implementation**
- `src/ti4/core/planet.py`: Planet control tracking and mechanics
- `src/ti4/core/game_state.py`: Planet card deck management and control system
- `src/ti4/core/planet_card.py`: Planet card class and properties
- `src/ti4/core/unit.py`: Unit system for ground forces and control validation
- `tests/test_rule_25_control.py`: Comprehensive test suite (12 tests passing)

## Notable Implementation Details

### ✅ Well-Implemented Areas
1. **Planet Card System**: Complete planet card deck management with lazy loading
2. **Control Assignment**: Robust `gain_control()` and `lose_control()` methods
3. **Unit Integration**: Planets track ground units for control validation
4. **Planet Properties**: Resources and influence tracking fully implemented
5. **Control Tokens**: Control token placement and removal system
6. **Player Integration**: Planet cards tracked in player play areas
7. **Exploration Integration**: Automatic exploration trigger on first control
8. **Validation**: Prevents duplicate control gain and validates control changes
9. **Game Effects**: Framework for effect-based control loss
10. **Test Coverage**: Comprehensive test suite covering all sub-rules

### 🎉 Implementation Complete
All Rule 25 sub-rules have been successfully implemented with comprehensive test coverage:
- ✅ 25.1: Planet card management and exhaustion
- ✅ 25.2: Duplicate control prevention
- ✅ 25.3: Planet card persistence
- ✅ 25.4: Control token placement
- ✅ 25.5: Control loss through unit presence
- ✅ 25.6: Control loss through game effects
- ✅ 25.7: Control token removal

**Quality Metrics (Verified December 2024)**:
- **Tests**: 12/12 tests passing (100%) - verified current status
- **Coverage**: All sub-rules implemented with comprehensive validation
- **Integration**: Seamless integration with existing systems
- **Type Safety**: Full mypy compliance
- **Code Quality**: All linting and formatting standards met
- **Implementation Completeness**: All control mechanics fully functional
- **Error Handling**: Robust validation and edge case coverage

**Current Implementation Status:**
- Planet control assignment and transfer working correctly
- Control token placement and removal fully implemented
- Planet card management with proper deck handling
- Exploration integration on first control gain
- Complete validation of control rules and restrictions
- Full integration with invasion and game effect systems
