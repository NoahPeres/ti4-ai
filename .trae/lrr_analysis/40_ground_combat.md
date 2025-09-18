# Rule 40: GROUND COMBAT

## Category Overview
**Rule Type:** Combat Mechanics  
**Complexity:** High  
**Frequency:** High (occurs during invasions)  
**Dependencies:** Ground Forces, Invasion, Sustain Damage, Combat Modifiers

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
- **Test Coverage:** ✅ Comprehensive (`test_combat.py`)
- **Details:** Dice rolling mechanics fully implemented with proper hit calculation based on combat values

### 42.2 - Assign Hits (WELL IMPLEMENTED) 
- **Implementation Status:** ✅ COMPLETE
- **Code Location:** `CombatResolver.resolve_sustain_damage_abilities()`
- **Test Coverage:** ✅ Comprehensive (`test_combat.py`)
- **Details:** Hit assignment with sustain damage resolution properly implemented

### 42.3 - Combat Rounds (PARTIALLY IMPLEMENTED)
- **Implementation Status:** ⚠️ PARTIAL
- **Code Location:** Individual combat mechanics exist but no round management
- **Test Coverage:** ❌ Missing round-based tests
- **Details:** Combat resolution exists but lacks multi-round combat loop

### 42.4 - Combat End Conditions (NOT IMPLEMENTED)
- **Implementation Status:** ❌ MISSING
- **Code Location:** No dedicated ground combat controller
- **Test Coverage:** ❌ Missing
- **Details:** No implementation of combat end detection or timing effects

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
- `test_combat.py::test_roll_dice_for_unit()` - Basic dice rolling
- `test_combat.py::test_calculate_hits()` - Hit calculation from dice
- `test_combat.py::test_resolve_sustain_damage_abilities()` - Sustain damage resolution
- `test_combat.py::test_apply_combat_modifiers()` - Combat modifiers
- `test_unit.py::test_sustain_damage_*()` - Sustain damage mechanics

### Missing Tests ❌
- Ground combat round management
- Multi-round combat scenarios
- Combat end condition detection
- Ground combat integration with invasion
- Combat timing effects ("start of combat", "end of combat")

## Implementation Files

### Core Implementation ✅
- `src/ti4/core/combat.py` - `CombatResolver` class with dice and hit mechanics
- `src/ti4/core/unit.py` - Unit combat stats and sustain damage
- `src/ti4/core/unit_stats.py` - Combat values and dice counts

### Missing Implementation ❌
- Ground combat controller/manager
- Combat round state management
- Integration with invasion system
- Combat timing effect system

## Notable Implementation Details

### Well Implemented ✅
1. **Dice Rolling System** - Robust dice rolling with proper randomization
2. **Hit Calculation** - Accurate hit determination based on combat values
3. **Sustain Damage** - Complete sustain damage mechanics with state management
4. **Combat Modifiers** - Support for +/- modifiers to combat rolls
5. **Unit Combat Stats** - All ground forces have proper combat values

### Implementation Gaps ❌
1. **Combat Round Management** - No system to manage multiple combat rounds
2. **Combat State Tracking** - No tracking of combat progression
3. **End Condition Detection** - No automatic detection of combat end
4. **Timing Effects** - No support for "start/end of combat" effects
5. **Integration Layer** - No connection between combat mechanics and invasion system

## Action Items

1. **HIGH PRIORITY** - Create `GroundCombatController` class to manage combat rounds
2. **HIGH PRIORITY** - Implement combat state tracking and round progression
3. **HIGH PRIORITY** - Add combat end condition detection
4. **MEDIUM PRIORITY** - Integrate ground combat with invasion system
5. **MEDIUM PRIORITY** - Implement combat timing effects system
6. **MEDIUM PRIORITY** - Add comprehensive ground combat integration tests
7. **LOW PRIORITY** - Create ground combat UI components
8. **LOW PRIORITY** - Add combat animation and visual feedback
9. **LOW PRIORITY** - Implement combat replay functionality
10. **LOW PRIORITY** - Add combat statistics and analytics

## Priority Assessment
**PRIORITY: HIGH**

Ground combat is a core game mechanic that occurs frequently during invasions. While the fundamental combat mechanics (dice rolling, hit calculation, sustain damage) are well implemented, the system lacks the higher-level orchestration needed for complete ground combat resolution. The missing round management and integration with the invasion system represent significant gaps in gameplay functionality.

The existing foundation is solid and extensible, making implementation of the missing pieces straightforward but essential for complete game functionality.