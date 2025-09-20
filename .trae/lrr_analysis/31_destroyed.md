# Rule 31: DESTROYED - Analysis

## Category Overview
**Rule Type:** Core Combat Mechanic
**Priority:** HIGH
**Status:** PARTIALLY IMPLEMENTED
**Complexity:** Medium

## Raw LRR Text
```
31 DESTROYED
When a unit is destroyed, it is returned to its owner's reinforcements.

31.1 When a player assigns hits that were produced against their units, that player chooses a number of their units to be destroyed equal to the number of hits produced against those units.

31.2 If a player's unit is removed from the board by a game effect, it is not treated as being destroyed; effects that trigger when a unit is destroyed are not triggered.

RELATED TOPICS: Anti-Fighter Barrage, Bombardment, Space Cannon, Space Combat, Sustain Damage
```

## Sub-Rules Analysis

### 31.1 Hit Assignment and Destruction
- **Status:** IMPLEMENTED
- **Description:** Player choice in hit assignment to units
- **Implementation:** Found in `combat.py` with `assign_hits_by_player_choice()` and validation methods

### 31.2 Removal vs Destruction Distinction
- **Status:** NOT IMPLEMENTED
- **Description:** Distinguishes between destruction (triggers effects) and removal (no triggers)
- **Gap:** No clear distinction in codebase between removal types

## Related Topics
- Anti-Fighter Barrage
- Bombardment
- Space Cannon
- Space Combat
- Sustain Damage

## Dependencies
- Combat system (hit resolution)
- Unit abilities (sustain damage)
- Reinforcement pools
- Effect triggering system
- Player choice mechanics

## Test References

### Existing Tests
- `test_combat.py`: Hit assignment validation, sustain damage prevention
- `test_system.py`: Unit removal from space
- `test_integration.py`: Unit removal mechanics
- Multiple destroyer unit tests (combat scenarios)

### Missing Tests
- Destruction vs removal distinction
- Reinforcement return mechanics
- Destruction effect triggers
- Edge cases for hit assignment

## Implementation Files

### Core Implementation
- `src/ti4/core/combat.py`: Hit assignment and resolution
- `src/ti4/core/unit.py`: Unit abilities and stats
- `src/ti4/core/system.py`: Unit removal methods

### Missing Implementation
- Reinforcement pool management
- Destruction effect system
- Removal vs destruction logic
- Unit destruction event system

## Notable Implementation Details

### Well Implemented
- Hit assignment with player choice
- Hit assignment validation
- Sustain damage integration
- Basic unit removal from systems

### Gaps and Issues
- No reinforcement pool tracking
- Missing destruction vs removal distinction
- No destruction effect triggering system
- Limited unit lifecycle management
- No formal unit destruction events

## Action Items

1. **Implement reinforcement pool system** - Track units returned after destruction
2. **Add destruction vs removal logic** - Distinguish between destruction and removal effects
3. **Create destruction event system** - Handle effects that trigger on unit destruction
4. **Enhance unit lifecycle management** - Proper tracking of unit states and transitions
5. **Add reinforcement return mechanics** - Automatic return of destroyed units to pools
6. **Implement destruction effect triggers** - System for abilities that activate on destruction
7. **Add comprehensive destruction tests** - Cover all destruction scenarios and edge cases
8. **Create unit removal validation** - Ensure proper handling of different removal types
9. **Add destruction logging and tracking** - Monitor unit destruction for game state
10. **Implement destruction-related abilities** - Handle units with destruction-triggered effects

## Priority Assessment
**MEDIUM-HIGH** - Critical for combat resolution but partially functional. Missing reinforcement management and effect distinction impacts game state integrity and strategic depth.
