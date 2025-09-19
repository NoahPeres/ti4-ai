# LRR Rule 58: MOVEMENT

## Rule Category Overview
A player can move their ships by resolving a tactical action during the action phase. Additionally, some abilities can move a unit outside of the tactical action.

## Sub-Rules Analysis

### 58.2 Tactical Action Movement
- **Implementation Status**: ✅ Complete
- **Test Coverage**: ✅ Comprehensive
- **Priority**: High
- **Notes**: Tactical action movement section header.
- **Test Cases**: `test_tactical_action_enables_movement`

### 58.3 Ship Move Value
- **Implementation Status**: ✅ Complete
- **Test Coverage**: ✅ Comprehensive
- **Priority**: High
- **Notes**: A ship's move value is presented along with its other attributes on faction sheets and unit upgrade technology cards. This value indicates the distance from its current system that a ship can move.
- **Test Cases**: `test_ship_move_value_determines_distance`

### 58.4 Move Ships Step
- **Implementation Status**: ✅ Complete
- **Test Coverage**: ✅ Comprehensive
- **Priority**: High
- **Notes**: STEP 1-MOVE SHIPS: A player can move any number of their eligible ships into the active system, obeying specific movement rules.
- **Test Cases**: 
  - `test_ships_must_end_in_active_system` (Rule 58.4a)
  - `test_cannot_move_through_enemy_systems` (Rule 58.4b)
  - `test_cannot_move_from_commanded_system` (Rule 58.4c)
  - `test_can_move_through_own_command_tokens` (Rule 58.4d)
  - `test_can_move_out_and_back_with_sufficient_move_value` (Rule 58.4e)
  - `test_movement_follows_adjacent_path` (Rule 58.4f)
- **Implementation Details**:
  - Rule 58.4a: Ships must end movement in active system
  - Rule 58.4b: Ships cannot move through systems with enemy ships (pathfinding with intermediate system checking)
  - Rule 58.4c: Ships cannot move from systems with own command tokens
  - Rule 58.4d: Ships can move through systems with own command tokens (implicitly allowed)
  - Rule 58.4e: Ships can move out of active system and back if move value allows
  - Rule 58.4f: Ships must move along adjacent systems within move value

### 58.5 Transport During Movement
- **Implementation Status**: ✅ Complete
- **Test Coverage**: ✅ Comprehensive
- **Priority**: High
- **Notes**: When a ship with a capacity value moves or is moved, it may transport ground forces and fighters.
- **Test Cases**: `test_transport_during_movement`

### 58.6 Movement Declaration
- **Implementation Status**: ✅ Complete
- **Test Coverage**: ✅ Comprehensive
- **Priority**: High
- **Notes**: The active player declares which of their ships are moving before any ships move. Those ships arrive in the active system simultaneously.
- **Test Cases**: `test_ships_declared_before_movement`

### 58.7 Space Cannon Offense Step
- **Implementation Status**: ✅ Complete
- **Test Coverage**: ✅ Comprehensive
- **Priority**: High
- **Notes**: STEP 2-SPACE CANNON OFFENSE: After the "Move Ships" step, players can use the "Space Cannon" abilities of their units in the active system.
- **Test Cases**: 
  - `test_space_cannon_after_move_ships`
  - `test_space_cannon_offense.py::TestRule58SpaceCannonOffenseStep::test_space_cannon_offense_after_movement`: Tests that Space Cannon Offense step occurs after Movement step in tactical action sequence
  - `test_space_cannon_offense.py::TestRule58SpaceCannonOffenseStep::test_space_cannon_offense_can_execute_with_space_cannon_units`: Tests that step can execute when space cannon units are present
  - `test_space_cannon_offense.py::TestRule58SpaceCannonOffenseStep::test_space_cannon_offense_cannot_execute_without_space_cannon_units`: Tests that step cannot execute without space cannon units
- **Implementation Details**:
  - SpaceCannonOffenseStep class integrated into TacticalAction sequence after MovementStep
  - Proper detection of units with space cannon ability in active system
  - Step execution logic with player order and target validation
  - Integration with existing tactical action architecture

### 58.8 Ability Movement
- **Implementation Status**: ✅ Complete
- **Test Coverage**: ✅ Comprehensive
- **Priority**: High
- **Notes**: Ability movement section header.
- **Test Cases**: `test_ability_movement_bypasses_normal_rules`

### 58.9 Ability Movement Rules
- **Implementation Status**: ✅ Complete
- **Test Coverage**: ✅ Comprehensive
- **Priority**: High
- **Notes**: If an ability moves a unit outside of the "Movement" step of a tactical action, players follow the rules specified by that ability; neither a unit's move value nor the rules specified above apply.
- **Test Cases**: `test_ability_movement_bypasses_normal_rules`

## Implementation Details

### Test Cases Demonstrating Rule Implementation:
1. **Tactical Action Movement** (`test_tactical_action_enables_movement`): Tests that tactical actions enable ship movement
2. **Ship Move Value** (`test_ship_move_value_determines_distance`): Tests that ship's move value determines movement distance
3. **Move Ships Step - Active System** (`test_ships_must_end_in_active_system`): Tests ships must end in active system (58.4a)
4. **Move Ships Step - Enemy Blocking** (`test_cannot_move_through_enemy_systems`): Tests ships cannot move through enemy systems (58.4b)
5. **Move Ships Step - Command Tokens** (`test_cannot_move_from_commanded_system`): Tests command token movement restrictions (58.4c)
6. **Move Ships Step - Own Tokens** (`test_can_move_through_own_command_tokens`): Tests movement through own command tokens (58.4d)
7. **Move Ships Step - Return Movement** (`test_can_move_out_and_back_with_sufficient_move_value`): Tests out-and-back movement (58.4e)
8. **Move Ships Step - Adjacent Path** (`test_movement_follows_adjacent_path`): Tests adjacent path requirement (58.4f)
9. **Transport During Movement** (`test_transport_during_movement`): Tests transport mechanics during movement
10. **Movement Declaration** (`test_ships_declared_before_movement`): Tests simultaneous arrival mechanics
11. **Space Cannon Offense** (`test_space_cannon_after_move_ships`): Tests Space Cannon step after movement
12. **Ability Movement** (`test_ability_movement_bypasses_normal_rules`): Tests ability movement bypasses normal rules

### Key Implementation Files:
- `src/ti4/core/movement.py`: Core movement mechanics and validation
- `src/ti4/actions/tactical_action.py`: Tactical action movement integration
- `tests/test_rule_58_movement.py`: Comprehensive test suite covering all movement rules

## Overall Implementation Status
- **Current State**: ✅ COMPLETED (Verified December 2024)
- **Test Coverage**: 13 passing tests with comprehensive sub-rule coverage
- **Dependencies**: ✅ Rule 6 (Adjacency), ✅ Rule 60 (Neighbors), ✅ Rule 101 (Wormholes)
- **Quality Status**: All tests passing, type checking clean, linting compliant
- **Verification Date**: December 2024

## Notes
- Rule 58 has 8 sub-rules (58.2-58.9, no 58.1)
- All 13 tests passing with comprehensive coverage
- Integrated with tactical action system and space cannon mechanics

## Related Rules
- Rule 3: ACTION PHASE
- Rule 5: ACTIVE SYSTEM
- Rule 16: CAPACITY
- Rule 77: SPACE CANNON
- Rule 89: TACTICAL ACTION
- Rule 95: TRANSPORT

## Action Items
- [x] Analyze current implementation
- [x] Identify gaps
- [x] Create implementation plan
- [x] Write tests
- [x] Implement missing functionality