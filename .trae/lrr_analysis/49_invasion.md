# LRR Rule 49: INVASION

## Rule Category Overview
Invasion is the process of landing ground forces on a planet to gain control of it. The invasion process consists of several steps that must be resolved in order.

## Raw LRR Text
```
49. INVASION
During an invasion, players resolve the following steps:

49.1 STEP 1—BOMBARDMENT: The active player may use the "Bombardment" ability of any of their units in the active system.

49.2 STEP 2—COMMIT GROUND FORCES: If the active player has ground forces in the space area of the active system, that player may commit any number of those ground forces to land on any of the planets in that system; the active player is not required to commit any ground forces.

49.3 STEP 3—SPACE CANNON DEFENSE: The player who controls each planet that the active player committed ground forces to may use the "Space Cannon" ability of any of their units on that planet against the committed ground forces.

49.4 STEP 4—GROUND COMBAT: Players resolve ground combat on each planet that has units that belong to both the active player and other players.

49.5 STEP 5—ESTABLISH CONTROL: The active player gains control of each planet that still contains at least one of their ground forces.
```

## Sub-Rules Analysis

### 49.1 Bombardment
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Notes**: The active player may use the "Bombardment" ability of any of their units in the active system.
- **Test Cases**:
  - `test_bombardment_step_uses_bombardment_abilities` - Tests that bombardment abilities are executed when available
  - `test_bombardment_step_returns_commit_ground_forces` - Tests proper step sequencing

### 49.2 Commit Ground Forces
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Notes**: The active player may commit ground forces from space to planets. Commitment is optional.
- **Test Cases**:
  - `test_commit_ground_forces_step_requires_ground_forces` - Tests that step works when no ground forces available
  - `test_commit_ground_forces_step_returns_space_cannon_defense` - Tests proper step sequencing

### 49.3 Space Cannon Defense
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Notes**: The defending player may use the "Space Cannon" ability of any of their units on the planet.
- **Test Cases**:
  - `test_space_cannon_defense_step_uses_space_cannon` - Tests space cannon defense execution
  - `test_space_cannon_defense_step_returns_ground_combat` - Tests proper step sequencing

### 49.4 Ground Combat
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Notes**: Players resolve ground combat on the planet using the GroundCombatController.
- **Test Cases**:
  - `test_ground_combat_step_resolves_combat` - Tests ground combat resolution
  - `test_ground_combat_step_returns_establish_control` - Tests proper step sequencing

### 49.5 Establish Control
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Notes**: The active player gains control of planets where they still have ground forces.
- **Test Cases**:
  - `test_establish_control_step_gains_control` - Tests planet control assignment
  - `test_establish_control_step_returns_production` - Tests proper step sequencing

## Overall Implementation Status
- **Current State**: Complete
- **Estimated Effort**: Large (Completed)
- **Dependencies**: BombardmentSystem, GroundCombatController, CombatResolver
- **Blockers**: None

## Implementation Details
- **Main Class**: `InvasionController` in `src/ti4/core/invasion.py`
- **Integration**: Uses existing `BombardmentSystem` and `GroundCombatController`
- **Test File**: `tests/test_rule_49_invasion.py`
- **Test Coverage**: 10 test cases covering all 5 invasion steps

## Notes
- Rule 49 has 5 sub-rules, all implemented
- Full integration with existing combat and bombardment systems
- Comprehensive test coverage with proper TDD approach
- All tests passing

## Related Rules
- Rule 15: BOMBARDMENT (integrated via BombardmentSystem)
- Rule 42: GROUND COMBAT (integrated via GroundCombatController)
- Rule 25: CONTROL (planet control assignment)
- Rule 79: SPACE CANNON (space cannon defense)

## Action Items
- [x] Analyze current implementation
- [x] Identify gaps
- [x] Create implementation plan
- [x] Write tests
- [x] Implement missing functionality
- [ ] Write integration tests for complete invasion flow
