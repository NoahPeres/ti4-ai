# LRR Rule Analysis: Rule 71 - READIED

## Rule Category Overview
**Rule 71: READIED** - Defines the readied state for cards and the mechanics for exhausting and readying cards throughout the game.

## Implementation Status: ❌ NOT IMPLEMENTED (0%)
- **Test Coverage**: No tests found for readied/exhausted mechanics
- **Implementation**: No card state management system found
- **Integration**: No integration with resource spending or ability resolution
- **Quality**: No implementation to assess

## Raw LRR Text
```
71 READIED
Cards have a readied state, which indicates that a player can exhaust or resolve the abilities on those cards.
71.1 A card that is readied is placed faceup in a player's play area; a card that is exhausted is placed facedown in a player's area.
71.2 A player can exhaust a readied planet card to spend resources or influence from that card's planet.
71.3 A player can exhaust certain readied technology cards to resolve those cards' abilities.
a	Such a technology will specifically instruct a player to exhaust the card as part of the ability's cost.
71.4 If a card is exhausted, a player cannot resolve that card's abilities or spend resources or influence on that card until it is readied.
71.5 During a "Ready Cards" step, each player readies all of their exhausted cards by flipping them faceup.
71.6 When a player performs a strategic action, they exhaust their chosen strategy card.
a	That card is later readied during the status phase.
RELATED TOPICS: Abilities, Exhausted, Status Phase
```

## Sub-Rules Analysis

### 71.0 Basic Readied Concept
**Rule**: "Cards have a readied state, which indicates that a player can exhaust or resolve the abilities on those cards."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No card state management system found
- **Tests**: No tests for readied/exhausted states
- **Assessment**: Core card state system not implemented
- **Priority**: HIGH
- **Dependencies**: Requires card management system and game state tracking
- **Notes**: Fundamental mechanic for resource management and ability usage

### 71.1 Card State Representation
**Rule**: "A card that is readied is placed faceup in a player's play area; a card that is exhausted is placed facedown in a player's area."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No visual/state representation for card orientation
- **Tests**: No tests for card state representation
- **Assessment**: Card state visualization not implemented
- **Priority**: HIGH
- **Dependencies**: Requires UI system and card state management
- **Notes**: Visual indicator of card availability for use

### 71.2 Planet Card Exhaustion
**Rule**: "A player can exhaust a readied planet card to spend resources or influence from that card's planet."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No planet card exhaustion for resource spending
- **Tests**: No tests for planet exhaustion mechanics
- **Assessment**: Resource spending exhaustion not implemented
- **Priority**: HIGH
- **Dependencies**: Requires planet card system and resource management
- **Notes**: Core economic mechanic for spending resources and influence

### 71.3 Technology Card Exhaustion
**Rule**: "A player can exhaust certain readied technology cards to resolve those cards' abilities."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No technology card exhaustion system
- **Tests**: No tests for technology exhaustion
- **Assessment**: Technology exhaustion costs not implemented
- **Priority**: MEDIUM
- **Dependencies**: Requires technology system and ability resolution
- **Notes**: Some technologies require exhaustion as activation cost

### 71.4 Exhausted Card Restrictions
**Rule**: "If a card is exhausted, a player cannot resolve that card's abilities or spend resources or influence on that card until it is readied."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No enforcement of exhausted card restrictions
- **Tests**: No tests for exhausted card limitations
- **Assessment**: Exhaustion restrictions not enforced
- **Priority**: HIGH
- **Dependencies**: Requires card state validation and ability system
- **Notes**: Critical for preventing double-use of resources and abilities

### 71.5 Ready Cards Step
**Rule**: "During a 'Ready Cards' step, each player readies all of their exhausted cards by flipping them faceup."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No Ready Cards step implementation
- **Tests**: No tests for card readying process
- **Assessment**: Status phase card readying not implemented
- **Priority**: HIGH
- **Dependencies**: Requires status phase system and card state management
- **Notes**: Essential for resetting card availability each round

### 71.6 Strategy Card Exhaustion
**Rule**: "When a player performs a strategic action, they exhaust their chosen strategy card."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No strategy card exhaustion tracking
- **Tests**: No tests for strategy card state changes
- **Assessment**: Strategy card exhaustion not implemented
- **Priority**: HIGH
- **Dependencies**: Requires strategy card system and strategic action tracking
- **Notes**: Prevents multiple uses of strategy cards per round

## Related Topics
- **Abilities (Rule 1)**: Many abilities require card exhaustion as cost
- **Exhausted (Rule 34)**: Complementary rule defining exhausted state
- **Status Phase (Rule 81)**: Contains Ready Cards step
- **Resources (Rule 75)**: Planet exhaustion for resource spending
- **Strategy Cards (Rule 83)**: Strategy card exhaustion mechanics

## Test References

### Current Test Coverage
- **No Tests Found**: No readied/exhausted related tests in the codebase

### Missing Test Scenarios
- Card state management (readied/exhausted)
- Planet card exhaustion for resource spending
- Technology card exhaustion for abilities
- Exhausted card usage restrictions
- Ready Cards step in status phase
- Strategy card exhaustion and readying
- Visual representation of card states

## Implementation Files

### Core Implementation
- **MISSING**: Card state management system
- **MISSING**: Planet card exhaustion mechanics
- **MISSING**: Technology card exhaustion system
- **MISSING**: Ready Cards step implementation

### Supporting Files
- **MISSING**: Card state tests
- **MISSING**: Exhaustion validation tests
- **MISSING**: Status phase integration tests

## Notable Details

### Strengths
- Clear rule definition for card states
- Well-defined exhaustion and readying mechanics
- Integration points with multiple game systems

### Areas Needing Attention
- No implementation exists for any card state mechanics
- No test coverage for readied/exhausted functionality
- No integration with resource spending or ability systems
- Missing Ready Cards step in status phase

## Implementation Status

**Overall Progress**: 0%

### Not Implemented (❌)
- **Rule 71.0**: Basic readied state concept and card availability
- **Rule 71.1**: Card state representation and visual indicators
- **Rule 71.2**: Planet card exhaustion for resource spending
- **Rule 71.3**: Technology card exhaustion for ability costs
- **Rule 71.4**: Exhausted card usage restrictions and validation
- **Rule 71.5**: Ready Cards step in status phase
- **Rule 71.6**: Strategy card exhaustion and readying

## Priority Implementation Tasks

### High Priority
1. **Card State System** - Implement basic readied/exhausted state management
2. **Planet Exhaustion** - Connect planet cards to resource spending
3. **Ready Cards Step** - Implement status phase card readying
4. **Exhaustion Validation** - Prevent use of exhausted cards

### Medium Priority
1. **Technology Exhaustion** - Implement technology card exhaustion costs
2. **Strategy Card States** - Track strategy card exhaustion
3. **Visual Representation** - Card state indicators in UI

### Low Priority
1. **Advanced Validation** - Complex exhaustion scenarios
2. **Performance Optimization** - Efficient card state tracking

## Test Coverage Summary

**Total Tests**: 0 tests
- No readied/exhausted related tests found in codebase

## Action Items

### High Priority
1. **Design Card State System**: Architecture for readied/exhausted mechanics
2. **Implement Planet Exhaustion**: Connect to resource spending system
3. **Add Ready Cards Step**: Status phase card readying implementation
4. **Create Exhaustion Validation**: Prevent invalid card usage

### Medium Priority
1. **Technology Integration**: Exhaustion costs for technology abilities
2. **Strategy Card States**: Track and manage strategy card exhaustion
3. **Comprehensive Testing**: Full test suite for card state mechanics

### Low Priority
1. **UI Integration**: Visual indicators for card states
2. **Edge Case Handling**: Complex exhaustion scenarios
3. **Performance Optimization**: Efficient state management

## Priority Assessment
- **Overall Priority**: HIGH
- **Implementation Status**: 0% (no implementation found)
- **Blocking Dependencies**: Affects resource spending, ability usage, status phase
- **Impact**: Core game mechanic affecting multiple systems
