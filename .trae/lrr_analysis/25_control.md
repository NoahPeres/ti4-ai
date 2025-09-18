# Rule 25: CONTROL

## Category Overview
**Priority**: High  
**Implementation Status**: Partial  
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
**Status**: ⚠️ Partially Implemented  
**Implementation**: Basic planet control tracking exists, but planet card management missing  
**Details**: 
- Planet control assignment implemented
- Planet card deck management not implemented
- Planet card transfer between players not implemented
- Automatic planet exploration on first control not implemented
- Planet card exhaustion on gain not implemented

### 25.2 - Cannot Gain Already Controlled Planet
**Status**: ❌ Not Implemented  
**Implementation**: No validation preventing duplicate control gain  
**Details**: No checks to prevent gaining control of already controlled planets

### 25.3 - Planet Card Persistence
**Status**: ❌ Not Implemented  
**Implementation**: No planet card play area management  
**Details**: Planet cards not tracked in player play areas

### 25.4 - Control Without Units (Control Tokens)
**Status**: ❌ Not Implemented  
**Implementation**: Control token placement system missing  
**Details**: 
- Control token placement on planets not implemented
- Control without unit presence not supported
- Control token tracking not implemented

### 25.5 - Losing Control Through Unit Presence
**Status**: ⚠️ Partially Implemented  
**Implementation**: Basic control change exists but invasion timing missing  
**Details**: 
- Basic control transfer implemented
- Invasion step "Establish Control" timing not implemented
- Unit presence validation for control loss not complete

### 25.6 - Control Loss Through Game Effects
**Status**: ❌ Not Implemented  
**Implementation**: No game effect-based control loss system  
**Details**: No framework for losing control through abilities or effects

### 25.7 - Control Token Removal
**Status**: ❌ Not Implemented  
**Implementation**: Control token removal not implemented  
**Details**: No system for removing control tokens when losing control

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
**Existing Tests**:
- `test_planet.py`: Basic planet control tracking and changes
- `test_victory_conditions.py`: Control planets objective references

**Missing Tests**:
- Planet card management and transfer
- Control token placement and removal
- Planet exploration on first control
- Control loss through unit presence
- Control loss through game effects
- Invasion step control determination
- Planet card exhaustion mechanics

## Implementation Files
**Existing**:
- `src/ti4/core/planet.py`: Basic planet control tracking
- `src/ti4/core/unit.py`: Unit system for ground forces

**Missing**:
- Planet card system
- Control token management
- Planet exploration integration
- Invasion control mechanics
- Game effect control loss system
- Planet card deck management

## Notable Implementation Details

### Well-Implemented Areas
1. **Basic Planet Control**: Planet objects have control tracking
2. **Control Assignment**: Basic `set_control()` method exists
3. **Unit Placement**: Planets can track ground units
4. **Planet Properties**: Resources and influence tracking implemented

### Implementation Gaps
1. **Planet Card System**: No planet card deck or management
2. **Control Tokens**: No control token placement or tracking
3. **Planet Exploration**: No exploration trigger on first control
4. **Control Validation**: No prevention of duplicate control gain
5. **Invasion Integration**: Missing invasion step control determination
6. **Game Effect Integration**: No system for effect-based control loss

## Action Items

1. **Implement Planet Card System**
   - Create planet card deck management
   - Add planet card transfer between players
   - Implement planet card exhaustion on gain
   - Handle first-time vs. transfer scenarios
   - Track planet cards in player play areas

2. **Add Control Token Management**
   - Implement control token placement on planets
   - Support control without unit presence
   - Add control token removal on control loss
   - Track control tokens per player
   - Validate control token availability

3. **Integrate Planet Exploration**
   - Trigger exploration on first planet control
   - Connect with exploration system
   - Handle exploration timing and resolution
   - Support multiple planet exploration ordering
   - Implement exploration deck management

4. **Implement Control Validation**
   - Prevent gaining control of already controlled planets
   - Validate unit presence for control changes
   - Check control token requirements
   - Enforce control change rules
   - Provide clear error messages

5. **Add Invasion Control Mechanics**
   - Implement "Establish Control" step in invasion
   - Handle control determination timing
   - Support multiple planet invasion scenarios
   - Integrate with tactical action system
   - Coordinate with combat resolution

6. **Create Game Effect Control System**
   - Framework for effect-based control loss
   - Support various control-affecting abilities
   - Handle timing and resolution order
   - Integrate with ability system
   - Track control change sources

7. **Implement Planet Card Persistence**
   - Track planet cards in player play areas
   - Handle card state (exhausted/ready)
   - Support card transfer on control change
   - Maintain card-planet associations
   - Implement card deck management

8. **Add Control Change Events**
   - Event system for control gain/loss
   - Trigger dependent systems (exploration, abilities)
   - Handle cascading control effects
   - Support control change listeners
   - Maintain control history

9. **Create Comprehensive Testing**
   - Planet card management scenarios
   - Control token placement and removal
   - Exploration integration testing
   - Invasion control determination
   - Game effect control loss scenarios
   - Multi-player control conflicts

10. **Integrate with Existing Systems**
    - Connect with objective system
    - Link with resource/influence spending
    - Coordinate with unit movement
    - Integrate with ability system
    - Support victory condition checking