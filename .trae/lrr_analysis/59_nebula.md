# LRR Rule 59: NEBULA

## Rule Category Overview
A nebula is an anomaly that affects movement and combat.

## Sub-Rules Analysis

### 59.1 Nebula Movement Restriction
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Implementation**: `src/ti4/core/movement.py:validate_movement_with_anomalies()`
- **Test Cases**:
  - `test_nebula_movement_only_into_active_system` (tests/test_rule_09_anomalies.py)
  - `test_nebula_blocks_movement_when_not_active` (tests/test_anomaly_movement_integration.py)
- **Notes**: A ship can only move into a nebula if it is the active system. **CORRECTLY IMPLEMENTED** with active system validation.

### 59.2 Move Value in Nebula
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Implementation**: `src/ti4/core/movement.py:calculate_effective_movement_range()`
- **Test Cases**:
  - `test_nebula_sets_move_value_to_one` (tests/test_rule_09_anomalies.py)
  - `test_nebula_movement_value_override` (tests/test_anomaly_movement_integration.py)
- **Notes**: A ship that begins the "Movement" step of a tactical action in a nebula treats its move value as "1" for the duration of that step. **CORRECTLY IMPLEMENTED**.

### 59.3 Combat in Nebula
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Implementation**: `src/ti4/core/combat.py` and `src/ti4/core/anomaly_manager.py:get_combat_modifiers()`
- **Test Cases**:
  - `test_nebula_combat_defender_bonus` (tests/test_nebula_combat_effects.py)
  - `test_nebula_combat_integration` (tests/test_nebula_combat_integration.py)
- **Notes**: If a space combat occurs in a nebula, the defender applies +1 to each combat roll of their ships during that combat. **CORRECTLY IMPLEMENTED**.

## Overall Implementation Status
- **Current State**: Complete
- **Estimated Effort**: Large (completed)
- **Dependencies**: Movement system, combat system, active system tracking
- **Blockers**: None

## Notes
- Rule 59 has 3 sub-rules - ALL IMPLEMENTED
- All nebula effects properly integrated with movement and combat systems
- Comprehensive test coverage ensures correct behavior in all scenarios
- Active system validation correctly implemented (uses destination as default when not specified)

## Related Rules
- Rule 9: ANOMALIES (general anomaly framework)
- Rule 58: MOVEMENT (movement integration)
- Rule 78: SPACE COMBAT (combat bonus integration)
- Rule 5: ACTIVE SYSTEM (active system validation)

## Implementation Details

### Key Files
- `src/ti4/core/movement.py` - Movement restrictions and move value override
- `src/ti4/core/combat.py` - Combat bonus application
- `src/ti4/core/anomaly_manager.py` - Nebula effect management
- `src/ti4/core/constants.py` - AnomalyType.NEBULA definition

### Test Coverage
- `tests/test_rule_09_anomalies.py` - Core nebula rule tests
- `tests/test_nebula_combat_*.py` - Combat effect tests
- `tests/test_anomaly_movement_integration.py` - Movement integration tests
- `tests/test_anomaly_integration_*.py` - End-to-end integration tests

## Action Items
- [x] Analyze current implementation
- [x] Identify gaps
- [x] Create implementation plan
- [x] Write tests
- [x] Implement missing functionality
- [x] **ALL COMPLETED** - Nebula rules fully implemented with comprehensive test coverage
