# Rule 77: SPACE CANNON (UNIT ABILITY)

## Category Overview
Units that have the "Space Cannon" ability can use it during two different steps of a player's tactical action.

## Sub-Rules Analysis

### 77.1 - Space Cannon Offense
- **Note**: During "Space Cannon Offense" step of tactical action, player can use Space Cannon abilities of units in active system
- **Implementation Status**: ✅ IMPLEMENTED
- **Test Coverage**: `test_space_cannon_offense_basic`, `test_space_cannon_offense_multiple_units`

### 77.2 - Space Cannon Defense
- **Note**: During "Space Cannon Defense" step of tactical action, opponent can use Space Cannon abilities of units in active system
- **Implementation Status**: ✅ IMPLEMENTED
- **Test Coverage**: `test_space_cannon_defense_basic`, `test_space_cannon_defense_multiple_units`

### 77.3 - Hit Assignment
- **Note**: Hits produced by Space Cannon abilities must be assigned to ships in space area of active system
- **Implementation Status**: ✅ IMPLEMENTED
- **Test Coverage**: `test_space_cannon_hit_assignment`, `test_space_cannon_no_valid_targets`

### 77.3c - PDS II Adjacent Systems
- **Note**: PDS units with PDS II upgrade can use Space Cannon ability against ships in systems adjacent to PDS unit's system
- **Implementation Status**: ✅ IMPLEMENTED
- **Test Coverage**: `test_space_cannon_pds_ii_adjacent_systems`

### 77.4 - PDS Range
- **Note**: PDS unit can use Space Cannon ability against ships in systems adjacent to PDS unit's system
- **Implementation Status**: ✅ IMPLEMENTED
- **Test Coverage**: `test_space_cannon_pds_ii_adjacent_systems`

## Implementation Details

### Test Cases Demonstrating Rule Implementation:
1. **Basic Space Cannon Offense** (`test_space_cannon_offense_basic`): Tests that PDS units in active system can fire during offense step
2. **Multiple Unit Space Cannon** (`test_space_cannon_offense_multiple_units`): Tests multiple PDS units firing in same system
3. **Space Cannon Defense** (`test_space_cannon_defense_basic`): Tests opponent PDS units firing during defense step
4. **Hit Assignment** (`test_space_cannon_hit_assignment`): Tests hits are properly assigned to ships in space
5. **No Valid Targets** (`test_space_cannon_no_valid_targets`): Tests behavior when no valid targets exist
6. **PDS II Adjacent Systems** (`test_space_cannon_pds_ii_adjacent_systems`): Tests PDS II units can fire at adjacent systems

### Key Implementation Files:
- `src/ti4/actions/tactical_action.py`: Main space cannon mechanics in `_get_space_cannon_units_for_player` method
- `tests/test_space_cannon_offense.py`: Comprehensive test suite covering all space cannon rules

## Related Rules
- Rule 63: PDS
- Rule 79: Space Dock
- Rule 89: Tactical Action

## Action Items
- [x] Analyze Space Cannon offense mechanics
- [x] Review Space Cannon defense timing
- [x] Examine hit assignment rules
- [x] Study PDS range capabilities
- [x] Investigate tactical action integration
- [x] Implement PDS II adjacent system mechanics
