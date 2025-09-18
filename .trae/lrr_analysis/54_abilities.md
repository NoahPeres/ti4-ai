# Rule 54: ABILITIES

## Category Overview
**Rule Type**: Core Game Framework  
**Complexity**: Very High  
**Implementation Priority**: Critical  
**Dependencies**: All Game Systems (foundational rule)  

## Raw LRR Text
From `lrr.txt` section 1 (Note: Rule 54 in sequence, but LRR section 1):

**1** ABILITIES  
Cards and faction sheets each have abilities that players can resolve to trigger various game effects.

**1.1** If information in this Rules Reference contradicts the Learn to Play booklet, the Rules Reference takes precedence.

**1.2** If a card ability contradicts information in the Rules Reference, the card takes precedence. If both the card and the rules can be followed at the same time, they should be.

**1.3** Each ability describes when and how a player can resolve it.

**1.4** If an ability with a specified duration is resolved, the effect of the ability remains through that duration, even if the component that caused the ability is removed.

**1.5** If an ability contains the word "Action," a player must use a component action during the action phase to resolve that ability.

**1.6** If an ability uses the word "cannot," that effect is absolute.
- If two abilities use the word "cannot," a persistent ability takes precedence over a one-time ability and an enabling ability takes precedence over a cancel ability.

**1.7** When a player resolves an ability, they must resolve the ability in its entirety. Any parts of the ability preceded by the word "may" are optional, and the player resolving the ability may choose not to resolve those parts.

**1.8** Abilities on components that remain in play are mandatory unless those abilities use the word "may."

**1.9** If an ability has multiple effects separated by the word "and," a player must resolve as many of the ability's effects as possible. However, if the player cannot resolve all of its effects, that player is allowed to resolve as many as they can.

**1.10** COSTS

**1.11** Some abilities have a cost that is followed by an effect. The cost of an ability is separated from the effect by the word "to" or by a semicolon. A player cannot resolve the effect of such an ability if they cannot resolve that ability's cost.

**1.12** Some examples of an ability's cost include spending resources, spending trade goods, spending command tokens, exhausting cards, purging cards, and activating specific systems.

**1.13** TIMING

**1.14** If the timing of an ability uses the word "before" or "after," the ability's effect occurs immediately before or after the described timing event, respectively.

**1.15** If the timing of an ability uses the word "when," the ability's effect occurs at the moment of the described timing event.

**1.16** Each ability can be resolved once for each occurrence of that ability's timing event.

**1.17** If an ability has the same timing as another ability, players can choose the order in which they resolve those abilities.

**1.18** If an ability was resolved, then its timing event occurs again, the ability can be resolved again.

**1.19** If there are multiple abilities that players wish to resolve at the same time during the action phase, each player takes a turn resolving an ability in initiative order, beginning with the active player. This process continues until each player has resolved each ability that they wish to resolve.

**1.20** If there are multiple abilities that players wish to resolve at the same time during the strategy or agenda phases, players take turns resolving abilities starting with the speaker and proceeding clockwise. This process continues until each player has resolved each ability that they wish to resolve.

**1.21** COMPONENT-SPECIFIC RULES

**1.22** The opening paragraph of each ability found on an action card describes when a player can resolve that card's ability.

**1.23** The opening paragraph of most abilities found on promissory notes describes when a player can resolve that card's ability.
- Some promissory notes have abilities that trigger as soon as a player receives the card.

**1.24** Abilities on agenda cards correspond to an outcome. Players resolve these abilities during the agenda phase after players vote for a particular outcome.

**1.25** Some abilities found on faction sheets and technology cards are component actions.

**1.26** If a unit's ability uses the phrase "this system" or "this planet," the ability is referring to the system or planet that contains that unit.

**Related Topics**: Action Cards, Leaders, Promissory Notes, Strategy Card, Technology

## Sub-Rules Analysis

### 1.1 - Rules Reference Precedence
- **Status**: ➖ Not Applicable (Meta-rule)
- **Location**: Documentation principle
- **Test Coverage**: Not applicable
- **Implementation Notes**: Documentation hierarchy, not code

### 1.2 - Card Ability Precedence
- **Status**: ❌ Not Implemented
- **Location**: No ability precedence system found
- **Test Coverage**: None found
- **Implementation Notes**: Critical - cards must override base rules

### 1.3 - Ability Description Requirements
- **Status**: ⚠️ Partially Implemented
- **Location**: `src/ti4/actions/action.py` - Action base class
- **Test Coverage**: `test_action.py` - Basic action interface
- **Implementation Notes**: Framework exists but limited to actions

### 1.4 - Ability Duration
- **Status**: ❌ Not Implemented
- **Location**: No duration tracking system found
- **Test Coverage**: None found
- **Implementation Notes**: Need temporal effect system

### 1.5 - Action Abilities
- **Status**: ⚠️ Partially Implemented
- **Location**: Action framework exists
- **Test Coverage**: Basic action tests
- **Implementation Notes**: Framework exists but needs action phase integration

### 1.6 - Cannot Effects
- **Status**: ❌ Not Implemented
- **Location**: No "cannot" effect system found
- **Test Coverage**: None found
- **Implementation Notes**: Critical - absolute restrictions system needed

### 1.7 - Complete Resolution
- **Status**: ❌ Not Implemented
- **Location**: No ability resolution validation found
- **Test Coverage**: None found
- **Implementation Notes**: Need mandatory/optional part handling

### 1.8 - Mandatory Abilities
- **Status**: ❌ Not Implemented
- **Location**: No mandatory ability system found
- **Test Coverage**: None found
- **Implementation Notes**: Auto-trigger system needed

### 1.9 - Multiple Effects Resolution
- **Status**: ❌ Not Implemented
- **Location**: No multi-effect resolution system found
- **Test Coverage**: None found
- **Implementation Notes**: Partial resolution handling needed

### 1.11-1.12 - Ability Costs
- **Status**: ⚠️ Partially Implemented
- **Location**: Some resource systems exist
- **Test Coverage**: Basic resource tests
- **Implementation Notes**: Individual cost types exist but not unified

### 1.14-1.18 - Timing System
- **Status**: ❌ Not Implemented
- **Location**: No temporal ability system found
- **Test Coverage**: None found
- **Implementation Notes**: Event system with before/after/when hooks needed

### 1.19-1.20 - Simultaneous Resolution
- **Status**: ❌ Not Implemented
- **Location**: No simultaneous ability resolution found
- **Test Coverage**: None found
- **Implementation Notes**: Initiative order and speaker-based resolution needed

### 1.22-1.26 - Component-Specific Rules
- **Status**: ❌ Not Implemented
- **Location**: No component-specific ability systems found
- **Test Coverage**: None found
- **Implementation Notes**: Action cards, promissory notes, agenda cards, unit abilities all missing

## Related Topics
- **Rule 2**: ACTION CARDS (card-based abilities)
- **Rule 69**: PURGE (ability cost type)
- **Rule 71**: READIED (ability availability)
- **Rule 83**: STRATEGY CARD (strategy card abilities)
- **All Combat Rules**: Unit abilities in combat
- **All Phase Rules**: Phase-specific ability timing

## Dependencies
- **Event System**: For timing-based abilities (before/after/when)
- **Card System**: For card-based abilities
- **Resource System**: For ability costs
- **Phase System**: For phase-specific ability resolution
- **Initiative System**: For simultaneous ability resolution
- **Component System**: For component-specific abilities
- **Duration Tracking**: For temporary effects

## Test References
### Current Test Coverage:
- `test_unit.py`: Unit abilities testing
  - Sustain damage ability detection and usage
  - Anti-fighter barrage, space cannon, bombardment abilities
  - Deploy, planetary shield, production abilities
  - Multiple abilities on same unit
  - Unit abilities integration testing

- `test_combat.py`: Combat-related abilities
  - Sustain damage abilities in combat resolution
  - Unit abilities in combat context

- `test_integration.py`: Faction-specific abilities (basic)

### Test Scenarios Covered:
1. **Unit Abilities**: Comprehensive unit ability testing
2. **Combat Integration**: Abilities in combat context
3. **Ability Detection**: Identifying units with specific abilities
4. **Multiple Abilities**: Units with multiple abilities

### Missing Test Scenarios:
1. **Card Abilities**: No action card, promissory note, or agenda card ability tests
2. **Ability Precedence**: No tests for card vs rules precedence
3. **Timing System**: No before/after/when timing tests
4. **Mandatory vs Optional**: No tests for "may" vs mandatory abilities
5. **Cannot Effects**: No tests for absolute restrictions
6. **Duration Effects**: No tests for temporary abilities
7. **Cost System**: No unified ability cost testing
8. **Simultaneous Resolution**: No tests for multiple ability resolution
9. **Component Actions**: No tests for action phase ability usage

## Implementation Files
### Core Implementation:
- `src/ti4/actions/action.py`: Basic Action base class
- `src/ti4/core/unit.py`: Unit abilities (sustain damage, etc.)
- `src/ti4/actions/tactical_action.py`: Tactical action framework

### Supporting Files:
- Unit ability implementations
- Basic action framework
- Combat ability integration

### Missing Implementation:
- General ability framework
- Card ability system (action cards, promissory notes, agenda cards)
- Timing and event system
- Ability precedence system
- Duration tracking system
- Cost validation system
- Mandatory ability triggers
- Cannot effect system
- Simultaneous resolution system

## Notable Implementation Details

### Strengths:
1. **Unit Abilities**: Well-implemented unit ability system
2. **Combat Integration**: Abilities work in combat context
3. **Action Framework**: Basic action structure exists
4. **Comprehensive Testing**: Unit abilities thoroughly tested

### Areas Needing Attention:
1. **General Framework**: No unified ability system
2. **Card Abilities**: Action cards, promissory notes, agenda cards missing
3. **Timing System**: No event-based ability triggers
4. **Precedence Rules**: No card vs rules precedence
5. **Duration Effects**: No temporary ability system
6. **Cost Validation**: No unified cost system
7. **Mandatory Triggers**: No automatic ability resolution

### Architecture Quality:
- **Good**: Unit abilities and combat integration
- **Needs Work**: General ability framework and card systems
- **Missing**: Timing, precedence, and duration systems

## Action Items

### Critical Priority:
1. **Design General Ability Framework**: Unified system for all ability types
2. **Implement Card Ability Precedence**: Cards override rules system
3. **Create Timing/Event System**: Before/after/when ability triggers
4. **Add Cannot Effect System**: Absolute restriction handling

### High Priority:
5. **Implement Action Card Abilities**: Action card system with abilities
6. **Add Duration Tracking**: Temporary effect system
7. **Create Cost Validation**: Unified ability cost system
8. **Implement Mandatory Triggers**: Auto-resolve mandatory abilities

### Medium Priority:
9. **Add Promissory Note Abilities**: Promissory note system
10. **Implement Agenda Card Abilities**: Agenda card ability system
11. **Create Simultaneous Resolution**: Initiative-based ability resolution
12. **Add Component Actions**: Action phase ability usage

### Low Priority:
13. **Expand Unit Abilities**: Additional unit ability types
14. **Add Faction Abilities**: Faction sheet abilities
15. **Implement Technology Abilities**: Technology card abilities
16. **Create Ability UI**: Visual ability feedback system

## Priority Assessment
**Overall Priority**: Critical - Abilities are the core game mechanic

**Implementation Status**: Partial (25%)
- Unit abilities: ✅ Well Implemented
- Action framework: ⚠️ Basic Structure
- Card abilities: ❌ Missing
- Timing system: ❌ Missing
- Precedence system: ❌ Missing
- Duration tracking: ❌ Missing
- Cost validation: ❌ Missing

**Recommended Focus**: 
1. Design unified ability framework that encompasses all ability types
2. Implement card ability precedence system (critical for game integrity)
3. Create event-based timing system for before/after/when triggers
4. Add cannot effect system for absolute restrictions

The current implementation has excellent unit abilities but lacks the general framework needed for the full ability system. This is a foundational system that affects every aspect of the game, making it critical priority despite the significant implementation effort required.