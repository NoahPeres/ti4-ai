# Rule 96: UNITS Analysis

## Category Overview
**Rule Type**: Core Game Mechanics
**Scope**: Unit representation, types, and supply management
**Related Systems**: Production, reinforcements, fleet management, tokens

## Raw LRR Text
```
96 UNITS
A unit is represented by a plastic figure.
96.1 There are three types of units: ships, ground forces, and structures.
96.2 Each color of plastic comes with the following units:
• 10 Fighters
• 4 Carriers
• 5 Dreadnoughts
• 1 Flagship
• 4 Mechs
• 3 Space Docks
• 6 PDS units
• 8 Destroyers
• 8 Cruisers
• 2 War Suns
• 12 Infantry
96.3 Units exist either on the game board or in a player's reinforcements.
```

## Sub-Rules Analysis

### 96.1 - Unit Types (✅ Implemented)
**Status**: Fully implemented
**Implementation**: `UnitType` enum in `constants.py` defines all unit types
**Coverage**: Ships, ground forces, and structures properly categorized

### 96.2 - Unit Supply Limits (❌ Not Implemented)
**Status**: Not implemented
**Missing**: No enforcement of plastic piece limits per faction
**Impact**: Players could theoretically exceed physical game limits
**Required**: Supply tracking and validation system

### 96.3 - Unit Location States (⚠️ Partially Implemented)
**Status**: Partially implemented
**Current**: Units can be placed on board via various systems
**Missing**: Explicit reinforcement pool management and tracking
**Gap**: No clear distinction between "on board" vs "in reinforcements"

## Related Topics
- **Fighter Tokens (Rule 36)**: Token representation for fighters
- **Infantry Tokens (Rule 46)**: Token representation for infantry
- **Producing Units (Rule 67)**: Unit creation and supply limitations
- **Components (Rule 23)**: Physical component limitations and substitutions
- **Captured Units (Rule 17)**: Unit capture and reinforcement mechanics

## Test References

### Current Test Coverage
- `test_unit.py`: Unit creation, stats, and ability validation
- `test_fleet_management.py`: Fleet composition and limits
- `test_tactical_action.py`: Unit placement and movement
- `constants.py`: Unit type enumeration

### Missing Test Scenarios
- Unit supply limit enforcement
- Reinforcement pool management
- Plastic piece vs token distinction
- Unit removal to reinforcements when supply exceeded
- Fighter/infantry token replacement rules

## Implementation Files

### Core Implementation
- `src/ti4/core/unit.py`: Unit class with stats and abilities
- `src/ti4/core/constants.py`: UnitType enumeration
- `src/ti4/core/unit_stats.py`: Unit statistics and abilities
- `src/ti4/core/fleet.py`: Fleet management (partial)

### Supporting Files
- `UNIT_ABILITIES_IMPLEMENTATION.md`: Unit ability matrix
- Various test files for unit mechanics

## Notable Details

### Strengths
- Comprehensive unit type system with proper enumeration
- Well-implemented unit statistics and abilities
- Good test coverage for basic unit functionality
- Clear separation of unit types (ships, ground forces, structures)

### Areas Needing Attention
- No supply limit enforcement (critical for game balance)
- Missing reinforcement pool management
- No distinction between plastic pieces and tokens
- Lack of unit removal/replacement mechanics when supply exceeded

## Action Items

### High Priority
1. **Implement supply limit tracking** - Track available units per faction
2. **Add reinforcement pool management** - Explicit on-board vs reinforcement states
3. **Create unit supply validation** - Prevent exceeding physical limits

### Medium Priority
4. **Implement token/plastic distinction** - Fighter and infantry token mechanics
5. **Add unit removal mechanics** - Automatic removal when supply exceeded
6. **Enhance test coverage** - Supply limits and reinforcement scenarios

### Low Priority
7. **Add supply limit configuration** - Configurable limits per faction/unit type
8. **Implement supply warnings** - Alert when approaching limits

## Priority Assessment
**Priority**: High
**Implementation Status**: 40%
**Rationale**: Core unit representation works, but missing critical supply management that affects game balance and rule compliance. Physical component limitations are fundamental to TI4 gameplay.
