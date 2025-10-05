# LRR Rule Analysis: Section 9 - ANOMALIES

## Category Overview
Anomalies are special system tiles with unique rules that affect movement and gameplay. There are four types: asteroid fields, nebulae, supernovas, and gravity rifts. Each anomaly type has distinct effects on ship movement and combat, and some may contain planets while still maintaining their anomaly properties.

## Sub-Rules Analysis

### 9.1 Anomaly Identification 🟡 MEDIUM
**Raw LRR Text**: "An anomaly is identified by a red border located on the tile's corners."

**Implementation Status**: ⚠️ PARTIAL
- **Code**: `System.is_anomaly()` method in `src/ti4/core/system.py`
- **Tests**: `test_system_anomaly_identification` (tests/test_rule_09_anomalies.py)
- **Assessment**: Logical identification implemented, visual borders not implemented
- **Priority**: MEDIUM
- **Dependencies**: Requires system tile visual properties
- **Notes**: Red border is the visual indicator for anomaly tiles - logical detection works

### 9.2 Anomaly Types 🟢 COMPLETE
**Raw LRR Text**: "There are four types of anomalies: asteroid fields, nebulae, supernovas, and gravity rifts."

**Implementation Status**: ✅ COMPLETE
- **Code**: `AnomalyType` enum in `src/ti4/core/constants.py`, full implementation in `AnomalyManager`
- **Tests**: Comprehensive test coverage across multiple test files
- **Assessment**: All four anomaly types fully implemented with effects
- **Priority**: HIGH (COMPLETED)
- **Dependencies**: Complete
- **Notes**: All four distinct anomaly types implemented with correct effects

### 9.2a Anomalies with Planets 🟢 COMPLETE
**Raw LRR Text**: "Some anomalies contain planets; those systems are still anomalies."

**Implementation Status**: ✅ COMPLETE
- **Code**: `System` class supports both planets and anomalies simultaneously
- **Tests**: `test_anomaly_system_with_planets` (tests/test_rule_09_anomalies.py)
- **Assessment**: Dual nature systems (anomaly + planets) fully supported
- **Priority**: MEDIUM (COMPLETED)
- **Dependencies**: Complete
- **Notes**: Systems can be both anomalies and contain planets simultaneously

### 9.3 Anomaly Art Identification 🟢 LOW
**Raw LRR Text**: "Each type of anomaly is identified by its art, as follows: [Asteroid Field, Supernova, Nebula, Gravity Rift artwork descriptions]"

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No artwork identification system
- **Tests**: No art-based identification tests
- **Assessment**: Visual art identification not implemented (not needed for core logic)
- **Priority**: LOW
- **Dependencies**: Requires asset management and visual identification system
- **Notes**: Each anomaly has distinct artwork for identification

### 9.4 Ability-Created Anomalies 🟢 COMPLETE
**Raw LRR Text**: "Abilities can cause a system tile to become an anomaly; that system tile is an anomaly in addition to its other properties."

**Implementation Status**: ✅ COMPLETE
- **Code**: `AnomalyManager.add_anomaly_to_system()` and `convert_system_to_anomaly_type()`
- **Tests**: `test_dynamic_anomaly_assignment` (tests/test_dynamic_anomaly_assignment.py)
- **Assessment**: Dynamic anomaly transformation fully implemented
- **Priority**: MEDIUM (COMPLETED)
- **Dependencies**: Complete
- **Notes**: Systems can gain anomaly properties through game effects

### 9.5 Multiple Anomaly Types 🟢 COMPLETE
**Raw LRR Text**: "Abilities can cause a system to be two different anomalies; that system has the properties of both anomalies."

**Implementation Status**: ✅ COMPLETE
- **Code**: `System.get_anomaly_types()` returns list, effects stack properly
- **Tests**: `test_multiple_anomaly_types_per_system` (tests/test_dynamic_anomaly_assignment.py)
- **Assessment**: Stacking anomaly effects fully implemented
- **Priority**: MEDIUM (COMPLETED)
- **Dependencies**: Complete
- **Notes**: Systems can have multiple anomaly types simultaneously with combined effects

## Related Anomaly Types (Cross-References)

### Asteroid Field (Rule 11) 🟢 COMPLETE
**Effect**: "A ship cannot move through or into an asteroid field."
- **Implementation Status**: ✅ COMPLETE
- **Priority**: HIGH (COMPLETED)
- **Implementation**: `src/ti4/core/movement.py:validate_movement_with_anomalies()`
- **Tests**: `test_asteroid_field_blocks_movement` (tests/test_rule_09_anomalies.py)

### Nebula (Rule 59) 🟢 COMPLETE
**Effects**:
- Ships can only move into nebula if it's the active system
- Ships in nebula have move value of 1
- Defender gets +1 to combat rolls in nebula
- **Implementation Status**: ✅ COMPLETE
- **Priority**: HIGH (COMPLETED)
- **Implementation**: Movement validation in `movement.py`, combat effects in `combat.py`
- **Tests**: `test_nebula_movement_restrictions`, `test_nebula_combat_effects` (multiple test files)

### Supernova (Rule 86) 🟢 COMPLETE
**Effect**: "A ship cannot move through or into a supernova."
- **Implementation Status**: ✅ COMPLETE
- **Priority**: HIGH (COMPLETED)
- **Implementation**: `src/ti4/core/movement.py:validate_movement_with_anomalies()`
- **Tests**: `test_supernova_blocks_movement` (tests/test_rule_09_anomalies.py)

### Gravity Rift (Rule 41) 🟢 COMPLETE
**Effects**:
- Ships moving out/through get +1 move value
- Roll die when exiting: 1-3 destroys ship
- Can affect same ship multiple times
- **Implementation Status**: ✅ COMPLETE
- **Priority**: HIGH (COMPLETED)
- **Implementation**: `src/ti4/core/movement.py`, `src/ti4/core/movement_rules.py`
- **Tests**: Comprehensive gravity rift test suite (tests/test_rule_09_anomalies.py)

## Dependencies Summary

### Critical Dependencies
- **System Tile System**: Base system for anomaly properties (Rule 88)
- **Movement System**: All anomalies affect movement in some way (Rule 58)
- **Combat System**: Nebulae affect combat rolls (Rule 78)
- **Ability System**: For dynamic anomaly creation (Rule 1)
- **Unit Destruction**: Gravity rifts can destroy units

### Related Systems
- **Planet System**: Some anomalies contain planets (Rule 64)
- **Active System**: Nebulae interact with active system rules (Rule 5)
- **Visual Assets**: Anomaly identification through artwork
- **Effect Stacking**: Multiple anomaly types on same system
- **Property Modification**: Dynamic anomaly assignment

## Test References
- **Core System**: `tests/test_rule_09_anomalies.py` - Comprehensive anomaly rule tests
- **Integration Tests**: `tests/test_anomaly_integration_*.py` - End-to-end anomaly testing
- **Movement Integration**: `tests/test_anomaly_movement_integration.py` - Movement + anomaly interactions
- **Combat Integration**: `tests/test_nebula_combat_*.py` - Nebula combat effect tests
- **Performance Tests**: `tests/test_anomaly_performance_validation.py` - Scalability testing
- **Error Handling**: `tests/test_anomaly_error_handling.py` - Edge cases and error conditions

## Implementation Status: ✅ COMPLETE
All core anomaly functionality has been implemented with comprehensive test coverage:

### ✅ Completed Features
1. ✅ **Core anomaly system** with all four anomaly types
2. ✅ **Movement restriction validation** for asteroid fields and supernovas
3. ✅ **Nebula movement rules** (active system only, move value 1)
4. ✅ **Nebula combat effects** (+1 defender bonus)
5. ✅ **Gravity rift mechanics** (movement bonus and destruction risk with correct stacking)
6. ✅ **Dynamic anomaly assignment** system for abilities
7. ✅ **Anomaly stacking support** for multiple types per system
8. ✅ **Planet system integration** for anomalies containing planets
9. ✅ **Comprehensive test suite** for all anomaly types and interactions

### 🔄 Future Enhancements (Low Priority)
- **Visual identification** system for anomaly recognition (artwork-based)
- **Enhanced UI integration** for anomaly visualization
