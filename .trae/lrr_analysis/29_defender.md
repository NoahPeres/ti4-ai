# Rule 29: DEFENDER - Analysis and Implementation

## Category Overview
**Rule Type:** Combat Mechanics
**Priority:** MEDIUM
**Implementation Status:** ✅ IMPLEMENTED

## Raw LRR Text
```text
29 DEFENDER
In a space or ground combat, the non-active player is the defender.

RELATED TOPICS: Attacker, Invasion, Nebula, Space Combat
```

## Rule Analysis

### Core Definition
- **Primary Rule**: In any combat (space or ground), the non-active player is the defender
- **Scope**: Applies to both space combat and ground combat scenarios
- **Key Principle**: Defender status is determined by activity, not by who initiated the combat

### Related Combat Mechanics

#### 1. Retreat Priority (Rule 78.4)
- Defenders announce retreats first during the "Announce Retreat" step
- If defender retreats, attacker cannot retreat in that combat round

#### 2. Combat Roll Order (Rule 78.4)
- Attacker rolls all combat dice before defender
- This sequence is important for abilities that allow rerolling opponent's dice

#### 3. Nebula Combat Bonus (Rule 59.3)
- If space combat occurs in a nebula, defender applies +1 to each combat roll of their ships
- This is a specific defender advantage in nebula systems

## Implementation Status

### ✅ Completed Implementation

#### Core Defender Identification
- **Location**: `src/ti4/core/combat.py` - `CombatRoleManager` class
- **Methods**:
  - `get_defender_id()`: Returns single defender ID for two-player combat
  - `get_defender_ids()`: Returns all defender IDs for multi-player combat
  - `get_ground_combat_defender_id(system, planet_name)`: Returns defender ID for ground combat

#### Implementation Details
```python
def get_defender_id(self, system: System) -> str:
    """Get the defender player ID (non-active player in two-player combat)."""
    attacker_id = self.get_attacker_id(system)
    # Returns non-active player as defender

def get_defender_ids(self, system: System) -> list[str]:
    """Get all defender player IDs (all non-active players in combat)."""
    # Returns all non-active players as defenders
```

### 🔄 Partial Implementation

#### Retreat Priority Mechanics
- **Status**: ✅ IMPLEMENTED via RetreatManager class
- **Location**: `RetreatManager` class with defender priority logic

#### Nebula Combat Bonus
- **Status**: Not yet implemented
- **Requirement**: +1 combat modifier for defenders in nebula systems
- **Note**: Nebula system type and combat modifiers need to be implemented

## Test Coverage

### ✅ Comprehensive Test Suite
**File**: `tests/test_rule_29_defender.py`

#### Test Cases Implemented:
Tests include:
- `test_defender_is_non_active_player_space_combat`
- `test_defender_is_non_active_player_ground_combat`
- `test_multiple_defenders_in_space_combat`
- `test_defender_role_changes_with_active_player`
- `test_defender_retreat_priority`
- `test_attacker_cannot_retreat_after_defender_announces`
- `test_attacker_can_retreat_if_defender_does_not`
- `test_no_combat_raises_error_for_defender`
- `test_defender_role_consistency_across_combat_rounds`
- `test_defender_identification_with_mixed_unit_types`
- `test_ground_combat_defender_with_multiple_planets`
- `test_get_defender_id_fails_with_multiple_defenders`

### Test Results
- **Status**: All 12 tests passing ✅
- **Coverage**: Core defender identification functionality fully tested
- **Validation**: Confirms Rule 29 implementation is correct

## Rule Compliance

### ✅ Fully Compliant
- **Core Definition**: Non-active player correctly identified as defender
- **Space Combat**: Defender identification works correctly
- **Ground Combat**: Defender identification works correctly
- **Multi-Player**: Multiple defenders handled appropriately

### 🔄 Pending Implementation
- **Nebula Bonus**: +1 combat modifier for defenders in nebula systems

## Integration Points

### Related Rules
- **Rule 13 (ATTACKER)**: Complementary rule defining active player as attacker
- **Rule 78 (SPACE COMBAT)**: Includes retreat step (e.g., 78.4) and combat sequencing
- **Rule 59 (NEBULA)**: Defender combat bonus in nebula systems

### System Dependencies
- **CombatRoleManager**: Core defender identification logic
- **RetreatManager**: ✅ IMPLEMENTED - Retreat priority functionality complete
- **System/Anomaly**: Nebula detection for combat bonuses
- **CombatResolver**: Combat modifier application

## Conclusion

Rule 29 (DEFENDER) is **substantially implemented** with core functionality complete and comprehensive test coverage. The basic defender identification mechanics work correctly for both space and ground combat scenarios.

**Remaining work**:
1. Add nebula combat bonus for defenders
2. These are enhancements to the core rule rather than fundamental requirements

The implementation correctly follows the LRR definition that "the non-active player is the defender" in all combat scenarios.
