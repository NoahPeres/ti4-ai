# Rule 87: SUSTAIN DAMAGE (UNIT ABILITY)

## Category Overview
Some units have the "Sustain Damage" ability. Immediately before a player assigns hits to their units, that player can use the "Sustain Damage" ability of any of their units in the active system.

## Implementation Status: 85% COMPLETE ✅

### Current Implementation
- **Core Classes**: `Unit`, `UnitStats`, `CombatResolver`
- **Test Coverage**: 8 dedicated tests covering sustain damage mechanics
- **Key Methods**:
  - `Unit.has_sustain_damage() -> bool`
  - `Unit.sustain_damage()` - activates ability
  - `Unit.repair()` - repairs damaged units
  - `CombatResolver.resolve_sustain_damage_abilities()`

### Test Cases Demonstrating Implementation
- `test_unit.py::test_sustain_damage_ability_detection()` - Rule 87.1 (ability detection)
- `test_unit.py::test_sustain_damage_activation()` - Rule 87.1 (hit cancellation)
- `test_unit.py::test_sustain_damage_invalid_unit()` - Rule 87.2 (damaged unit restrictions)
- `test_unit.py::test_sustain_damage_repair()` - Rule 87.3 (repair mechanics)
- `test_combat.py::test_resolve_sustain_damage_abilities()` - Rule 87.4 (combat integration)
- `test_combat.py::test_sustain_damage_prevents_destruction()` - Rule 87.1 (hit prevention)
- `test_combat.py::test_sustain_damage_can_only_be_used_once()` - Rule 87.2 (usage limitation)
- `test_rule_78_space_combat.py::test_combat_with_sustain_damage_units()` - Rule 87.4 (space combat)

## Sub-Rules Analysis

### 87.1 - Hit Cancellation ✅ IMPLEMENTED
- **Status**: ✅ Complete
- **Implementation**: `Unit.sustain_damage()` method, `CombatResolver.resolve_sustain_damage_abilities()`
- **Tests**: `test_sustain_damage_activation()`, `test_sustain_damage_prevents_destruction()`

### 87.2 - Damaged Unit Function ✅ IMPLEMENTED
- **Status**: ✅ Complete
- **Implementation**: Unit damage state tracking, `has_sustain_damage()` checks damage state
- **Tests**: `test_sustain_damage_invalid_unit()`, `test_sustain_damage_can_only_be_used_once()`

### 87.3 - Repair Requirement ✅ IMPLEMENTED
- **Status**: ✅ Complete
- **Implementation**: `Unit.repair()` method, status phase integration
- **Tests**: `test_sustain_damage_repair()`

### 87.4 - Usage Timing ✅ IMPLEMENTED
- **Status**: ✅ Complete
- **Implementation**: Combat resolver integration, space cannon integration
- **Tests**: `test_resolve_sustain_damage_abilities()`, space combat tests

### 87.5 - Direct Destruction Exception 🔄 PARTIAL
- **Status**: 🔄 Needs validation - direct destruction effects may need explicit handling
- **Implementation**: Basic framework exists but needs verification

### 87.6 - Faction Technology Enhancement ❌ NOT IMPLEMENTED
- **Status**: ❌ Missing - Barony of Letnev "Non-Euclidean Shielding" enhancement
- **Implementation**: Needs faction-specific technology system

## Related Rules
- Rule 1: Abilities ✅ (implemented via unit abilities system)
- Rule 42: Ground Combat ✅ (integrated)
- Rule 78: Space Combat ✅ (integrated)

## Remaining Work (15%)
1. **Rule 87.5 Validation**: Verify direct destruction effects properly bypass sustain damage
2. **Rule 87.6 Implementation**: Add Barony of Letnev faction technology enhancement
3. **Edge Case Testing**: Additional test coverage for complex scenarios

## Action Items
- [x] ✅ Analyze Sustain Damage mechanics
- [x] ✅ Review damage state management
- [x] ✅ Examine repair timing and methods
- [x] ✅ Study hit assignment interactions
- [ ] 🔄 Investigate faction-specific enhancements
- [ ] 🔄 Validate direct destruction exception handling
