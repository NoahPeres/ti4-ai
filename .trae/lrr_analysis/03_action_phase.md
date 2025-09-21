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

## Dependencies Summary

**Critical Dependencies:**
- Pass state tracking system (for 3.3, 3.4, 3.5)
- Legal action detection (for 3.2)
- Strategy card usage tracking (for 3.4)
- Component action framework (for 3.1)

**Related Systems:**
- Game state machine (phase transitions)
- Turn order management
- Strategy card system
- Action validation system

## Action Items

1. **Implement pass state tracking system** - Track which players have passed and prevent further actions
2. **Add legal action detection** - Determine when a player must pass due to no available actions
3. **Implement strategy card usage tracking** - Prevent passing until strategic actions are used
4. **Complete component action framework** - Finish implementation of third action type
5. **Add pass enforcement validation** - Ensure players cannot act after passing
6. **Implement sub-rule exceptions** - Handle transactions and secondary abilities for passed players
7. **Add automatic phase progression** - Transition to status phase when all players have passed
