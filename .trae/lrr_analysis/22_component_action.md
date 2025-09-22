# LRR Rule Analysis: Rule 22 - COMPONENT ACTION

## Category Overview
**Rule Category**: Action System - Core Mechanics
**Priority**: HIGH
**Implementation Status**: SIGNIFICANTLY IMPROVED - Action Card Integration Complete
**Dependencies**: Action Phase (Rule 3), ✅ Action Cards (Rule 2) - COMPLETED, Technology (Rule 90), Leaders, Exploration, Relics, Promissory Notes

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
**Status**: ✅ SIGNIFICANTLY IMPROVED - Action Cards Complete
**Implementation**: Action card component actions fully implemented with "Action" header recognition
**Tests**: Comprehensive action card tests in `test_action_cards.py` (39/39 passing)
**Priority**: HIGH
**Notes**: Action cards fully integrated with component action system. Other components (tech, leaders, etc.) still need implementation.

### 22.2 - Action Resolution
**Status**: ✅ SIGNIFICANTLY IMPROVED - Action Card Resolution Complete
**Implementation**: Action card text parsing and instruction execution fully implemented
**Tests**: Action card resolution tests in `test_action_cards.py`
**Priority**: HIGH
**Notes**: Action card ability text parsing and execution system complete. Other component types need similar implementation.

### 22.3 - Complete Resolution Requirement
**Status**: ✅ IMPLEMENTED FOR ACTION CARDS
**Implementation**: Action card validation ensures abilities can be completely resolved before execution
**Tests**: Complete resolution validation tests in `test_action_cards.py`
**Priority**: HIGH
**Notes**: Critical rule implemented for action cards - prevents partial ability resolution. Needs extension to other components.

### 22.4 - Action Cancellation
**Status**: ✅ IMPLEMENTED FOR ACTION CARDS
**Implementation**: Action card cancellation system fully implemented
**Tests**: Action cancellation tests in `test_action_cards.py`
**Priority**: MEDIUM
**Notes**: Canceled actions don't consume the player's action for the turn

## Related Topics
- **Rule 1**: ABILITIES - Component actions are a type of ability
- **Rule 2**: ✅ ACTION CARDS - COMPLETED - Major source of component actions fully implemented
- **Rule 3**: ACTION PHASE - When component actions can be performed
- **Rule 90**: TECHNOLOGY - Technology cards can have component actions (pending)
- **Leaders**: Leader cards can have component actions (pending)
- **Exploration**: Exploration cards can have component actions (pending)
- **Relics**: Relic cards can have component actions (pending)
- **Promissory Notes**: Can have component actions (pending)
- **Faction Sheets**: Can have faction-specific component actions (pending)

## Dependencies
- Action phase implementation with turn management
- ✅ Component systems - ACTION CARDS COMPLETE (39/39 tests passing)
- ✅ Ability text parsing and execution system - IMPLEMENTED FOR ACTION CARDS
- ✅ Action validation and cancellation mechanics - IMPLEMENTED FOR ACTION CARDS
- ✅ "Action" header recognition system - IMPLEMENTED FOR ACTION CARDS
- Pending: Technology, leaders, exploration, relics, promissory notes component actions

## Test References

### Existing Tests
- `test_action.py`: Basic action interface tests
- ✅ `test_action_cards.py`: **COMPREHENSIVE ACTION CARD COMPONENT ACTION TESTS (39/39 passing)**
  - Action card "Action" header recognition
  - Action card text parsing and instruction execution
  - Complete resolution validation for action cards
  - Action card cancellation mechanics
  - Action card integration with component action system
- `test_technology.py`: Research technology action tests (lines 109-278)
- `test_game_controller.py`: Some action controller tests

### Missing Tests
- Component action identification by "Action" header (for non-action-card components)
- Action text parsing and instruction following (for technology, leaders, etc.)
- Complete resolution validation before execution (for other component types)
- Action cancellation mechanics (for other component types)
- Component-specific action tests (tech cards, leaders, exploration, relics, promissory notes)
- Action phase integration with all component action types

## Implementation Files

### Existing Files
- `src/ti4/actions/action.py`: Base `Action` class
- `src/ti4/actions/tactical_action.py`: `TacticalAction` implementation
- ✅ `src/ti4/game/action_cards.py`: **COMPLETE ACTION CARD COMPONENT ACTION SYSTEM**
- `src/ti4/core/game_controller.py`: Basic action management
- `tests/test_action.py`: Basic action tests
- ✅ `tests/test_action_cards.py`: **COMPREHENSIVE ACTION CARD TESTS (39/39 passing)**

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
- ✅ **COMPLETE ACTION CARD COMPONENT ACTION SYSTEM**
  - Action card "Action" header recognition
  - Action card text parsing and instruction execution
  - Complete resolution validation for action cards
  - Action card cancellation mechanics
  - Comprehensive test coverage (39/39 tests passing)

### Implementation Gaps
- No "Action" header recognition system (for non-action-card components)
- No component action identification (for technology, leaders, etc.)
- No ability text parsing for instructions (for other component types)
- No complete resolution validation (for other components)
- No action cancellation mechanics (for other components)
- Missing component-specific action implementations (technology, leaders, exploration, relics, promissory notes)

### Critical Missing Features
- Component action discovery and registration (for non-action-card components)
- Ability text parsing and execution (for technology, leaders, etc.)
- Pre-execution validation (Rule 22.3) for other component types
- Action cancellation system (Rule 22.4) for other component types

## Action Items

### ✅ COMPLETED - Action Card Component Actions
1. ✅ **Implement "Action" header recognition system** - COMPLETED for action cards
2. ✅ **Create component action registry** - COMPLETED for action cards
3. ✅ **Build ability text parser** - COMPLETED for action cards
4. ✅ **Add complete resolution validation** - COMPLETED for action cards
5. ✅ **Implement action cancellation system** - COMPLETED for action cards
6. ✅ **Create action card component actions** - COMPLETED (39/39 tests passing)

### 🔄 REMAINING - Other Component Types
7. **Add technology component actions** - Implement technology card component actions
8. **Build leader component actions** - Implement leader-based component actions
9. **Create exploration component actions** - Implement exploration card component actions
10. **Add relic component actions** - Implement relic-based component actions
11. **Create promissory note component actions** - Implement promissory note component actions
12. **Create comprehensive component action tests** - Cover remaining component action mechanics
13. **Integrate component actions with action phase** - Ensure proper turn management for all types
