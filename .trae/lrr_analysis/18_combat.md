# Rule 18: COMBAT (ATTRIBUTE)

## Category Overview
**Priority**: HIGH  
**Implementation Status**: MOSTLY IMPLEMENTED  
**Complexity**: MEDIUM  

Rule 18 defines the combat attribute for units, including hit calculation and burst icon mechanics. This is a fundamental combat mechanic that determines unit effectiveness in battle.

## Raw LRR Text

### 18 COMBAT (ATTRIBUTE)
Combat is an attribute of some units that is presented on faction sheets and unit upgrade technology cards.

**18.1** During combat, if a unit's combat roll produces a result equal to or greater than its combat value, it produces a hit.

**18.2** If a unit's combat value contains two or more burst icons, instead of rolling a single die, the player rolls one die for each burst icon when making that unit's combat rolls.

## Sub-Rules Analysis

### 18.0 - Combat Attribute Definition
- **Status**: IMPLEMENTED
- **Description**: Combat attribute presented on faction sheets and technology cards
- **Implementation**: `UnitStats.combat_value: Optional[int]`, `Unit.get_combat_value()`

### 18.1 - Hit Calculation
- **Status**: IMPLEMENTED
- **Description**: Roll >= combat value produces hit
- **Implementation**: `CombatResolver.calculate_hits()`, comprehensive dice rolling system

### 18.2 - Burst Icon Mechanics
- **Status**: NOT IMPLEMENTED
- **Description**: Multiple burst icons = multiple dice per unit
- **Implementation Needed**: Burst icon detection, multi-dice rolling per burst

## Related Topics
- Ground Combat
- Invasion
- Space Combat

## Dependencies
- **Unit Stats System**: Combat values and dice counts
- **Dice Rolling System**: Random number generation and hit calculation
- **Combat Resolution System**: Integration with combat phases
- **Technology System**: Combat value modifications
- **Faction System**: Faction-specific combat modifications

## Test References

### Existing Tests
- `test_combat.py` - Comprehensive combat resolver tests
  - `test_roll_dice_for_unit()` - Basic dice rolling
  - `test_roll_dice_for_multi_dice_unit()` - Multi-dice units
  - `test_calculate_hits_multiple_dice()` - Hit calculation
  - `test_unit_combat_dice_values()` - Unit dice counts
  - `test_apply_combat_modifiers()` - Combat modifiers
- `test_integration.py` - Combat value integration tests
- `test_fleet_management.py` - Combat value modifications

### Missing Tests Needed
- `test_burst_icon_mechanics.py` - Burst icon dice rolling
- `test_combat_value_validation.py` - Combat value bounds checking
- `test_faction_combat_modifications.py` - Faction-specific combat changes
- `test_technology_combat_effects.py` - Technology combat modifications

## Implementation Files

### Existing Files
- `src/ti4/core/combat.py` - Combat resolution system
  - `CombatResolver` class with dice rolling and hit calculation
  - `roll_dice_for_unit()` method
  - `calculate_hits()` method
  - `calculate_hits_with_modifiers()` method
- `src/ti4/core/unit.py` - Unit combat interface
  - `get_combat_value()` method
  - `get_combat_dice()` method
- `src/ti4/core/unit_stats.py` - Combat value storage
  - `UnitStats.combat_value: Optional[int]`
  - `UnitStats.combat_dice: int`

### Missing Files Needed
- `src/ti4/mechanics/burst_icon_handler.py` - Burst icon mechanics
- `src/ti4/mechanics/combat_modifiers.py` - Combat modification system

## Notable Implementation Details

### Well-Implemented Areas
1. **Basic Combat System** - Dice rolling and hit calculation working
2. **Combat Value Integration** - Units properly expose combat values
3. **Multi-Dice Support** - Units can roll multiple dice
4. **Combat Modifiers** - Support for +/- modifiers to hit
5. **Comprehensive Testing** - Good test coverage for core mechanics

### Implementation Gaps
1. **Burst Icon System** - No detection or handling of burst icons
2. **Burst Icon Dice Rolling** - Multiple dice per burst icon not implemented
3. **Visual Burst Representation** - No system for burst icon display

### Integration Points
- **Space Combat**: Uses combat resolution for ship battles
- **Ground Combat**: Uses combat resolution for ground battles
- **Anti-Fighter Barrage**: Uses combat mechanics for special attacks
- **Bombardment**: Uses combat mechanics for planetary attacks

## Action Items

1. **Implement Burst Icon Detection** - Add burst icon parsing to unit stats
2. **Create Burst Icon Dice System** - Roll multiple dice per burst icon
3. **Add Burst Icon Validation** - Ensure proper burst icon handling
4. **Enhance Combat Value Display** - Show burst icons in unit information
5. **Create Burst Icon Tests** - Comprehensive testing for burst mechanics
6. **Update Combat Documentation** - Document burst icon mechanics
7. **Add Faction Burst Icons** - Support faction-specific burst icons
8. **Integrate with Technology System** - Burst icon modifications via tech
9. **Add Combat Value Bounds Checking** - Validate combat values (1-10)
10. **Create Combat Attribute Validation** - Ensure proper combat attribute handling