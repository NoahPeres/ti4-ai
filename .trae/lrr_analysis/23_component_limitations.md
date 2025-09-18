# Rule 23: COMPONENT LIMITATIONS

## Category Overview
**Priority**: High  
**Implementation Status**: Partial  
**Core Concept**: Defines how to handle depleted game components including dice, tokens, units, and cards

## Raw LRR Text
```
23 COMPONENT LIMITATIONS
If a component type is depleted during the game, players obey the following rules:

23.1 DICE: Dice are not limited; players can roll any number of dice by rolling the same dice multiple times.

23.2 TOKENS: Tokens are limited to those included in the game, except for the following:
• Control Tokens
• Fighter Tokens  
• Trade Good Tokens
• Infantry Tokens

23.3 If any of the above tokens are depleted, players can use a suitable substitute, such as a coin or bead.

23.4 UNITS: Units are limited to those included in the game, except for fighters and ground forces.
a When a player would place a unit, if there are none of that type left in their reinforcements, that player can remove a unit from any system that does not contain one of their command tokens and place that unit in their reinforcements. A player can remove any number of their units in this way; however, any units that are removed must be placed immediately. Abilities cannot force a player to remove and place a unit in this manner.
b When producing a fighter or infantry unit, a player can use a fighter or infantry token, as appropriate, from the supply instead of a plastic piece. These tokens must be accompanied by at least one plastic piece of the same type; players can swap infantry and fighter tokens for plastic pieces at any time.

23.5 CARDS: When a deck is depleted, players shuffle the deck's discard pile and place it facedown to create a new deck.

RELATED TOPICS: Producing Units, Units
```

## Sub-Rules Analysis

### 23.1 - Dice Limitations
**Status**: ✅ Implemented  
**Implementation**: Dice rolling is handled through game mechanics without physical limitations  
**Details**: Digital implementation naturally handles unlimited dice rolls

### 23.2 - Token Limitations  
**Status**: ⚠️ Partially Implemented  
**Implementation**: Some token types tracked, but not all limitation rules enforced  
**Details**: Control tokens, fighter tokens, infantry tokens, and trade good tokens should be unlimited with substitutes allowed

### 23.3 - Token Substitutes
**Status**: ❌ Not Implemented  
**Implementation**: No substitute mechanism for depleted tokens  
**Details**: Need system to handle token depletion with suitable substitutes

### 23.4 - Unit Limitations
**Status**: ⚠️ Partially Implemented  
**Implementation**: Fleet capacity validation exists, but unit redeployment rules missing  
**Details**: 
- Unit removal from non-command token systems not implemented
- Fighter/infantry token substitution partially implemented
- Plastic piece requirements not enforced

### 23.5 - Card Deck Depletion
**Status**: ❌ Not Implemented  
**Implementation**: No deck reshuffling mechanism  
**Details**: Need to handle depleted decks by shuffling discard piles

## Related Topics
- Producing Units (Rule 67)
- Units (Rule 96)
- Fighter Tokens (Rule 36)
- Infantry Tokens (Rule 46)
- Reinforcements (Rule 72)
- Fleet Pool (Rule 37)

## Dependencies
- Unit production system
- Token management system
- Fleet capacity validation
- Command token placement tracking
- Card deck management

## Test References
**Existing Tests**:
- `test_fleet_management.py`: Fleet capacity validation tests
- `test_integration.py`: Fleet capacity integration tests
- `test_utils.py`: Fleet capacity assertion utilities

**Missing Tests**:
- Unit redeployment from systems without command tokens
- Token substitution mechanisms
- Fighter/infantry token requirements
- Card deck reshuffling
- Component limitation edge cases

## Implementation Files
**Existing**:
- `src/ti4/core/fleet.py`: FleetCapacityValidator class
- `src/ti4/core/exceptions.py`: FleetCapacityError, FleetSupplyError
- `src/ti4/core/units.py`: Unit type definitions

**Missing**:
- Component limitation manager
- Token substitution system
- Unit redeployment mechanics
- Deck management system

## Notable Implementation Details

### Well-Implemented Areas
1. **Fleet Capacity Validation**: Comprehensive system for validating fleet capacity limits
2. **Unit Type Management**: Basic unit type definitions and validation
3. **Exception Handling**: Specific exceptions for capacity and supply errors

### Implementation Gaps
1. **Unit Redeployment**: No mechanism to remove units from systems without command tokens
2. **Token Substitution**: Missing system for handling depleted token types
3. **Fighter/Infantry Tokens**: Incomplete implementation of token/plastic piece rules
4. **Deck Management**: No reshuffling mechanism for depleted card decks
5. **Component Tracking**: No system to track component depletion

## Action Items

1. **Implement Unit Redeployment System**
   - Create mechanism to remove units from systems without command tokens
   - Ensure immediate placement requirement is enforced
   - Prevent ability-forced redeployment

2. **Create Token Substitution Manager**
   - Track token supply levels
   - Implement substitute mechanism for depleted unlimited tokens
   - Handle control, fighter, infantry, and trade good token substitutes

3. **Complete Fighter/Infantry Token System**
   - Enforce plastic piece accompaniment requirements
   - Implement token-to-plastic swapping mechanics
   - Validate token placement rules

4. **Implement Deck Reshuffling System**
   - Detect depleted card decks
   - Shuffle discard piles to create new decks
   - Handle multiple deck types (exploration, relics, etc.)

5. **Create Component Limitation Manager**
   - Central system to track all component limitations
   - Coordinate between different limitation types
   - Provide unified interface for limitation checks

6. **Add Comprehensive Testing**
   - Unit redeployment scenarios
   - Token substitution edge cases
   - Fighter/infantry token validation
   - Deck depletion and reshuffling

7. **Implement Component Supply Tracking**
   - Track available components in supply
   - Monitor component depletion states
   - Trigger appropriate limitation responses

8. **Create Reinforcement Management**
   - Track units in player reinforcements
   - Handle reinforcement depletion scenarios
   - Coordinate with unit redeployment system

9. **Add Limitation Validation**
   - Validate component limitation compliance
   - Prevent invalid component usage
   - Provide clear error messages for violations

10. **Document Component Limitation Rules**
    - Create comprehensive documentation
    - Include examples of limitation scenarios
    - Provide guidance for edge cases