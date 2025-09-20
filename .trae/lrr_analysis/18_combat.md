# Rule 18: Combat (Attribute) Analysis

## Category Overview
**Rule Type:** Unit Attribute  
**Priority:** High  
**Implementation Status:** ✅ Complete  
**Complexity:** Medium  
**Dependencies:** Space Combat, Ground Combat, Dice Rolling

## Raw LRR Text
```
18 COMBAT (ATTRIBUTE)	
Combat is an attribute of some units that is presented on faction sheets and unit upgrade technology cards.
18.1 During combat, if a unit's combat roll produces a result equal to or greater than its combat value, it produces a hit.
18.2 If a unit's combat value contains two or more burst icons, instead of rolling a single die, the player rolls one die for each burst icon when making that unit's combat rolls.
RELATED TOPICS: Ground Combat, Invasion, Space Combat
```

## Sub-Rules Analysis

### 18.0 - Combat Attribute Definition
**Status**: ✅ Implemented
**Description**: Combat is an attribute of units presented on faction sheets and unit upgrade technology cards.
**Implementation**: Unit class has combat_value attribute
**Test Coverage**: Covered in unit tests

### 18.1 - Hit Calculation
**Status**: ✅ Implemented  
**Description**: During combat, if a unit's combat roll produces a result equal to or greater than its combat value, it produces a hit.
**Implementation**: `CombatResolver.calculate_hits()` method
**Test Coverage**: 
- `test_combat_hit_calculation()` - Basic hit calculation
- `test_combat_miss_calculation()` - Miss scenarios
- `test_combat_edge_cases()` - Edge case scenarios

### 18.2 - Burst Icon Mechanics
**Status**: ✅ Implemented
**Description**: If a unit's combat value contains two or more burst icons, the player rolls one die for each burst icon.
**Implementation**: `roll_dice_for_unit_with_burst_icons()` method in combat.py
**Test Coverage**:
- `test_burst_icon_single_die()` - Units without burst icons roll single die
- `test_burst_icon_multiple_dice()` - Units with burst icons roll multiple dice
- `test_burst_icon_count_determines_dice()` - Burst icon count determines dice count
- `test_burst_icon_visual_vs_actual()` - Burst icons are visual representation; combat_dice contains the total dice count including burst icons
- `test_burst_icon_hit_calculation()` - Hit calculation with burst icons

## Core Implementation

### Key Classes
- `Unit`: Contains combat_value attribute
- `CombatResolver`: Handles combat calculations and burst icon mechanics

### Key Methods
- `roll_dice_for_unit_with_burst_icons()`: Handles dice rolling for units with burst icons
- `calculate_hits_with_burst_icons()`: Alias for clarity in burst icon hit calculation
- `calculate_hits()`: Standard hit calculation based on combat values

## Test Coverage
**Test File**: `tests/test_rule_18_burst_icons.py`
**Coverage**: ✅ Comprehensive (5 test cases covering all aspects)
**Status**: All tests passing

## Integration Points
- **Space Combat**: Uses Rule 18 for ship combat calculations
- **Ground Combat**: Uses Rule 18 for ground force combat calculations  
- **Unit System**: Combat values stored as unit attributes
- **Dice System**: Integrates with general dice rolling mechanics

## Future Enhancements
- Combat modifiers from technologies/abilities
- Advanced burst icon interactions
- Combat value modifications during gameplay

## Recent Updates
- 2024-01-XX: Updated analysis to reflect current implementation status
- 2024-01-XX: Verified all sub-rules are implemented and tested
- 2024-01-XX: Added raw LRR text section back to documentation