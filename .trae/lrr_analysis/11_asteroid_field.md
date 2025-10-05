# Rule 11: ASTEROID FIELD

## Category Overview
**Rule Type**: Anomaly
**Complexity**: Low
**Dependencies**: Movement, Anomalies, System Tiles
**Implementation Status**: ✅ COMPLETE

An asteroid field is an anomaly that affects movement by completely blocking ship movement through or into the system. This is one of the four types of anomalies in TI4, identified by its distinctive art and red border.

## Sub-Rules Analysis

### 11.1 Movement Restriction ✅ COMPLETE
**Raw LRR Text**: "A ship cannot move through or into an asteroid field."

**Implementation Status**: ✅ COMPLETE
**Current State**: Fully implemented with comprehensive validation
**Implementation Files**:
- `src/ti4/core/movement.py:validate_movement_with_anomalies()` - Movement blocking logic
- `src/ti4/core/constants.py:AnomalyType.ASTEROID_FIELD` - Anomaly type definition
- `src/ti4/core/system.py:has_anomaly_type()` - Asteroid field detection

**Test Coverage**:
- `test_asteroid_field_blocks_movement` (tests/test_rule_09_anomalies.py)
- `test_asteroid_field_blocks_transit` (tests/test_rule_09_anomalies.py)
- `test_movement_validation_with_asteroid_fields` (tests/test_anomaly_movement_integration.py)

**Key Requirements**: ✅ ALL IMPLEMENTED
- ✅ **Absolute Movement Block**: Ships cannot enter asteroid field systems at all
- ✅ **No Transit**: Ships cannot move through asteroid field systems to reach other destinations
- ✅ **Complete Restriction**: No exceptions or special abilities override this rule

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
- **Core Tests**: `tests/test_rule_09_anomalies.py` - Comprehensive asteroid field tests
- **Integration Tests**: `tests/test_anomaly_movement_integration.py` - Movement validation with asteroid fields
- **End-to-End Tests**: `tests/test_anomaly_integration_*.py` - Full system integration
- **Error Handling**: `tests/test_anomaly_error_handling.py` - Edge cases and error conditions

## Implementation Files
- `src/ti4/core/movement.py` - Movement validation with asteroid field blocking
- `src/ti4/core/system.py` - System anomaly type detection and management
- `src/ti4/core/constants.py` - AnomalyType.ASTEROID_FIELD definition
- `src/ti4/core/anomaly_manager.py` - Anomaly system management and effects

## Implementation Status: ✅ COMPLETE

### ✅ Completed Features
1. ✅ **Asteroid Field Detection** - Full system anomaly type tracking
2. ✅ **Movement Blocking Logic** - Complete movement restriction implementation
3. ✅ **Movement Validation Integration** - Integrated with all movement systems
4. ✅ **Comprehensive Testing** - Full test coverage for all scenarios
5. ✅ **System Tile Management** - Complete anomaly property management
6. ✅ **Path Finding Integration** - Movement validation prevents invalid paths
7. ✅ **Error Handling** - Robust error handling and validation
8. ✅ **Performance Optimization** - Efficient anomaly checking and caching

### 🔄 Future Enhancements (Low Priority)
- **Visual Indicators** - UI display of asteroid field restrictions
- **Enhanced Analytics** - Movement impact tracking and logging

## Key Implementation Details

### Movement Blocking Logic
```python
# In src/ti4/core/movement.py:validate_movement_with_anomalies()
if anomaly_type in {AnomalyType.ASTEROID_FIELD, AnomalyType.SUPERNOVA}:
    return False  # Absolute movement block
```

### Test Coverage Examples
- `test_asteroid_field_blocks_movement_into_system`
- `test_asteroid_field_blocks_movement_through_system`
- `test_asteroid_field_with_planets_still_blocks_movement`
- `test_multiple_asteroid_fields_in_path_all_blocked`
