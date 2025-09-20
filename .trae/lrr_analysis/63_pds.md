# Rule 63: PDS

## Category Overview
**Rule Type**: Unit/Structure Mechanics
**Complexity**: Medium
**Dependencies**: Construction Strategy Card, Space Cannon, Structures

## Raw LRR Text
```
63 PDS
A PDS (planetary defense system) is a structure that allows a player to defend their territory against invading forces.
63.1  Each PDS has the "Space Cannon" ability.
63.2 The primary way by which players acquire PDS units is by resolving either the primary or secondary ability of the "Construction" strategy card.
63.3 A PDS unit is placed on a planet. Each planet can have a maximum of two PDS units.
63.4 If a player's PDS is ever on a planet that does not contain any of their own ground forces and contains a unit that belongs to another player, that PDS is destroyed.
RELATED TOPICS: Structures, Space Cannon
```

## Sub-Rules Analysis

### 63.1 - Space Cannon Ability ✅ IMPLEMENTED
**Status**: Fully implemented
**Implementation**: Unit stats system correctly assigns space cannon ability to PDS units
**Test Coverage**: Comprehensive tests verify PDS has space cannon ability

### 63.2 - Acquisition via Construction ⚠️ PARTIALLY IMPLEMENTED
**Status**: Basic structure placement exists, strategy card integration unclear
**Implementation**: Construction strategy card mentioned in LRR but implementation status unknown
**Test Coverage**: No specific tests for PDS acquisition through Construction strategy card

### 63.3 - Placement and Limits ❌ NOT IMPLEMENTED
**Status**: Not implemented
**Implementation**: No validation for maximum 2 PDS per planet
**Test Coverage**: No tests for PDS placement limits

### 63.4 - Destruction Conditions ❌ NOT IMPLEMENTED
**Status**: Not implemented
**Implementation**: No logic for automatic PDS destruction when isolated
**Test Coverage**: No tests for PDS destruction scenarios

## Related Topics
- **Structures**: PDS is a structure type with placement rules
- **Space Cannon**: Core ability of PDS units for defensive fire
- **Construction Strategy Card**: Primary acquisition method
- **Planet Control**: Required for PDS placement and survival
- **Ground Forces**: Required for PDS survival on contested planets

## Test References

### Current Coverage
- `test_unit.py`: PDS ability detection (space cannon, planetary shield)
- `test_combat.py`: Space cannon defensive fire mechanics
- Unit stats verification for PDS attributes

### Missing Test Scenarios
- PDS acquisition through Construction strategy card
- Maximum 2 PDS per planet validation
- PDS destruction when isolated from ground forces
- PDS placement on controlled planets only
- Integration with structure placement rules

## Implementation Files

### Core Implementation
- `src/ti4/core/unit_stats.py`: PDS unit statistics and abilities
- `src/ti4/core/combat.py`: Space cannon combat mechanics
- `src/ti4/core/unit.py`: Unit ability detection methods

### Supporting Systems
- Strategy card system (Construction card implementation)
- Structure placement validation system
- Planet control tracking system
- Unit destruction mechanics

## Notable Details

### Strengths
- Solid foundation for PDS unit abilities (space cannon, planetary shield)
- Combat integration for space cannon defensive fire
- Clear unit type definition and stats

### Areas Needing Attention
- **Structure Limits**: No enforcement of 2 PDS per planet maximum
- **Acquisition System**: Construction strategy card integration unclear
- **Destruction Logic**: Missing automatic destruction when isolated
- **Placement Validation**: No verification of planet control requirements

## Action Items
1. **HIGH**: Implement PDS placement limit validation (2 per planet)
2. **HIGH**: Add PDS destruction logic when isolated from ground forces
3. **MEDIUM**: Verify Construction strategy card integration for PDS acquisition
4. **MEDIUM**: Add placement validation requiring planet control
5. **LOW**: Enhance test coverage for all PDS-specific mechanics

## Priority Assessment
**Priority**: High
**Implementation Status**: 40%
**Rationale**: PDS units have solid ability foundation but lack critical placement rules and destruction mechanics. These are fundamental to proper PDS gameplay and strategic balance.
