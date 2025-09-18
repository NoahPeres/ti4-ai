# Rule 53: LEGENDARY PLANETS

## Category Overview
**Rule Type**: Planet Mechanics  
**Complexity**: Medium  
**Implementation Priority**: Medium  
**Dependencies**: Planet Control, Planet Cards, Abilities System  

## Raw LRR Text
From `lrr.txt` section 53:

**53** LEGENDARY PLANETS  
Legendary planets grant the player that controls them unique, planet-specific abilities.

**53.1** A legendary planet is indicated by the legendary planet icon.

**53.2** When a player gains control of a legendary planet, they also place its legendary planet ability card in their play area.
- If a player gains control of a legendary planet ability card from the deck, it is readied.
- If a player gains control of an exhausted legendary planet ability card, it remains exhausted.

**53.3** Players can use the abilities on the legendary planet ability cards in their play area.

**53.4** If a legendary planet's planet card is purged, its corresponding legendary planet ability card is also purged.

**Related Topics**: Planets

## Sub-Rules Analysis

### 53.1 - Legendary Planet Icon
- **Status**: ❌ Not Implemented
- **Location**: No legendary planet icon system found
- **Test Coverage**: None found
- **Implementation Notes**: Visual identification system missing

### 53.2 - Legendary Planet Ability Cards
- **Status**: ❌ Not Implemented
- **Location**: No legendary planet ability card system found
- **Test Coverage**: None found
- **Implementation Notes**: Ability card management system missing

### 53.3 - Using Legendary Planet Abilities
- **Status**: ❌ Not Implemented
- **Location**: No legendary planet ability usage system found
- **Test Coverage**: None found
- **Implementation Notes**: Ability activation system missing

### 53.4 - Purging Legendary Planet Cards
- **Status**: ❌ Not Implemented
- **Location**: No purge interaction system found
- **Test Coverage**: None found
- **Implementation Notes**: Purge mechanics not connected to legendary planets

## Related Topics
- **Rule 64**: PLANETS (basic planet mechanics)
- **Rule 1**: ABILITIES (ability system framework)
- **Rule 12**: ATTACH (card attachment mechanics)
- **Rule 34**: EXHAUSTED (exhausted/readied state)
- **Rule 69**: PURGE (purge mechanics)
- **Rule 17**: CONTROL (planet control mechanics)

## Dependencies
- **Planet System**: Basic planet control and management
- **Abilities Framework**: System for planet-specific abilities
- **Card Management**: Legendary planet ability cards
- **Exhausted/Readied**: State management for ability cards
- **Purge System**: Card removal mechanics
- **Visual Indicators**: Legendary planet icon system

## Test References
### Limited Test Coverage Found:
- `test_planet.py`: Basic planet structure testing
  - Planet creation with resources and influence
  - Planet control tracking
  - Unit placement on planets
  - Basic planet mechanics

### Test Scenarios Covered:
1. **Basic Planet Creation**: Planets with resources and influence
2. **Control Tracking**: Planet control by players
3. **Unit Management**: Ground forces on planets
4. **Control Changes**: Setting planet control

### Missing Test Scenarios:
1. **Legendary Planet Identification**: No tests for legendary planet icons
2. **Ability Card Management**: No tests for legendary planet ability cards
3. **Ability Usage**: No tests for using legendary planet abilities
4. **Card States**: No tests for readied/exhausted ability cards
5. **Purge Interaction**: No tests for purging legendary planet cards
6. **Control Integration**: No tests for gaining legendary abilities on control

## Implementation Files
### Core Implementation:
- `src/ti4/core/planet.py`: Basic Planet class with resources, influence, and control
- Basic planet structure exists but no legendary planet features

### Supporting Files:
- Planet control mechanics
- Unit placement on planets

### Missing Implementation:
- Legendary planet identification system
- Legendary planet ability card system
- Ability card management (readied/exhausted states)
- Legendary planet ability usage
- Purge interaction with legendary planets
- Visual legendary planet icon system

## Notable Implementation Details

### Strengths:
1. **Basic Planet Structure**: Solid foundation with Planet class
2. **Control System**: Planet control tracking implemented
3. **Unit Management**: Ground forces can be placed on planets
4. **Resource System**: Planets have resources and influence values

### Areas Needing Attention:
1. **Legendary Features**: No legendary planet-specific features implemented
2. **Ability Cards**: No legendary planet ability card system
3. **Visual Indicators**: No legendary planet icon system
4. **Ability Framework**: No planet-specific ability system
5. **State Management**: No readied/exhausted state for ability cards
6. **Purge Integration**: No purge mechanics for legendary planets

### Architecture Quality:
- **Good**: Basic planet structure and control system
- **Needs Work**: Legendary planet features entirely missing
- **Missing**: Ability card system and visual indicators

## Action Items

### High Priority:
1. **Create Legendary Planet System**: Identify and mark legendary planets
2. **Implement Ability Cards**: Legendary planet ability card management
3. **Add Ability Usage**: System for using legendary planet abilities

### Medium Priority:
4. **Visual Indicators**: Legendary planet icon system
5. **State Management**: Readied/exhausted states for ability cards
6. **Control Integration**: Automatic ability card gain on planet control

### Low Priority:
7. **Purge Integration**: Connect purge mechanics to legendary planets
8. **Legendary Planet Library**: Implement specific legendary planet abilities
9. **UI Integration**: Visual feedback for legendary planet abilities

## Priority Assessment
**Overall Priority**: Medium - Legendary planets add strategic depth but are not core mechanics

**Implementation Status**: Not Started (5%)
- Basic planet structure: ✅ Complete
- Planet control: ✅ Complete
- Legendary planet identification: ❌ Missing
- Ability card system: ❌ Missing
- Ability usage: ❌ Missing
- Visual indicators: ❌ Missing

**Recommended Focus**: 
1. Design legendary planet identification system
2. Create legendary planet ability card framework
3. Implement ability usage mechanics
4. Add visual legendary planet indicators

The basic planet system provides a good foundation, but legendary planet features are completely missing. This represents a significant gap in planet mechanics, though it's not as critical as core systems like combat or movement. The implementation would require extending the existing planet system with ability card management and visual identification features.