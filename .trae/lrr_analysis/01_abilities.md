# Rule 1: ABILITIES

## Category Overview
Cards and faction sheets each have abilities that players can resolve to trigger various game effects.

## Sub-Rules Analysis

### 1.1 - Rules Reference Precedence
**Raw LRR Text**: "If information in this Rules Reference contradicts the Learn to Play booklet, the Rules Reference takes precedence."

**Priority**: LOW - Documentation precedence rule
**Implementation Status**: ✅ IMPLEMENTED (implicit in design)
**Test References**: N/A - Documentation rule
**Notes**: This is a meta-rule about rule precedence, not a game mechanic

### 1.2 - Card Ability Precedence
**Raw LRR Text**: "If a card ability contradicts information in the Rules Reference, the card takes precedence. If both the card and the rules can be followed at the same time, they should be."

**Priority**: CRITICAL - Core game mechanic
**Implementation Status**: ✅ IMPLEMENTED
**Test References**: `tests/test_rule_01_abilities.py` - 14 tests passing covering timing windows, precedence, costs, and ability resolution
**Implementation Files**: `src/ti4/core/abilities.py` - Complete ability system with timing, precedence, and resolution
**Notes**: Essential for card-based game mechanics. Need ability precedence system.

### 1.3 - Ability Description
**Raw LRR Text**: "Each ability describes when and how a player can resolve it."
**Sub-rule**: "If an ability with a specified duration is resolved, the effect of the ability remains through that duration, even if the component that caused the ability is removed."

**Priority**: HIGH - Core ability framework
**Implementation Status**: ⚠️ PARTIAL - Basic Action class exists
**Test References**: `tests/test_action.py`
**Notes**: Need general ability system beyond just actions. Duration tracking missing.

### 1.4 - Multiple Abilities Per Card
**Raw LRR Text**: "If a card has multiple abilities, each ability is presented as its own paragraph."

**Priority**: HIGH - Card system requirement
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Cards need to support multiple distinct abilities

### 1.5 - Action Abilities
**Raw LRR Text**: "If an ability contains the word 'Action,' a player must use a component action during the action phase to resolve that ability."

**Priority**: HIGH - Action phase integration
**Implementation Status**: ⚠️ PARTIAL - Action framework exists
**Test References**: `tests/test_action.py`
**Notes**: Framework exists but needs action phase integration

### 1.6 - Cannot Effects
**Raw LRR Text**: "If an ability uses the word 'cannot,' that effect is absolute."
**Sub-rule**: "If two abilities use the word 'cannot,' a persistent ability takes precedence over a one-time ability and an enabling ability takes precedence over a cancel ability."

**Priority**: CRITICAL - Rule enforcement
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: "Cannot" must override everything. Need precedence system for conflicting "cannot" effects.

### 1.7 - Ability Resolution Requirements
**Raw LRR Text**: "When a player resolves an ability, they must resolve the ability in its entirety. Any parts of the ability preceded by the word 'may' are optional, and the player resolving the ability may choose not to resolve those parts."

**Priority**: HIGH - Ability validation
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Need system to ensure abilities are fully resolved with optional parts

### 1.8 - Mandatory vs Optional Abilities
**Raw LRR Text**: "Abilities on components that remain in play are mandatory unless those abilities use the word 'may.'"

**Priority**: HIGH - Automatic triggers
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: System needs to automatically trigger mandatory abilities

### 1.9 - Multiple Effects Resolution
**Raw LRR Text**: "If an ability has multiple effects separated by the word 'and,' a player must resolve as many of the ability's effects as possible. However, if the player cannot resolve all of its effects, that player is allowed to resolve as many as they can."

**Priority**: MEDIUM - Partial resolution
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Complex system needed for partial ability resolution

### 1.10 - Costs Section Header
**Raw LRR Text**: "COSTS" (section header)

**Priority**: N/A - Section divider
**Implementation Status**: N/A
**Test References**: N/A

### 1.11 - Cost Requirements
**Raw LRR Text**: "Some abilities have a cost that is followed by an effect. The cost of an ability is separated from the effect by the word 'to' or by a semicolon. A player cannot resolve the effect of such an ability if they cannot resolve that ability's cost."

**Priority**: HIGH - Cost validation
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Critical for ability system - must validate costs before allowing effects

### 1.12 - Cost Examples
**Raw LRR Text**: "Some examples of an ability's cost include spending resources, spending trade goods, spending command tokens, exhausting cards, purging cards, and activating specific systems."

**Priority**: MEDIUM - Cost types
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Need comprehensive cost validation system for all resource types

### 1.13 - Timing Section Header
**Raw LRR Text**: "TIMING" (section header)

**Priority**: N/A - Section divider
**Implementation Status**: N/A
**Test References**: N/A

### 1.14 - Before/After Timing
**Raw LRR Text**: "If the timing of an ability uses the word 'before' or 'after,' the ability's effect occurs immediately before or after the described timing event, respectively."
**Sub-rule**: "For example, if an ability is resolved 'after a ship is destroyed,' the ability must be resolved as soon as the ship is destroyed and not later during that turn or round."

**Priority**: CRITICAL - Core timing system
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Foundation for all ability timing. Must be precise and immediate.

### 1.15 - When Timing
**Raw LRR Text**: "If the timing of an ability uses the word 'when,' the ability's effect occurs at the moment of the described timing event."
**Sub-rule**: "Such an ability typically modifies or replaces the timing event in some way."

**Priority**: CRITICAL - Highest priority timing
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: "When" abilities can modify/replace events. Highest timing priority.

### 1.16 - Timing Priority
**Raw LRR Text**: "Effects that occur 'when' an event happens take priority over effects that occur 'after' an event happens."

**Priority**: CRITICAL - Timing precedence
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Essential for proper ability resolution order

### 1.17 - Then Requirements
**Raw LRR Text**: "If an ability uses the word 'then,' a player must resolve the effect that occurs before the word 'then' or they cannot resolve the effect that occurs after the word 'then.'"

**Priority**: HIGH - Conditional effects
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Sequential dependency validation required

### 1.18 - Ability Frequency
**Raw LRR Text**: "Each ability can be resolved once for each occurrence of that ability's timing event. For example, if an ability is resolved 'At the start of combat,' it can be resolved at the start of each combat."

**Priority**: HIGH - Trigger tracking
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Need system to track ability usage per trigger event

### 1.19 - Action Phase Ability Resolution
**Raw LRR Text**: "If there are multiple abilities that players wish to resolve at the same time during the action phase, each player takes a turn resolving an ability in initiative order, beginning with the active player. This process continues until each player has resolved each ability that they wish to resolve during that window."

**Priority**: HIGH - Multi-player timing
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Complex multi-player ability resolution system needed

### 1.20 - Strategy/Agenda Phase Ability Resolution
**Raw LRR Text**: "If there are multiple abilities that players wish to resolve at the same time during the strategy or agenda phases, players take turns resolving abilities starting with the speaker and proceeding clockwise. This process continues until each player has resolved each ability that they wish to resolve during that window."

**Priority**: HIGH - Phase-specific resolution
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Different resolution order for different phases

### 1.21 - Component-Specific Rules Header
**Raw LRR Text**: "COMPONENT-SPECIFIC RULES" (section header)

**Priority**: N/A - Section divider
**Implementation Status**: N/A
**Test References**: N/A

### 1.22 - Action Card Abilities
**Raw LRR Text**: "The opening paragraph of each ability found on an action card describes when a player can resolve that card's ability."

**Priority**: HIGH - Action card system
**Implementation Status**: ⚠️ PARTIAL - Basic action cards exist
**Test References**: Various action card tests
**Notes**: Need comprehensive action card ability system

### 1.23 - Promissory Note Abilities
**Raw LRR Text**: "The opening paragraph of most abilities found on promissory notes describes when a player can resolve that card's ability."
**Sub-rule**: "Some promissory notes have abilities that trigger as soon as a player receives the card."

**Priority**: HIGH - Promissory note system
**Implementation Status**: ⚠️ PARTIAL - Basic promissory notes exist
**Test References**: `tests/test_rule_69_promissory_notes.py`
**Notes**: Need immediate trigger system for some promissory notes

### 1.24 - Agenda Card Abilities
**Raw LRR Text**: "Abilities on agenda cards correspond to an outcome. Players resolve these abilities during the agenda phase after players vote for a particular outcome."

**Priority**: MEDIUM - Agenda system
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Agenda phase integration needed

### 1.25 - Faction Abilities
**Raw LRR Text**: "Each faction has faction abilities presented on its faction sheet. Each faction's flagship has one or more unique abilities. Some abilities provide players with perpetual effects."

**Priority**: HIGH - Faction system
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Faction-specific abilities and flagship abilities needed

### 1.26 - Unit Abilities
**Raw LRR Text**: "Some units have unit abilities. These abilities are named and presented above a unit's attributes on a player's faction sheet or on a unit upgrade card. Each unit ability has unique rules for when a player can resolve that ability. The following abilities are unit abilities:"

**Priority**: HIGH - Unit system
**Implementation Status**: ⚠️ PARTIAL - Basic unit abilities exist
**Test References**: Various unit tests
**Notes**: Unit abilities partially implemented but need full ability system integration

### 1.27 - System/Planet References
**Raw LRR Text**: "If a unit's ability uses the phrase 'this system' or 'this planet,' the ability is referring to the system or planet that contains that unit."

**Priority**: MEDIUM - Context resolution
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Context-aware ability resolution needed

## Implementation Priority Summary

### CRITICAL (Must implement first):
- **1.2**: Card ability precedence over rules
- **1.6**: "Cannot" effects absolute precedence
- **1.14**: Before/After timing system
- **1.15**: "When" timing system
- **1.16**: Timing priority (when > after)

### HIGH (Core functionality):
- **1.3**: Ability description and duration tracking
- **1.5**: Action abilities integration
- **1.7**: Complete ability resolution
- **1.8**: Mandatory ability triggers
- **1.11**: Cost validation system
- **1.17**: "Then" conditional effects
- **1.18**: Ability frequency tracking
- **1.19**: Action phase multi-player resolution
- **1.20**: Strategy/agenda phase resolution
- **1.22**: Action card abilities
- **1.23**: Promissory note abilities
- **1.25**: Faction abilities
- **1.26**: Unit abilities

### MEDIUM (Supporting features):
- **1.4**: Multiple abilities per card
- **1.9**: Partial resolution of "and" effects
- **1.12**: Cost type examples
- **1.24**: Agenda card abilities
- **1.27**: Context resolution

## Key Timing Windows Identified from Compendium:

### Action Phase Timing:
- "Action:" - Component actions
- "At the start of your turn"
- "After you perform an action"
- "During the action phase"

### Combat Timing:
- "At the start of combat"
- "At the start of a space combat"
- "At the start of an invasion"
- "After you win a space combat"
- "During a combat round"

### Strategy/Agenda Timing:
- "After an agenda is revealed"
- "When you are elected as the outcome"
- "Before a player casts votes"
- "At the end of the strategy phase"

### Production/Movement Timing:
- "After you activate a system"
- "After you produce units"
- "After a player moves ships into a system"
- "When another player activates a system"

### Technology/Research Timing:
- "After the Jol-Nar player researches a technology"
- "After you explore a planet"
- "At the end of your turn"

## Test Case Requirements:

Each sub-rule needs comprehensive test coverage:
1. **Basic functionality tests** - Does the rule work as intended?
2. **Edge case tests** - Boundary conditions and error cases
3. **Integration tests** - How does it interact with other rules?
4. **Precedence tests** - Conflict resolution between abilities
5. **Timing tests** - Proper sequencing of ability resolution
**Implementation Status**: ⚠️ PARTIAL - Individual systems exist
**Test References**: Basic resource tests exist
**Notes**: Individual cost types partially exist but not unified

### 1.13 - Timing Section Header
**Raw LRR Text**: "TIMING" (section header)

**Priority**: N/A - Section divider
**Implementation Status**: N/A
**Test References**: N/A

### 1.14 - Before/After Timing
**Raw LRR Text**: "If the timing of an ability uses the word 'before' or 'after,' the ability's effect occurs immediately before or after the described timing event, respectively."
**Sub-rule**: "For example, if an ability is resolved 'after a ship is destroyed,' the ability must be resolved as soon as the ship is destroyed and not later during that turn or round."

**Priority**: HIGH - Event system
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Need event system with before/after hooks

### 1.15 - When Timing
**Raw LRR Text**: "If the timing of an ability uses the word 'when,' the ability's effect occurs at the moment of the described timing event."
**Sub-rule**: "Such an ability typically modifies or replaces the timing event in some way."

**Priority**: HIGH - Event modification
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: "When" abilities modify or replace the timing event

### 1.16 - Timing Priority
**Raw LRR Text**: "Effects that occur 'when' an event happens take priority over effects that occur 'after' an event happens."

**Priority**: MEDIUM - Priority resolution
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Need priority queue for simultaneous effects

### 1.17 - Then Conditional Effects
**Raw LRR Text**: "If an ability uses the word 'then,' a player must resolve the effect that occurs before the word 'then' or they cannot resolve the effect that occurs after the word 'then.'"

**Priority**: MEDIUM - Conditional logic
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Need conditional execution validation

### 1.18 - Ability Frequency
**Raw LRR Text**: "Each ability can be resolved once for each occurrence of that ability's timing event. For example, if an ability is resolved 'At the start of combat,' it can be resolved at the start of each combat."

**Priority**: MEDIUM - Usage tracking
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Need to track ability usage per trigger event

### 1.19 - Simultaneous Resolution (Action Phase)
**Raw LRR Text**: "If there are multiple abilities that players wish to resolve at the same time during the action phase, each player takes a turn resolving an ability in initiative order, beginning with the active player. This process continues until each player has resolved each ability that they wish to resolve during that window."

**Priority**: HIGH - Initiative system
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Complex system for resolving multiple abilities in initiative order

### 1.20 - Simultaneous Resolution (Other Phases)
**Raw LRR Text**: "If there are multiple abilities that players wish to resolve at the same time during the strategy or agenda phases, players take turns resolving abilities starting with the speaker and proceeding clockwise. This process continues until each player has resolved each ability that they wish to resolve during that window."

**Priority**: HIGH - Speaker system
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Different resolution order for non-action phases

### 1.21 - Component-Specific Rules Section Header
**Raw LRR Text**: "COMPONENT-SPECIFIC RULES" (section header)

**Priority**: N/A - Section divider
**Implementation Status**: N/A
**Test References**: N/A

### 1.22 - Action Card Abilities
**Raw LRR Text**: "The opening paragraph of each ability found on an action card describes when a player can resolve that card's ability."

**Priority**: MEDIUM - Action cards
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Action card abilities are timing-specific

### 1.23 - Promissory Note Abilities
**Raw LRR Text**: "The opening paragraph of most abilities found on promissory notes describes when a player can resolve that card's ability."
**Sub-rule**: "Some promissory notes have abilities that trigger as soon as a player receives the card."

**Priority**: MEDIUM - Promissory notes
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Some promissory abilities trigger on receipt

### 1.24 - Agenda Card Abilities
**Raw LRR Text**: "Abilities on agenda cards correspond to an outcome. Players resolve these abilities during the agenda phase after players vote for a particular outcome."

**Priority**: MEDIUM - Agenda system
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Agenda abilities are outcome-based and phase-specific

### 1.25 - Faction Abilities
**Raw LRR Text**: "Each faction has faction abilities presented on its faction sheet. Each faction's flagship has one or more unique abilities. Some abilities provide players with perpetual effects."

**Priority**: HIGH - Faction system
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: `tests/test_integration.py` has `test_faction_specific_abilities` stub
**Notes**: Faction abilities are perpetual and faction-specific

### 1.26 - Unit Abilities
**Raw LRR Text**: "Some units have unit abilities. These abilities are named and presented above a unit's attributes on a player's faction sheet or on a unit upgrade card. Each unit ability has unique rules for when a player can resolve that ability. The following abilities are unit abilities: Anti-Fighter Barrage, Bombardment, Deploy, Planetary Shield, Production, Space Cannon, Sustain Damage"

**Priority**: HIGH - Unit system
**Implementation Status**: ✅ IMPLEMENTED - Unit abilities exist
**Test References**: `tests/test_unit.py` - comprehensive unit ability tests, `tests/test_combat.py` - sustain damage tests
**Notes**: All unit abilities implemented with comprehensive test coverage

### 1.27 - Contextual References
**Raw LRR Text**: "If a unit's ability uses the phrase 'this system' or 'this planet,' the ability is referring to the system or planet that contains that unit."

**Priority**: MEDIUM - Context resolution
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Need system to resolve "this system" and "this planet" references

## Dependencies Summary
- **Event System**: Required for timing-based abilities (1.14, 1.15, 1.16, 1.18, 1.19, 1.20)
- **Card Systems**: Action cards, promissory notes, agenda cards (1.22, 1.23, 1.24)
- **Faction System**: For faction-specific abilities (1.25)
- **Resource Systems**: For cost validation (1.11, 1.12)
- **Initiative/Speaker Systems**: For simultaneous resolution (1.19, 1.20)
- **Precedence System**: For conflicting abilities (1.2, 1.6)

## Action Items for Full Implementation
1. **CRITICAL**: Implement ability precedence system (1.2, 1.6)
2. **HIGH**: Create general ability framework with duration tracking (1.3)
3. **HIGH**: Implement cost validation system (1.11)
4. **HIGH**: Build event system with before/after/when timing (1.14, 1.15)
5. **HIGH**: Create simultaneous ability resolution system (1.19, 1.20)
6. **MEDIUM**: Implement contextual reference resolution (1.27)
7. **MEDIUM**: Add partial effect resolution for "and" separated effects (1.9)

## Related Rules
- Rule 2: Action Cards
- Leaders
- Promissory Notes
- Strategy Card
- Technology
