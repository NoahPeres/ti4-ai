# LRR Rule Analysis: Section 99 - WARFARE (STRATEGY CARD)

## Category Overview
The Warfare strategy card (initiative 6) allows players to remove command tokens from the board and redistribute their command tokens between pools, providing tactical flexibility and command token management.

## Raw LRR Text
```
99 WARFARE (STRATEGY CARD)
The "Warfare" strategy card allows a player to remove a command token from the board and redistribute their command tokens between their tactic, fleet, and strategy pools. This card's initiative value is "6." During the action phase, if the active player has the "Warfare" strategy card, they can perform a strategic action to resolve that card's primary ability.
To resolve the primary ability on the "Warfare" strategy card, the active player performs the following steps:
99.1 STEP 1-The active player removes any one of their command tokens from the game board. Then, that player gains that command token by placing it in a pool of their choice on their command sheet.
99.2 STEP 2-The active player can redistribute their command tokens.
```

## Sub-Rules Analysis

### 99.1 Command Token Removal (Step 1)
**Rule**: "The active player removes any one of their command tokens from the game board. Then, that player gains that command token by placing it in a pool of their choice on their command sheet."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No warfare strategy card implementation found
- **Tests**: No warfare-specific tests
- **Assessment**: Core mechanic missing - no command token removal from board
- **Priority**: HIGH
- **Dependencies**: Requires command token board tracking, removal mechanics
- **Notes**: Critical for tactical flexibility and command token economy

### 99.2 Command Token Redistribution (Step 2)
**Rule**: "The active player can redistribute their command tokens."

**Implementation Status**: ❌ NOT IMPLEMENTED  
- **Code**: No redistribution mechanics found
- **Tests**: No redistribution tests
- **Assessment**: Command pool management missing entirely
- **Priority**: HIGH
- **Dependencies**: Requires command pool system, redistribution UI/mechanics
- **Notes**: Essential for strategic command token allocation

### 99.3 Secondary Ability (Implied)
**Rule**: Secondary ability allows other players to spend strategy pool token for similar benefit

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No secondary ability implementation
- **Tests**: No secondary ability tests  
- **Assessment**: Strategy card secondary mechanics missing
- **Priority**: MEDIUM
- **Dependencies**: Requires secondary ability framework
- **Notes**: Standard pattern for all strategy cards

### 99.4 Initiative Value
**Rule**: "This card's initiative value is '6.'"

**Implementation Status**: ✅ IMPLEMENTED
- **Code**: Strategy card system includes initiative values
- **Tests**: Initiative ordering tests exist in test_game_controller.py
- **Assessment**: Basic strategy card framework exists
- **Priority**: LOW

### 99.5 Strategic Action Requirement
**Rule**: "During the action phase, if the active player has the 'Warfare' strategy card, they can perform a strategic action to resolve that card's primary ability."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No warfare-specific strategic action
- **Tests**: No warfare strategic action tests
- **Assessment**: Strategy card activation missing
- **Priority**: HIGH
- **Dependencies**: Requires strategic action system, warfare card logic
- **Notes**: Part of core strategy card mechanics

## Related Topics
- Rule 20: COMMAND TOKENS - Token management and pools
- Rule 82: STRATEGIC ACTION - Strategy card activation
- Rule 83: STRATEGY CARD - General strategy card mechanics
- Rule 81: STATUS PHASE - Command token redistribution timing

## Test References

### Current Coverage
- **test_game_controller.py**: Basic strategy card selection and initiative ordering
- **No warfare-specific tests found**

### Missing Test Scenarios
- Command token removal from board
- Command token redistribution between pools
- Warfare primary ability resolution
- Warfare secondary ability mechanics
- Integration with command token limits
- Board state validation after token removal

## Implementation Files

### Core Files
- **src/ti4/core/game_controller.py**: Basic strategy card framework exists
- **Missing**: Warfare strategy card implementation
- **Missing**: Command token redistribution system

### Supporting Files
- **Missing**: Command token board management
- **Missing**: Strategy card ability implementations
- **Missing**: Command pool manipulation utilities

## Notable Details

### Strengths
- Basic strategy card framework exists with initiative values
- Strategy card selection system implemented
- Turn order based on initiative working

### Areas Needing Attention
- **No warfare-specific implementation**: Complete absence of warfare mechanics
- **Missing command token management**: No board token removal or redistribution
- **No strategic action integration**: Warfare card cannot be activated
- **Missing secondary abilities**: No framework for other players to benefit
- **No command pool validation**: No enforcement of pool limits or rules

## Action Items

### High Priority
- [ ] Implement warfare strategy card primary ability (command token removal + redistribution)
- [ ] Create command token board management system
- [ ] Add strategic action integration for warfare card
- [ ] Implement command token redistribution mechanics

### Medium Priority  
- [ ] Add warfare secondary ability for other players
- [ ] Create comprehensive warfare strategy card tests
- [ ] Add command pool validation and limits
- [ ] Integrate with existing command token system

### Low Priority
- [ ] Add UI for command token redistribution
- [ ] Create warfare card usage analytics
- [ ] Add advanced redistribution strategies

## Priority Assessment
**Overall Priority**: HIGH
**Implementation Status**: 15% (only basic framework)
**Complexity**: Medium
**Dependencies**: Command token system, strategic actions

The Warfare strategy card is a fundamental game mechanic that provides crucial command token flexibility. The complete absence of implementation makes this a high-priority item for core gameplay functionality.