# Rule 78: Space Combat - Analysis

## Raw LRR Text

```text
78 SPACE COMBAT
After resolving the "Space Cannon Offense" step of a tactical action, if two players have ships in the active system, those players must resolve a space combat.

78.1 If the active player is the only player with ships in the system, they skip the "Space Combat" step of the tactical action and proceeds to the "Invasion" step.

78.2 If an ability occurs "before combat," it occurs immediately before the "Anti-Fighter Barrage" step.
a    During the first round of a combat, "start of combat" and "start of combat round" effects occur during the same timing window.
b    During the last round of a combat, "end of combat" and "end of combat round" effects occur during the same timing window.

To resolve a space combat, players perform the following steps:

78.3 STEP 1-ANTI-FIGHTER BARRAGE: If this is the first round of a space combat, the players may simultaneously use the "Anti-Fighter Barrage" ability of any of their units in the active system.
a    If one or both players no longer have ships in the active system after resolving this step, the space combat ends immediately.
b    Players cannot resolve "Anti-Fighter Barrage" abilities during any rounds of space combat other than the first round.
c    This step still occurs if no fighters are present.

78.4 STEP 2-ANNOUNCE RETREATS: Each player may announce a retreat, beginning with the defender.
a    A retreat will not occur immediately; the units retreat during the "Retreat" step.
b    If the defender announces a retreat, the attacker cannot announce a retreat during that combat round.
c    A player cannot announce a retreat if there is not at least one eligible system to retreat to.

78.5 STEP 3-ROLL DICE: Each player rolls one die for each ship they have in the active system; this is called a combat roll. If a unit's combat roll produces a result that is equal to or greater than that unit's combat value, that result produces a hit.
a    If a unit's combat value contains two or more burst icons, the player rolls one die for each burst icon instead.
b    If a player has ships that have different combat values in the active system, that player rolls these dice separately.
c    First, that player should roll all dice for units with a combat value of "1." Then, that player should roll all dice for units with combat value of "2," and then "3," continuing in numerical order until that player has rolled dice for each of their ships.
d    The player counts each hit their combat rolls produce. The total number of hits produced will destroy units during the "Assign Hits" step.
e    If a player has an ability that rerolls a die or affects a die after it is rolled, that player must resolve such an ability immediately after rolling all of their dice.
f    The attacker makes all of their combat rolls during this step before the defender. This procedure is important for abilities that allow a player to reroll an opponent's die.

78.6 STEP 4-ASSIGN HITS: Each player in the combat must choose and destroy one of their own ships in the active system for each hit their opponent produced.
a    Before assigning hits, players may use their units' "Sustain Damage" abilities to cancel hits.
b    When a unit is destroyed, the player who controls that unit removes it from the board and places it in their reinforcements.

78.7 STEP 5-RETREAT: If a player announced a retreat during step 2, and there is still an eligible system for their units to retreat to, they must retreat.
a    If a player announced a retreat during the "Announce Retreats" step, but their opponent has no ships remaining in the system, the combat immediately ends and the retreat does not occur.
b    To retreat, a player takes all of their ships with a move value in the combat and moves them to a single system that is adjacent to the active system. That player's fighters and ground forces in the space area of the active system that are unable to move or be transported are removed.
c    The system that a player's units retreat to must contain one or more of that player's units, a planet they control, or both. Additionally, the system cannot contain ships controlled by another player.
d    If any of a player's units successfully retreat and are moved into an adjacent system, that player must place a command token from their reinforcements in the system to which their units retreated. If that system already contains one of their command tokens, that player does not place an additional token there. If the player has no command tokens in their reinforcements, that player must use one from their command sheet instead.

78.8 After the "Retreat" step, if both players still have ships in the active system, those players resolve another round of space combat beginning with the "Announce Retreats" step.

78.9 Space combat ends when only one player-or neither player- has a ship in the space area of the active system.
a    During the last round of a combat, "end of combat" and "end of combat round" effects occur during the same timing window.

78.10 After a combat ends, the player with one or more ships remaining in the system is the winner of the combat; the other player is the loser of the combat. If neither player has a ship remaining, the combat ends in a draw and there is no winner.
a    If the winner of the combat has fighters or ground forces in the space area of the active system and those units exceed the capacity of that player's ships in that system, that player must choose and remove any excess units.

RELATED TOPICS: Capacity, Fleet Pool, Opponent, Sustain Damage, Tactical Action, Transport
```

## Overview
Space combat is a complex system involving multiple phases and steps. This analysis covers the implementation status of each rule component.

## Rule Breakdown and Test Coverage

### Rule 78.1: Combat Detection
**Status**: ✅ Implemented
**Description**: Combat occurs when ships of different players occupy the same system during certain game actions.
**Test Cases**:
- `test_combat_detection_with_ships()` - Verifies combat is detected when opposing ships are present
- `test_no_combat_without_ships()` - Verifies no combat when no ships present
- `test_no_combat_same_player()` - Verifies no combat between same player's units

### Rule 78.2: Combat Initiation
**Status**: ✅ Implemented
**Description**: Combat begins with the first combat round.
**Test Cases**:
- `test_combat_initiation()` - Verifies combat starts properly with correct participants
- `test_combat_round_creation()` - Verifies combat rounds are created with proper structure

### Rule 78.3: Announce Retreats Step
**Status**: ✅ Implemented
**Description**: At the start of each combat round, players may announce retreat, beginning with the defender.
**Implementation Note**: The attacker may announce retreat only if the defender has not announced and an eligible system exists. Per LRR 78.4.b, if the defender announces retreat, the attacker cannot announce retreat during that combat round. Per LRR 78.4.c, a player cannot announce retreat without at least one eligible system.
**Test Cases**:
- `test_announce_retreats_step()` - Verifies both attacker and defender retreat announcement scenarios

### Rule 78.5: Roll Dice Step
**Status**: ✅ Implemented
**Description**: Players roll dice for their participating units.
**Test Cases**:
- `test_roll_dice_step()` - Verifies dice rolling mechanics for combat units
- `test_dice_results_calculation()` - Verifies hit calculation from dice results

### Rule 78.6: Assign Hits Step
**Status**: ✅ Implemented
**Description**: Players assign hits to their units, potentially destroying them.
**Test Cases**:
- `test_assign_hits_step()` - Verifies hit assignment and unit destruction
- `test_hit_assignment_priority()` - Verifies proper hit assignment rules

### Rule 78.7: Retreat Step
**Status**: ✅ Implemented
**Description**: If retreat was announced, the retreating player moves their ships.
**Test Cases**:
- `test_retreat_step()` - Verifies retreat execution when announced
- `test_no_retreat_when_not_announced()` - Verifies no retreat when not announced

### Rule 78.8: Combat Continuation After Retreat
**Status**: ✅ Implemented
**Description**: After retreat execution, if both players still have ships in the system, combat continues with a new round starting at the "Announce Retreats" step.
**Test Cases**:
- `test_rule_78_8_combat_continuation_after_retreat()` - Verifies combat continues after partial retreat
  - Tests that combat continues when both sides have remaining ships
  - Tests that new combat round starts at ANNOUNCE_RETREATS step
  - Tests that retreated units don't participate in continued combat

### Rule 78.9: Combat Ending Conditions
**Status**: ✅ Implemented
**Description**: Combat ends when one or both players have no ships remaining in the system, or when all eligible players retreat.
**Test Cases**:
- `test_rule_78_9_combat_ends_no_attacker_ships()` - Tests combat ends when attacker has no ships
- `test_rule_78_9_combat_ends_no_defender_ships()` - Tests combat ends when defender has no ships
- `test_rule_78_9_combat_ends_no_ships_either_side()` - Tests combat ends when neither side has ships

### Rule 78.10: Winner and Loser Determination
**Status**: ✅ Implemented
**Description**: The player with ships remaining in the system after combat is the winner. If no player has ships, the combat is a draw.
**Test Cases**:
- `test_rule_78_10_attacker_wins()` - Tests attacker victory when defender has no ships
  - Verifies winner is set to attacker
  - Verifies loser is set to defender
  - Verifies is_draw is False
- `test_rule_78_10_defender_wins()` - Tests defender victory when attacker has no ships
  - Verifies winner is set to defender
  - Verifies loser is set to attacker
  - Verifies is_draw is False
- `test_rule_78_10_draw_result()` - Tests draw when neither side has ships
  - Verifies winner is None
  - Verifies loser is None
  - Verifies is_draw is True

## Implementation Notes

### Key Classes
- `SpaceCombat`: Main combat orchestrator
- `CombatRound`: Represents a single round of combat
- `SpaceCombatResult`: Contains final combat outcome
- `CombatDetector`: Determines when combat should occur

### Combat Flow
1. Combat detection triggers `SpaceCombat` creation
2. `start_combat()` creates first `CombatRound`
3. Each round follows the step sequence (announce retreats → roll dice → assign hits → retreat)
4. `should_continue()` checks if combat should continue
5. `end_combat()` determines final result

### Test Coverage Summary
- **Total Test Classes**: 4 (Detection, Basic Mechanics, Resolution, Advanced Mechanics)
- **Total Test Methods**: 20+
- **Rules 78.7-78.10 Coverage**: 7 dedicated test cases
- **Coverage Status**: All core space combat rules implemented and tested

## Recent Updates
- Added comprehensive test coverage for rules 78.7-78.10
- Implemented retreat execution mechanics
- Added proper combat continuation logic after retreats
- Implemented winner/loser/draw determination
- All tests passing as of latest implementation
