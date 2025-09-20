# LRR Rule Analysis: Rule 22 - COMPONENT ACTION

## Category Overview
**Rule Category**: Action System - Core Mechanics
**Priority**: HIGH
**Implementation Status**: PARTIALLY IMPLEMENTED
**Dependencies**: Action Phase (Rule 3), Action Cards (Rule 2), Technology (Rule 90), Leaders, Exploration, Relics, Promissory Notes

## Raw LRR Text

### 22 COMPONENT ACTION
A component action is a type of action that a player can perform during their turn of an action phase.

**22.1** Component actions can be found on various game components, including action cards, technology cards, leaders, exploration cards, relics, promissory notes, and faction sheets. Each component action is indicated by an "Action" header.

**22.2** To perform a component action, a player reads the action's text and follows the instructions as described.

**22.3** A component action cannot be performed if its ability cannot be completely resolved.

**22.4** If a component action is canceled, it does not use that player's action.

**Related Topics**: Abilities, Action Cards, Action Phase, Exploration, Leaders, Promissory Notes, Relics, Technology

## Sub-Rules Analysis

### 22.1 - Component Action Sources
**Status**: ⚠️ PARTIALLY IMPLEMENTED
**Implementation**: Basic action framework exists but component-specific actions missing
**Tests**: Basic action tests exist in `test_action.py`
**Priority**: HIGH
**Notes**: Need action headers on all component types (action cards, tech cards, leaders, etc.)

### 22.2 - Action Resolution
**Status**: ⚠️ PARTIALLY IMPLEMENTED
**Implementation**: Basic action execution exists but no text parsing/instruction following
**Tests**: Basic action resolution tests exist
**Priority**: HIGH
**Notes**: Need ability text parsing and instruction execution system

### 22.3 - Complete Resolution Requirement
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No validation that abilities can be completely resolved before execution
**Tests**: No complete resolution validation tests
**Priority**: HIGH
**Notes**: Critical rule - prevents partial ability resolution

### 22.4 - Action Cancellation
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No action cancellation system
**Tests**: No cancellation tests
**Priority**: MEDIUM
**Notes**: Canceled actions don't consume the player's action for the turn

## Related Topics
- **Rule 1**: ABILITIES - Component actions are a type of ability
- **Rule 2**: ACTION CARDS - Major source of component actions
- **Rule 3**: ACTION PHASE - When component actions can be performed
- **Rule 90**: TECHNOLOGY - Technology cards can have component actions
- **Leaders**: Leader cards can have component actions
- **Exploration**: Exploration cards can have component actions
- **Relics**: Relic cards can have component actions
- **Promissory Notes**: Can have component actions
- **Faction Sheets**: Can have faction-specific component actions

## Dependencies
- Action phase implementation with turn management
- Component systems (action cards, technology, leaders, etc.)
- Ability text parsing and execution system
- Action validation and cancellation mechanics
- "Action" header recognition system

## Test References

### Existing Tests
- `test_action.py`: Basic action interface tests
- `test_technology.py`: Research technology action tests (lines 109-278)
- `test_game_controller.py`: Some action controller tests

### Missing Tests
- Component action identification by "Action" header
- Action text parsing and instruction following
- Complete resolution validation before execution
- Action cancellation mechanics
- Component-specific action tests (action cards, tech cards, leaders, etc.)
- Action phase integration with component actions

## Implementation Files

### Existing Files
- `src/ti4/actions/action.py`: Base `Action` class
- `src/ti4/actions/tactical_action.py`: `TacticalAction` implementation
- `src/ti4/core/game_controller.py`: Basic action management
- `tests/test_action.py`: Basic action tests

### Missing Files
- Component action registry/factory
- Action text parser and executor
- Action validation system
- Component-specific action implementations
- Action cancellation system

## Notable Implementation Details

### Well-Implemented
- Basic action framework with `Action` base class
- Tactical action implementation with step-based architecture
- Basic action interface and testing

### Implementation Gaps
- No "Action" header recognition system
- No component action identification
- No ability text parsing for instructions
- No complete resolution validation
- No action cancellation mechanics
- Missing component-specific action implementations

### Critical Missing Features
- Component action discovery and registration
- Ability text parsing and execution
- Pre-execution validation (Rule 22.3)
- Action cancellation system (Rule 22.4)

## Action Items

1. **Implement "Action" header recognition system** - Identify component actions by header text
2. **Create component action registry** - Catalog all available component actions from various sources
3. **Build ability text parser** - Parse and execute component action instructions
4. **Add complete resolution validation** - Ensure abilities can be fully resolved before execution
5. **Implement action cancellation system** - Handle canceled actions without consuming player's turn
6. **Create action card component actions** - Implement action card-based component actions
7. **Add technology component actions** - Implement technology card component actions
8. **Build leader component actions** - Implement leader-based component actions
9. **Create comprehensive component action tests** - Cover all component action mechanics
10. **Integrate component actions with action phase** - Ensure proper turn management and validation
