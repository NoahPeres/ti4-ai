# LRR Rule Analysis: Rule 45 - INVASION

## Category Overview
**Rule Type**: Combat System & Tactical Action Step  
**Complexity**: High  
**Scope**: Ground combat and planetary invasion mechanics  

## Raw LRR Text
```
49 INVASION
During the "Invasion" step of a tactical action, the active player can commit ground forces to land on planets and can resolve ground combat against other players' units. To resolve the invasion step, players perform the following steps:

49.1 STEP 1-BOMBARDMENT: The active player may use the "Bombardment" abilities of any of their units in the active system.
49.2 STEP 2-COMMIT GROUND FORCES: The active player may commit any number of their ground forces from the space area of the active system to land on any of the planets in that system.
a The active player may choose to commit ground forces to a planet that does not contain any of their opponent's ground forces.
b The active player cannot commit ground forces to a planet that contains one of their command tokens.
c When a player commits ground forces to a planet, those units are placed on that planet.
49.3 STEP 3-SPACE CANNON DEFENSE: If the active player commits any ground forces to a planet that contains units that have the "Space Cannon" ability, those "Space Cannon" abilities can be used against the committed ground forces.
a If the active player committed ground forces to more than one planet that contained units with a "Space Cannon" ability, the active player chooses the order in which those "Space Cannon" abilities are resolved.
49.4 STEP 4-GROUND COMBAT: If the active player has ground forces on a planet in the active system that contains another player's ground forces, those players resolve a ground combat on that planet.
a If players must resolve a combat on more than one planet, the active player chooses the order in which those combats are resolved.
49.5 STEP 5-ESTABLISH CONTROL: The active player gains control of each planet they committed ground forces to if that planet still contains at least one of their ground forces.
a When a player gains control of a planet, any structures on the planet that belong to other players are immediately destroyed.
b When a player gains control of a planet, they gain the planet card that matches that planet and exhaust that card.
c A player cannot gain control of a planet they already control.
d If there was a combat, and all units belonging to both players were destroyed, the player who was the defender retains control of the planet and places one of their control tokens on the planet.
```

## Sub-Rules Analysis

### 49.0 Invasion Overview
**Rule**: "During the 'Invasion' step of a tactical action, the active player can commit ground forces to land on planets and can resolve ground combat against other players' units."

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Basic ground force movement exists in `movement.py`
- **Tests**: Ground force transport tests in `test_movement.py`
- **Assessment**: Transport mechanics exist but full invasion sequence missing
- **Priority**: HIGH
- **Dependencies**: Requires tactical action system and combat resolution

### 49.1 Step 1 - Bombardment
**Rule**: "The active player may use the 'Bombardment' abilities of any of their units in the active system."

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Bombardment ability detection in `Unit` class
- **Tests**: Bombardment ability tests in `test_unit.py`
- **Assessment**: Unit abilities exist but bombardment resolution missing
- **Priority**: HIGH
- **Dependencies**: Requires combat system integration

### 49.2 Step 2 - Commit Ground Forces
**Rule**: "The active player may commit any number of their ground forces from the space area of the active system to land on any of the planets in that system."
**Sub-rules**: Landing restrictions and placement mechanics

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Ground force transport in `movement.py`
- **Tests**: Ground force commitment tests in `test_tactical_action.py`
- **Assessment**: Basic transport exists but commitment validation missing
- **Priority**: HIGH
- **Dependencies**: Requires command token validation and planet control checks

### 49.3 Step 3 - Space Cannon Defense
**Rule**: "If the active player commits any ground forces to a planet that contains units that have the 'Space Cannon' ability, those 'Space Cannon' abilities can be used against the committed ground forces."

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Space cannon ability in `combat.py` and `Unit` class
- **Tests**: Space cannon defensive fire tests in `test_combat.py`
- **Assessment**: Space cannon mechanics exist but invasion integration missing
- **Priority**: HIGH
- **Dependencies**: Requires invasion step integration

### 49.4 Step 4 - Ground Combat
**Rule**: "If the active player has ground forces on a planet in the active system that contains another player's ground forces, those players resolve a ground combat on that planet."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No ground combat resolution system found
- **Tests**: No ground combat tests found
- **Assessment**: Core ground combat mechanics missing
- **Priority**: HIGH
- **Dependencies**: Requires combat resolution system for ground forces

### 49.5 Step 5 - Establish Control
**Rule**: "The active player gains control of each planet they committed ground forces to if that planet still contains at least one of their ground forces."
**Sub-rules**: Planet control mechanics, structure destruction, planet card acquisition

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Planet control tracking in `Planet` class
- **Tests**: Planet control tests in `test_planet.py`
- **Assessment**: Basic control tracking exists but invasion control mechanics missing
- **Priority**: HIGH
- **Dependencies**: Requires planet card system and structure management

## Related Topics
- **Ground Combat (Rule 42)**: Combat resolution mechanics
- **Ground Forces (Rule 43)**: Unit types and transport
- **Bombardment (Unit Ability)**: Pre-combat bombardment
- **Space Cannon (Unit Ability)**: Defensive fire mechanics
- **Tactical Action (Rule 89)**: Parent action containing invasion
- **Control (Rule 25)**: Planet control mechanics
- **Planets (Rule 64)**: Planet cards and control tokens

## Dependencies
- **Combat System**: Ground combat resolution mechanics
- **Tactical Action System**: Invasion as step 4 of tactical action
- **Unit Abilities**: Bombardment and space cannon integration
- **Planet Control**: Control establishment and validation
- **Command Token System**: Landing restriction validation

## Test References
**Current Test Coverage**: ⚠️ PARTIAL
- **Unit Abilities**: Bombardment and space cannon abilities tested
- **Ground Force Transport**: Basic transport mechanics tested
- **Ground Force Commitment**: Some commitment tests in tactical action
- **Space Cannon Defense**: Defensive fire mechanics tested

**Missing Test Areas**:
- Complete invasion step sequence
- Ground combat resolution
- Bombardment during invasion
- Planet control establishment
- Structure destruction on control change
- Multiple planet invasion scenarios

## Implementation Files
**Current Implementation**: ⚠️ PARTIAL

**Relevant Files**:
- `src/ti4/core/combat.py`: Space cannon and sustain damage mechanics
- `src/ti4/core/movement.py`: Ground force transport operations
- `src/ti4/core/unit.py`: Unit abilities (bombardment, space cannon)
- `tests/test_combat.py`: Space cannon defensive fire tests
- `tests/test_unit.py`: Bombardment ability tests
- `tests/test_tactical_action.py`: Ground force commitment tests

**Missing Components**:
- Complete invasion step sequence
- Ground combat resolution system
- Bombardment resolution during invasion
- Planet control establishment mechanics
- Structure destruction on control change
- Integration with tactical action system

## Notable Implementation Details

### Current Unit Abilities
- Bombardment ability detection implemented for dreadnoughts and war suns
- Space cannon ability implemented with defensive fire mechanics
- Sustain damage mechanics work for ground combat units (mechs)
- Unit ability testing comprehensive

### Current Transport System
- Ground force transport from space area to planets exists
- Basic ground force commitment mechanics in tactical actions
- Transport capacity validation implemented

### Missing Invasion Mechanics
- No complete invasion step sequence
- No ground combat resolution system
- No bombardment resolution during invasion
- No planet control establishment from invasion
- No structure destruction mechanics

### Test Coverage Gaps
- No complete invasion sequence tests
- No ground combat resolution tests
- No bombardment integration tests
- No planet control establishment tests

## Action Items

### High Priority
1. **Implement Ground Combat Resolution**
   - Create ground combat system following Rule 42 mechanics
   - Add dice rolling and hit assignment for ground forces
   - Implement combat rounds until one side eliminated

2. **Implement Complete Invasion Sequence**
   - Create invasion step controller with 5 sub-steps
   - Integrate bombardment resolution in step 1
   - Add ground force commitment validation in step 2
   - Integrate space cannon defense in step 3

3. **Implement Planet Control Establishment**
   - Add control establishment mechanics in step 5
   - Implement structure destruction on control change
   - Add planet card acquisition and exhaustion

### Medium Priority
4. **Bombardment Integration**
   - Integrate bombardment abilities with invasion step 1
   - Add bombardment target selection and resolution
   - Implement bombardment hit assignment to ground forces

5. **Enhanced Validation**
   - Add command token landing restrictions
   - Validate planet control prerequisites
   - Add multiple planet invasion order selection

### Low Priority
6. **Comprehensive Testing**
   - Add complete invasion sequence tests
   - Test ground combat resolution scenarios
   - Test bombardment and space cannon integration
   - Test planet control establishment scenarios

## Priority Assessment
**Overall Priority**: 🔴 CRITICAL

**Rationale**:
- Invasion is core tactical action step
- Ground combat is fundamental combat mechanic
- Planet control is essential for resource acquisition
- Multiple unit abilities depend on invasion mechanics

**Implementation Effort**: HIGH
- Complex multi-step sequence with validation
- Ground combat system needs full implementation
- Integration with multiple existing systems required
- Extensive testing needed for combat scenarios

**Dependencies**: High complexity integration with tactical actions, combat system, and planet control