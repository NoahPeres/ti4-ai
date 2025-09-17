# LRR Rule Analysis: Section 3 - ACTION PHASE

## 3. ACTION PHASE

**Rule Category Overview**: During the action phase, each player takes a turn in initiative order. During a player's turn, they perform a single action. After each player has taken a turn, player turns begin again in initiative order. This process continues until all players have passed.

### 3.1 Three Action Types
**Rule**: "During a player's turn, they may perform one of the following three types of actions: a strategic action, a tactical action, or a component action."

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Action types exist in `src/ti4/actions/` directory
- **Tests**: `tests/test_action.py` tests action interface
- **Assessment**: Basic action structure exists but not fully integrated with game flow
- **Priority**: CRITICAL
- **Dependencies**: Requires action phase flow and turn management
- **Notes**: The three action types are fundamental to TI4 gameplay

### 3.2 Must Pass If Cannot Act
**Rule**: "If a player cannot perform an action, they must pass."

**Implementation Status**: ⚠️ PARTIAL
- **Code**: `GameController.pass_turn()` exists in `src/ti4/core/game_controller.py`
- **Tests**: Some game controller tests exist in `tests/test_game_controller.py`
- **Assessment**: Pass mechanism exists but no enforcement of "must pass" rule
- **Priority**: HIGH
- **Dependencies**: Requires action validation and forced pass logic
- **Notes**: System must detect when no legal actions are available

### 3.3 No Actions After Passing
**Rule**: "After a player has passed, they have no further turns and cannot perform additional actions during that action phase."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No pass state tracking
- **Tests**: No tests for post-pass restrictions
- **Assessment**: Critical for turn order integrity - passed players must be excluded
- **Priority**: CRITICAL
- **Dependencies**: Requires pass state tracking and action validation
- **Notes**: Sub-rules allow some exceptions:
  - "During a turn that a player passes, they can resolve transactions and 'at the start of your turn' abilities."
  - "A player that has passed can still resolve the secondary ability of other players' strategy cards."
  - "It is possible for a player to perform multiple, consecutive actions during an action phase if all other players have passed during that action phase."

### 3.4 Must Perform Strategic Action Before Passing
**Rule**: "A player cannot pass until they have performed the strategic action of their strategy card."

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Strategy card system exists in `GameController`
- **Tests**: Some strategy card tests exist
- **Assessment**: Strategy cards exist but no pass restriction enforcement
- **Priority**: CRITICAL
- **Dependencies**: Requires strategic action tracking and pass validation
- **Notes**: Sub-rule: "During a three-player or four-player game, a player cannot pass until they have exhausted both of their strategy cards."

### 3.5 Proceed to Status Phase After All Pass
**Rule**: "After all players have passed, play proceeds to the status phase."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No phase transition system
- **Tests**: No phase transition tests
- **Assessment**: Need automatic phase progression when all players pass
- **Priority**: HIGH
- **Dependencies**: Requires phase management and pass tracking for all players
- **Notes**: This completes the action phase and triggers the next game round phase