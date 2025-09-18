# Rule 51: OBJECTIVES

## Category Overview
**Rule Type**: Core Victory Mechanics  
**Complexity**: High  
**Implementation Priority**: Critical  
**Dependencies**: Victory Points, Game Phases, Player State, Resources  

## Raw LRR Text
From `lrr.txt` section 61:

**61** Players can score objectives to gain victory points.

**61.1** There are two types of objective cards: public objectives and secret objectives.
- Each public objective has a "I" or "II" on the back of its card; all other objectives are secret objectives.

**61.2** Each objective card indicates a number of victory points that a player gains by scoring that objective.

**61.3** Each objective card indicates the phase during which a player can score that objective-the status, action, or agenda phases.

**61.4** Each objective card describes the requirement a player must fulfill to score that objective.

**61.5** If a player fulfills the requirement described on an objective card, they can score that objective following the timing indicated on the card, either during the action phase or the status phase.
- When a player scores an objective during the status phase, they must fulfill the requirement on the card during the "Score Objectives" step of the status phase to score that objective.
- When a player scores an objective during the action phase, they can do so at any time during that phase.
- When a player scores an objective during the agenda phase, they can do so at any time during that phase.

**61.6** A player can score a maximum of one public objective and one secret objective during each status phase.

**61.8** A player can score each objective only once during the game.

**61.9** If an objective requires a player to destroy one or more units, those units can be destroyed by producing hits against them, playing action cards, using technology, or any number of other abilities that use the "destroy" terminology.

**61.10** Players can score some objectives by spending resources, influence, or tokens, as described by the objective card.

**61.11-61.16** PUBLIC OBJECTIVES: Public objectives are revealed to all players, scored by placing control tokens, and require home system control.

**61.17-61.22** SECRET OBJECTIVES: Secret objectives are hidden until scored, players start with one, can have up to three total, and can gain more via Imperial strategy card.

## Sub-Rules Analysis

### 61.1 - Objective Types
- **Status**: ✅ Implemented
- **Location**: `objective.py` - Objective dataclass with `is_public` field
- **Test Coverage**: Good - objective creation tests exist
- **Implementation Notes**: Basic structure implemented

### 61.2 - Victory Point Values
- **Status**: ✅ Implemented
- **Location**: `objective.py` - `points` field in Objective dataclass
- **Test Coverage**: Good - victory point awarding tested
- **Implementation Notes**: Point values properly tracked

### 61.3 - Phase Timing
- **Status**: ❌ Not Implemented
- **Location**: No phase-specific scoring logic found
- **Test Coverage**: None found
- **Implementation Notes**: Phase restrictions not enforced

### 61.4-61.5 - Requirement Fulfillment
- **Status**: ⚠️ Partially Implemented
- **Location**: `CompletableObjective` abstract class, basic implementations
- **Test Coverage**: Limited - basic completion detection tested
- **Implementation Notes**: Framework exists but most objectives not implemented

### 61.6 - Scoring Limits
- **Status**: ❌ Not Implemented
- **Location**: No per-phase scoring limits
- **Test Coverage**: None found
- **Implementation Notes**: One public + one secret per status phase not enforced

### 61.8 - One-Time Scoring
- **Status**: ✅ Implemented
- **Location**: `game_state.py` - `completed_objectives` tracking
- **Test Coverage**: Good - duplicate completion prevention tested
- **Implementation Notes**: Properly prevents duplicate scoring

### 61.9 - Destruction Requirements
- **Status**: ❓ Unknown
- **Location**: No specific destruction tracking for objectives
- **Test Coverage**: None found
- **Implementation Notes**: Needs integration with combat system

### 61.10 - Resource/Influence Spending
- **Status**: ⚠️ Partially Implemented
- **Location**: `SpendResourcesObjective` stub implementation
- **Test Coverage**: Basic test exists but not functional
- **Implementation Notes**: Framework exists but not connected to resource system

### 61.11-61.16 - Public Objectives
- **Status**: ⚠️ Partially Implemented
- **Location**: `public_objectives.py` with basic implementations
- **Test Coverage**: Limited - basic structure tested
- **Implementation Notes**: Framework exists but most objectives not implemented

### 61.17-61.22 - Secret Objectives
- **Status**: ❌ Not Implemented
- **Location**: No secret objective system found
- **Test Coverage**: None found
- **Implementation Notes**: Secret objective mechanics missing

## Related Topics
- **Rule 98**: VICTORY POINTS (victory point tracking)
- **Rule 85**: STATUS PHASE (objective scoring timing)
- **Rule 2**: ACTION PHASE (action phase objective scoring)
- **Rule 24**: AGENDA PHASE (agenda phase objective scoring)
- **Rule 45**: IMPERIAL (secret objective acquisition)
- **Rule 17**: COMMAND TOKENS (objective scoring tokens)

## Dependencies
- **Victory Points**: Victory point tracking system
- **Game Phases**: Phase management for scoring timing
- **Player State**: Player resource and unit tracking
- **Control Tokens**: Token placement for scored objectives
- **Strategy Cards**: Imperial card for secret objectives
- **Combat System**: Unit destruction tracking

## Test References
### Good Test Coverage Found:
- `test_victory_conditions.py`: Comprehensive objective system testing
  - Victory point tracking and awarding
  - Objective creation and completion detection
  - Public objective implementations
  - Duplicate completion prevention
  - Victory condition checking

### Test Scenarios Covered:
1. **Basic Victory Points**: Player starts with zero, can award points
2. **Objective Structure**: Objective cards with proper data structure
3. **Completion Detection**: Basic objective completion tracking
4. **Duplicate Prevention**: Cannot complete same objective twice
5. **Victory Conditions**: 10 victory points triggers win

### Missing Test Scenarios:
1. **Phase-Specific Scoring**: No tests for phase timing restrictions
2. **Scoring Limits**: No tests for one public + one secret per status phase
3. **Secret Objectives**: No secret objective tests
4. **Resource Spending**: No functional resource spending objective tests
5. **Destruction Objectives**: No unit destruction objective tests

## Implementation Files
### Core Implementation:
- `src/ti4/core/objective.py`: Base `Objective` dataclass and `CompletableObjective` interface
- `src/ti4/core/public_objectives.py`: Basic public objective implementations
- `src/ti4/core/game_state.py`: Objective completion tracking and victory point management

### Supporting Files:
- Victory point tracking in game state
- Event system for objective completion (in usage examples)

### Missing Implementation:
- Secret objective system
- Phase-specific scoring logic
- Comprehensive objective library
- Resource/influence spending integration
- Unit destruction tracking for objectives

## Notable Implementation Details

### Strengths:
1. **Solid Foundation**: Good basic structure with Objective dataclass and completion tracking
2. **Victory Point Integration**: Proper victory point awarding and tracking
3. **Duplicate Prevention**: Cannot score same objective twice
4. **Extensible Design**: CompletableObjective interface allows easy addition of new objectives
5. **Test Coverage**: Good test coverage for implemented features

### Areas Needing Attention:
1. **Phase Timing**: No enforcement of phase-specific scoring rules
2. **Scoring Limits**: No limits on objectives per phase
3. **Secret Objectives**: Entire secret objective system missing
4. **Objective Library**: Most actual objectives not implemented
5. **Resource Integration**: Spending objectives not connected to resource system
6. **Combat Integration**: Destruction objectives not connected to combat system

### Architecture Quality:
- **Excellent**: Basic objective structure and completion tracking
- **Good**: Victory point integration and duplicate prevention
- **Needs Work**: Phase timing and scoring limits
- **Missing**: Secret objectives and comprehensive objective library

## Action Items

### High Priority:
1. **Implement Phase-Specific Scoring**: Enforce timing restrictions for objective scoring
2. **Add Scoring Limits**: Implement one public + one secret per status phase limit
3. **Create Secret Objective System**: Hidden objectives, Imperial card integration, 3-objective limit

### Medium Priority:
4. **Expand Objective Library**: Implement all Stage I and Stage II public objectives
5. **Resource Integration**: Connect spending objectives to resource system
6. **Combat Integration**: Connect destruction objectives to combat system

### Low Priority:
7. **Objective UI**: Visual feedback for objective progress and completion
8. **Objective Events**: Publish events when objectives are scored
9. **Objective History**: Track objective scoring history for replay

## Priority Assessment
**Overall Priority**: Critical - Objectives are the primary victory condition in TI4

**Implementation Status**: Partial (40%)
- Basic objective structure: ✅ Complete
- Victory point integration: ✅ Complete
- Completion tracking: ✅ Complete
- Phase timing: ❌ Missing
- Scoring limits: ❌ Missing
- Secret objectives: ❌ Missing
- Objective library: ⚠️ Minimal

**Recommended Focus**: 
1. Implement phase-specific scoring rules and limits
2. Create comprehensive secret objective system
3. Expand objective library with actual TI4 objectives
4. Integrate with resource and combat systems

The objective system has a solid foundation but is missing critical gameplay elements like phase timing, scoring limits, and the secret objective system. The basic structure is well-designed and extensible, making it a good foundation for completing the implementation.