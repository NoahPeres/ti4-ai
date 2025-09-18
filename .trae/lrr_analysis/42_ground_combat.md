# LRR Rule 42: GROUND COMBAT

## Rule Category Overview
During the "Ground Combat" step of an invasion, if the active player has ground forces on a planet that contains another player's ground forces, those players resolve a ground combat on that planet.

## Sub-Rules Analysis

### 42.1 Step 1 - Roll Dice
- **Implementation Status**: [ ] Not Implemented / [ ] Partial / [ ] Complete
- **Test Coverage**: [ ] None / [ ] Basic / [ ] Comprehensive
- **Priority**: High/Medium/Low
- **Notes**: Each player rolls one die for each ground force they have on the planet; this is a combat roll. If a unit's combat roll produces a result that is equal to or greater than that unit's combat value, that roll produces a hit. If a unit's combat value contains two or more burst icons, the player rolls one die for each burst icon instead.

### 42.2 Step 2 - Assign Hits
- **Implementation Status**: [ ] Not Implemented / [ ] Partial / [ ] Complete
- **Test Coverage**: [ ] None / [ ] Basic / [ ] Comprehensive
- **Priority**: High/Medium/Low
- **Notes**: Each player in the combat must choose one of their own ground forces on the planet to be destroyed for each hit result their opponent produced. When a unit is destroyed, the player who controls that unit removes it from the board and places it in their reinforcements.

### 42.3 Combat Rounds
- **Implementation Status**: [ ] Not Implemented / [ ] Partial / [ ] Complete
- **Test Coverage**: [ ] None / [ ] Basic / [ ] Comprehensive
- **Priority**: High/Medium/Low
- **Notes**: After assigning hits, if both players still have ground forces on the planet, players resolve a new combat round starting with the "Roll Dice" step.

### 42.4 Combat End
- **Implementation Status**: [ ] Not Implemented / [ ] Partial / [ ] Complete
- **Test Coverage**: [ ] None / [ ] Basic / [ ] Comprehensive
- **Priority**: High/Medium/Low
- **Notes**: Ground combat ends when only one player (or neither player) has ground forces on the planet. During the first round of a combat, "start of combat" and "start of combat round" effects occur during the same timing window. During the last round of a combat, "end of combat" and "end of combat round" effects occur during the same timing window. After a combat ends, the player with one or more ground forces remaining on the planet is the winner of the combat; the other player is the loser of the combat. If neither player has a ground force remaining, there is no winner; the combat ends in a draw.

## Overall Implementation Status
- **Current State**: Not Started/In Progress/Complete
- **Estimated Effort**: Small/Medium/Large
- **Dependencies**: 
- **Blockers**: 

## Notes
- 

## Related Rules
- Rule 46: INVASION
- Rule 63: PLANETS

## Action Items
- [ ] Analyze current implementation
- [ ] Identify gaps
- [ ] Create implementation plan
- [ ] Write tests
- [ ] Implement missing functionality
