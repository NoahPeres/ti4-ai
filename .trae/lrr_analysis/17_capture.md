# Rule 17: CAPTURE

## Category Overview
**Priority**: HIGH  
**Implementation Status**: NOT IMPLEMENTED  
**Complexity**: HIGH  

Rule 17 defines the capture mechanics for units, including placement on faction sheets, return conditions, and blockade interactions. This is a critical combat and strategic mechanic that affects unit availability and player resources.

## Raw LRR Text

### 17 CAPTURE
Some abilities instruct a player to capture a unit, preventing the unit's original owner from using it.

**17.1** If a player captures a non-fighter ship or mech, they place it on their faction sheet. When such a unit is returned, it is placed into the reinforcements of the original owner.

**17.2** A captured non-fighter ship or mech is returned under the following circumstances:
- b. If an ability instructs the capturing player to return the unit as part of an ability's cost.
- c. If the player whose unit was captured blockades a space dock of the player who captured the unit.

**17.3** If a player captures a fighter or infantry, it is placed in its reinforcements instead of on the capturing player's faction sheet; the capturing player places a fighter or infantry token from the supply on their faction sheet instead.

**17.4** Captured fighters and infantry do not belong to any player and are returned only when an ability instructs the capturing player to do so.
- a. Captured fighters and infantry cannot be returned as part of a transaction.
- b. Captured fighters and infantry are not returned as the result of a blockade.
- c. When a captured fighter or infantry is returned, it is placed in the supply.

**17.5** While a unit is captured, it cannot be produced or placed by its original owner until it is returned.

**17.6** If one or more of a player's space docks is being blockaded, that player cannot capture units from the blockading players.

## Sub-Rules Analysis

### 17.0 - Core Capture Concept
- **Status**: NOT IMPLEMENTED
- **Description**: Basic capture mechanic preventing original owner from using unit
- **Implementation Needed**: Capture system, unit ownership tracking

### 17.1 - Non-Fighter Ship/Mech Capture
- **Status**: NOT IMPLEMENTED  
- **Description**: Captured ships/mechs go to faction sheet, return to reinforcements
- **Implementation Needed**: Faction sheet storage, unit return mechanics

### 17.2 - Return Conditions for Ships/Mechs
- **Status**: NOT IMPLEMENTED
- **Description**: Units returned via abilities or blockade counter-capture
- **Implementation Needed**: Ability cost system, blockade capture interaction

### 17.3 - Fighter/Infantry Capture
- **Status**: NOT IMPLEMENTED
- **Description**: Captured fighters/infantry become tokens on faction sheet
- **Implementation Needed**: Token system, reinforcement placement

### 17.4 - Fighter/Infantry Return Rules
- **Status**: NOT IMPLEMENTED
- **Description**: Special return rules for captured fighters/infantry
- **Implementation Needed**: Token return system, supply placement

### 17.5 - Production Restriction
- **Status**: NOT IMPLEMENTED
- **Description**: Captured units cannot be produced by original owner
- **Implementation Needed**: Production validation, unit availability tracking

### 17.6 - Blockade Capture Restriction
- **Status**: NOT IMPLEMENTED
- **Description**: Blockaded players cannot capture from blockading players
- **Implementation Needed**: Blockade state checking, capture validation

## Related Topics
- Blockaded (Rule 14)
- Fighter Tokens
- Ground Combat
- Infantry Tokens  
- Space Combat

## Dependencies
- **Faction Sheet System**: Storage for captured units
- **Blockade System**: Blockade state tracking and validation
- **Combat System**: Integration with capture-causing abilities
- **Token System**: Fighter/infantry token management
- **Production System**: Validation against captured units
- **Unit Ownership System**: Tracking original vs current ownership

## Test References

### Existing Tests
- No existing tests found for capture mechanics

### Missing Tests Needed
- `test_capture_non_fighter_ship.py` - Ship capture to faction sheet
- `test_capture_mech.py` - Mech capture mechanics
- `test_capture_fighter_infantry.py` - Token-based capture
- `test_captured_unit_return.py` - Return conditions and mechanics
- `test_blockade_capture_interaction.py` - Blockade preventing capture
- `test_production_restriction.py` - Cannot produce captured units
- `test_ability_cost_return.py` - Returning units as ability costs
- `test_capture_validation.py` - Capture attempt validation
- `test_faction_sheet_storage.py` - Captured unit storage
- `test_token_management.py` - Fighter/infantry token handling

## Implementation Files

### Existing Files
- No existing capture-related implementation found

### Missing Files Needed
- `src/ti4/core/capture.py` - Core capture mechanics
- `src/ti4/core/faction_sheet.py` - Faction sheet management
- `src/ti4/mechanics/capture_validator.py` - Capture validation logic
- `src/ti4/mechanics/blockade_capture.py` - Blockade-capture interactions
- `src/ti4/core/token_manager.py` - Fighter/infantry token system
- `src/ti4/mechanics/unit_return.py` - Unit return mechanics

## Action Items

1. **Implement Core Capture System** - Create capture mechanics with unit ownership transfer
2. **Create Faction Sheet Management** - Storage system for captured non-fighter ships and mechs
3. **Implement Token System** - Fighter/infantry token management for captures
4. **Add Blockade-Capture Integration** - Prevent capture when blockaded, enable counter-capture
5. **Create Unit Return Mechanics** - Return captured units under specified conditions
6. **Implement Production Restrictions** - Prevent production of captured units by original owner
7. **Add Capture Validation** - Validate capture attempts based on game state
8. **Create Ability Cost Integration** - Support returning captured units as ability costs
9. **Implement Comprehensive Testing** - Full test coverage for all capture scenarios
10. **Add Combat Integration** - Connect capture mechanics with combat resolution system