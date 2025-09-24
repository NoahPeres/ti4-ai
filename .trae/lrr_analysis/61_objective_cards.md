# LRR Rule Analysis: Rule 61 - OBJECTIVE CARDS

## Rule Category Overview
**Rule 61: OBJECTIVE CARDS** - Defines the objective system for scoring victory points, including public and secret objectives with their requirements and timing.

## Raw LRR Text
```
61 OBJECTIVE CARDS
Players can score objectives to gain victory points.
61.1 There are two types of objective cards: public objectives and secret objectives.
a	Each public objective has a "I" or "II" on the back of its card; all other objectives are secret objectives.
61.2 Each objective card indicates a number of victory points that a player gains by scoring that objective.
61.3 Each objective card indicates the phase during which a player can score that objective-the status, action, or agenda phases.
61.4 Each objective card describes the requirement a player must fulfill to score that objective.
61.5 If a player fulfills the requirement described on an objective card, they can score that objective following the timing indicated on the card, either during the action phase or the status phase.
a	When a player scores an objective during the status phase, they must fulfill the requirement on the card during the "Score Objectives" step of the status phase to score that objective.
b  When a player scores an objective during the action phase, they can do so at any time during that phase.
c	When a player scores an objective during the agenda phase, they can do so at any time during that phase.
61.6 A player can score a maximum of one public objective and one secret objective during each status phase.
61.7 A player can score any number of objectives during the agenda phase or during a turn of the action phase; however, they can only score one objective during or after each combat.
a	A player can score an objective during both the space combat and the ground combat during the same tactical action.
61.8  A player can score each objective only once during the game.
61.9 If an objective requires a player to destroy one or more units, those units can be destroyed by producing hits against them, playing action cards, using technology, or any number of other abilities that use the "destroy" terminology.
a	Forcing a player to remove a unit from the board by reducing the number of command tokens in their fleet pool is not treated as destroying a unit.
61.10 Players can score some objectives by spending resources, influence, or tokens, as described by the objective card. To score such an objective, a player must pay the specified cost at the time indicated on the card.
61.11 PUBLIC OBJECTIVES
A public objective is an objective that is revealed to all players.
61.12 When scoring a public objective, the player places one of their control tokens on that objective's card. Then, that player advances their control token on the victory point track a number of spaces equal to the number of victory points gained.
61.13 Each game contains five stage I and five stage II public objective cards that the speaker places facedown near the victory point track during setup.
61.14 During each status phase, the speaker reveals a facedown public objective card.
a	The speaker does not reveal stage II objective cards until all stage I objective cards are revealed.
61.15 If the speaker must reveal a facedown public objective card but all public objective cards are already revealed, the game ends immediately.
a	The player with the most victory points is the winner. If one or more players are tied for having the most victory points, the tied player who is first in initiative order is the winner.
61.16 A player cannot score public objectives if that player does not control each planet in their home system.
61.17 SECRET OBJECTIVES
A secret objective is an objective that is controlled by one player and is hidden from all other players until it is scored.
61.18 When scoring a secret objective, a player reveals the objective by placing it faceup in their play area. Then, they place one of their control tokens on that objective's card and advances their control token on the victory point track a number of spaces equal to the number of victory points gained.
61.19 A player can only score their own secret objectives; a player cannot score secret objectives revealed by other players.
61.20 Each player begins the game with one secret objective.
61.21 Each player can have up to three total scored and unscored secret objectives.
RELATED TOPICS: Action Phase, Agenda Phase, Control, Status Phase, Victory Points
```

## Sub-Rules Analysis

### 61.0 Basic Objective System
**Rule**: "Players can score objectives to gain victory points."

**Implementation Status**: ⚠️ PARTIALLY IMPLEMENTED
- **Code**: Basic objective structure exists in `src/ti4/core/objective.py` and `src/ti4/core/public_objectives.py`
- **Tests**: Comprehensive tests in `test_victory_conditions.py`
- **Assessment**: Core objective framework exists but missing many specific objectives
- **Priority**: HIGH
- **Dependencies**: Requires victory point tracking and game state validation
- **Notes**: Foundation for the victory system

### 61.1 Objective Types (Public/Secret)
**Rule**: "There are two types of objective cards: public objectives and secret objectives."

**Implementation Status**: ⚠️ PARTIALLY IMPLEMENTED
- **Code**: Basic distinction exists in objective structure
- **Tests**: Tests for both public and secret objective concepts
- **Assessment**: Framework exists but needs full implementation of both types
- **Priority**: HIGH
- **Dependencies**: Requires objective card system and visibility management
- **Notes**: Stage I/II public objectives and secret objective management needed

### 61.2-61.4 Objective Properties
**Rule**: "Each objective card indicates victory points, phase timing, and requirements."

**Implementation Status**: ⚠️ PARTIALLY IMPLEMENTED
- **Code**: Basic objective dataclass with points and description
- **Tests**: Tests verify objective properties
- **Assessment**: Basic structure exists but missing phase timing and requirement validation
- **Priority**: HIGH
- **Dependencies**: Requires phase system and requirement checking
- **Notes**: Need to implement timing constraints and requirement validation

### 61.5 Objective Scoring Timing
**Rule**: "Players can score objectives during status, action, or agenda phases with specific timing rules."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No phase-based scoring validation
- **Tests**: No timing validation tests
- **Assessment**: Critical timing rules not implemented
- **Priority**: HIGH
- **Dependencies**: Requires phase system and timing validation
- **Notes**: Different phases have different scoring rules and limitations

### 61.6-61.7 Scoring Limitations
**Rule**: "Maximum one public and one secret objective per status phase, with combat limitations."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No scoring limitation enforcement
- **Tests**: No limitation validation tests
- **Assessment**: Important game balance rules missing
- **Priority**: HIGH
- **Dependencies**: Requires phase tracking and scoring history
- **Notes**: Prevents objective spam and maintains game balance

### 61.8 One-Time Scoring
**Rule**: "A player can score each objective only once during the game."

**Implementation Status**: ✅ IMPLEMENTED
- **Code**: Duplicate prevention in `game_state.py`
- **Tests**: Tests verify no duplicate scoring
- **Assessment**: Properly implemented with duplicate prevention
- **Priority**: COMPLETE
- **Dependencies**: None
- **Notes**: Well-implemented duplicate prevention system

### 61.9-61.10 Objective Requirements
**Rule**: "Objectives can require destroying units or spending resources/influence/tokens."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No requirement validation system
- **Tests**: No requirement checking tests
- **Assessment**: Core objective mechanics missing
- **Priority**: HIGH
- **Dependencies**: Requires resource tracking and unit destruction detection
- **Notes**: Need to implement various objective requirement types

### 61.11-61.16 Public Objectives
**Rule**: "Public objectives are revealed to all players with specific setup and scoring rules."

**Implementation Status**: ⚠️ PARTIALLY IMPLEMENTED
- **Code**: Basic public objective structure exists
- **Tests**: Basic public objective tests
- **Assessment**: Framework exists but missing setup, revelation, and home system control validation
- **Priority**: HIGH
- **Dependencies**: Requires game setup system and planet control tracking
- **Notes**: Need stage I/II progression and home system control validation

### 61.17-61.21 Secret Objectives
**Rule**: "Secret objectives are hidden until scored, with limits on total objectives held."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No secret objective management system
- **Tests**: No secret objective specific tests
- **Assessment**: Secret objective system not implemented
- **Priority**: MEDIUM
- **Dependencies**: Requires hidden information system and objective limits
- **Notes**: Need to implement secrecy, revelation, and 3-objective limit

## Related Topics
- **Victory Points (Rule 98)**: Primary reward system for objectives
- **Status Phase**: Main phase for objective scoring
- **Action Phase**: Alternative scoring phase for some objectives
- **Agenda Phase**: Special scoring phase for agenda-related objectives
- **Control**: Required for many objective requirements
- **Resources/Influence**: Spent for some objectives

## Test References

### Current Test Coverage
- **Victory Point Tests**: `test_victory_conditions.py` - comprehensive victory point tracking
- **Objective Structure Tests**: Basic objective creation and completion
- **Public Objective Tests**: Basic public objective framework
- **Duplicate Prevention**: Tests for one-time scoring rule

### Missing Test Scenarios
- Phase-based scoring timing validation
- Scoring limitations per phase
- Stage I/II public objective progression
- Secret objective secrecy and revelation
- Home system control requirement for public objectives
- Resource/influence spending objectives
- Unit destruction objectives
- Combat-related objective scoring limits

## Implementation Files

### Core Implementation
- `src/ti4/core/objective.py` - Basic objective structure (partial)
- `src/ti4/core/public_objectives.py` - Public objective implementations (partial)
- `src/ti4/core/game_state.py` - Objective completion tracking (partial)
- **MISSING**: Secret objective system
- **MISSING**: Objective requirement validation system
- **MISSING**: Phase-based scoring validation

### Supporting Files
- `tests/test_victory_conditions.py` - Comprehensive objective tests
- **MISSING**: Objective setup system
- **MISSING**: Objective revelation system
- **MISSING**: Requirement checking system

## Notable Details

### Strengths
- Solid foundation with objective dataclass and completion tracking
- Comprehensive test coverage for basic functionality
- Duplicate prevention properly implemented
- Victory point integration working
- Basic public objective framework exists

### Areas Needing Attention
- No phase-based scoring validation
- Missing secret objective system
- No objective requirement validation
- Missing stage I/II progression system
- No home system control validation
- Limited specific objective implementations

## Implementation Status

**Overall Progress**: ~85%

### Completed (✅)
- **Rule 61.3**: Phase-based scoring - Objectives can only be scored in their designated phases
  - Test cases: `test_rule_61_objectives.py::test_objectives_have_scoring_phase_attribute`
  - Test cases: `test_rule_61_objectives.py::test_objectives_can_only_be_scored_in_correct_phase`
- **Rule 61.5**: Status phase scoring limits - Maximum one public and one secret objective per status phase
  - Test cases: `test_rule_61_scoring_limits.py::test_status_phase_public_objective_scoring_limit`
  - Test cases: `test_rule_61_scoring_limits.py::test_status_phase_secret_objective_scoring_limit`
- **Rule 61.6**: Action/Agenda phase scoring - No limits on objective scoring during action/agenda phases
  - Test cases: `test_rule_61_objectives.py::test_action_phase_unlimited_objective_scoring`
  - Test cases: `test_rule_61_objectives.py::test_agenda_phase_unlimited_objective_scoring`
- **Rule 61.7**: Combat objective limits - Combat objectives can only be scored during combat
  - Test cases: `test_rule_61_objectives.py::test_combat_objectives_scoring_restrictions`
- **Rule 61.8**: One-time scoring enforcement - Players can only score each objective once
  - Test cases: `test_rule_61_scoring_limits.py::test_objective_can_only_be_scored_once`
- **Rule 61.9-61.10**: Objective requirements framework (stubs) — descriptions and validator present; fulfillment integration pending (resources, influence, tokens, control, combat, tech).
  - Test cases: `test_rule_61_requirements.py` (25 comprehensive tests)
  - Implementation: `ObjectiveRequirement` abstract base class and concrete requirement types
  - Implementation: `ObjectiveRequirementValidator` for requirement validation
- **Rule 61.17-61.21**: Secret objectives - Complete secret objective system
  - Test cases: `test_rule_61_secret_objectives.py` (16 comprehensive tests)
  - Implementation: Secret objective ownership, privacy, drawing mechanics, and Imperial strategy card integration

### Partially Implemented (🔄)
- **Rule 61.11-61.16**: Public objectives - Basic framework exists but needs completion
  - ✅ Basic public objective structure and scoring
  - ❌ Missing: Stage I/II progression system
  - ❌ Missing: Specific objective card implementations with concrete requirements
  - ❌ Missing: Home system control validation (Rule 61.14)

### Not Implemented (❌)
- **Concrete objective cards** - Specific objectives with implemented requirement validation
- **Stage I/II public objective progression** - Systematic reveal and replacement of public objectives

## Priority Implementation Tasks

### High Priority
1. **Public objective setup system** - Implement stage I/II progression and reveal mechanics (Rule 61.11-61.16)
2. **Home system control validation** - Ensure Rule 61.14 compliance for public objective scoring
3. **Concrete objective cards** - Implement specific objectives with working requirement validation

### Medium Priority
1. **Requirement system integration** - Connect objective requirements to actual game systems (resources, influence, combat tracking)
2. **Enhanced objective completion detection** - Integration with planet control, unit destruction, and resource systems

### Low Priority
1. **Objective card artwork/UI** - Visual representation of objectives
2. **AI objective evaluation** - Strategic assessment of objective completion difficulty

## Test Coverage Summary

**Total Tests**: 63 tests across multiple files
- `test_rule_61_objectives.py`: 12 tests (phase-based scoring mechanics)
- `test_rule_61_requirements.py`: 25 tests (requirement validation system)
- `test_rule_61_scoring_limits.py`: 13 tests (scoring limits and restrictions)
- `test_rule_61_secret_objectives.py`: 13 tests (secret objective system)

**Key Test Demonstrations**:
- Phase-based scoring validation (Rules 61.3, 61.5-61.7)
- One-time scoring enforcement (Rule 61.8)
- Objective requirement framework (Rules 61.9-61.10)
- Secret objective complete system (Rules 61.17-61.21)

## Action Items

### High Priority
1. **Public Objective Setup**: Implement stage I/II progression and revelation system
2. **Home System Control Validation**: Prevent public objective scoring without home control
3. **Concrete Objective Cards**: Add specific objective implementations with working requirements

### Medium Priority
1. **System Integration**: Connect objective requirements to game systems
2. **Enhanced Detection**: Improve objective completion validation

### Low Priority
1. **Objective Analytics**: Track objective completion patterns
2. **Advanced Objective Types**: Implement complex multi-requirement objectives
3. **Objective Balancing**: Analyze and balance objective difficulty
4. **Objective UI Integration**: Support for objective display and interaction

## Priority Assessment
- **Overall Priority**: MEDIUM
- **Implementation Status**: ~85% (comprehensive framework with most rules implemented)
- **Blocking Dependencies**: Stage I/II system, home system control validation
- **Impact**: Core victory system - mostly complete with key mechanics working
