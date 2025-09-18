# Rule 58: SPACE DOCK Analysis

## Category Overview
**Rule Type**: Structure/Unit  
**Complexity**: Medium  
**Dependencies**: High (Construction, Producing Units, Structures, Planets)

## Raw LRR Text

### 79 SPACE DOCK
A space dock is a structure that allows players to produce units.

79.1 Each space dock has a "Production" ability that indicates the number of units it can produce.

79.2 The primary way in which players acquire space docks is by resolving either the primary or secondary abilities of the "Construction" strategy card.

79.3 Space docks are placed on planets. Each planet can have a maximum of one space dock.

79.4 If a player's space dock is ever on a planet that does not contain any of their ground forces and contains a unit that belongs to another player, that space dock is destroyed.

a The Clan of Saar's "Floating Factory" faction-specific space dock is destroyed when it is blockaded; that is to say, when it is in a system with another player's ships and none of the Clan of Saar's ships.

RELATED TOPICS: Construction, Producing Units, Structures

### Related Structure Rules (85.1, 85.4)
85.1 Structures are always placed on planets.
a The Clan of Saar's "Floating Factory" faction-specific space dock is placed in a system's space area.

85.4 A player can have a maximum of one space dock on each planet.

## Sub-Rules Analysis

### 79.1 - Production Ability ✅ IMPLEMENTED
- **Status**: Fully implemented
- **Implementation**: `UnitStats.production: int = 2` for space_dock
- **Test Coverage**: ✅ `test_unit.py::test_production_ability()`
- **Notes**: Base space dock has production value of 2

### 79.2 - Acquisition via Construction ⚠️ PARTIALLY IMPLEMENTED
- **Status**: Construction strategy card exists but space dock placement logic needs verification
- **Implementation**: Strategy card system exists, but specific space dock placement mechanics unclear
- **Test Coverage**: ❌ No specific tests for space dock construction
- **Notes**: Requires integration with Construction strategy card

### 79.3 - Placement Rules ⚠️ PARTIALLY IMPLEMENTED
- **Status**: Planet placement concept exists, but specific space dock placement validation unclear
- **Implementation**: Structure placement system exists in principle
- **Test Coverage**: ❌ No tests for space dock placement restrictions
- **Notes**: One space dock per planet rule needs enforcement

### 79.4 - Destruction Conditions ❌ NOT IMPLEMENTED
- **Status**: Not implemented
- **Implementation**: No logic for space dock destruction based on ground force presence
- **Test Coverage**: ❌ No tests for space dock destruction
- **Notes**: Critical rule for space dock vulnerability

### 79.4a - Clan of Saar Exception ❌ NOT IMPLEMENTED
- **Status**: Not implemented
- **Implementation**: No faction-specific space dock handling
- **Test Coverage**: ❌ No tests for Floating Factory mechanics
- **Notes**: Requires faction-specific implementation

## Related Topics

### Direct Dependencies
- **Construction Strategy Card**: Primary acquisition method
- **Producing Units (67)**: Core functionality of space docks
- **Structures (85)**: Space docks are structures with placement rules
- **Planets**: Space docks are placed on planets

### Indirect Dependencies
- **Ground Forces**: Required for space dock protection
- **Tactical Actions**: Production occurs during tactical actions
- **Blockaded**: Affects Clan of Saar's Floating Factory

## Test References

### Current Test Coverage
- ✅ `test_unit.py::test_production_ability()` - Tests space dock production value
- ✅ `test_combat.py` - Tests space dock as non-combat unit
- ✅ `test_unit.py` - Tests space dock unit abilities

### Missing Test Scenarios
- ❌ Space dock placement on planets
- ❌ One space dock per planet restriction
- ❌ Space dock destruction when undefended
- ❌ Construction strategy card space dock placement
- ❌ Clan of Saar Floating Factory mechanics
- ❌ Space dock production during tactical actions
- ❌ Space dock blockade scenarios

## Implementation Files

### Core Implementation
- `src/ti4/core/unit_stats.py` - Space dock stats (production=2, cost=4)
- `src/ti4/core/unit.py` - Unit class with production ability methods
- `src/ti4/core/system.py` - Planet-based unit placement

### Supporting Systems
- `src/ti4/core/structures.py` - Structure placement logic (if exists)
- `src/ti4/core/strategy_cards.py` - Construction strategy card
- `src/ti4/core/production.py` - Production system integration

### Test Files
- `tests/test_unit.py` - Unit ability tests
- `tests/test_combat.py` - Non-combat unit verification

## Notable Details

### Implementation Strengths
1. **Basic Unit Stats**: Space dock correctly defined with production=2
2. **Production Ability**: Unit production method exists and tested
3. **Non-Combat Status**: Correctly identified as non-combat unit
4. **Cost Definition**: Proper cost value (4 resources)

### Areas Needing Attention
1. **Placement System**: No clear space dock placement validation
2. **Destruction Logic**: Missing vulnerability mechanics
3. **Construction Integration**: Unclear how Construction strategy card places space docks
4. **Faction Specifics**: No Clan of Saar Floating Factory implementation
5. **Planet Restrictions**: One per planet rule not enforced

### Critical Gaps
1. **Space Dock Destruction**: Core vulnerability mechanic missing
2. **Placement Validation**: No enforcement of placement rules
3. **Faction Variants**: Clan of Saar special case not handled

## Action Items

### High Priority
1. **Implement space dock destruction logic** - When undefended by ground forces
2. **Add space dock placement validation** - One per planet restriction
3. **Integrate with Construction strategy card** - Space dock placement mechanics

### Medium Priority
4. **Implement Clan of Saar Floating Factory** - Faction-specific space dock variant
5. **Add comprehensive space dock tests** - Placement, destruction, production scenarios
6. **Validate production integration** - Ensure space docks work in tactical actions

### Low Priority
7. **Add space dock blockade mechanics** - For Floating Factory destruction
8. **Implement structure placement system** - General structure management

## Priority Assessment

**Overall Priority**: High  
**Implementation Status**: ~40% Complete  
**Risk Level**: Medium

Space docks are fundamental to the production system and have specific placement and vulnerability rules that are currently missing. The basic unit functionality exists, but the strategic placement and destruction mechanics need implementation to ensure proper game balance and rule compliance.