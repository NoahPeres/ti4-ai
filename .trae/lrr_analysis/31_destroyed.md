# Rule 31: DESTROYED - Analysis

## Category Overview
**Rule Type:** Core Combat Mechanic
**Priority:** HIGH
**Status:** FULLY IMPLEMENTED ✅
**Complexity:** Medium

## Raw LRR Text
```
31 DESTROYED
When a unit is destroyed, it is returned to its owner's reinforcements.

31.1 When a player assigns hits that were produced against their units, that player chooses a number of their units to be destroyed equal to the number of hits produced against those units.

31.2 If a player's unit is removed from the board by a game effect, it is not treated as being destroyed; effects that trigger when a unit is destroyed are not triggered.

RELATED TOPICS: Anti-Fighter Barrage, Bombardment, Space Cannon, Space Combat, Sustain Damage
```

## Sub-Rules Analysis

### 31.1 Hit Assignment and Destruction
- **Status:** FULLY IMPLEMENTED ✅
- **Description:** Player choice in hit assignment to units
- **Implementation:** Found in `combat.py` with `assign_hits_by_player_choice()` and validation methods

### 31.2 Removal vs Destruction Distinction
- **Status:** FULLY IMPLEMENTED ✅
- **Description:** Distinguishes between destruction (triggers effects) and removal (no triggers)
- **Implementation:** Implemented in `destruction.py` with separate `destroy_unit()` and `remove_unit()` methods

## Related Topics
- Anti-Fighter Barrage
- Bombardment
- Space Cannon
- Space Combat
- Sustain Damage

## Dependencies
- Combat system (hit resolution)
- Unit abilities (sustain damage)
- Reinforcement pools
- Effect triggering system
- Player choice mechanics

## Test References

### Implemented Tests ✅
- `test_rule_31_destroyed.py`: Comprehensive Rule 31 test suite with 13 test cases
  - `test_destroy_unit_on_planet_returns_to_reinforcements`: Tests basic destruction mechanics
  - `test_destroy_unit_in_space_returns_to_reinforcements`: Tests space unit destruction
  - `test_destroy_unit_without_reinforcements`: Tests destruction without reinforcement pool
  - `test_destroy_nonexistent_unit`: Tests error handling for invalid units
  - `test_remove_unit_no_destruction_effects`: Tests Rule 31.2 removal vs destruction
  - `test_remove_unit_from_planet`: Tests planet unit removal
  - `test_remove_unit_from_space`: Tests space unit removal
  - `test_remove_nonexistent_unit`: Tests error handling for removal
  - `test_destroy_units_batch`: Tests batch destruction
  - `test_destroy_unit_in_combat`: Tests combat destruction
  - `test_remove_unit_for_fleet_pool`: Tests fleet pool removal
  - `test_invalid_hit_assignment_too_many_hits`: Tests hit assignment validation
  - `test_invalid_hit_assignment_nonexistent_unit`: Tests hit assignment validation
- `test_combat.py`: Hit assignment validation, sustain damage prevention
- `test_system.py`: Unit removal from space
- `test_integration.py`: Unit removal mechanics

## Implementation Files

### Core Implementation ✅
- `src/ti4/core/destruction.py`: Complete unit destruction and removal system
  - `UnitDestructionManager`: Main class for handling unit destruction
  - `destroy_unit()`: Destroys units and returns them to reinforcements
  - `remove_unit()`: Removes units without triggering destruction effects (Rule 31.2)
  - `destroy_units()`: Batch destruction functionality
  - `destroy_unit_in_combat()`: Combat-specific destruction
  - `remove_unit_for_fleet_pool()`: Fleet pool removal
- `src/ti4/core/reinforcements.py`: Reinforcement pool management
- `src/ti4/core/combat.py`: Hit assignment and resolution with validation
- `src/ti4/core/unit.py`: Unit abilities and stats
- `src/ti4/core/system.py`: Unit removal methods

## Notable Implementation Details

### Fully Implemented ✅
- Hit assignment with player choice and validation
- Duplicate hit assignment prevention
- Sustain damage integration
- Unit removal from systems (space and planets)
- Reinforcement pool tracking and management
- Destruction vs removal distinction (Rule 31.2)
- Destruction effect triggering system
- Comprehensive unit lifecycle management
- Unit destruction event system
- Batch destruction capabilities
- Combat-specific destruction handling
- Fleet pool removal mechanics
- Error handling for invalid operations
- Comprehensive test coverage (13 test cases)

## Implementation Summary ✅

Rule 31: DESTROYED has been **FULLY IMPLEMENTED** with comprehensive test coverage.

### Key Achievements:
1. ✅ **Complete destruction system** - `UnitDestructionManager` handles all destruction scenarios
2. ✅ **Reinforcement pool integration** - Units properly return to reinforcements when destroyed
3. ✅ **Rule 31.2 compliance** - Clear distinction between destruction and removal
4. ✅ **Combat integration** - Hit assignment validation prevents duplicate assignments
5. ✅ **Comprehensive testing** - 13 test cases covering all scenarios and edge cases
6. ✅ **Error handling** - Proper validation and error messages for invalid operations
7. ✅ **Effect system** - Destruction effects can be registered and triggered
8. ✅ **Batch operations** - Support for destroying multiple units efficiently

### Test Cases Demonstrating Implementation:
- **Basic destruction**: `test_destroy_unit_on_planet_returns_to_reinforcements`
- **Rule 31.2 compliance**: `test_remove_unit_no_destruction_effects`
- **Hit assignment validation**: `test_invalid_hit_assignment_too_many_hits`
- **Combat integration**: `test_destroy_unit_in_combat`
- **Batch operations**: `test_destroy_units_batch`
- **Error handling**: `test_destroy_nonexistent_unit`

## Priority Assessment
**COMPLETED** ✅ - Rule 31 is fully implemented with robust testing and proper integration with the combat system and reinforcement pools.
