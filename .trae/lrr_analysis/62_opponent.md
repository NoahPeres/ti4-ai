# LRR Rule Analysis: Rule 62 - OPPONENT

## Rule Category Overview
**Rule 62: OPPONENT** - Defines who qualifies as an opponent during combat situations and the restrictions for non-opponents.

## Raw LRR Text
```
62 OPPONENT	
During combat, a player's opponent is the other player that either has ships in the system at the start of the space combat or has ground forces on the planet at the start of a ground combat.
62.1 Players who do not have units on either side of a combat are not opponents. Those players cannot use abilities or have abilities used against them that are used against an opponent.
RELATED TOPICS: Ground Combat, Invasion, Space Combat
```

## Sub-Rules Analysis

### 62.0 Basic Opponent Definition
**Rule**: "During combat, a player's opponent is the other player that either has ships in the system at the start of the space combat or has ground forces on the planet at the start of a ground combat."

**Implementation Status**: ⚠️ PARTIALLY IMPLEMENTED
- **Code**: Basic combat participant detection exists in `src/ti4/core/combat.py`
- **Tests**: Combat participant tests in `test_combat.py`
- **Assessment**: Can identify combat participants but lacks formal opponent relationship tracking
- **Priority**: HIGH
- **Dependencies**: Requires combat system and unit ownership tracking
- **Notes**: Foundation exists but needs opponent-specific relationship management

### 62.1 Non-Opponent Restrictions
**Rule**: "Players who do not have units on either side of a combat are not opponents. Those players cannot use abilities or have abilities used against them that are used against an opponent."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No non-opponent ability restriction system
- **Tests**: No non-opponent restriction tests
- **Assessment**: Critical rule for preventing third-party interference in combat
- **Priority**: HIGH
- **Dependencies**: Requires ability system and opponent validation
- **Notes**: Important for game balance - prevents uninvolved players from affecting combat

## Related Topics
- **Ground Combat**: Determines ground combat opponents based on planet presence
- **Space Combat**: Determines space combat opponents based on system presence
- **Invasion**: Related to ground combat opponent determination
- **Combat System**: Core system that uses opponent relationships
- **Abilities**: Many abilities are restricted to use against opponents only

## Test References

### Current Test Coverage
- **Combat Participant Tests**: `test_combat.py` - basic participant identification
- **Combat Detection Tests**: Tests for when combat should occur between different players
- **Integration Tests**: Combat scenarios with multiple players
- **Utility Functions**: Helper functions for asserting combat participants

### Missing Test Scenarios
- Opponent relationship validation during combat
- Non-opponent ability restriction enforcement
- Third-party player exclusion from combat abilities
- Opponent-specific ability targeting validation
- Mixed combat scenarios with multiple non-participating players

## Implementation Files

### Core Implementation
- `src/ti4/core/combat.py` - Combat participant detection (partial)
- **MISSING**: Opponent relationship management system
- **MISSING**: Non-opponent ability restriction system
- **MISSING**: Opponent validation for ability targeting

### Supporting Files
- `tests/test_combat.py` - Combat participant tests
- `tests/test_integration.py` - Multi-player combat scenarios
- `tests/test_utils.py` - Combat participant assertion utilities
- **MISSING**: Opponent-specific test scenarios
- **MISSING**: Non-opponent restriction tests

## Notable Details

### Strengths
- Basic combat participant detection working
- Can identify multiple players in combat situations
- Integration tests cover multi-player scenarios
- Combat detection properly identifies when combat should occur

### Areas Needing Attention
- No formal opponent relationship tracking
- Missing non-opponent ability restrictions
- No validation for opponent-specific abilities
- Lack of third-party interference prevention
- No opponent-based ability targeting validation

## Action Items

### High Priority
1. **Opponent Relationship System**: Implement formal opponent tracking during combat
2. **Non-Opponent Restrictions**: Prevent non-participants from using/being targeted by opponent abilities
3. **Ability Targeting Validation**: Ensure opponent-specific abilities only target actual opponents
4. **Combat Participant Validation**: Strengthen participant identification and opponent determination

### Medium Priority
1. **Third-Party Prevention**: Implement systems to prevent uninvolved player interference
2. **Opponent-Specific Tests**: Add comprehensive test coverage for opponent mechanics
3. **Ability System Integration**: Connect opponent validation with ability system
4. **Multi-Player Combat Scenarios**: Enhance support for complex multi-player combat situations

### Low Priority
1. **Opponent Analytics**: Track opponent relationships and combat patterns
2. **Advanced Opponent Rules**: Handle edge cases and complex opponent scenarios
3. **Performance Optimization**: Optimize opponent detection for large games
4. **Documentation**: Document opponent mechanics and edge cases

## Priority Assessment
- **Overall Priority**: HIGH
- **Implementation Status**: ~30% (basic participant detection exists)
- **Blocking Dependencies**: Ability system, combat system enhancements
- **Impact**: Critical for combat integrity and game balance - prevents rule violations