# Rule 10: ANTI-FIGHTER BARRAGE (UNIT ABILITY)

## Category Overview
**Rule Type**: Unit Ability
**Complexity**: Medium
**Dependencies**: Space Combat, Unit Stats, Dice Rolling
**Implementation Status**: 🟡 Partially Implemented

Anti-Fighter Barrage is a unit ability that allows certain units (primarily Destroyers) to attack enemy fighters before normal space combat begins. This ability occurs during the first round of space combat only and follows specific targeting and timing rules.

## Sub-Rules Analysis

### 10.1 STEP 1 - Anti-Fighter Barrage Rolls 🔴 HIGH PRIORITY
**Raw LRR Text**: "Each player rolls dice for each of their units in the combat that has the 'Anti-Fighter Barrage' ability; this is called an anti-fighter barrage roll. A hit is produced for each die roll that is equal to or greater than the unit's anti-fighter barrage value."

**Implementation Status**: 🟡 Partially Implemented
**Current State**: Basic ability detection and dice rolling implemented in `CombatResolver.perform_anti_fighter_barrage()`
**Missing Elements**:
- Anti-fighter barrage value system (currently uses combat value)
- Proper ability display format parsing ("Anti-Fighter Barrage X (xY)")
- Integration with space combat timing

**Sub-components**:
- **10.1.a** - Ability presentation on faction sheets and upgrade cards
- **10.1.b** - Ability display format ("Anti-Fighter Barrage X (xY)")
- **10.1.c** - Combat roll effects exclusion (rerolls, modifiers don't affect AFB)
- **10.1.d** - Ability usable even without fighters present

### 10.2 STEP 2 - Assign Hits to Fighters 🔴 HIGH PRIORITY
**Raw LRR Text**: "Each player must choose and destroy one of their fighters in the active system for each hit their opponent's anti-fighter barrage roll produced."

**Implementation Status**: 🔴 Not Implemented
**Current State**: No hit assignment or fighter destruction logic
**Missing Elements**:
- Hit assignment system for anti-fighter barrage
- Fighter destruction mechanics
- Excess hit handling (when hits > available fighters)

**Sub-components**:
- **10.2.a** - Excess hits have no effect when more hits than fighters

## Related Topics
- **Destroyed**: Fighter destruction mechanics
- **Space Combat**: Timing and integration with combat phases
- **Unit Abilities**: General ability system framework
- **Dice Rolling**: Combat dice mechanics

## Dependencies Summary

### Critical Dependencies
1. **Space Combat System** - AFB occurs during first round of space combat
2. **Unit Stats System** - Anti-fighter barrage values and dice counts
3. **Hit Assignment System** - Choosing and destroying fighters
4. **Active System Tracking** - Determining which fighters can be targeted

### Related Systems
1. **Combat Resolver** - Integration with combat flow
2. **Unit Destruction** - Fighter removal mechanics
3. **Ability System** - Unit ability detection and usage
4. **Game State Management** - Tracking combat rounds and timing

## Test References
- `test_combat.py::test_anti_fighter_barrage_timing()` - Basic timing test
- `test_combat.py::test_anti_fighter_barrage_only_targets_fighters()` - Target filtering
- `test_unit.py::test_anti_fighter_barrage_ability()` - Ability detection
- `test_unit.py::test_multiple_abilities_on_same_unit()` - Multi-ability units

## Implementation Files
- `src/ti4/core/combat.py` - `CombatResolver.perform_anti_fighter_barrage()`
- `src/ti4/core/unit.py` - `Unit.has_anti_fighter_barrage()`
- `src/ti4/data/unit_stats.py` - Unit ability definitions

## Action Items

1. **Implement Anti-Fighter Barrage Value System** 🔴 HIGH
   - Add `anti_fighter_barrage_value` and `anti_fighter_barrage_dice` to UnitStats
   - Parse ability display format ("Anti-Fighter Barrage X (xY)")
   - Update unit data with proper AFB values

2. **Implement Hit Assignment for AFB** 🔴 HIGH
   - Create fighter selection and destruction logic
   - Handle excess hits properly (no effect when hits > fighters)
   - Integrate with player choice system for target selection

3. **Integrate AFB with Space Combat Timing** 🔴 HIGH
   - Ensure AFB occurs only in first round of space combat
   - Implement proper "before combat" timing
   - Add AFB step to combat resolution flow

4. **Implement Combat Roll Effect Exclusions** 🟡 MEDIUM
   - Ensure rerolls and modifiers don't affect AFB rolls
   - Separate AFB dice rolling from regular combat rolls
   - Add proper effect filtering

5. **Add Comprehensive AFB Testing** 🟡 MEDIUM
   - Test AFB value system and dice rolling
   - Test hit assignment and fighter destruction
   - Test timing integration with space combat
   - Test edge cases (no fighters, excess hits)

6. **Implement Ability Usage Without Fighters** 🟢 LOW
   - Allow AFB to be used even when no fighters present
   - Enable hits to trigger specific abilities (future expansion)
   - Add proper validation and effect handling

7. **Add Faction Sheet Integration** 🟢 LOW
   - Display AFB abilities on faction sheets
   - Show upgrade card effects on AFB
   - Implement proper ability presentation

8. **Create AFB Documentation** 🟢 LOW
   - Document AFB mechanics and timing
   - Add examples of AFB usage
   - Create developer guide for AFB implementation

9. **Optimize AFB Performance** 🟢 LOW
   - Efficient fighter filtering and targeting
   - Minimize dice rolling overhead
   - Optimize hit assignment algorithms

10. **Add AFB Analytics and Logging** 🟢 LOW
    - Track AFB usage statistics
    - Log AFB hits and effectiveness
    - Add debugging information for AFB resolution
