# Rule 57: SPACE COMBAT

## Category Overview
**Rule Type**: Combat Mechanics & Resolution  
**Complexity**: High  
**Implementation Priority**: High  
**Dependencies**: Unit System, Combat Resolution, Tactical Actions  

## Raw LRR Text
From `lrr.txt` Rule 78: SPACE COMBAT:

**78. SPACE COMBAT**  
After resolving the "Space Cannon Offense" step of a tactical action, if two players have ships in the active system, those players must resolve a space combat.

**78.1** If the active player is the only player with ships in the system, they skip the "Space Combat" step of the tactical action and proceeds to the "Invasion" step.

**78.2** If an ability occurs "before combat," it occurs immediately before the "Anti-Fighter Barrage" step.
a. During the first round of a combat, "start of combat" and "start of combat round" effects occur during the same timing window.
b. During the last round of a combat, "end of combat" and "end of combat round" effects occur during the same timing window.

**To resolve a space combat, players perform the following steps:**

**78.3 STEP 1-ANTI-FIGHTER BARRAGE**: A unit with the "Anti-Fighter Barrage" ability may be able to destroy an opponent's fighters at the onset of a space battle. During the "Anti-Fighter Barrage" step of the first round of space combat, players perform the following steps:
- **10.1 STEP 1**: Each player rolls dice for each of their units in the combat that has the "Anti-Fighter Barrage" ability; this is called an anti-fighter barrage roll. A hit is produced for each die roll that is equal to or greater than the unit's anti-fighter barrage value.
- **10.2 STEP 2**: Each player must choose and destroy one of their fighters in the active system for each hit their opponent's anti-fighter barrage roll produced.

**78.4 STEP 2-ANNOUNCE RETREATS**: Each player may announce a retreat, beginning with the defender.
a. A retreat will not occur immediately; the units retreat during the "Retreat" step.
b. If the defender announces a retreat, the attacker cannot announce a retreat during that combat round.
c. A player cannot announce a retreat if there is not at least one eligible system to retreat to.

**78.5 STEP 3-ROLL DICE**: Each player rolls one die for each ship they have in the active system; this is called a combat roll. If a unit's combat roll produces a result that is equal to or greater than that unit's combat value, that result produces a hit.
a. If a unit's combat value contains two or more burst icons, the player rolls one die for each burst icon instead.
b. If a player has ships that have different combat values in the active system, that player rolls these dice separately.

**78.6 STEP 4-ASSIGN HITS**: Each player in the combat must choose one of their own ships in the active system to be destroyed for each hit result their opponent produced.
a. When a unit is destroyed, the player who controls that unit removes it from the board and places it in their reinforcements.
b. A player can choose to not assign a hit to a unit if that unit has an ability that allows it to cancel hits, such as "Sustain Damage."

**78.7 STEP 5-RETREAT**: Players who announced a retreat remove all of their ships in the active system and place them in an adjacent system that does not contain ships that belong to another player. The retreat cannot be to the system the active player's ships moved from unless that system contains the retreating player's units.

**78.8 STEP 6-CONTINUE COMBAT**: After assigning hits, if both players still have ships in the active system, players resolve a new combat round starting with the "Announce Retreats" step.

**78.9** Space combat ends when only one player (or neither player) has ships in the active system.

**Related Combat Abilities**:
- **Anti-Fighter Barrage (Rule 10)**: Destroys fighters before main combat
- **Sustain Damage (Rule 87)**: Allows units to absorb hits without destruction
- **Space Cannon Offense (Rule 77.2-77.5)**: Pre-combat bombardment

**Related Topics**: Active System, Attacker, Defender, Destroyed, Sustain Damage, Movement, Tactical Action

## Sub-Rules Analysis

### Combat Initiation (78.1)
- **Status**: ⚠️ Partially Implemented
- **Location**: No explicit space combat initiation system found
- **Test Coverage**: No combat initiation tests found
- **Implementation Notes**: No system to detect when space combat should occur

### Anti-Fighter Barrage Step (78.3, 10.1-10.2)
- **Status**: ✅ Implemented
- **Location**: `src/ti4/core/combat.py` - `perform_anti_fighter_barrage()`
- **Test Coverage**: `test_combat.py` - Anti-fighter barrage timing and targeting tests
- **Implementation Notes**: Well-implemented with proper fighter targeting

### Retreat Announcement (78.4)
- **Status**: ❌ Not Implemented
- **Location**: No retreat system found
- **Test Coverage**: No retreat tests found
- **Implementation Notes**: No retreat announcement or execution system

### Combat Dice Rolling (78.5)
- **Status**: ✅ Implemented
- **Location**: `src/ti4/core/combat.py` - Combat resolution system
- **Test Coverage**: `test_combat.py` - Combat dice and hit calculation tests
- **Implementation Notes**: Solid implementation with proper combat value handling

### Hit Assignment (78.6)
- **Status**: ⚠️ Partially Implemented
- **Location**: `src/ti4/core/combat.py` - Hit assignment with sustain damage
- **Test Coverage**: `test_combat.py` - Sustain damage resolution tests
- **Implementation Notes**: Sustain damage implemented but no general hit assignment

### Retreat Execution (78.7)
- **Status**: ❌ Not Implemented
- **Location**: No retreat execution system found
- **Test Coverage**: No retreat execution tests found
- **Implementation Notes**: No system to move retreating units

### Combat Round Continuation (78.8-78.9)
- **Status**: ❌ Not Implemented
- **Location**: No multi-round combat system found
- **Test Coverage**: No multi-round combat tests found
- **Implementation Notes**: No system for continuing combat rounds

## Related Topics
- **Rule 10**: ANTI-FIGHTER BARRAGE (pre-combat fighter destruction)
- **Rule 13**: ATTACKER (combat participant identification)
- **Rule 18**: COMBAT (general combat mechanics)
- **Rule 29**: DEFENDER (combat participant identification)
- **Rule 77**: SPACE CANNON (pre-combat bombardment)
- **Rule 87**: SUSTAIN DAMAGE (hit mitigation)

## Dependencies
- **Unit System**: For combat participants and abilities (✅ Implemented)
- **Tactical Action System**: For combat initiation (⚠️ Basic Implementation)
- **Active System Tracking**: For combat location (✅ Implemented)
- **Dice Rolling System**: For combat resolution (✅ Implemented)
- **Hit Assignment System**: For damage resolution (⚠️ Partial Implementation)
- **Retreat System**: For combat withdrawal (❌ Missing)
- **Multi-Round System**: For extended combat (❌ Missing)

## Test References
### Current Test Coverage:
- `test_combat.py`: Combat mechanics and abilities testing
  - Anti-fighter barrage timing and targeting
  - Combat dice values and rolling
  - Sustain damage resolution
  - Space cannon defensive fire
  - Combat modifier application
- `test_unit.py`: Unit combat abilities testing
  - Anti-fighter barrage ability identification
  - Combat ability matrix validation
  - Unit-specific ability testing

### Test Scenarios Covered:
1. **Anti-Fighter Barrage**: Proper timing and fighter targeting
2. **Combat Dice Rolling**: Correct dice counts and hit calculation
3. **Sustain Damage**: Hit mitigation and unit preservation
4. **Space Cannon Defense**: Defensive fire capabilities
5. **Combat Modifiers**: Dice roll modification effects
6. **Unit Abilities**: Combat-related ability identification

### Missing Test Scenarios:
1. **Combat Initiation**: When space combat should trigger
2. **Retreat Mechanics**: Retreat announcement and execution
3. **Multi-Round Combat**: Extended combat resolution
4. **Hit Assignment**: General hit assignment without sustain damage
5. **Combat End Conditions**: When combat should end
6. **Combat Integration**: Full tactical action integration
7. **Combat Timing**: Before/after combat effects
8. **Combat Participants**: Attacker/defender identification

## Implementation Files
### Core Implementation:
- `src/ti4/core/combat.py`: Combat resolution system with abilities
- `src/ti4/core/unit.py`: Unit combat abilities and stats
- `src/ti4/core/unit_stats.py`: Combat values and ability definitions

### Supporting Files:
- `tests/test_combat.py`: Comprehensive combat testing
- `tests/test_unit.py`: Unit ability testing
- `UNIT_ABILITIES_IMPLEMENTATION.md`: Combat ability documentation

### Missing Implementation:
- Space combat orchestration system
- Retreat announcement and execution
- Multi-round combat management
- Combat initiation detection
- Hit assignment without sustain damage
- Combat end condition checking
- Combat timing effects system

## Notable Implementation Details

### Strengths:
1. **Unit Combat Abilities**: Excellent implementation of anti-fighter barrage, sustain damage, space cannon
2. **Combat Dice System**: Solid dice rolling and hit calculation
3. **Ability Integration**: Well-integrated unit abilities in combat
4. **Test Coverage**: Comprehensive testing of implemented features
5. **Combat Values**: Proper combat value handling and burst icons

### Areas Needing Attention:
1. **Combat Orchestration**: No overall space combat management system
2. **Retreat System**: Missing retreat announcement and execution
3. **Multi-Round Combat**: No system for extended combat
4. **Combat Integration**: Not integrated with tactical actions
5. **Hit Assignment**: Limited to sustain damage scenarios
6. **Combat Timing**: No before/after combat effect system

### Architecture Quality:
- **Excellent**: Unit abilities and combat dice mechanics
- **Good**: Individual combat components and testing
- **Needs Work**: Overall combat orchestration and flow
- **Missing**: Retreat system and multi-round combat

## Action Items

### High Priority:
1. **Implement Space Combat Orchestration**: Complete space combat management system
2. **Add Combat Initiation Detection**: Trigger space combat during tactical actions
3. **Create Retreat System**: Retreat announcement and execution mechanics
4. **Implement Multi-Round Combat**: Extended combat resolution system

### Medium Priority:
5. **Add Hit Assignment System**: General hit assignment beyond sustain damage
6. **Create Combat End Detection**: Proper combat termination conditions
7. **Integrate with Tactical Actions**: Full tactical action combat integration
8. **Add Combat Timing Effects**: Before/after combat effect system

### Low Priority:
9. **Add Combat Analytics**: Combat statistics and analysis
10. **Create Combat Visualization**: Visual combat representation
11. **Add Combat History**: Track combat outcomes and statistics
12. **Implement Advanced Combat Rules**: Special combat scenarios and edge cases

## Priority Assessment
**Overall Priority**: High - Space combat is a core game mechanic

**Implementation Status**: Strong Foundation (60%)
- Unit combat abilities: ✅ Complete
- Combat dice system: ✅ Complete
- Anti-fighter barrage: ✅ Complete
- Sustain damage: ✅ Complete
- Space cannon: ✅ Complete
- Combat orchestration: ❌ Missing
- Retreat system: ❌ Missing
- Multi-round combat: ❌ Missing
- Combat integration: ❌ Missing

**Recommended Focus**: 
1. Build space combat orchestration system that coordinates all combat steps
2. Implement retreat announcement and execution mechanics
3. Add multi-round combat support for extended battles
4. Integrate space combat with tactical action system

The current implementation has excellent individual combat components (abilities, dice, hit resolution) but lacks the overall orchestration system that ties everything together into a complete space combat experience. The unit abilities are particularly well-implemented, providing a solid foundation for the complete system. The main gap is the lack of a comprehensive combat manager that handles the full combat sequence, retreat mechanics, and multi-round resolution. This is a high-priority system since space combat is central to TI4 gameplay and the foundation is already strong.