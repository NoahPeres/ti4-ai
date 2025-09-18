# Rule 3: ACTION PHASE

## Category Overview
During the action phase, each player takes a turn in initiative order performing actions. This process continues until all players have passed, then play proceeds to the status phase.

## Sub-Rules Analysis

### 3.1 - Three Action Types
**Raw LRR Text**: "During a player's turn, they may perform one of the following three types of actions: a strategic action, a tactical action, or a component action."

**Priority**: CRITICAL - Core action system
**Implementation Status**: ⚠️ PARTIAL - Strategic and tactical actions exist
**Test References**: `tests/test_game_controller.py`, `tests/test_tactical_action.py`
**Notes**: Strategic and tactical actions implemented, component actions need work

### 3.2 - Forced Pass Condition
**Raw LRR Text**: "If a player cannot perform an action, they must pass."

**Priority**: HIGH - Game flow control
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Need legal action detection system to enforce this rule

### 3.3 - Pass State Behavior
**Raw LRR Text**: "After a player has passed, they have no further turns and cannot perform additional actions during that action phase."
**Sub-rules**: 
- "During a turn that a player passes, they can resolve transactions and 'at the start of your turn' abilities."
- "A player that has passed can still resolve the secondary ability of other players' strategy cards."
- "It is possible for a player to perform multiple, consecutive actions during an action phase if all other players have passed during that action phase."

**Priority**: CRITICAL - Pass state tracking
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Critical gap - no pass state tracking system exists

### 3.4 - Strategic Action Requirements
**Raw LRR Text**: "A player cannot pass until they have performed the strategic action of their strategy card."
**Sub-rule**: "During a three-player or four-player game, a player cannot pass until they have exhausted both of their strategy cards."

**Priority**: HIGH - Strategy card enforcement
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Need strategy card usage tracking before allowing pass

### 3.5 - Phase Transition
**Raw LRR Text**: "After all players have passed, play proceeds to the status phase."

**Priority**: CRITICAL - Game flow progression
**Implementation Status**: ✅ IMPLEMENTED
**Test References**: `tests/test_game_state_machine.py`
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