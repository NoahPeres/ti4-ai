# Rule 47: LEGENDARY PLANETS

## Category Overview
**Rule Type**: Core Mechanics - Planet Special Abilities
**Complexity**: Medium
**Dependencies**: High (Planets, Control, Abilities, Exploration)
**Implementation Priority**: Medium

## Raw LRR Text
```
53 LEGENDARY PLANETS
Legendary planets grant the player that controls them unique, planet-specific abilities.

53.1 A legendary planet is indicated by the legendary planet icon.

53.2 When a player gains control of a legendary planet, they also place its legendary planet ability card in their play area.
a	If a player gains control of a legendary planet ability card from the deck, it is readied.
b  If a player gains control of an exhausted legendary planet ability card, it remains exhausted.

53.3 Players can use the abilities on the legendary planet ability cards in their play area.

53.4 If a legendary planet's planet card is purged, its corresponding legendary planet ability card is also purged.

RELATED TOPICS: Planets
```

## Sub-Rules Analysis

### 53.1 - Legendary Planet Identification
- **Status**: ❌ Not Implemented
- **Description**: Legendary planets identified by special icon
- **Implementation Need**: Visual/data representation of legendary planet icon
- **Priority**: Medium

### 53.2 - Legendary Planet Ability Cards
- **Status**: ❌ Not Implemented
- **Description**: Gaining control grants corresponding ability card
- **Implementation Need**:
  - Legendary planet ability card system
  - Automatic card placement when gaining control
  - Readied/exhausted state tracking
- **Priority**: High

### 53.3 - Using Legendary Planet Abilities
- **Status**: ❌ Not Implemented
- **Description**: Players can use abilities from cards in play area
- **Implementation Need**:
  - Ability activation system for legendary planets
  - Play area management for ability cards
- **Priority**: High

### 53.4 - Legendary Planet Card Purging
- **Status**: ❌ Not Implemented
- **Description**: Purging planet card also purges ability card
- **Implementation Need**: Linked purging system between planet and ability cards
- **Priority**: Medium

## Related Topics
- **Planets (64)**: Base planet mechanics and control
- **Control**: Planet control mechanics
- **Abilities**: General ability resolution system
- **Exhausted (34)**: Card exhaustion mechanics
- **Purge**: Card removal mechanics

## Dependencies
- Planet control system must be implemented
- General ability system framework
- Card state management (readied/exhausted)
- Play area management system

## Test References
**Current Test Coverage**: ❌ None Found
- No specific tests for legendary planet mechanics found
- No tests for legendary planet ability cards
- No tests for legendary planet icon identification

**Missing Test Areas**:
- Legendary planet identification
- Ability card placement when gaining control
- Ability card state management (readied/exhausted)
- Using legendary planet abilities
- Linked purging of planet and ability cards

## Implementation Files
**Core Files**:
- `src/ti4/core/planet.py` - Basic planet structure (no legendary support)

**Missing Implementation Areas**:
- Legendary planet ability card system
- Legendary planet icon/identification system
- Play area management for ability cards
- Ability activation for legendary planets

## Notable Implementation Details

### Current Planet Implementation
- Basic Planet class with name, resources, influence
- Control tracking via `controlled_by` field
- Unit placement support
- **Missing**: Legendary planet support, ability card system

### Key Implementation Gaps
1. **Legendary Planet Identification**: No system to mark planets as legendary
2. **Ability Card System**: No legendary planet ability cards implemented
3. **Play Area Management**: No system for managing ability cards in play area
4. **Linked Card Management**: No system for linking planet cards to ability cards

## Action Items

### High Priority
1. **Implement Legendary Planet Ability Card System**
   - Create ability card data structure
   - Implement automatic card placement when gaining control
   - Add readied/exhausted state tracking

2. **Add Legendary Planet Support to Planet Class**
   - Add legendary planet identification
   - Link to corresponding ability cards
   - Implement ability activation system

### Medium Priority
3. **Implement Play Area Management**
   - System for managing ability cards in play area
   - Ability usage from play area cards

4. **Add Linked Purging System**
   - Purge ability cards when planet cards are purged
   - Maintain consistency between linked cards

### Low Priority
5. **Add Comprehensive Testing**
   - Test legendary planet identification
   - Test ability card placement and state management
   - Test ability usage and purging mechanics

## Priority Assessment
**Overall Priority**: Medium
- Legendary planets add strategic depth but are not core to basic gameplay
- Implementation requires significant new systems (ability cards, play area management)
- Should be implemented after core planet and ability systems are stable
- Important for complete game experience but not blocking for basic functionality

**Implementation Complexity**: High
- Requires new ability card system
- Complex state management between planet and ability cards
- Integration with existing planet and ability systems needed
