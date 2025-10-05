# LRR Rule 41: GRAVITY RIFT

## Rule Category Overview
A gravity rift is an anomaly that affects movement.

## Sub-Rules Analysis

### 41.1 Movement Bonus
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Test Cases**:
  - `test_gravity_rift_movement_bonus_single_system` (tests/test_rule_09_anomalies.py)
  - `test_gravity_rift_movement_bonus_stacking` (tests/test_rule_09_anomalies.py)
  - `test_movement_range_with_gravity_rift_bonus` (tests/test_anomaly_movement_integration.py)
- **Implementation**: `src/ti4/core/movement.py:calculate_effective_movement_range()`
- **Notes**: A ship that will move out of or through a gravity rift at any time during its movement, applies +1 to its move value. This can allow a ship to reach the active system from farther away than it normally could. **CORRECTLY IMPLEMENTED**: Bonuses stack for each gravity rift encountered in the path.

### 41.2 Exit Risk
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Test Cases**:
  - `test_gravity_rift_destruction_on_low_roll` (tests/test_anomaly_error_handling.py)
  - `test_gravity_rift_destruction_survival_on_high_roll` (tests/test_anomaly_error_handling.py)
  - `test_gravity_rift_destruction_roll_normalization` (tests/test_rule_09_anomalies.py)
- **Implementation**: `src/ti4/core/movement_rules.py:check_gravity_rift_destruction()` and `apply_gravity_rift_destruction()`
- **Notes**: For each ship that would move out of or through a gravity rift, one die is rolled immediately before it exits the gravity rift system; on a result of 1-3, that ship is removed from the board. Dice are not rolled for units that are being transported by ships that have capacity. Units that are being transported are removed from the board if the ship transporting them is removed from the board. Units that are removed are returned to the player's reinforcements.

### 41.3 Multiple Effects
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: Medium
- **Test Cases**:
  - `test_gravity_rift_multiple_effects_same_movement` (tests/test_rule_09_anomalies.py)
  - `test_gravity_rift_movement_bonus_stacking` (tests/test_rule_09_anomalies.py)
- **Implementation**: Handled by path-based bonus calculation in movement.py
- **Notes**: A gravity rift can affect the same ship multiple times during a single movement. **IMPLEMENTED**: Each gravity rift in the path provides +1 movement and requires destruction roll.

### 41.4 Multiple Rifts
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Basic
- **Priority**: Low
- **Test Cases**:
  - `test_system_with_multiple_gravity_rifts` (tests/test_rule_09_anomalies.py)
- **Implementation**: `src/ti4/core/system.py:has_anomaly_type()` treats multiple instances as single anomaly
- **Notes**: A system that contains multiple gravity rifts is treated as a single gravity rift. **IMPLEMENTED**: System anomaly checking handles this correctly.

## Overall Implementation Status
- **Current State**: Complete
- **Estimated Effort**: Large (completed)
- **Dependencies**: Movement system, dice rolling, anomaly management
- **Blockers**: None

## Notes
- **CRITICAL CORRECTION**: CodeRabbit incorrectly suggested removing gravity rift bonus stacking. Rule 41.1 explicitly states bonuses apply for moving "out of OR THROUGH" gravity rifts, meaning stacking is correct.
- All sub-rules are fully implemented with comprehensive test coverage
- Roll normalization (0-9 to 1-10) properly handles dice system integration
- Movement bonus calculation correctly stacks for each gravity rift in the path

## Related Rules
- Rule 4: ANOMALIES
- Rule 57: MOVEMENT

## Action Items
- [ ] Analyze current implementation
- [ ] Identify gaps
- [ ] Create implementation plan
- [ ] Write tests
- [ ] Implement missing functionality
