# Rule 59: SPACE CANNON Analysis

## Category Overview
**Rule Type**: Unit Ability/Combat  
**Complexity**: High  
**Dependencies**: High (Combat, PDS, Tactical Actions, Movement, Invasion)

## Raw LRR Text

### 77 SPACE CANNON
77.1 A player is not required to be the active player to use their "Space Cannon" ability of their units.

### 77.2 SPACE CANNON OFFENSE
During a tactical action, after the "Move Ships" substep of the "Movement" step, beginning with the active player and proceeding clockwise, each player may use the "Space Cannon" ability of each of their units in the active system by performing the following steps:

77.3 STEP 1-ROLL DICE: The player rolls dice for each of their units in the active system that has the "Space Cannon" ability; this is a space cannon roll. One hit is produced for each result that is equal to or greater than the unit's "Space Cannon" value.

a A unit's "Space Cannon" ability is presented along with a unit's attributes on faction sheets and unit upgrade technology cards.

b "Space Cannon" is displayed as "Space Cannon X (xY)." The X is the minimum value needed for a die to produce a hit, and Y is the number of dice rolled. Not all "Space Cannon" abilities are accompanied by a (Y) value; a space cannon roll for such a unit consists of one die.

c If a player has a PDS unit upgrade technology, they can use the "Space Cannon" ability of their PDS units that are in systems that are adjacent to the active system. The hits are still assigned to units in the active system.

d Game effects that reroll, modify, or otherwise affect combat rolls do not affect space cannon rolls.

77.4 This ability can be used even if no ships were moved during the "Move Ships" step.

77.5 STEP 2-ASSIGN HITS: The active player must choose and destroy one of their ships in the active system for each hit the space cannon roll produced.

a Players other than the active player must target the active player's units.

b If the active player is using the "Space Cannon" ability of their units, they choose a player who has ships in the active system. That player must choose and destroy one of their ships in the active system for each hit the space cannon roll produced.

### 77.6 SPACE CANNON DEFENSE
During the invasion step of a tactical action, after ground forces have been committed to land on planets, players other than the active player can resolve the "Space Cannon" ability of their units on those planets by performing the following steps:

77.7 STEP 1-ROLL DICE: Each player may use the "Space Cannon" ability of each of their units on the invaded planet by rolling a specific number of dice for each of those units; this is called a space cannon roll. A hit is produced for each die roll that is equal to or greater than the unit's "Space Cannon" value.

a If a unit has a "Space Cannon" ability, it is present on its faction sheet and technology cards.

b "Space Cannon" is displayed as "Space Cannon X (xY)." The X is the minimum value needed for a die to produce a hit, and Y is the number of dice rolled. Not all "Space Cannon" abilities are accompanied by a (Y) value; a space cannon roll for such a unit consists of one die.

d Game effects that allow the use of "Space Cannon" abilities against ships in adjacent systems have no effect during Space Cannon Defense.

77.8 STEP 2-ASSIGN HITS: The active player must choose and destroy one of their ground forces on the planet for each hit the space cannon roll produced.

a Hits can only be assigned to units that are on the same planet as the units using the "Space Cannon" ability.

### Related PDS Rules (63.1)
63.1 Each PDS has the "Space Cannon" ability.

## Sub-Rules Analysis

### 77.1 - Non-Active Player Usage ⚠️ PARTIALLY IMPLEMENTED
- **Status**: Basic ability detection exists, but timing/turn order logic unclear
- **Implementation**: `Unit.has_space_cannon()` method exists
- **Test Coverage**: ✅ `test_unit.py::test_space_cannon_ability()`
- **Notes**: Turn order for space cannon resolution not implemented

### 77.2-77.5 - Space Cannon Offense ⚠️ PARTIALLY IMPLEMENTED
- **Status**: Basic mechanics exist, but full tactical action integration missing
- **Implementation**: `CombatResolver.perform_space_cannon()` method exists
- **Test Coverage**: ✅ `test_combat.py::test_space_cannon_defensive_fire()`
- **Notes**: Missing tactical action timing, turn order, hit assignment

### 77.3 - Dice Rolling ✅ IMPLEMENTED
- **Status**: Basic dice rolling implemented
- **Implementation**: Space cannon roll mechanics in combat resolver
- **Test Coverage**: ✅ Tests verify PDS rolls 1 die for space cannon
- **Notes**: Basic functionality works

### 77.3a - Unit Attributes ✅ IMPLEMENTED
- **Status**: Space cannon ability properly defined in unit stats
- **Implementation**: `UnitStats.space_cannon: bool` for PDS
- **Test Coverage**: ✅ Comprehensive unit ability tests
- **Notes**: PDS correctly has space cannon ability

### 77.3b - Space Cannon Display Format ❌ NOT IMPLEMENTED
- **Status**: Not implemented
- **Implementation**: No parsing of "Space Cannon X (xY)" format
- **Test Coverage**: ❌ No tests for multiple dice space cannon
- **Notes**: Currently assumes 1 die per unit

### 77.3c - PDS Adjacent Systems ❌ NOT IMPLEMENTED
- **Status**: Not implemented
- **Implementation**: No adjacent system space cannon logic
- **Test Coverage**: ❌ No tests for PDS upgrade technology effects
- **Notes**: Critical PDS upgrade mechanic missing

### 77.3d - Combat Roll Immunity ❌ NOT IMPLEMENTED
- **Status**: Not implemented
- **Implementation**: No distinction between combat and space cannon rolls
- **Test Coverage**: ❌ No tests for roll modification immunity
- **Notes**: Important for technology interactions

### 77.4 - No Movement Required ❌ NOT IMPLEMENTED
- **Status**: Not implemented
- **Implementation**: No tactical action integration to verify this
- **Test Coverage**: ❌ No tests for space cannon without movement
- **Notes**: Requires tactical action system integration

### 77.5 - Hit Assignment ❌ NOT IMPLEMENTED
- **Status**: Not implemented
- **Implementation**: No hit assignment or unit destruction logic
- **Test Coverage**: ❌ No tests for space cannon hit resolution
- **Notes**: Critical for space cannon effectiveness

### 77.6-77.8 - Space Cannon Defense ❌ NOT IMPLEMENTED
- **Status**: Not implemented
- **Implementation**: No invasion step space cannon logic
- **Test Coverage**: ❌ No tests for space cannon defense
- **Notes**: Completely missing defensive space cannon

### 63.1 - PDS Space Cannon ✅ IMPLEMENTED
- **Status**: Fully implemented
- **Implementation**: PDS units have space_cannon=True in stats
- **Test Coverage**: ✅ Comprehensive PDS ability tests
- **Notes**: Basic PDS space cannon ability works

## Related Topics

### Direct Dependencies
- **PDS (63)**: Primary units with space cannon ability
- **Tactical Actions**: Space cannon timing during movement and invasion
- **Combat System**: Dice rolling and hit resolution
- **Movement**: Space cannon offense triggers after ship movement
- **Invasion**: Space cannon defense during ground force commitment

### Indirect Dependencies
- **Technology**: PDS upgrades affect space cannon range
- **Adjacent Systems**: Required for PDS upgrade effects
- **Turn Order**: Space cannon resolution order
- **Unit Destruction**: Hit assignment and unit removal

## Test References

### Current Test Coverage
- ✅ `test_unit.py::test_space_cannon_ability()` - Tests PDS space cannon detection
- ✅ `test_combat.py::test_space_cannon_defensive_fire()` - Tests basic space cannon mechanics
- ✅ Unit ability matrix tests - Comprehensive ability detection

### Missing Test Scenarios
- ❌ Space cannon offense during tactical actions
- ❌ Space cannon defense during invasion
- ❌ PDS adjacent system space cannon (with upgrade)
- ❌ Multiple dice space cannon units
- ❌ Space cannon hit assignment and unit destruction
- ❌ Space cannon without ship movement
- ❌ Turn order for space cannon resolution
- ❌ Space cannon immunity to combat roll modifiers
- ❌ Space cannon targeting rules

## Implementation Files

### Core Implementation
- `src/ti4/core/unit_stats.py` - PDS space cannon ability (space_cannon=True)
- `src/ti4/core/unit.py` - Space cannon ability detection methods
- `src/ti4/core/combat.py` - Basic space cannon mechanics

### Supporting Systems
- `src/ti4/core/tactical_action.py` - Tactical action integration (needs work)
- `src/ti4/core/invasion.py` - Invasion step space cannon (missing)
- `src/ti4/core/technology.py` - PDS upgrade effects (missing)

### Test Files
- `tests/test_unit.py` - Unit ability tests
- `tests/test_combat.py` - Basic space cannon tests

## Notable Details

### Implementation Strengths
1. **Basic Ability Detection**: PDS correctly identified as having space cannon
2. **Unit Stats Integration**: Space cannon properly defined in unit stats
3. **Basic Mechanics**: Simple space cannon roll functionality exists
4. **Test Foundation**: Good coverage of basic ability detection

### Areas Needing Attention
1. **Tactical Action Integration**: No proper timing during tactical actions
2. **Hit Assignment**: No logic for destroying units from space cannon hits
3. **Space Cannon Defense**: Completely missing invasion step mechanics
4. **PDS Upgrades**: No adjacent system space cannon capability
5. **Multiple Dice**: No support for units with multiple space cannon dice
6. **Turn Order**: No proper resolution order implementation

### Critical Gaps
1. **Space Cannon Defense**: Major defensive mechanic missing
2. **Hit Resolution**: No actual unit destruction from space cannon
3. **Tactical Action Timing**: Not integrated with movement/invasion steps
4. **PDS Upgrade Effects**: Adjacent system capability missing

## Action Items

### High Priority
1. **Implement space cannon defense** - During invasion step
2. **Add hit assignment and unit destruction** - Make space cannon effective
3. **Integrate with tactical action system** - Proper timing and turn order

### Medium Priority
4. **Implement PDS upgrade adjacent system effects** - Technology integration
5. **Add multiple dice space cannon support** - Parse "Space Cannon X (xY)" format
6. **Implement space cannon immunity to combat modifiers** - Separate roll types

### Low Priority
7. **Add comprehensive space cannon tests** - All scenarios and edge cases
8. **Implement space cannon targeting rules** - Player choice mechanics
9. **Add space cannon without movement scenarios** - Complete tactical action coverage

## Priority Assessment

**Overall Priority**: High  
**Implementation Status**: ~30% Complete  
**Risk Level**: High

Space cannon is a fundamental defensive mechanic that affects both ship movement and ground invasions. The current implementation only covers basic ability detection and simple dice rolling. The critical defensive mechanics during invasion and the tactical action integration are completely missing, making this a high-priority implementation gap that affects game balance and strategic depth.