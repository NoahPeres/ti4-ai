# LRR Rule Analysis: Section 1 - ABILITIES

## 1. ABILITIES

**Rule Category Overview**: Cards and faction sheets each have abilities that players can resolve to trigger various game effects.

### 1.1 Rules Reference Precedence
**Rule**: "If information in this Rules Reference contradicts the Learn to Play booklet, the Rules Reference takes precedence."

**Implementation Status**: ➖ NOT APPLICABLE
- **Code**: No explicit precedence system exists
- **Tests**: No tests verify rule precedence
- **Assessment**: This is a meta-rule about documentation hierarchy, not implementable in code
- **Priority**: META (documentation principle)
- **Notes**: This establishes that LRR is authoritative over Learn to Play

### 1.2 Card Ability Precedence  
**Rule**: "If a card ability contradicts information in the Rules Reference, the card takes precedence. If both the card and the rules can be followed at the same time, they should be."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No ability precedence system exists
- **Tests**: No tests for ability precedence
- **Assessment**: Critical for card-based game mechanics - cards must be able to override base rules
- **Priority**: CRITICAL
- **Dependencies**: Requires general ability system first
- **Notes**: This is fundamental to how TI4 works - cards create exceptions to rules

### 1.3 Ability Description Requirements
**Rule**: "Each ability describes when and how a player can resolve it."

**Implementation Status**: ⚠️ PARTIAL
- **Code**: `Action` base class exists in `src/ti4/actions/action.py`
- **Tests**: `tests/test_action.py` tests action interface
- **Assessment**: Basic structure exists but no general ability framework beyond actions
- **Priority**: HIGH
- **Notes**: Need to expand beyond just actions to all abilities

### 1.4 Multiple Abilities Per Card
**Rule**: "If a card has multiple abilities, each ability is presented as its own paragraph."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No multi-ability card system
- **Tests**: No tests for multiple abilities
- **Assessment**: Cards need to support multiple distinct abilities
- **Priority**: HIGH
- **Dependencies**: Requires card system and ability framework

### 1.5 Action Abilities Require Component Action
**Rule**: "If an ability contains the word 'Action,' a player must use a component action during the action phase to resolve that ability."

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Action framework exists, component actions partially implemented
- **Tests**: Basic action tests exist in `tests/test_action.py`
- **Assessment**: Framework exists but needs action phase integration
- **Priority**: HIGH
- **Dependencies**: Requires action phase flow and component action system

### 1.6 Cannot Effects Are Absolute
**Rule**: "If an ability uses the word 'cannot,' that effect is absolute."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No "cannot" effect system
- **Tests**: No tests for absolute restrictions
- **Assessment**: Critical for rule enforcement - "cannot" must override everything
- **Priority**: CRITICAL
- **Notes**: Sub-rule: "If two abilities use the word 'cannot,' a persistent ability takes precedence over a one-time ability and an enabling ability takes precedence over a cancel ability."

### 1.7 Must Resolve Abilities Entirely
**Rule**: "When a player resolves an ability, they must resolve the ability in its entirety. Any parts of the ability preceded by the word 'may' are optional, and the player resolving the ability may choose not to resolve those parts."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No ability resolution validation
- **Tests**: No tests for complete resolution
- **Assessment**: Need system to ensure abilities are fully resolved with optional parts
- **Priority**: HIGH
- **Dependencies**: Requires ability parsing and resolution framework

### 1.8 Mandatory vs Optional Abilities
**Rule**: "Abilities on components that remain in play are mandatory unless those abilities use the word 'may.'"

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No distinction between mandatory and optional abilities
- **Tests**: No tests for mandatory abilities
- **Assessment**: System needs to automatically trigger mandatory abilities
- **Priority**: HIGH
- **Dependencies**: Requires ability framework and trigger system

### 1.9 Resolve As Many Effects As Possible
**Rule**: "If an ability has multiple effects separated by the word 'and,' a player must resolve as many of the ability's effects as possible. However, if the player cannot resolve all of its effects, that player is allowed to resolve as many as they can."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No partial effect resolution system
- **Tests**: No tests for partial resolution
- **Assessment**: Complex system needed for partial ability resolution
- **Priority**: MEDIUM
- **Dependencies**: Requires ability parsing and effect validation

### 1.10 COSTS (Section Header)
**Rule**: Section header for ability costs

**Implementation Status**: ➖ NOT APPLICABLE
- **Notes**: This is just a section divider

### 1.11 Ability Costs Must Be Payable
**Rule**: "Some abilities have a cost that is followed by an effect. The cost of an ability is separated from the effect by the word 'to' or by a semicolon. A player cannot resolve the effect of such an ability if they cannot resolve that ability's cost."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No cost validation system
- **Tests**: No tests for cost validation
- **Assessment**: Critical for ability system - must validate costs before allowing effects
- **Priority**: HIGH
- **Dependencies**: Requires resource system and ability parsing

### 1.12 Cost Examples
**Rule**: "Some examples of an ability's cost include spending resources, spending trade goods, spending command tokens, exhausting cards, purging cards, and activating specific systems."

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Some resource systems exist but not integrated
- **Tests**: Basic resource tests exist
- **Assessment**: Individual cost types partially exist but not unified
- **Priority**: MEDIUM
- **Dependencies**: Requires resource, command token, and card systems

### 1.13 TIMING (Section Header)
**Rule**: Section header for ability timing

**Implementation Status**: ➖ NOT APPLICABLE
- **Notes**: This is just a section divider

### 1.14 Before/After Timing
**Rule**: "If the timing of an ability uses the word 'before' or 'after,' the ability's effect occurs immediately before or after the described timing event, respectively."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No temporal ability system
- **Tests**: No tests for timing
- **Assessment**: Need event system with before/after hooks
- **Priority**: HIGH
- **Dependencies**: Requires event system and ability framework
- **Notes**: Example given: "after a ship is destroyed" must be resolved immediately

### 1.15 When Timing
**Rule**: "If the timing of an ability uses the word 'when,' the ability's effect occurs at the moment of the described timing event."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No event-triggered ability system
- **Tests**: No tests for "when" timing
- **Assessment**: "When" abilities modify or replace the timing event
- **Priority**: HIGH
- **Dependencies**: Requires event system and ability framework

### 1.16 When vs After Priority
**Rule**: "Effects that occur 'when' an event happens take priority over effects that occur 'after' an event happens."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No timing priority system
- **Tests**: No tests for timing priority
- **Assessment**: Need priority queue for simultaneous effects
- **Priority**: MEDIUM
- **Dependencies**: Requires timing system and priority resolution

### 1.17 Then Conditional Effects
**Rule**: "If an ability uses the word 'then,' a player must resolve the effect that occurs before the word 'then' or they cannot resolve the effect that occurs after the word 'then.'"

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No conditional ability system
- **Tests**: No tests for conditional effects
- **Assessment**: Need conditional execution validation
- **Priority**: MEDIUM
- **Dependencies**: Requires ability parsing and conditional logic

### 1.18 Ability Frequency Per Trigger
**Rule**: "Each ability can be resolved once for each occurrence of that ability's timing event. For example, if an ability is resolved 'At the start of combat,' it can be resolved at the start of each combat."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No ability frequency tracking
- **Tests**: No tests for frequency limits
- **Assessment**: Need to track ability usage per trigger event
- **Priority**: MEDIUM
- **Dependencies**: Requires event system and usage tracking

### 1.19 Simultaneous Ability Resolution (Action Phase)
**Rule**: "If there are multiple abilities that players wish to resolve at the same time during the action phase, each player takes a turn resolving an ability in initiative order, beginning with the active player. This process continues until each player has resolved each ability that they wish to resolve during that window."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No simultaneous ability resolution system
- **Tests**: No tests for simultaneous resolution
- **Assessment**: Complex system for resolving multiple abilities in initiative order
- **Priority**: HIGH
- **Dependencies**: Requires initiative order, active player system, and ability queue

### 1.20 Simultaneous Ability Resolution (Other Phases)
**Rule**: "If there are multiple abilities that players wish to resolve at the same time during the strategy or agenda phases, players take turns resolving abilities starting with the speaker and proceeding clockwise. This process continues until each player has resolved each ability that they wish to resolve during that window."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No phase-specific ability resolution
- **Tests**: No tests for speaker-based resolution
- **Assessment**: Different resolution order for non-action phases
- **Priority**: HIGH
- **Dependencies**: Requires speaker system, phase detection, and ability queue

### 1.21 COMPONENT-SPECIFIC RULES (Section Header)
**Rule**: Section header for component-specific ability rules

**Implementation Status**: ➖ NOT APPLICABLE
- **Notes**: This is just a section divider

### 1.22 Action Card Ability Timing
**Rule**: "The opening paragraph of each ability found on an action card describes when a player can resolve that card's ability."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No action card system
- **Tests**: No action card tests
- **Assessment**: Action cards need timing descriptions in their text
- **Priority**: HIGH
- **Dependencies**: Requires action card system and ability parsing

### 1.23 Promissory Note Ability Timing
**Rule**: "The opening paragraph of most abilities found on promissory notes describes when a player can resolve that card's ability."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No promissory note system
- **Tests**: No promissory note tests
- **Assessment**: Promissory notes have different timing rules than action cards
- **Priority**: MEDIUM
- **Dependencies**: Requires promissory note system
- **Notes**: Sub-rule: "Some promissory notes have abilities that trigger as soon as a player receives the card."

### 1.24 Agenda Card Abilities
**Rule**: "Abilities on agenda cards correspond to an outcome. Players resolve these abilities during the agenda phase after players vote for a particular outcome."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No agenda system
- **Tests**: No agenda tests
- **Assessment**: Agenda abilities are outcome-based and phase-specific
- **Priority**: MEDIUM
- **Dependencies**: Requires agenda phase and voting system

### 1.25 Faction Abilities
**Rule**: "Each faction has faction abilities presented on its faction sheet. Each faction's flagship has one or more unique abilities. Some abilities provide players with perpetual effects."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No faction ability system
- **Tests**: No faction ability tests
- **Assessment**: Faction abilities are perpetual and faction-specific
- **Priority**: HIGH
- **Dependencies**: Requires faction system and perpetual effect tracking

### 1.26 Unit Abilities
**Rule**: "Some units have unit abilities. These abilities are named and presented above a unit's attributes on a player's faction sheet or on a unit upgrade card. Each unit ability has unique rules for when a player can resolve that ability."

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Basic unit system exists in `src/ti4/core/unit.py`
- **Tests**: Some unit tests exist
- **Assessment**: Unit structure exists but no abilities implemented
- **Priority**: HIGH
- **Dependencies**: Requires unit ability framework
- **Notes**: Lists specific unit abilities: Anti-Fighter Barrage, Bombardment, Deploy, Planetary Shield, Production, Space Cannon, Sustain Damage

### 1.27 Contextual References
**Rule**: "If a unit's ability uses the phrase 'this system' or 'this planet,' the ability is referring to the system or planet that contains that unit."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No contextual reference system
- **Tests**: No tests for contextual references
- **Assessment**: Need system to resolve "this system" and "this planet" references
- **Priority**: MEDIUM
- **Dependencies**: Requires unit location tracking and ability parsing