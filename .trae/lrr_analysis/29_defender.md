# Rule 29: DEFENDER - Analysis and Implementation

## Category Overview
**Rule Type:** Combat Mechanics
**Priority:** MEDIUM
**Implementation Status:** ✅ IMPLEMENTED

## Raw LRR Text
```
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

#### 1. Retreat Priority (Rule 67.2)
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
  - `get_ground_combat_defender_id()`: Returns defender ID for ground combat

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
- **Status**: Basic retreat functionality exists but defender-first priority not explicitly implemented
- **Location**: `RetreatManager` class exists but needs defender priority logic

#### Nebula Combat Bonus
- **Status**: Not yet implemented
- **Requirement**: +1 combat modifier for defenders in nebula systems
- **Note**: Nebula system type and combat modifiers need to be implemented

## Test Coverage

### ✅ Comprehensive Test Suite
**File**: `tests/test_rule_29_defender.py`

#### Test Cases Implemented:
1. **Basic Defender Identification**
   - `test_defender_is_non_active_player_space_combat`
   - `test_defender_is_non_active_player_ground_combat`

2. **Multi-Player Combat**
   - `test_multiple_defenders_in_space_combat`
   - `test_ground_combat_defender_with_multiple_planets`

3. **Edge Cases**
   - `test_no_combat_raises_error`
   - `test_single_player_no_defender`
   - `test_defender_identification_with_mixed_units`

4. **Combat Role Consistency**
   - `test_attacker_defender_roles_consistent`
   - `test_ground_combat_roles_consistent`

5. **Integration Tests**
   - `test_defender_role_in_actual_combat_scenario`
   - `test_defender_changes_with_active_player`

### Test Results
- **Status**: All 11 tests passing ✅
- **Coverage**: Core defender identification functionality fully tested
- **Validation**: Confirms Rule 29 implementation is correct

## Rule Compliance

### ✅ Fully Compliant
- **Core Definition**: Non-active player correctly identified as defender
- **Space Combat**: Defender identification works correctly
- **Ground Combat**: Defender identification works correctly
- **Multi-Player**: Multiple defenders handled appropriately

### 🔄 Pending Implementation
- **Retreat Priority**: Defender-first retreat announcement
- **Nebula Bonus**: +1 combat modifier for defenders in nebula systems

## Integration Points

### Related Rules
- **Rule 13 (ATTACKER)**: Complementary rule defining active player as attacker
- **Rule 67 (RETREAT)**: Defender retreat priority mechanics
- **Rule 78 (SPACE COMBAT)**: Combat roll order and defender bonuses
- **Rule 59 (NEBULA)**: Defender combat bonus in nebula systems

### System Dependencies
- **CombatRoleManager**: Core defender identification logic
- **RetreatManager**: Retreat priority implementation needed
- **System/Anomaly**: Nebula detection for combat bonuses
- **CombatResolver**: Combat modifier application

## Conclusion

Rule 29 (DEFENDER) is **substantially implemented** with core functionality complete and comprehensive test coverage. The basic defender identification mechanics work correctly for both space and ground combat scenarios.

**Remaining work**:
1. Implement defender-first retreat priority
2. Add nebula combat bonus for defenders
3. These are enhancements to the core rule rather than fundamental requirements

The implementation correctly follows the LRR definition that "the non-active player is the defender" in all combat scenarios.
  - `CombatInitiator.get_combat_participants()`: Groups units by owner
  - Combat mechanics present but role distinction unclear

### Missing Implementation
- Explicit defender/attacker role assignment
- Defender-specific combat abilities
- Role-based combat timing and restrictions

## Notable Implementation Details

### Well-Implemented
- Combat participant identification system
- Basic combat mechanics framework
- Unit combat capabilities

### Gaps
- **No explicit defender role tracking:** Combat system doesn't distinguish attacker/defender
- **Missing role-based mechanics:** No defender-specific abilities or restrictions
- **Unclear combat initiation:** Active player determination in combat context
- **No retreat mechanics:** Defender retreat rules not implemented

## Action Items

1. **Add explicit attacker/defender role tracking** to combat system
2. **Implement defender-specific combat mechanics** and timing rules
3. **Create defender role identification** in CombatInitiator class
4. **Add defender retreat mechanics** with proper restrictions
5. **Implement role-based ability timing** (defender announces retreats first)
6. **Create comprehensive defender tests** covering all combat scenarios
7. **Add multi-player combat** defender determination logic
8. **Implement nebula effects** on defender roles if applicable
9. **Add defender-specific UI indicators** for combat clarity
10. **Document combat role mechanics** in game rules and help system

## Priority Assessment
**MEDIUM Priority** - While combat roles are fundamental, the basic combat system works without explicit role distinction. However, proper implementation is needed for:
- Retreat mechanics (defenders retreat first)
- Role-specific abilities
- Tournament/competitive play accuracy
- Advanced combat scenarios
