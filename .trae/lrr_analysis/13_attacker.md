# Rule 13: ATTACKER

## Category Overview
**Rule Type:** Combat Role Definition
**Priority:** High
**Complexity:** Low
**Implementation Status:** ✅ COMPLETED

Rule 13 defines the fundamental combat role assignment in TI4, establishing that the active player is always the attacker during combat situations.

## Sub-Rules Analysis

### 13.0 - Attacker Role Definition
**Raw LRR Text:**
> "During combat, the active player is the attacker."

**Analysis:**
- Simple but fundamental rule for combat resolution
- Active player = attacker in all combat scenarios (space combat, ground combat)
- Determines combat initiative, retreat options, and ability timing
- Critical for proper combat flow and rule interactions

**Priority:** High - Core combat mechanic affecting all combat scenarios

## Related Topics
- **Defender:** The non-active player in combat situations
- **Invasion:** Ground combat where active player attacks defending forces
- **Space Combat:** Space battles where active player is the attacker

## Dependencies
- Active player tracking system
- Combat resolution system
- Turn order and initiative mechanics
- Retreat mechanics (attacker restrictions)
- Combat timing and ability resolution order

## Test References
**Implemented Test Coverage:** Comprehensive attacker role testing
- `tests/test_rule_13_attacker.py`: Complete test suite for Rule 13
  - `test_attacker_role_in_space_combat`: Verifies active player is attacker in space combat
  - `test_attacker_role_in_ground_combat`: Verifies active player is attacker in ground combat
  - `test_active_player_changes_attacker_role`: Tests attacker role changes with active player
  - `test_attacker_role_with_tactical_action`: Tests attacker role during tactical actions
  - `test_attacker_role_persists_during_combat_rounds`: Tests role persistence across combat rounds
  - `test_no_combat_raises_error`: Tests error handling when no combat exists
  - `test_multiple_defenders_single_attacker`: Tests single attacker with multiple defenders
  - `test_retreat_manager_initialization`: Tests retreat system integration

## Implementation Files
**Current Implementation Status:** ✅ COMPLETED
- `src/ti4/core/combat.py`: CombatRoleManager class with attacker/defender role assignment
  - `get_attacker_id()`: Returns active player as attacker in space combat
  - `get_defender_id()`: Returns non-active player as defender in space combat
  - `get_ground_combat_attacker_id()`: Returns active player as attacker in ground combat
  - `get_ground_combat_defender_id(system, planet_name)`: Returns non-active player as defender in ground combat
  - `has_combat()`: Detects combat scenarios in systems
- `src/ti4/core/system.py`: Added `get_ground_forces_on_planet()` method for ground combat detection
- `tests/test_rule_13_attacker.py`: Complete test suite with 8 passing tests

## Implementation Summary

**✅ COMPLETED IMPLEMENTATION**

Rule 13 has been fully implemented with comprehensive test coverage. The implementation includes:

### Key Components Implemented:
1. **CombatRoleManager Class** (`src/ti4/core/combat.py`):
   - Proper attacker/defender role assignment based on active player
   - Separate methods for space combat and ground combat scenarios
   - Combat detection logic for both space and ground battles

2. **Ground Combat Support** (`src/ti4/core/system.py`):
   - Added `get_ground_forces_on_planet()` method to detect ground forces
   - Enables proper ground combat detection and role assignment

3. **Comprehensive Test Suite** (`tests/test_rule_13_attacker.py`):
   - 8 test cases covering all aspects of Rule 13
   - Tests for both space and ground combat scenarios
   - Edge case testing and error handling
   - Integration with retreat system

### Test Cases Demonstrating Rule 13 Implementation:
- **`test_attacker_role_in_space_combat`**: Confirms active player is attacker in space battles
- **`test_attacker_role_in_ground_combat`**: Confirms active player is attacker in ground battles
- **`test_active_player_changes_attacker_role`**: Verifies attacker role follows active player changes
- **`test_attacker_role_with_tactical_action`**: Tests attacker role during tactical action execution
- **`test_attacker_role_persists_during_combat_rounds`**: Ensures role consistency across combat rounds
- **`test_no_combat_raises_error`**: Validates proper error handling when no combat exists
- **`test_multiple_defenders_single_attacker`**: Tests scenarios with multiple defending players
- **`test_retreat_manager_initialization`**: Confirms integration with retreat mechanics

### Implementation Notes:
- Rule 13 is foundational to combat mechanics and properly integrated with existing systems
- The implementation correctly handles both space combat and ground combat scenarios
- All tests pass, confirming the rule works as specified in the LRR
- The implementation is ready for use by other combat-related rules and systems

**Status:** ✅ Ready for production use
