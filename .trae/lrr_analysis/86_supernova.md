# Rule 86: SUPERNOVA

## Category Overview
**Rule Type**: Anomaly
**Complexity**: Low
**Dependencies**: Movement, Anomalies, System Tiles
**Implementation Status**: ✅ COMPLETE

A supernova is an anomaly that affects movement by completely blocking ship movement through or into the system. This is one of the four types of anomalies in TI4, functionally identical to asteroid fields in terms of movement restriction.

## Sub-Rules Analysis

### 86.1 Movement Restriction ✅ COMPLETE
**Raw LRR Text**: "A ship cannot move through or into a supernova."

**Implementation Status**: ✅ COMPLETE
**Implementation**: `src/ti4/core/movement.py:validate_movement_with_anomalies()`
**Test Coverage**: [x] Comprehensive
**Priority**: High (COMPLETED)

**Test Cases**:
- `test_supernova_blocks_movement` (tests/test_rule_09_anomalies.py)
- `test_supernova_blocks_transit` (tests/test_rule_09_anomalies.py)
- `test_movement_validation_with_supernovas` (tests/test_anomaly_movement_integration.py)

**Key Requirements**: ✅ ALL IMPLEMENTED
- ✅ **Absolute Movement Block**: Ships cannot enter supernova systems at all
- ✅ **No Transit**: Ships cannot move through supernova systems to reach other destinations
- ✅ **Complete Restriction**: No exceptions or special abilities override this rule

## Related Rules
- Rule 9: ANOMALIES (general anomaly framework)
- Rule 58: MOVEMENT (movement integration)
- Rule 11: ASTEROID FIELD (identical movement restriction behavior)

## Implementation Details

### Key Files
- `src/ti4/core/movement.py` - Movement blocking logic (same as asteroid fields)
- `src/ti4/core/constants.py` - AnomalyType.SUPERNOVA definition
- `src/ti4/core/system.py` - Supernova detection and management
- `src/ti4/core/anomaly_manager.py` - Anomaly system management

### Movement Blocking Logic
```python
# In src/ti4/core/movement.py:validate_movement_with_anomalies()
if anomaly_type in {AnomalyType.ASTEROID_FIELD, AnomalyType.SUPERNOVA}:
    return False  # Absolute movement block for both anomaly types
```

### Test Coverage
- **Core Tests**: `tests/test_rule_09_anomalies.py` - Comprehensive supernova tests
- **Integration Tests**: `tests/test_anomaly_movement_integration.py` - Movement validation
- **End-to-End Tests**: `tests/test_anomaly_integration_*.py` - Full system integration
- **Error Handling**: `tests/test_anomaly_error_handling.py` - Edge cases

## Action Items
- [x] Analyze supernova movement restrictions
- [x] Review anomaly classification system
- [x] Examine ship movement limitations
- [x] Study anomaly interaction mechanics
- [x] Investigate navigation around supernovas
- [x] **ALL COMPLETED** - Supernova rules fully implemented with comprehensive test coverage

## Implementation Status: ✅ COMPLETE
All supernova functionality has been implemented with the same robust movement blocking as asteroid fields, ensuring consistent behavior across similar anomaly types.
