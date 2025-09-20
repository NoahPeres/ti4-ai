# LRR Rule Analysis: Section 8 - AGENDA PHASE

## Category Overview
The agenda phase is where players cast votes on agenda cards that can change the rules of the game. This phase is triggered after the custodians token is removed from Mecatol Rex and involves resolving two agendas per round. Players use their planets' influence values to cast votes, with the speaker controlling agenda revelation and tie-breaking.

## Sub-Rules Analysis

### 8.1 Phase Activation and Structure 🔴 HIGH
**Raw LRR Text**: "Players skip the agenda phase during the early portion of each game. After the custodians token is removed from Mecatol Rex, the agenda phase is added to each game round. To resolve the agenda phase, players perform the following steps:"

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Basic phase transitions exist in `test_game_state_machine.py`
- **Tests**: Phase transition tests but no custodians token logic
- **Assessment**: Phase structure exists but custodians token trigger missing
- **Priority**: HIGH
- **Dependencies**: Requires custodians token system and Mecatol Rex control
- **Notes**: Critical game progression trigger - unlocks political gameplay

### 8.2 First Agenda Resolution Steps 🔴 HIGH
**Raw LRR Text**: "STEP 1-FIRST AGENDA: Players resolve the first agenda by following these steps in order: i. REVEAL AGENDA: The speaker draws one agenda card from the top of the agenda deck and reads it aloud to all players, including all of its possible outcomes. ii. VOTE: Each player, starting with the player to the left of the speaker and continuing clockwise, can cast votes for an outcome of the current agenda. iii. RESOLVE OUTCOME: Players tally each vote that was cast and resolve the outcome that received the most votes."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No agenda resolution system
- **Tests**: No agenda step tests
- **Assessment**: Core agenda mechanics completely missing
- **Priority**: HIGH
- **Dependencies**: Requires speaker system, agenda deck, and voting mechanics
- **Notes**: Three-step process with specific turn order

### 8.3 Second Agenda Resolution 🔴 HIGH
**Raw LRR Text**: "STEP 2-SECOND AGENDA: Players repeat the 'First Agenda' step of this phase for a second agenda."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No multi-agenda system
- **Tests**: No second agenda tests
- **Assessment**: Agenda phase requires exactly two agenda resolutions
- **Priority**: HIGH
- **Dependencies**: Requires first agenda system completion
- **Notes**: Each agenda phase resolves exactly two agendas

### 8.4 Planet Readying and Round Transition 🟡 MEDIUM
**Raw LRR Text**: "STEP 3-READY PLANETS: Each player readies each of their exhausted planets. Then, a new game round begins starting with the strategy phase."

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Planet exhaustion exists in planet system
- **Tests**: Planet exhaustion tests in `test_planet.py`
- **Assessment**: Planet readying exists but not integrated with agenda phase
- **Priority**: MEDIUM
- **Dependencies**: Requires planet exhaustion system and phase transitions
- **Notes**: Automatic planet readying at agenda phase end

### 8.6 Vote Casting Mechanics 🔴 HIGH
**Raw LRR Text**: "To cast votes, a player exhausts any number of their planets and chooses an outcome. The number of votes cast for that outcome is equal to the combined influence values of the planets that the player exhausts. When a player exhausts a planet to cast votes, that player must cast the full amount of votes provided by that planet."

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Planet influence values exist, exhaustion system exists
- **Tests**: Influence values tested in `test_planet.py`
- **Assessment**: Components exist but no voting integration
- **Priority**: HIGH
- **Dependencies**: Requires vote counting system and outcome selection
- **Notes**: All-or-nothing planet exhaustion for voting

### 8.7 Single Outcome Voting Restriction 🟡 MEDIUM
**Raw LRR Text**: "A player cannot cast votes for multiple outcomes of the same agenda. Each vote a player casts must be for the same outcome."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No vote validation system
- **Tests**: No voting restriction tests
- **Assessment**: Vote splitting prevention not implemented
- **Priority**: MEDIUM
- **Dependencies**: Requires voting system and validation rules
- **Notes**: Prevents strategic vote splitting

### 8.8 For/Against Voting 🟡 MEDIUM
**Raw LRR Text**: "Some agendas have 'For' and 'Against' outcomes. When a player casts votes on such an agenda, that player must cast their votes either 'For' or 'Against.'"

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No agenda outcome types
- **Tests**: No For/Against voting tests
- **Assessment**: Binary voting system not implemented
- **Priority**: MEDIUM
- **Dependencies**: Requires agenda card outcome system
- **Notes**: Specific agenda type with binary choices

### 8.9-8.11 Election Mechanics 🟡 MEDIUM
**Raw LRR Text**: "Some agendas instruct players to elect either a player or a planet. When a player casts votes for such an agenda, that player must cast their vote for an eligible player or planet as described on the agenda. When electing a player, a player can cast votes for themselves. When electing a planet, a player must cast votes for a planet that is controlled by a player."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No election system
- **Tests**: No election tests
- **Assessment**: Player/planet election mechanics missing
- **Priority**: MEDIUM
- **Dependencies**: Requires eligibility validation and vote targeting
- **Notes**: Self-voting allowed for player elections

### 8.12 Vote Declaration 🟢 LOW
**Raw LRR Text**: "When casting votes, a player must declare aloud the outcome for which their votes are being cast."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No vote declaration system
- **Tests**: No declaration tests
- **Assessment**: Vote transparency requirement
- **Priority**: LOW
- **Dependencies**: Requires voting UI and announcement system
- **Notes**: Ensures vote transparency

### 8.13 Trade Goods Restriction 🟡 MEDIUM
**Raw LRR Text**: "Trade goods cannot be spent to cast votes."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No vote payment validation
- **Tests**: No trade goods restriction tests
- **Assessment**: Payment method restriction not enforced
- **Priority**: MEDIUM
- **Dependencies**: Requires voting system and payment validation
- **Notes**: Prevents trade goods from being used as votes

### 8.14 Abstention Option 🟢 LOW
**Raw LRR Text**: "A player may choose to abstain by not casting any votes."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No abstention system
- **Tests**: No abstention tests
- **Assessment**: Optional voting not implemented
- **Priority**: LOW
- **Dependencies**: Requires voting system with skip option
- **Notes**: Players can choose not to participate

### 8.15-8.16 Additional Vote Effects 🟡 MEDIUM
**Raw LRR Text**: "Some game effects allow a player to cast additional votes for an outcome. These votes cannot be cast for a different outcome than other votes cast by that player. If a player cannot vote on an agenda because of a game effect, that player cannot cast votes for that agenda by exhausting planets or through any other game effect."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No additional vote effects or voting restrictions
- **Tests**: No vote effect tests
- **Assessment**: Vote modification and restriction effects missing
- **Priority**: MEDIUM
- **Dependencies**: Requires effect system and vote validation
- **Notes**: Handles special voting abilities and restrictions

### 8.18-8.19 Outcome Resolution and Tie-Breaking 🔴 HIGH
**Raw LRR Text**: "To resolve an outcome, the speaker follows the instructions on the agenda card. If there is a tie for the outcome that received the most votes, or if no outcome receives any votes, the speaker decides which of the tied outcomes to resolve. The speaker's decision is not a vote."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No outcome resolution or speaker tie-breaking
- **Tests**: No tie-breaking tests
- **Assessment**: Critical speaker powers missing
- **Priority**: HIGH
- **Dependencies**: Requires speaker system and outcome execution
- **Notes**: Speaker has decisive power in ties

### 8.20-8.21 Law vs Directive Resolution 🔴 HIGH
**Raw LRR Text**: "If an 'Elect' or 'For' outcome of a law was resolved, that card remains in play and permanently affects the game. If a directive or an 'Against' outcome of a law was resolved, that card is placed in the agenda discard pile."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No law persistence or directive discard system
- **Tests**: No resolution outcome tests
- **Assessment**: Agenda card lifecycle not implemented
- **Priority**: HIGH
- **Dependencies**: Requires agenda card system and permanent effects
- **Notes**: Different outcomes have different persistence rules

### 8.22 Outcome Prediction 🟢 LOW
**Raw LRR Text**: "Some game effects instruct a player to predict an outcome. To predict an outcome, a player declares aloud the outcome they think will receive the most votes. That player must make this prediction after the agenda is revealed but before any votes have been cast."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No prediction system
- **Tests**: No prediction tests
- **Assessment**: Special agenda interaction not implemented
- **Priority**: LOW
- **Dependencies**: Requires prediction tracking and timing validation
- **Notes**: Timing-sensitive prediction mechanic

## Dependencies Summary

### Critical Dependencies
- **Speaker System**: Controls agenda revelation and tie-breaking (Rule 80)
- **Custodians Token**: Triggers agenda phase activation
- **Agenda Card System**: Laws and directives with outcomes (Rule 7)
- **Planet Exhaustion**: For vote casting with influence values
- **Influence System**: Determines voting power (Rule 47)

### Related Systems
- **Politics Strategy Card**: Manipulates agenda deck (Rule 66)
- **Game Phase System**: Phase transitions and round management
- **Player Turn Order**: Clockwise voting from speaker's left
- **Victory Points**: Some agendas award victory points
- **Trade Goods**: Explicitly cannot be used for voting

## Test References
- **Phase Transitions**: `test_game_state_machine.py` includes AGENDA phase
- **Planet Influence**: `test_planet.py` tests influence values
- **Planet Exhaustion**: `test_planet.py` tests exhaustion mechanics
- **No Agenda-Specific Tests**: No voting, speaker, or custodians tests found

## Action Items
1. **Implement custodians token system** and Mecatol Rex trigger
2. **Create speaker system** with agenda revelation and tie-breaking
3. **Build voting mechanics** with influence-based vote casting
4. **Implement agenda resolution steps** with proper turn order
5. **Add outcome resolution system** with law/directive handling
6. **Create vote validation** for restrictions and additional effects
7. **Integrate planet readying** with agenda phase completion
8. **Add comprehensive test suite** for all agenda phase mechanics
