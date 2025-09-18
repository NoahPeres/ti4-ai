# Rule 27: CUSTODIANS TOKEN - Analysis

## Category Overview
**Rule Type**: Game Token/Mechanic  
**Priority**: HIGH  
**Complexity**: MEDIUM  
**Dependencies**: Mecatol Rex, Influence, Victory Points, Agenda Phase, Ground Forces  

## Raw LRR Text
```
27 CUSTODIANS TOKEN	
The custodians token begins each game on Mecatol Rex. The token represents the caretakers that safeguard the seat of the empire until such time as the galactic council can be reconvened.

27.1 Units can move into the system that contains Mecatol Rex following normal rules; however, players cannot commit ground forces to land on Mecatol Rex until the custodians token is removed from the planet.

27.2 Before the "Commit Ground Forces" step of an invasion, the active player can remove the custodians token from Mecatol Rex by spending six influence. Then, that player must commit at least one ground force to land on the planet.
a	If a player cannot commit ground forces to land on Mecatol Rex, they cannot remove the custodians token.

27.3 When a player removes the custodians token from Mecatol Rex, they take the token from the game board and place it in their play area. Then, they gain one victory point.

27.4 After a player removes the custodians token from Mecatol Rex, the agenda phase is added to all subsequent game rounds, including the game round during which the custodians token was removed from Mecatol Rex.

RELATED TOPICS: Agenda Phase, Influence, Victory Points
```

## Sub-Rules Analysis

### 27.1 Movement Restriction to Mecatol Rex
**Status**: ❌ NOT IMPLEMENTED  
**Implementation**: No custodians token system or Mecatol Rex landing restrictions  
**Tests**: No tests for ground force landing restrictions  
**Notes**: Core mechanic preventing ground force landing until token removal missing  

### 27.2 Token Removal via Influence Spending
**Status**: ❌ NOT IMPLEMENTED  
**Implementation**: No influence spending system for custodians token removal  
**Tests**: No tests for influence spending or token removal  
**Notes**: Requires 6 influence spending + mandatory ground force commitment  

### 27.2a Ground Force Commitment Requirement
**Status**: ❌ NOT IMPLEMENTED  
**Implementation**: No validation for ground force availability during token removal  
**Tests**: No tests for ground force commitment validation  
**Notes**: Must have available ground forces to remove token  

### 27.3 Victory Point Award
**Status**: ⚠️ PARTIAL  
**Implementation**: Victory point system exists but not connected to custodians token  
**Tests**: Victory point tests exist but not for custodians token  
**Notes**: Basic VP system exists but needs custodians token integration  

### 27.4 Agenda Phase Activation
**Status**: ❌ NOT IMPLEMENTED  
**Implementation**: No agenda phase system or game round modification  
**Tests**: No tests for agenda phase activation  
**Notes**: Critical game state change - enables political gameplay  

## Related Topics
- **Agenda Phase** (Rule 8): Political voting system activated by token removal
- **Influence** (Rule 47): Currency for removing custodians token
- **Victory Points** (Rule 98): Reward for removing token
- **Mecatol Rex** (Rule 54): Central planet protected by token
- **Invasion** (Rule 49): Ground force landing mechanics
- **Ground Forces** (Rule 43): Units that must be committed

## Dependencies
- **Mecatol Rex System**: ❌ Missing (special planet mechanics)
- **Influence System**: ⚠️ Partial (basic influence exists)
- **Victory Points**: ✅ Implemented (basic VP tracking)
- **Agenda Phase**: ❌ Missing (political system)
- **Ground Forces**: ✅ Implemented (basic unit system)
- **Game Round System**: ⚠️ Partial (basic phases exist)

## Test References

### Existing Tests
- `test_victory_conditions.py`: Victory point tracking and awarding
- `test_game_logger.py`: References to "mecatol_rex" system ID
- `test_enhanced_exceptions.py`: Error handling with Mecatol Rex context
- `test_scenario_library.py`: Sol infantry on Mecatol Rex scenario

### Missing Tests
- Custodians token placement and removal
- Influence spending for token removal
- Ground force landing restrictions on Mecatol Rex
- Victory point award for token removal
- Agenda phase activation after token removal
- Ground force commitment validation

## Implementation Files

### Core Implementation
- Victory point system: ✅ Exists in game state
- Influence system: ⚠️ Basic implementation exists
- Ground forces: ✅ Unit system exists

### Missing Implementation
- Custodians token entity and mechanics
- Mecatol Rex special planet properties
- Agenda phase system
- Token removal validation logic
- Game round modification system

## Notable Implementation Details

### Well-Implemented
- **Victory Point System**: Comprehensive VP tracking and awarding
- **Basic Unit System**: Ground forces exist and can be managed
- **Game State Management**: Foundation exists for token tracking
- **System References**: Mecatol Rex referenced in various contexts

### Implementation Gaps
- **Token System**: No custodians token entity or mechanics
- **Landing Restrictions**: No prevention of ground force landing
- **Influence Spending**: No connection between influence and token removal
- **Agenda Phase**: Complete absence of political system
- **Game Flow Control**: No mechanism to modify game rounds

## Action Items

1. **Create custodians token entity** - Implement token with placement and removal mechanics
2. **Add Mecatol Rex special properties** - Implement landing restrictions and token tracking
3. **Implement influence spending system** - Connect influence to token removal (6 influence cost)
4. **Add ground force landing validation** - Prevent landing until token removed
5. **Create agenda phase system** - Implement political voting mechanics
6. **Add token removal rewards** - Connect token removal to victory point award
7. **Implement game round modification** - Add agenda phase to subsequent rounds
8. **Add ground force commitment validation** - Ensure forces available before token removal
9. **Create comprehensive token tests** - Cover all custodians token scenarios
10. **Integrate with invasion system** - Connect token removal to invasion mechanics

## Priority Assessment
**HIGH** - Custodians token is a fundamental game mechanic that controls access to Mecatol Rex and activates the political game (agenda phase). Currently completely unimplemented despite being central to game progression.