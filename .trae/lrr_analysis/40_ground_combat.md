# Rule 40: GROUND COMBAT

## Category Overview
**Rule Type:** Combat Mechanics
**Complexity:** High
**Frequency:** High (occurs during invasions)
**Dependencies:** Ground Forces, Invasion, Sustain Damage, Combat Modifiers
**Implementation Status:** ✅ **COMPLETED** (December 2024)

## Raw LRR Text
```
42 GROUND COMBAT
During the "Ground Combat" step of an invasion, if the active player has ground forces on a planet that contains another player's ground forces, those players resolve a ground combat on that planet. To resolve a ground combat, players perform the following steps:

42.1 STEP 1-ROLL DICE: Each player rolls one die for each ground force they have on the planet; this is a combat roll. If a unit's combat roll produces a result that is equal to or greater than that unit's combat value, that roll produces a hit.
a If a unit's combat value contains two or more burst icons, the player rolls one die for each burst icon instead.

42.2 STEP 2-ASSIGN HITS: Each player in the combat must choose one of their own ground forces on the planet to be destroyed for each hit result their opponent produced.
a When a unit is destroyed, the player who controls that unit removes it from the board and places it in their reinforcements.

42.3 After assigning hits, if both players still have ground forces on the planet, players resolve a new combat round starting with the "Roll Dice" step.

42.4 Ground combat ends when only one player (or neither player) has ground forces on the planet.
a During the first round of a combat, "start of combat" and "start of combat round" effects occur during the same timing window.
b During the last round of a combat, "end of combat" and "end of combat round" effects occur during the same timing window.
```

## Sub-Rules Analysis

### 42.1 - Roll Dice (WELL IMPLEMENTED)
- **Implementation Status:** ✅ COMPLETE
- **Code Location:** `CombatResolver.roll_dice_for_unit()`, `CombatResolver.calculate_hits()`
- **Test Coverage:** ✅ Comprehensive (`test_rule_40_ground_combat.py`)
- **Details:** Dice rolling mechanics fully implemented with proper hit calculation based on combat values

### 42.2 - Assign Hits (WELL IMPLEMENTED)
- **Implementation Status:** ✅ COMPLETE
- **Code Location:** `GroundCombatController._assign_hits_to_forces()`
- **Test Coverage:** ✅ Comprehensive (`test_rule_40_ground_combat.py`)
- **Details:** Hit assignment with hooks for sustain damage resolution and player choice. Player input for sustain and hit assignments is not yet passed into the controller API.

### 42.3 - Combat Rounds (WELL IMPLEMENTED)
- **Implementation Status:** ✅ COMPLETE
- **Code Location:** `GroundCombatController.resolve_combat_round()`, `GroundCombatController.resolve_ground_combat()`
- **Test Coverage:** ✅ Comprehensive (`test_rule_40_ground_combat.py`)
- **Details:** Multi-round combat loop with proper round management and continuation logic

### 42.4 - Combat End Conditions (WELL IMPLEMENTED)
- **Implementation Status:** ✅ COMPLETE
- **Code Location:** `GroundCombatController.resolve_combat_round()`, `GroundCombatController.resolve_ground_combat()`, `GroundCombatController._combat_should_continue()`
- **Test Coverage:** ✅ Comprehensive (`test_rule_40_ground_combat.py`)
- **Details:** Combat ending conditions implemented with winner determination. Timing effects not implemented.

## Related Topics
- **Rule 49: INVASION** - Ground combat occurs during invasion step
- **Rule 43: GROUND FORCES** - Units that participate in ground combat
- **Rule 87: SUSTAIN DAMAGE** - Damage absorption mechanics
- **Rule 15: BOMBARDMENT** - Pre-combat bombardment affects ground forces
- **Rule 56: MODIFIERS** - Combat modifiers affect dice rolls

## Dependencies
- Ground Forces system (units, placement, ownership)
- Combat resolution engine (dice rolling, hit calculation)
- Sustain damage mechanics
- Unit destruction and reinforcement management
- Combat timing and effect resolution

## Test References

### Existing Tests ✅
- `test_rule_40_ground_combat.py::test_ground_combat_basic_resolution()` - Complete ground combat scenarios
- `test_rule_40_ground_combat.py::test_ground_combat_with_sustain_damage()` - Sustain damage in ground combat
- `test_rule_40_ground_combat.py::test_ground_combat_multiple_rounds()` - Multi-round combat scenarios
- `test_rule_40_ground_combat.py::test_ground_combat_end_conditions()` - Combat end condition detection
- `test_unit.py::test_sustain_damage_*()` - Sustain damage mechanics

### Missing Tests ❌
- Ground combat integration with invasion system
- Combat timing effects ("start of combat", "end of combat")
- Complex multi-faction ground combat scenarios

## Implementation Files

### Core Implementation ✅
- `src/ti4/core/combat.py` - `CombatResolver` class with dice and hit mechanics
- `src/ti4/core/ground_combat.py` - `GroundCombatController` class for complete ground combat management
- `src/ti4/core/unit.py` - Unit combat stats and sustain damage
- `src/ti4/core/unit_stats.py` - Combat values and dice counts

### Missing Implementation ❌
- Integration with invasion system
- Combat timing effect system

## Notable Implementation Details

### Well Implemented ✅
1. **Dice Rolling System** - Robust dice rolling with proper randomization
2. **Hit Calculation** - Accurate hit determination based on combat values
3. **Sustain Damage** - Complete sustain damage mechanics with state management
4. **Combat Modifiers** - Support for +/- modifiers to combat rolls
5. **Unit Combat Stats** - All ground forces have proper combat values
6. **Combat Round Management** - Complete system to manage multiple combat rounds
7. **Combat State Tracking** - Full tracking of combat progression and round state
8. **End Condition Detection** - Automatic detection of combat end conditions
9. **Ground Combat Controller** - Dedicated controller for orchestrating ground combat

### Implementation Gaps ❌
1. **Timing Effects** - No support for "start/end of combat" effects
2. **Integration Layer** - No connection between combat mechanics and invasion system
3. **Multi-faction Combat** - Limited support for complex multi-faction scenarios
4. **Sustain Damage Choices in Ground Combat** - Player choice for sustaining damage not yet integrated into round flow

## Action Items

1. **HIGH PRIORITY** - Integrate ground combat with invasion system
2. **MEDIUM PRIORITY** - Implement combat timing effects system ("start/end of combat")
3. **MEDIUM PRIORITY** - Add support for complex multi-faction ground combat scenarios
4. **MEDIUM PRIORITY** - Add comprehensive ground combat integration tests with invasion
5. **LOW PRIORITY** - Create ground combat UI components
6. **LOW PRIORITY** - Add combat animation and visual feedback
7. **LOW PRIORITY** - Implement combat replay functionality
8. **LOW PRIORITY** - Add combat statistics and analytics

## Priority Assessment

### PRIORITY: MEDIUM

Ground combat is a core game mechanic that occurs frequently during invasions. The fundamental combat mechanics (dice rolling, hit calculation, sustain damage) are well implemented, and the system now includes complete round management and combat orchestration through the `GroundCombatController`. The main remaining work involves integrating ground combat with the invasion system and adding support for combat timing effects. While important, these are integration tasks rather than core functionality gaps.

The existing foundation is solid and extensible, making implementation of the remaining integration pieces straightforward and well-defined.
