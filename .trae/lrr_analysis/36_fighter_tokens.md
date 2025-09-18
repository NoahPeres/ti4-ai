# Rule 36: FIGHTER TOKENS - Analysis

## Category Overview
**Rule Type:** Unit Management Mechanic  
**Priority:** LOW-MEDIUM  
**Status:** PARTIALLY IMPLEMENTED  
**Complexity:** Low  

## Raw LRR Text
```
36 FIGHTER TOKENS
Fighter tokens are used to represent fighters when the plastic pieces are not available.

36.1 When producing a fighter unit, a player can use a fighter token from the supply instead of a plastic piece.
a Fighter tokens must be accompanied by at least one plastic piece of the same type.

36.2 Players can replace their plastic fighters with tokens at any time.

36.3 If a player ever has a fighter token in a system that does not contain one of their plastic fighters, that player must replace it with one of their plastic fighters from their reinforcements.
a If the player cannot replace the token, the unit is destroyed.

36.4 Fighter tokens come in values of one and three. A player can swap between these tokens as necessary.

RELATED TOPICS: Infantry Tokens, Producing Units
```

## Sub-Rules Analysis

### 36.1 Fighter Token Production
- **Status:** PARTIALLY IMPLEMENTED
- **Description:** Use fighter tokens from supply when producing fighters, must have plastic piece accompaniment
- **Gap:** Token production system exists but plastic piece requirement not enforced

### 36.2 Plastic-to-Token Replacement
- **Status:** NOT IMPLEMENTED
- **Description:** Players can freely replace plastic fighters with tokens at any time
- **Gap:** No token replacement interface or mechanics

### 36.3 Token-to-Plastic Requirement
- **Status:** NOT IMPLEMENTED
- **Description:** Fighter tokens must be replaced with plastic pieces if no plastic fighter in system
- **Gap:** No validation system for token-plastic piece requirements

### 36.4 Token Value System
- **Status:** NOT IMPLEMENTED
- **Description:** Fighter tokens come in values of 1 and 3, can be swapped as needed
- **Gap:** No token value system or swapping mechanics

## Related Topics
- Infantry Tokens
- Producing Units

## Dependencies
- Unit production system
- Fighter unit mechanics
- Reinforcement pool management
- Token supply management
- Plastic piece tracking
- System unit validation
- Unit destruction mechanics

## Test References

### Existing Tests
- Basic fighter unit tests exist
- Fleet management tests include fighter considerations
- Some fighter technology tests (Fighter II)

### Missing Tests
- Fighter token production with plastic piece requirement
- Token-to-plastic replacement validation
- Token value swapping (1 and 3 values)
- Automatic token destruction when no plastic piece available
- Token replacement interface functionality
- Supply token management

## Implementation Files

### Core Implementation
- Fighter units exist in unit system
- Basic unit production framework
- Some fighter-specific logic in fleet management

### Missing Implementation
- Fighter token class or system
- Token value management (1 and 3 values)
- Plastic piece requirement validation
- Token-plastic replacement mechanics
- Token supply management
- Automatic token destruction system
- Token swapping interface

## Notable Implementation Details

### Well Implemented
- Basic fighter unit mechanics exist
- Unit production system has foundation
- Fleet management considers fighters
- Fighter technology upgrades (Fighter II) partially implemented

### Gaps and Issues
- No token system implementation
- Missing plastic piece requirement enforcement
- No token value system (1 and 3 values)
- Missing token-plastic validation
- No token replacement interface
- Missing automatic token destruction
- No token supply management

## Action Items

1. **Implement fighter token class** - Create token representation with value system (1 and 3)
2. **Add plastic piece requirement validation** - Ensure tokens have accompanying plastic pieces
3. **Create token-plastic replacement system** - Allow swapping between tokens and plastic pieces
4. **Implement token value swapping** - Support changing between 1 and 3 value tokens
5. **Add token supply management** - Track available tokens in supply
6. **Create automatic token validation** - Check and destroy tokens without plastic pieces
7. **Implement token replacement interface** - UI for managing token-plastic swapping
8. **Add token production mechanics** - Support using tokens during unit production
9. **Create token destruction system** - Handle automatic token removal when invalid
10. **Add comprehensive token testing** - Test all token mechanics and edge cases

## Priority Assessment
**LOW-MEDIUM** - Quality of life feature that helps with component management but not essential for core gameplay. Important for physical game simulation but lower priority than core mechanics.