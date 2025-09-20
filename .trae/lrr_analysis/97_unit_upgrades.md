# Rule 97: UNIT UPGRADES Analysis

## Category Overview
**Rule Type**: Technology System
**Scope**: Unit upgrade technology cards, roman numeral progression, attribute improvements
**Related Systems**: Technology research, unit stats, faction sheets

## Raw LRR Text
```
97 UNIT UPGRADES
A unit upgrade is a type of technology card.
97.1 Unit upgrades share a name with a unit that is printed on a player's faction sheet, but have a higher roman numeral. For example, a player's "Carrier I" unit is upgraded by the unit upgrade technology "Carrier II."
a The Nekro Virus player may upgrade their units with units of the same type (e.g., "dreadnought" or "infantry") even if those unit's names do not match. If the Nekro Virus gains a unit upgrade technology of the same unit type as a unit upgrade technology they already have, the previous upgrade is removed, and they must use the same Valefar Assimilator token that was used to copy the previous upgrade.
97.2 Players place unit upgrades they gain faceup on their faction sheets, covering the unit that shares a name with that upgrade card.
97.3 The white arrows next to an attribute on a faction sheet indicate that the attribute will improve when the unit is upgraded.
97.4 After a player gains a unit upgrade card, each of that player's units that correspond to that upgrade card is treated as having the attributes and abilities printed on that upgrade card. Any previous attributes of that unit, such as the one printed on that player's faction sheet, are ignored.
97.5 A mech unit card is not a technology.
```

## Sub-Rules Analysis

### 97.1 - Roman Numeral Progression (✅ Implemented)
**Status**: Fully implemented
**Implementation**: Unit upgrade constants and technology system support roman numeral naming
**Coverage**: Carrier II, Cruiser II, Dreadnought II, Fighter II, Destroyer II properly defined
**Special Case**: Nekro Virus upgrade mechanics partially implemented

### 97.2 - Faction Sheet Placement (❌ Not Implemented)
**Status**: Not implemented
**Missing**: No visual faction sheet or card placement mechanics
**Impact**: Upgrade acquisition works but lacks proper UI representation
**Required**: Faction sheet UI system with card overlay mechanics

### 97.3 - Attribute Improvement Indicators (❌ Not Implemented)
**Status**: Not implemented
**Missing**: No white arrow indicators or visual upgrade hints
**Impact**: Players cannot see which attributes will improve
**Required**: UI system showing upgrade previews and improvements

### 97.4 - Attribute Replacement (✅ Implemented)
**Status**: Fully implemented
**Implementation**: `UnitStatsProvider` with technology modifiers replaces base stats
**Coverage**: Upgraded units use new attributes, ignoring base faction sheet values
**Validation**: Comprehensive test coverage for stat replacement

### 97.5 - Mech Exception (✅ Implemented)
**Status**: Correctly implemented
**Implementation**: Mech units handled separately from technology system
**Coverage**: Mech unit cards are not treated as technologies

## Related Topics
- **Technology (Rule 90)**: Technology research and prerequisites
- **Units (Rule 96)**: Base unit types and attributes
- **Faction Sheets**: Unit base statistics and upgrade indicators
- **Nekro Virus**: Special upgrade mechanics and Valefar Assimilator
- **Mechs (Rule 55)**: Non-technology unit cards

## Test References

### Current Test Coverage
- `test_technology.py`: Technology research with unit upgrade prerequisites
- `test_fleet_management.py`: Unit upgrade stat modifications and fleet effects
- `test_integration.py`: Technology upgrade scenarios with stat changes
- `test_unit.py`: Unit upgrade stat validation (Cruiser II, Fighter II)
- `test_scenario_library.py`: Game scenarios with unit upgrades

### Missing Test Scenarios
- Faction sheet card placement mechanics
- Visual upgrade indicator testing
- Nekro Virus upgrade replacement mechanics
- Mech vs technology distinction validation
- Upgrade preview and attribute comparison

## Implementation Files

### Core Implementation
- `src/ti4/core/unit_stats.py`: `UnitStatsProvider` with technology modifiers
- `src/ti4/core/constants.py`: Unit upgrade technology constants
- `src/ti4/core/unit.py`: Unit class with technology integration
- `tests/test_technology.py`: Technology research mechanics

### Supporting Files
- `UNIT_ABILITIES_IMPLEMENTATION.md`: Unit upgrade ability matrix
- Various test files for upgrade scenarios
- Game scenario builders with technology support

## Notable Details

### Strengths
- Robust technology modifier system for stat replacement
- Comprehensive test coverage for upgrade mechanics
- Proper separation of mech units from technology system
- Good integration with unit stats and fleet management
- Support for multiple upgrade technologies per unit type

### Areas Needing Attention
- No visual faction sheet or card placement system
- Missing upgrade preview and attribute improvement indicators
- Incomplete Nekro Virus special upgrade mechanics
- No UI representation of technology card overlay
- Lack of visual feedback for upgrade effects

## Action Items

### High Priority
1. **Implement faction sheet UI system** - Visual card placement and overlay mechanics
2. **Add upgrade preview system** - Show attribute improvements before research
3. **Create upgrade indicators** - Visual arrows and improvement hints

### Medium Priority
4. **Complete Nekro Virus mechanics** - Valefar Assimilator and upgrade replacement
5. **Add upgrade comparison UI** - Before/after stat comparison
6. **Enhance test coverage** - Visual and UI upgrade mechanics

### Low Priority
7. **Add upgrade animation system** - Visual feedback for technology acquisition
8. **Implement upgrade history** - Track upgrade progression per player

## Priority Assessment
**Priority**: Medium
**Implementation Status**: 70%
**Rationale**: Core upgrade mechanics work well with proper stat replacement and technology integration. Missing primarily UI/visual elements and special faction mechanics. Functional for gameplay but lacks polish for user experience.
