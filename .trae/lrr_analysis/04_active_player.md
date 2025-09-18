# Rule 4: ACTIVE PLAYER

## Category Overview
The active player is the player taking a turn during the action phase.

## Sub-Rules Analysis

### 4.1 - First Active Player
**Raw LRR Text**: "During the action phase, the player who is first in initiative order is the first active player."

**Priority**: CRITICAL - Core turn management
**Implementation Status**: ✅ IMPLEMENTED
**Test References**: `tests/test_game_controller.py::test_current_player_tracking`, `tests/test_game_controller.py::test_action_phase_turn_management`
**Notes**: Well implemented - initiative order determines first active player

### 4.2 - Turn Advancement
**Raw LRR Text**: "After the active player takes a turn, the next player in initiative order becomes the active player."

**Priority**: CRITICAL - Turn progression
**Implementation Status**: ✅ IMPLEMENTED
**Test References**: `tests/test_game_controller.py::test_turn_wrapping`, `tests/test_game_controller.py::test_action_phase_turn_management`
**Notes**: Properly implemented with correct turn cycling through `advance_turn()` method

### 4.3 - Turn Cycling with Pass State
**Raw LRR Text**: "After the last player in initiative order takes a turn, the player who is first in initiative order becomes the active player again, and turns begin again in initiative order, ignoring any players who have already passed."

**Priority**: HIGH - Pass state integration
**Implementation Status**: ⚠️ PARTIAL - Turn cycling works but pass state ignored
**Test References**: `tests/test_game_controller.py::test_turn_wrapping`
**Notes**: Turn cycling implemented but "ignoring any players who have already passed" not implemented - depends on Rule 3.3 pass state tracking

## Dependencies Summary

**Critical Dependencies:**
- Initiative order system (implemented)
- Turn advancement mechanism (implemented)
- Pass state tracking from Rule 3.3 (missing)

**Related Systems:**
- Action phase management
- Game controller turn tracking
- Player activation validation

## Action Items

1. **Integrate pass state tracking** - Modify turn advancement to skip players who have passed
2. **Add pass state validation** - Ensure turn cycling respects passed players
3. **Test pass state integration** - Add tests for turn cycling with passed players
- **Current State**: Not Started/In Progress/Complete
- **Estimated Effort**: Small/Medium/Large
- **Dependencies**: 
- **Blockers**: 

## Notes
- 
- 
- 

## Related Rules
- Rule 3: ACTION PHASE
- Rule 45: INITIATIVE ORDER
- Rule 85: TACTICAL ACTION
- Rule 84: STRATEGIC ACTION

## Action Items
- [ ] 
- [ ] 
- [ ]