# Rule 14: BLOCKADED

## Category Overview
**Priority**: High  
**Implementation Status**: Partially Implemented  
**Test Coverage**: Minimal  

Rule 14 defines the blockade mechanic, which restricts production capabilities of units when enemy ships are present in the same system without friendly ships. This is a critical strategic mechanic that affects production, unit capture, and territorial control.

## Sub-Rules Analysis

### 14.0 - Core Definition
**Raw LRR Text**: "A player's unit with 'Production' is blockaded if it is in a system that does not contain any of their ships and contains other players' ships."

**Implementation Status**: Not Implemented  
**Priority**: High  
**Details**: The core blockade detection logic is missing. Need to implement system-level checks for ship presence and production unit status.

### 14.1 - Production Restrictions
**Raw LRR Text**: "A player cannot use a blockaded unit to produce ships; that player can still use a blockaded unit to produce ground forces."

**Implementation Status**: Not Implemented  
**Priority**: High  
**Details**: Production system needs blockade validation. Ship production should be blocked while ground force production remains allowed.

### 14.2 - Unit Return Mechanism
**Raw LRR Text**: "When a player blockades another player's space dock, if the blockaded player has captured any of the blockading player's units, those units are returned to the blockading player's reinforcements."

**Implementation Status**: Not Implemented  
**Priority**: Medium  
**Details**: Requires integration with capture mechanics and automatic unit return system.

### 14.2a - Capture Prevention
**Raw LRR Text**: "While a player is blockading another player, the blockaded player cannot capture any of the blockading player's units."

**Implementation Status**: Not Implemented  
**Priority**: Medium  
**Details**: Combat system needs blockade-aware capture prevention logic.

## Related Topics
- Producing Units (Rule 67)
- Ships (Rule 78)
- Space Dock (Rule 79)
- Capture (Rule 17)
- Production (Unit Ability) (Rule 68)

## Dependencies
- **System State Management**: Ship presence detection
- **Production System**: Blockade validation in production logic
- **Combat System**: Capture mechanics integration
- **Unit Management**: Captured unit tracking and return

## Test References
- `test_unit.py`: Basic production ability tests (lines 131-142)
- **Missing**: Blockade detection tests
- **Missing**: Production restriction tests
- **Missing**: Unit return mechanism tests

## Implementation Files
- `src/ti4/units/unit.py`: Unit production abilities
- `src/ti4/game/system.py`: System state management
- `UNIT_ABILITIES_IMPLEMENTATION.md`: Production ability documentation
- **Missing**: Blockade detection system
- **Missing**: Production validation with blockade checks

## Action Items

1. **Implement Blockade Detection System**
   - Create `is_blockaded()` method for production units
   - Add system-level ship presence validation
   - Integrate with existing unit and system classes

2. **Add Production Restriction Logic**
   - Modify production system to check blockade status
   - Implement ship production blocking
   - Maintain ground force production capability

3. **Create Unit Return Mechanism**
   - Implement automatic captured unit return on blockade
   - Add integration with capture system
   - Handle reinforcement placement

4. **Add Capture Prevention Logic**
   - Modify combat system to prevent captures during blockade
   - Add blockade status checks to capture attempts
   - Ensure proper interaction with existing combat mechanics

5. **Implement Comprehensive Test Suite**
   - Add blockade detection tests
   - Test production restrictions (ships vs ground forces)
   - Test unit return mechanism
   - Test capture prevention during blockade

6. **Add Space Dock Specific Logic**
   - Handle Clan of Saar "Floating Factory" special case
   - Implement space dock destruction on blockade
   - Add faction-specific blockade rules

7. **Create System Integration**
   - Add blockade status to system state
   - Implement efficient blockade checking
   - Add UI indicators for blockaded units

8. **Add Validation and Error Handling**
   - Validate blockade conditions before production
   - Add clear error messages for blocked actions
   - Handle edge cases and faction abilities

9. **Implement Performance Optimization**
   - Cache blockade status calculations
   - Optimize ship presence queries
   - Minimize computational overhead

10. **Add Documentation and Examples**
    - Document blockade mechanics in code
    - Add usage examples for developers
    - Create integration guides for related systems