# Rule 29: DEFENDER - Analysis

## Category Overview
**Rule Type:** Combat Mechanics
**Priority:** MEDIUM
**Implementation Status:** PARTIALLY IMPLEMENTED

## Raw LRR Text
```
29 DEFENDER
During combat, the active player is the attacker.

RELATED TOPICS: Attacker, Invasion, Nebula, Space Combat
```

## Sub-Rules Analysis

### 29.1 Combat Role Definition
**Status:** ✅ IMPLEMENTED
**Implementation:** The concept is implicit in combat system - active player initiates combat
**Details:** The rule defines defender by exclusion (non-active player in combat)

## Related Topics
- **Attacker (Rule 13):** Defines active player as attacker during combat
- **Invasion (Rule 49):** Ground combat where defender role applies
- **Nebula:** Environmental effects that may affect combat roles
- **Space Combat (Rule 78):** Primary combat type where defender role is relevant

## Dependencies
- **Active Player (Rule 4):** Must be established to determine attacker/defender
- **Combat System:** Requires combat mechanics to be functional
- **Turn Order:** Initiative system determines who is active player

## Test References

### Existing Tests
- `test_combat.py`: Basic combat mechanics testing
  - Line 161: Combat dice verification for non-combat units

### Missing Tests
- Defender role identification in space combat
- Defender role identification in ground combat
- Defender-specific abilities and timing
- Multi-player combat defender determination
- Retreat mechanics for defenders vs attackers

## Implementation Files

### Existing Implementation
- `src/ti4/core/combat.py`: Combat system with participant tracking
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
