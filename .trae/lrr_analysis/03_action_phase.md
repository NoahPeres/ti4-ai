# Rule 3: ACTION PHASE

## Category Overview
During the action phase, each player takes a turn in initiative order performing actions. This process continues until all players have passed, then play proceeds to the status phase.

## Sub-Rules Analysis

### 3.1 - Three Action Types
**Raw LRR Text**: "During a player's turn, they may perform one of the following three types of actions: a strategic action, a tactical action, or a component action."

**Priority**: CRITICAL - Core action system
**Implementation Status**: ✅ IMPLEMENTED - Strategic and tactical actions exist
**Test References**: `tests/test_rule_03_action_phase.py::test_action_phase_turn_order_follows_initiative`
**Notes**: Strategic and tactical actions implemented, component actions need work

### 3.2 - Forced Pass Condition
**Raw LRR Text**: "If a player cannot perform an action, they must pass."

**Priority**: HIGH - Game flow control
**Implementation Status**: ✅ IMPLEMENTED - Must pass validation exists
**Test References**: `tests/test_rule_03_action_phase.py::test_player_must_pass_if_cannot_perform_action`
**Notes**: Implemented via `must_pass()` method and action validation

### 3.3 - Pass State Behavior
**Raw LRR Text**: "After a player has passed, they have no further turns and cannot perform additional actions during that action phase."
**Sub-rules**:
- "During a turn that a player passes, they can resolve transactions and 'at the start of your turn' abilities."
- "A player that has passed can still resolve the secondary ability of other players' strategy cards."
- "It is possible for a player to perform multiple, consecutive actions during an action phase if all other players have passed during that action phase."

**Priority**: CRITICAL - Pass state tracking
**Implementation Status**: ✅ IMPLEMENTED - Pass state tracking and turn cycling
**Test References**:
- `tests/test_rule_03_action_phase.py::test_passed_player_has_no_further_turns`
- `tests/test_rule_03_action_phase.py::test_pass_state_persists_across_rounds`
- `tests/test_rule_03_action_phase.py::test_consecutive_actions_when_others_passed`
- `tests/test_rule_03_action_phase.py::test_passed_player_can_resolve_secondary_abilities`
**Notes**: Comprehensive pass state tracking with proper turn cycling that skips passed players

### 3.4 - Strategic Action Requirements
**Raw LRR Text**: "A player cannot pass until they have performed the strategic action of their strategy card."
**Sub-rule**: "During a three-player or four-player game, a player cannot pass until they have exhausted both of their strategy cards."

**Priority**: HIGH - Strategy card enforcement
**Implementation Status**: ✅ IMPLEMENTED - Strategic action tracking for pass requirements
**Test References**:
- `tests/test_rule_03_action_phase.py::test_cannot_pass_without_strategic_action`
- `tests/test_rule_03_action_phase.py::test_three_player_game_requires_both_cards_exhausted`
**Notes**: Implemented via `can_pass()` method with strategic action usage tracking

### 3.5 - Phase Transition
**Raw LRR Text**: "After all players have passed, play proceeds to the status phase."

**Priority**: CRITICAL - Game flow progression
**Implementation Status**: ✅ IMPLEMENTED - Automatic phase transition
**Test References**: `tests/test_rule_03_action_phase.py::test_action_phase_completes_when_all_pass`
**Notes**: Phase transition logic exists in game state machine

## Current Implementation Status

### ✅ IMPLEMENTED (Core Foundation)
- **3.1**: Three action types - Strategic and tactical actions fully implemented
- **3.2**: Forced pass condition - Must pass validation exists via `must_pass()` method
- **3.3**: Pass state behavior - Pass state tracking and turn cycling implemented
- **3.4**: Strategic action requirements - Strategic action tracking for pass requirements implemented
- **3.5**: Phase transition - Automatic phase transition to status phase implemented

### ⚠️ PARTIALLY IMPLEMENTED (Needs Completion)
- **Component action framework** - Third action type needs completion
- **Legal action detection** - Forced pass scenarios need refinement
- **Transaction resolution during pass turns** - Edge cases need implementation

### ❌ GAPS IDENTIFIED
- **Component action system** - Framework exists but needs completion
- **Advanced legal action detection** - More sophisticated validation for forced pass scenarios
- **Edge case handling** - Some transaction and secondary ability edge cases during pass turns

## Priority Action Items for Completion

### HIGH (Core Functionality Gaps)
1. **Complete component action framework** - Finish implementation of third action type
2. **Refine legal action detection** - Improve validation for forced pass scenarios
3. **Implement transaction edge cases** - Handle transaction resolution during pass turns

### MEDIUM (Polish and Edge Cases)
4. **Enhanced pass state validation** - Additional validation for pass state edge cases
5. **Improved error handling** - Better error messages for invalid action attempts
6. **Integration testing** - More comprehensive integration with other game systems

## Blocking Relationships
- **Component actions** block full action type coverage
- **Legal action detection** affects game flow validation
- **Transaction edge cases** affect diplomatic gameplay during action phase

## Dependencies Summary

**✅ IMPLEMENTED Dependencies:**
- Pass state tracking system (3.3, 3.4, 3.5) - ✅ Complete
- Strategy card usage tracking (3.4) - ✅ Complete
- Game state machine (phase transitions) - ✅ Complete
- Turn order management - ✅ Complete

**⚠️ PARTIAL Dependencies:**
- Component action framework (3.1) - Needs completion
- Legal action detection (3.2) - Needs refinement
- Action validation system - Needs enhancement
