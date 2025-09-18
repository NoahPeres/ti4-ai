# LRR Rule Analysis: Rule 46 - LEADERS

## Category Overview
**Rule Type**: Faction-Specific Abilities & Character System  
**Complexity**: Medium-High  
**Scope**: Agent, commander, and hero leader mechanics  

## Raw LRR Text
```
51 LEADERS
Each player has several faction-specific leader cards that represent characters with unique abilities.
51.1 Each faction has three leaders; one agent, one commander, and one hero.
a The Nomad's "The Company" faction ability grants them two additional agents, for a total of five leaders.
51.2 A player's leaders are placed on their leader sheet during setup.
b The two additional Nomad agents are placed in the Nomad player's play area readied side up.

51.3 AGENTS
51.4 An agent does not need to be unlocked and begins the game in a readied state. They can be exhausted by resolving their abilities, and they ready during the "Ready Cards" step of the status phase.

51.5 COMMANDERS
51.6 A commander must be unlocked to use its abilities. A player unlocks their commander if they fulfill the conditions listed after the "Unlock" header.
a Each faction's commander has a unique "Unlock" condition.
b After a player fulfills the unlock condition of their commander, they flip it over to its unlocked side.
c A commander's unlock conditions cannot be met while an ability or game effect is being resolved. That is, pending abilities or partially resolved game effects must be completed before checking if conditions are met.
d A commander cannot flip to its locked side after it is unlocked, even if its owner no longer meets the unlock conditions.
51.7 A commander cannot be exhausted.
51.8 The "Alliance" promissory note allows a player to share their commander's ability with another player.
a A commander's owner can still use their commander's ability, even if another player has their "Alliance" promissory note.

51.9 HEROES
51.10 A hero must be unlocked to use its abilities. A player unlocks their hero if they fulfill the conditions listed after the "Unlock" header.
a The "Unlock" condition for each hero is to have three scored objectives; these can be any combination of secret objectives and public objectives.
b Victory points do not count toward unlocking heroes.
c After a player fulfills the unlock condition of their hero, they flip it to its unlocked side.
d A hero cannot flip to its locked side after it is unlocked.
51.11 A hero cannot be exhausted.
51.12 A hero is purged after its abilities are resolved.
a The Titans of Ul's hero is not purged; it is attached to the planet Elysium instead.
```

## Sub-Rules Analysis

### 51.0 Leaders Overview
**Rule**: "Each player has several faction-specific leader cards that represent characters with unique abilities."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No leader system found in codebase
- **Tests**: No leader-related tests found
- **Assessment**: Core leader system completely missing
- **Priority**: HIGH
- **Dependencies**: Requires leader sheet, faction-specific abilities, and state management

### 51.1 Leader Types and Quantities
**Rule**: "Each faction has three leaders; one agent, one commander, and one hero."
**Special Case**: "The Nomad's 'The Company' faction ability grants them two additional agents, for a total of five leaders."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No leader card system or faction-specific leader handling
- **Tests**: No tests for leader quantities or Nomad special case
- **Assessment**: Basic leader structure missing
- **Priority**: HIGH
- **Dependencies**: Requires faction system and leader card definitions

### 51.2 Leader Sheet Placement
**Rule**: "A player's leaders are placed on their leader sheet during setup."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No leader sheet system found
- **Tests**: No setup tests for leader placement
- **Assessment**: Leader sheet system missing from setup
- **Priority**: HIGH
- **Dependencies**: Requires leader sheet implementation and setup integration

### 51.3-51.4 Agent Mechanics
**Rule**: "An agent does not need to be unlocked and begins the game in a readied state. They can be exhausted by resolving their abilities, and they ready during the 'Ready Cards' step of the status phase."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No agent system or exhaustion mechanics
- **Tests**: No agent ability or readying tests
- **Assessment**: Agent system completely missing
- **Priority**: HIGH
- **Dependencies**: Requires exhaustion system and status phase integration

### 51.5-51.8 Commander Mechanics
**Rule**: "A commander must be unlocked to use its abilities. A player unlocks their commander if they fulfill the conditions listed after the 'Unlock' header."
**Sub-rules**: Unique unlock conditions, permanent unlocking, Alliance promissory note sharing

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No commander system or unlock condition tracking
- **Tests**: No commander unlock or Alliance promissory note tests
- **Assessment**: Commander system completely missing
- **Priority**: HIGH
- **Dependencies**: Requires unlock condition system and promissory note integration

### 51.9-51.12 Hero Mechanics
**Rule**: "A hero must be unlocked to use its abilities. A player unlocks their hero if they fulfill the conditions listed after the 'Unlock' header."
**Sub-rules**: Three scored objectives requirement, purging after use, Titans of Ul exception

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No hero system or objective tracking for unlocking
- **Tests**: No hero unlock or purging tests
- **Assessment**: Hero system completely missing
- **Priority**: HIGH
- **Dependencies**: Requires objective scoring system and purge mechanics

## Related Topics
- **Leader Sheet (Rule 50)**: Physical placement of leader cards
- **Exhausted (Rule 34)**: Agent exhaustion mechanics
- **Readied (Rule 71)**: Agent readying during status phase
- **Status Phase (Rule 84)**: Agent readying timing
- **Promissory Notes (Rule 69)**: Alliance note for commander sharing
- **Objective Cards (Rule 61)**: Hero unlock requirements
- **Purge (Rule 70)**: Hero purging after use

## Dependencies
- **Leader Sheet System**: Physical card placement and management
- **Exhaustion System**: Agent exhaustion and readying mechanics
- **Faction System**: Faction-specific leader definitions
- **Unlock Condition System**: Commander and hero unlock tracking
- **Objective Scoring System**: Hero unlock requirement tracking
- **Promissory Note System**: Alliance note for commander sharing
- **Purge System**: Hero purging mechanics

## Test References
**Current Test Coverage**: ❌ NONE
- **Leadership Strategy Card**: Only references found are to Leadership strategy card, not leader system
- **No Leader Tests**: No tests for agents, commanders, heroes, or leader mechanics

**Missing Test Areas**:
- Agent exhaustion and readying mechanics
- Commander unlock condition tracking
- Hero unlock from scored objectives
- Leader ability resolution
- Alliance promissory note sharing
- Hero purging mechanics
- Nomad special case (5 leaders total)

## Implementation Files
**Current Implementation**: ❌ NOT IMPLEMENTED

**Missing Components**:
- Leader card system
- Leader sheet implementation
- Agent exhaustion/readying system
- Commander unlock condition tracking
- Hero unlock and purging system
- Faction-specific leader definitions
- Alliance promissory note integration

**Required Files** (Not Found):
- `src/ti4/core/leader.py`: Leader card and ability system
- `src/ti4/core/leader_sheet.py`: Leader sheet management
- `src/ti4/leaders/`: Faction-specific leader definitions
- `tests/test_leader.py`: Leader system tests

## Notable Implementation Details

### Complete System Missing
- No leader-related code found in entire codebase
- No leader card definitions or faction-specific abilities
- No exhaustion system for agents
- No unlock condition tracking for commanders/heroes
- No integration with setup, status phase, or objective system

### Leadership vs Leaders Confusion
- Only "Leadership" references found are to Leadership strategy card
- No actual leader system implementation
- Clear distinction needed between strategy card and leader system

### Complex State Management Required
- Agent exhaustion/readying cycles
- Commander unlock condition validation
- Hero objective tracking and purging
- Alliance promissory note sharing mechanics

## Action Items

### High Priority
1. **Implement Core Leader System**
   - Create Leader card base class with agent/commander/hero types
   - Implement leader sheet for card placement and management
   - Add faction-specific leader definitions

2. **Implement Agent System**
   - Add agent exhaustion and readying mechanics
   - Integrate with status phase for automatic readying
   - Create agent ability resolution system

3. **Implement Commander System**
   - Add unlock condition tracking and validation
   - Implement permanent unlocking mechanics
   - Create Alliance promissory note sharing system

### Medium Priority
4. **Implement Hero System**
   - Add objective scoring tracking for hero unlock
   - Implement hero purging after ability use
   - Handle Titans of Ul special case (attachment to Elysium)

5. **Setup Integration**
   - Add leader placement to game setup sequence
   - Implement leader sheet initialization
   - Handle Nomad special case (5 leaders total)

### Low Priority
6. **Comprehensive Testing**
   - Add agent exhaustion/readying tests
   - Test commander unlock conditions
   - Test hero objective tracking and purging
   - Test Alliance promissory note mechanics
   - Test faction-specific leader abilities

## Priority Assessment
**Overall Priority**: 🟠 HIGH

**Rationale**:
- Leaders provide faction-specific asymmetric abilities
- Agent abilities are available from game start
- Commander unlocks provide mid-game power spikes
- Hero abilities are powerful late-game effects
- System affects faction balance and gameplay variety

**Implementation Effort**: HIGH
- Complete system needs implementation from scratch
- Complex state management for different leader types
- Faction-specific ability definitions required
- Integration with multiple game systems needed

**Dependencies**: Extensive integration with faction system, setup, status phase, objective tracking, and promissory notes