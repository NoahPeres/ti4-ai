# Rule 56: SPEAKER

## Category Overview
**Rule Type**: Player Role & Turn Order Management  
**Complexity**: Medium  
**Implementation Priority**: High  
**Dependencies**: Turn Order System, Strategy Cards, Agenda Phase  

## Raw LRR Text
From `lrr.txt` Rule 80: SPEAKER:

**80. SPEAKER**  
The speaker is the player who has the speaker token.

**80.1** During the strategy phase, the speaker is the first player to choose a strategy card.

**80.2** During the agenda phase, the speaker reveals the top agenda card from the agenda deck before each vote. The speaker is always the last player to vote and decides which outcome to resolve if the outcomes are tied.

**80.3** During setup, the speaker prepares the objectives.

**80.4** During the status phase, the speaker reveals a public objective.

**80.5** A random player gains the speaker token during setup before the game begins.

**80.6** During the action phase, if a player resolves the primary ability on the "Politics" strategy card, that player chooses any player other than the current speaker to gain the speaker token.

**80.7** If the speaker is eliminated from the game, the speaker token is passed to the player to the speaker's left.

**Setup Process (Step 1)**:
**STEP 1-DETERMINE SPEAKER**: Randomly determine one player to gain the speaker token; that player is the speaker.

**Politics Strategy Card (Rule 66)**:
**66.1** During the action phase, if the active player has the "Politics" strategy card, they can perform a strategic action to resolve that card's primary ability.

**66.2** To resolve the primary ability on the "Politics" strategy card, the active player resolves the following effects in order:
i. The active player chooses any player that does not have the speaker token. The active player may choose themselves as long as they do not have the speaker token. The chosen player places the speaker token in their play area; they are now the speaker.
ii. The active player draws two action cards.
iii. The active player secretly looks at the top two cards of the agenda deck. Then, that player places each card on either the top or the bottom of the deck. If they place both cards on either the top or bottom, they can place them in any order.

**Related Topics**: Agenda Card, Agenda Phase, Objective Cards, Politics, Strategy Phase

## Sub-Rules Analysis

### Speaker Token Assignment (80.5, Setup Step 1)
- **Status**: ⚠️ Partially Implemented
- **Location**: No explicit speaker token system found
- **Test Coverage**: No speaker assignment tests found
- **Implementation Notes**: Random speaker assignment during setup not implemented

### Strategy Phase Priority (80.1)
- **Status**: ⚠️ Partially Implemented
- **Location**: `src/ti4/core/game_controller.py` - strategy phase turn order
- **Test Coverage**: `test_game_controller.py` - strategy phase turn order tests
- **Implementation Notes**: Turn order exists but no explicit speaker-first logic

### Agenda Phase Responsibilities (80.2)
- **Status**: ❌ Not Implemented
- **Location**: No agenda phase implementation found
- **Test Coverage**: No agenda phase tests found
- **Implementation Notes**: No agenda card revealing or voting order system

### Objective Management (80.3, 80.4)
- **Status**: ❌ Not Implemented
- **Location**: No objective management system found
- **Test Coverage**: No objective revealing tests found
- **Implementation Notes**: No speaker-controlled objective revealing

### Politics Card Speaker Transfer (80.6, 66.2)
- **Status**: ❌ Not Implemented
- **Location**: No Politics strategy card implementation found
- **Test Coverage**: No Politics card tests found
- **Implementation Notes**: No speaker token transfer mechanism

### Speaker Elimination Handling (80.7)
- **Status**: ❌ Not Implemented
- **Location**: No elimination handling found
- **Test Coverage**: No elimination tests found
- **Implementation Notes**: No speaker succession system

## Related Topics
- **Rule 3**: ACTION PHASE (active player determination)
- **Rule 4**: ACTIVE PLAYER (initiative order)
- **Rule 8**: AGENDA PHASE (speaker voting responsibilities)
- **Rule 48**: INITIATIVE ORDER (turn order determination)
- **Rule 66**: POLITICS (speaker token transfer)
- **Rule 84**: STRATEGY PHASE (speaker chooses first)

## Dependencies
- **Player Management**: For speaker token ownership (⚠️ Basic Implementation)
- **Turn Order System**: For initiative order and clockwise progression (✅ Implemented)
- **Strategy Cards**: For Politics card speaker transfer (⚠️ Basic Implementation)
- **Agenda System**: For agenda phase responsibilities (❌ Missing)
- **Objective System**: For objective revealing (❌ Missing)
- **Elimination System**: For speaker succession (❌ Missing)

## Test References
### Current Test Coverage:
- `test_game_controller.py`: Turn order and strategy phase testing
  - Strategy phase turn order based on initiative
  - Multiple strategy cards turn order
  - Turn advancement and cycling
  - Initiative order determination

### Test Scenarios Covered:
1. **Turn Order Management**: Initiative-based turn order
2. **Strategy Phase Order**: Turn order for strategy card selection
3. **Turn Advancement**: Proper turn cycling through players
4. **Initiative Calculation**: Lowest initiative determines order

### Missing Test Scenarios:
1. **Speaker Token Assignment**: Random speaker selection during setup
2. **Speaker-First Strategy Selection**: Speaker chooses strategy cards first
3. **Politics Card Speaker Transfer**: Speaker token changing hands
4. **Agenda Phase Speaker Role**: Speaker reveals agendas and votes last
5. **Objective Revealing**: Speaker reveals objectives during phases
6. **Speaker Elimination**: Speaker token passing on elimination
7. **Tie-Breaking**: Speaker decides tied agenda outcomes
8. **Speaker Succession**: Clockwise speaker passing

## Implementation Files
### Core Implementation:
- `src/ti4/core/game_controller.py`: Turn order and strategy phase management
- `src/ti4/core/player.py`: Basic player structure (could hold speaker token)

### Supporting Files:
- `tests/test_game_controller.py`: Turn order and strategy phase tests
- `src/ti4/testing/scenario_builder.py`: Game setup utilities

### Missing Implementation:
- Speaker token management system
- Speaker assignment during setup
- Politics strategy card implementation
- Agenda phase with speaker responsibilities
- Objective revealing system
- Speaker elimination handling
- Speaker-specific turn order logic

## Notable Implementation Details

### Strengths:
1. **Turn Order System**: Solid initiative-based turn order calculation
2. **Strategy Phase Management**: Strategy card selection with proper ordering
3. **Turn Advancement**: Proper cycling through players in initiative order
4. **Multiple Strategy Cards**: Handles multiple cards per player correctly

### Areas Needing Attention:
1. **Speaker Token System**: No explicit speaker token or role tracking
2. **Speaker Privileges**: No implementation of speaker-first mechanics
3. **Politics Integration**: No Politics strategy card speaker transfer
4. **Agenda Phase**: Missing entire agenda phase with speaker responsibilities
5. **Objective Management**: No speaker-controlled objective revealing
6. **Elimination Handling**: No speaker succession on player elimination

### Architecture Quality:
- **Good**: Turn order mathematics and strategy phase structure
- **Needs Work**: Speaker role integration and privilege system
- **Missing**: Agenda phase and objective management systems

## Action Items

### High Priority:
1. **Implement Speaker Token System**: Add speaker token tracking to player/game state
2. **Add Speaker Assignment**: Random speaker selection during game setup
3. **Integrate Speaker-First Logic**: Speaker chooses strategy cards first
4. **Create Politics Card Implementation**: Speaker token transfer mechanism

### Medium Priority:
5. **Implement Agenda Phase**: Complete agenda phase with speaker responsibilities
6. **Add Objective Revealing**: Speaker-controlled objective management
7. **Create Speaker Elimination Handling**: Speaker succession system
8. **Add Agenda Tie-Breaking**: Speaker decides tied outcomes

### Low Priority:
9. **Add Speaker UI Indicators**: Visual speaker token representation
10. **Create Speaker History Tracking**: Track speaker changes over time
11. **Add Speaker Statistics**: Analytics for speaker role performance
12. **Implement Speaker Privileges Display**: Show speaker-specific options

## Priority Assessment
**Overall Priority**: High - Speaker role is fundamental to turn order and game flow

**Implementation Status**: Basic Foundation (30%)
- Turn order system: ✅ Complete
- Initiative calculation: ✅ Complete
- Strategy phase structure: ✅ Complete
- Speaker token system: ❌ Missing
- Speaker privileges: ❌ Missing
- Politics card integration: ❌ Missing
- Agenda phase: ❌ Missing
- Objective management: ❌ Missing

**Recommended Focus**: 
1. Add explicit speaker token tracking to game state and player objects
2. Implement speaker assignment during setup with random selection
3. Modify strategy phase to ensure speaker chooses first
4. Create Politics strategy card with speaker transfer functionality

The current implementation has excellent turn order mechanics that provide a solid foundation for speaker functionality. However, it lacks the explicit speaker role tracking and privileges that are central to the speaker system. The speaker role affects multiple game phases (setup, strategy, agenda, status) and is essential for proper game flow. While the underlying turn order system is well-implemented, the speaker-specific mechanics need to be added to complete this fundamental game system.