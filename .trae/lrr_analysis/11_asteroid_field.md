# Rule 11: ASTEROID FIELD

## Category Overview
**Rule Type**: Anomaly
**Complexity**: Low
**Dependencies**: Movement, Anomalies, System Tiles
**Implementation Status**: 🔴 Not Implemented

An asteroid field is an anomaly that affects movement by completely blocking ship movement through or into the system. This is one of the four types of anomalies in TI4, identified by its distinctive art and red border.

## Sub-Rules Analysis

### 11.1 Movement Restriction 🔴 HIGH PRIORITY
**Raw LRR Text**: "A ship cannot move through or into an asteroid field."

**Implementation Status**: 🔴 Not Implemented
**Current State**: `AnomalyRule` class exists but returns `True` for all movement checks
**Missing Elements**:
- Asteroid field detection in systems
- Movement blocking logic for asteroid fields
- Integration with movement validation system

**Key Requirements**:
- **Absolute Movement Block**: Ships cannot enter asteroid field systems at all
- **No Transit**: Ships cannot move through asteroid field systems to reach other destinations
- **Complete Restriction**: No exceptions or special abilities override this rule

## Related Topics
- **Anomalies**: General anomaly system and identification
- **Movement**: Ship movement rules and validation
- **System Tiles**: System identification and properties

## Dependencies Summary

### Critical Dependencies
1. **Anomaly Detection System** - Identifying asteroid fields in systems
2. **Movement Validation** - Blocking movement into/through asteroid fields
3. **System Properties** - Tracking which systems contain asteroid fields
4. **Movement Rules Engine** - Integration with movement restriction logic

### Related Systems
1. **Galaxy Management** - System tile placement and properties
2. **Tactical Action** - Movement step validation
3. **Path Finding** - Route calculation around blocked systems
4. **Game State** - Tracking system anomaly types

## Test References
- **No specific tests found** - Asteroid field movement restrictions are not currently tested
- `test_movement.py` - Contains general movement validation tests
- `test_tactical_action.py` - Contains movement plan validation tests

## Implementation Files
- `src/ti4/core/movement_rules.py` - `AnomalyRule` class (stub implementation)
- `src/ti4/core/movement.py` - Movement validation system
- `src/ti4/actions/tactical_action.py` - Movement plan validation

## Action Items

1. **Implement Asteroid Field Detection** 🔴 HIGH
   - Add asteroid field identification to system properties
   - Create system anomaly type tracking
   - Integrate with galaxy management system

2. **Implement Movement Blocking Logic** 🔴 HIGH
   - Update `AnomalyRule.can_move()` to block asteroid field movement
   - Add asteroid field checks to movement validation
   - Ensure both "into" and "through" movement is blocked

3. **Integrate with Movement Validation System** 🔴 HIGH
   - Update `MovementValidator` to check for asteroid fields
   - Add asteroid field validation to tactical action movement
   - Ensure path finding avoids asteroid fields

4. **Add Comprehensive Asteroid Field Testing** 🔴 HIGH
   - Test movement blocking into asteroid fields
   - Test movement blocking through asteroid fields
   - Test path finding around asteroid fields
   - Test edge cases and error handling

5. **Update System Tile Management** 🟡 MEDIUM
   - Add asteroid field properties to system tiles
   - Implement anomaly type detection from tile art/data
   - Create system anomaly query methods

6. **Implement Path Finding Integration** 🟡 MEDIUM
   - Update route calculation to avoid asteroid fields
   - Add alternative path finding when direct routes blocked
   - Optimize movement planning around obstacles

7. **Add Visual Indicators** 🟢 LOW
   - Display asteroid field restrictions in UI
   - Show blocked movement paths visually
   - Add asteroid field identification in system display

8. **Create Asteroid Field Documentation** 🟢 LOW
   - Document asteroid field mechanics
   - Add examples of movement restrictions
   - Create developer guide for anomaly implementation

9. **Optimize Performance** 🟢 LOW
   - Efficient asteroid field checking
   - Cache anomaly properties for systems
   - Minimize movement validation overhead

10. **Add Analytics and Logging** 🟢 LOW
    - Track asteroid field impact on movement
    - Log blocked movement attempts
    - Add debugging information for movement restrictions
