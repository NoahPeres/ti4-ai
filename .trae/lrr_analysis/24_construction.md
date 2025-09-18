# Rule 24: CONSTRUCTION (STRATEGY CARD)

## Category Overview
**Priority**: High  
**Implementation Status**: Partial  
**Core Concept**: Strategy card allowing players to construct PDS and space dock structures on planets they control

## Raw LRR Text
```
24 CONSTRUCTION (STRATEGY CARD)
The "Construction" strategy card allows players to construct structures on planets they control. This card's initiative value is "4."

24.1 During the action phase, if the active player has the "Construction" strategy card, they can perform a strategic action to resolve that card's primary ability.

24.2 To resolve the primary ability on the "Construction" strategy card, the active player may place either one PDS or one space dock on a planet they control. Then, that player may place an additional PDS on a planet they control.
a The structures can be placed on the same planet or different planets.
b The structures can be placed in any systems, regardless of whether the player has a command token in the system or not.

24.3 After the active player resolves the primary ability of the "Construction" strategy card, each other player, beginning with the player to the left of the active player and proceeding clockwise, may spend one command token from their strategy pool and place that command token in any system. If that player already has a command token in that system, the spent token is returned to their reinforcements instead. Then, that player places either one PDS or one space dock on a planet they control in that system.

24.4 When a player places either a PDS or space dock using the "Construction" strategy card, they take that PDS or space dock from their reinforcements.
a If a player does not have the unit in their reinforcements, that player can remove a unit from any system that does not contain one of their command tokens and place that unit in their reinforcements. Then, that player must place the unit on the game board as instructed by the effect that is placing the unit.

RELATED TOPICS: Initiative Order, Strategic Action, Strategy Card, Structures
```

## Sub-Rules Analysis

### 24.1 - Strategic Action Trigger
**Status**: ⚠️ Partially Implemented  
**Implementation**: Strategic action framework exists, but Construction-specific logic missing  
**Details**: Can perform strategic actions but Construction card primary ability not implemented

### 24.2 - Primary Ability Resolution
**Status**: ❌ Not Implemented  
**Implementation**: No Construction primary ability implementation  
**Details**: 
- Structure placement (PDS or space dock) not implemented
- Additional PDS placement not implemented
- Same/different planet placement rules not enforced
- System command token independence not implemented

### 24.3 - Secondary Ability Resolution
**Status**: ❌ Not Implemented  
**Implementation**: No Construction secondary ability implementation  
**Details**: 
- Command token spending from strategy pool not implemented
- Command token placement in systems not implemented
- Token return to reinforcements logic missing
- Structure placement in chosen system not implemented

### 24.4 - Structure Placement from Reinforcements
**Status**: ⚠️ Partially Implemented  
**Implementation**: Unit reinforcement system exists but Construction-specific rules missing  
**Details**: 
- Basic reinforcement system exists
- Unit removal from non-command token systems not implemented for Construction
- Immediate placement requirement not enforced

## Related Topics
- Initiative Order (Rule 48)
- Strategic Action (Rule 82)
- Strategy Card (Rule 83)
- Structures (Rule 85)
- PDS (Rule 63)
- Space Dock (Rule 79)
- Command Tokens (Rule 20)
- Reinforcements (Rule 72)

## Dependencies
- Strategic action system
- Strategy card framework
- Structure placement system
- Command token management
- Reinforcement system
- Planet control validation
- Turn order management

## Test References
**Existing Tests**:
- `test_game_controller.py`: Strategy card selection and strategic action framework
- `test_unit.py`: Space dock unit properties
- `test_combat.py`: Space dock combat properties

**Missing Tests**:
- Construction primary ability resolution
- Construction secondary ability resolution
- Structure placement validation
- Command token spending for secondary ability
- Reinforcement-based structure placement
- Multiple structure placement scenarios

## Implementation Files
**Existing**:
- `src/ti4/core/game_controller.py`: Strategic action framework
- `src/ti4/core/strategy_card.py`: Strategy card system
- `src/ti4/core/units.py`: Unit definitions including space dock

**Missing**:
- Construction strategy card implementation
- Structure placement system
- Construction-specific command token logic
- PDS placement validation
- Space dock placement validation

## Notable Implementation Details

### Well-Implemented Areas
1. **Strategic Action Framework**: Basic system for strategic actions exists
2. **Strategy Card System**: Strategy card selection and management implemented
3. **Unit Definitions**: Space dock and PDS unit types defined
4. **Turn Order**: Initiative-based turn order system exists

### Implementation Gaps
1. **Construction Primary Ability**: No implementation of structure placement
2. **Construction Secondary Ability**: Missing command token spending and structure placement
3. **Structure Placement Rules**: No validation of placement limits or requirements
4. **Reinforcement Integration**: Construction-specific reinforcement rules missing
5. **Planet Control Validation**: No verification of planet control for structure placement

## Action Items

1. **Implement Construction Primary Ability**
   - Create structure placement logic for PDS and space dock
   - Implement additional PDS placement option
   - Enforce same/different planet placement rules
   - Handle system command token independence

2. **Implement Construction Secondary Ability**
   - Add command token spending from strategy pool
   - Implement command token placement in systems
   - Handle token return to reinforcements when system occupied
   - Add structure placement in chosen system

3. **Create Structure Placement System**
   - Validate planet control requirements
   - Enforce structure placement limits (1 space dock, 2 PDS per planet)
   - Handle structure placement from reinforcements
   - Implement unit removal for missing reinforcements

4. **Add Construction Strategy Card Class**
   - Extend strategy card system with Construction-specific logic
   - Implement primary and secondary ability methods
   - Handle initiative value (4) and card properties
   - Integrate with strategic action system

5. **Implement Command Token Logic**
   - Add strategy pool command token spending
   - Handle command token placement in systems
   - Implement token return to reinforcements logic
   - Validate command token availability

6. **Add Structure Validation**
   - Verify planet control before placement
   - Check structure limits per planet
   - Validate reinforcement availability
   - Enforce immediate placement requirements

7. **Create Comprehensive Testing**
   - Primary ability structure placement scenarios
   - Secondary ability command token and structure placement
   - Edge cases (no reinforcements, occupied systems)
   - Multiple player interaction scenarios

8. **Integrate with Existing Systems**
   - Connect with planet control system
   - Integrate with reinforcement management
   - Link with command token tracking
   - Coordinate with turn order system

9. **Add Construction Validation**
   - Prevent invalid structure placements
   - Validate command token spending requirements
   - Check system and planet availability
   - Provide clear error messages

10. **Document Construction Mechanics**
    - Create comprehensive documentation
    - Include structure placement examples
    - Document command token interaction
    - Provide edge case guidance