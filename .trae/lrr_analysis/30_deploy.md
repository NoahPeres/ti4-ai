# Rule 30: DEPLOY - Analysis

## Category Overview
**Rule Type:** Unit Abilities  
**Priority:** MEDIUM-HIGH  
**Implementation Status:** PARTIALLY IMPLEMENTED  

## Raw LRR Text
```
30 DEPLOY
Some units have deploy abilities. Deploy abilities are indicated by the "Deploy" header and provide the means to place specific units on the game board without producing them as normal.

30.1 A player can use a unit's deploy ability when the ability's conditions are met to place that unit on the game board.
a A player does not have to spend resources to deploy a unit unless otherwise specified.

30.2 A player can only resolve a deploy ability to place a unit that is in their reinforcements.
a If there are no units that have a deploy ability in a player's reinforcements, the deploy ability cannot be used.

30.3 A unit's deploy ability can be resolved only once per timing window.

RELATED TOPICS: Abilities, Mechs, Reinforcements
```

## Sub-Rules Analysis

### 30.1 Deploy Ability Usage
**Status:** 🔶 PARTIALLY IMPLEMENTED  
**Implementation:** Unit has deploy flag but no deployment mechanics  
**Details:** Conditions and placement logic not implemented

### 30.1.a Resource-Free Deployment
**Status:** ❌ NOT IMPLEMENTED  
**Implementation:** No cost system for deploy abilities  
**Details:** Deploy should bypass normal resource costs

### 30.2 Reinforcement Requirement
**Status:** ❌ NOT IMPLEMENTED  
**Implementation:** No reinforcement validation for deploy  
**Details:** Must check unit availability in reinforcements

### 30.2.a Availability Check
**Status:** ❌ NOT IMPLEMENTED  
**Implementation:** No validation of deploy unit availability  
**Details:** Cannot deploy if no units with deploy ability in reinforcements

### 30.3 Timing Window Restriction
**Status:** ❌ NOT IMPLEMENTED  
**Implementation:** No timing window tracking for deploy abilities  
**Details:** Each deploy ability can only be used once per timing window

## Related Topics
- **Abilities:** General ability system framework
- **Mechs (Rule 55):** Primary units with deploy abilities
- **Reinforcements:** Unit pool management system

## Dependencies
- **Unit Abilities System:** Must support deploy ability detection
- **Reinforcements System:** Must track available units
- **Timing System:** Must track timing windows for ability usage
- **Resource System:** Must handle resource-free placement

## Test References

### Existing Tests
- `test_unit.py`: Deploy ability detection
  - Lines 105-116: Basic deploy ability identification for mechs
  - Lines 232-233: Deploy ability verification in comprehensive tests

### Missing Tests
- Deploy ability activation and placement
- Reinforcement validation for deploy
- Timing window restrictions
- Resource cost bypassing
- Deploy condition checking
- Multiple deploy attempts prevention

## Implementation Files

### Existing Implementation
- `src/ti4/core/unit.py`: Deploy ability detection
  - `Unit.has_deploy()`: Returns boolean for deploy capability
- `src/ti4/core/unit_stats.py`: Deploy ability flag
  - `UnitStats.deploy`: Boolean flag for deploy capability
  - Mech units have deploy=True in stats

### Missing Implementation
- Deploy ability activation system
- Reinforcement validation logic
- Timing window tracking
- Deploy placement mechanics
- Condition checking system

## Notable Implementation Details

### Well-Implemented
- Deploy ability detection for mechs
- Unit stats system with deploy flag
- Comprehensive unit ability testing framework

### Gaps
- **No deploy activation system:** Cannot actually use deploy abilities
- **Missing reinforcement integration:** No validation of unit availability
- **No timing restrictions:** Can't enforce once-per-timing-window rule
- **No placement mechanics:** No system to place deployed units
- **Missing condition system:** No way to check deploy ability conditions
- **No resource bypass:** Deploy still requires normal production costs

## Action Items

1. **Create deploy ability activation system** with condition checking
2. **Implement reinforcement validation** for deploy abilities
3. **Add timing window tracking** to prevent multiple uses
4. **Create deploy placement mechanics** for unit positioning
5. **Implement resource-free deployment** bypassing normal costs
6. **Add deploy condition system** for ability-specific requirements
7. **Create comprehensive deploy tests** covering all scenarios
8. **Integrate deploy with game actions** and turn structure
9. **Add deploy UI/UX elements** for player interaction
10. **Document deploy mechanics** in game rules and help system

## Priority Assessment
**MEDIUM-HIGH Priority** - Deploy abilities are important for:
- Mech unit functionality (core game mechanic)
- Strategic flexibility and positioning
- Faction-specific abilities and balance
- Advanced gameplay scenarios

While basic unit detection works, the complete absence of deployment mechanics significantly impacts gameplay depth and unit utility.