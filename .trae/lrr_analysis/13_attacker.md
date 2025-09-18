# Rule 13: ATTACKER

## Category Overview
**Rule Type:** Combat Role Definition  
**Priority:** High  
**Complexity:** Low  
**Implementation Status:** Partially Implemented  

Rule 13 defines the fundamental combat role assignment in TI4, establishing that the active player is always the attacker during combat situations.

## Sub-Rules Analysis

### 13.0 - Attacker Role Definition
**Raw LRR Text:**
> "During combat, the active player is the attacker."

**Analysis:**
- Simple but fundamental rule for combat resolution
- Active player = attacker in all combat scenarios (space combat, ground combat)
- Determines combat initiative, retreat options, and ability timing
- Critical for proper combat flow and rule interactions

**Priority:** High - Core combat mechanic affecting all combat scenarios

## Related Topics
- **Defender:** The non-active player in combat situations
- **Invasion:** Ground combat where active player attacks defending forces
- **Space Combat:** Space battles where active player is the attacker

## Dependencies
- Active player tracking system
- Combat resolution system
- Turn order and initiative mechanics
- Retreat mechanics (attacker restrictions)
- Combat timing and ability resolution order

## Test References
**Current Test Coverage:** Basic active player tracking exists
- `test_game_controller.py`: Tests active player tracking
- `test_diagnostic_tools.py`: Tests active player validation
- `test_tactical_action.py`: Uses active player in tactical actions
- No specific tests for attacker role in combat scenarios

## Implementation Files
**Current Implementation Status:** Partially Implemented
- Active player tracking exists in game controller
- Combat system exists but may not explicitly use attacker/defender roles
- `src/ti4/core/combat.py`: Combat resolution system
- `tests/test_combat.py`: Combat testing framework
- Missing explicit attacker/defender role assignment in combat

## Action Items

1. **Verify Combat Role Assignment**
   - Ensure combat system correctly identifies attacker as active player
   - Validate that all combat scenarios respect this rule
   - Check space combat and ground combat implementations

2. **Implement Explicit Role Tracking**
   - Add attacker/defender role properties to combat instances
   - Ensure roles are properly assigned at combat start
   - Make roles accessible for ability and timing resolution

3. **Update Combat Resolution Logic**
   - Ensure attacker goes first in relevant combat steps
   - Implement attacker-specific retreat restrictions
   - Handle attacker priority in ability timing

4. **Add Combat Role Tests**
   - Test that active player is always attacker in space combat
   - Test that active player is always attacker in ground combat
   - Test role assignment in multi-player combat scenarios
   - Test attacker-specific mechanics (retreat restrictions, etc.)

5. **Integrate with Retreat System**
   - Ensure attacker retreat restrictions are properly implemented
   - Test that defender can retreat before attacker
   - Validate retreat announcement order

6. **Update Combat Documentation**
   - Document attacker/defender role assignment clearly
   - Explain role implications for combat resolution
   - Provide examples of role-dependent mechanics

7. **Validate Ability Timing**
   - Ensure combat abilities respect attacker/defender timing
   - Test "before combat" abilities with proper role context
   - Validate ability resolution order based on roles

8. **Test Edge Cases**
   - Test combat scenarios with multiple defending players
   - Validate role assignment in complex tactical actions
   - Test role consistency across combat rounds

9. **Integration Testing**
   - Test attacker role in full tactical action sequences
   - Validate role assignment with space cannon interactions
   - Test role consistency with bombardment mechanics

10. **Performance Validation**
    - Ensure role assignment doesn't impact combat performance
    - Validate efficient role lookup during combat resolution
    - Test role assignment in high-frequency combat scenarios