# Rule 49: MOVEMENT

## Category Overview
**Rule Type**: Core Game Mechanics  
**Complexity**: High  
**Implementation Priority**: Critical  
**Dependencies**: Units, Systems, Tactical Actions, Technologies  

## Raw LRR Text
From `lrr.txt` sections 58.3-58.7, 89.2:

**58.3** A unit can move out of a system that contains one or more of that player's command tokens only by using the secondary ability of the "Leadership" strategy card.

**58.4** A unit cannot move through a system that contains ships that belong to another player unless it has the "Sustain Damage" ability.

**58.5** When a ship moves, it may pick up and transport fighters and ground forces in the space area of the system it is leaving, the space area of the system it is entering, and each space area it moves through.

**58.6** A ship cannot pick up units that belong to other players.

**58.7** If a ship has capacity, it can transport fighters and/or ground forces, but the combined number cannot exceed the ship's capacity value.

**89.2** During the "Movement" step of a tactical action, the active player may move any number of their ships that do not have a command token in their system into the active system.

## Sub-Rules Analysis

### 58.3 - Command Token Movement Restriction
- **Status**: ✅ Implemented
- **Location**: Movement validation logic
- **Test Coverage**: Limited - needs specific tests for Leadership secondary ability
- **Implementation Notes**: Basic restriction implemented, Leadership exception needs verification

### 58.4 - Movement Through Enemy Systems
- **Status**: ⚠️ Partially Implemented
- **Location**: Movement validation
- **Test Coverage**: None found
- **Implementation Notes**: Sustain Damage bypass not explicitly tested

### 58.5 - Transport During Movement
- **Status**: ✅ Well Implemented
- **Location**: `TransportOperation`, `TransportValidator`, `TransportExecutor`
- **Test Coverage**: Extensive - multiple transport scenarios tested
- **Implementation Notes**: Comprehensive transport mechanics with capacity validation

### 58.6 - Cannot Transport Enemy Units
- **Status**: ❓ Unknown
- **Location**: Transport validation
- **Test Coverage**: None found
- **Implementation Notes**: Needs explicit validation

### 58.7 - Capacity Limits
- **Status**: ✅ Well Implemented
- **Location**: Transport validation
- **Test Coverage**: Extensive - capacity validation thoroughly tested
- **Implementation Notes**: Multiple test cases for capacity limits

### 89.2 - Tactical Action Movement
- **Status**: ✅ Well Implemented
- **Location**: `TacticalAction`, `MovementPlan`, `MovementValidator`
- **Test Coverage**: Extensive - comprehensive tactical action movement tests
- **Implementation Notes**: Full implementation with joint validation

## Related Topics
- **Rule 42**: GROUND COMBAT (ground force movement)
- **Rule 67**: PRODUCING UNITS (unit placement)
- **Rule 68**: PRODUCTION (capacity mechanics)
- **Rule 78**: SPACE COMBAT (combat after movement)
- **Rule 16**: CAPACITY (transport mechanics)
- **Rule 86**: TACTICAL ACTION (movement step)

## Dependencies
- **Units**: Movement values, capacity, sustain damage ability
- **Systems**: Adjacency, command tokens, space areas
- **Technologies**: Gravity Drive (+1 movement)
- **Strategy Cards**: Leadership (movement from commanded systems)
- **Command Tokens**: Movement restrictions

## Test References
### Comprehensive Test Coverage Found:
- `test_movement.py`: Core movement validation and execution
- `test_tactical_action.py`: Tactical action movement integration
- `test_movement_command.py`: Command pattern implementation
- `test_integration.py`: Movement system integration
- `test_technology.py`: Gravity Drive technology effects
- `test_event_integration.py`: Movement event publishing
- `test_performance_benchmarks.py`: Movement performance testing

### Key Test Scenarios:
1. **Basic Movement Validation**: Adjacent system movement
2. **Technology Integration**: Gravity Drive effects
3. **Transport Mechanics**: Capacity validation, ground force transport
4. **Tactical Action Integration**: Joint movement planning
5. **Command System**: Movement command execution/undo
6. **Performance**: Movement validation benchmarks

## Implementation Files
### Core Implementation:
- `src/ti4/core/movement.py`: `MovementOperation`, `MovementValidator`, `MovementExecutor`
- `src/ti4/core/movement.py`: `TransportOperation`, `TransportValidator`, `TransportExecutor`
- `src/ti4/actions/tactical_action.py`: `MovementPlan`, `MovementValidator`
- `src/ti4/rules/movement_rules.py`: `MovementRule`, `MovementRuleEngine`
- `src/ti4/commands/movement.py`: `MovementCommand`

### Supporting Files:
- `src/ti4/constants.py`: Technology constants (Gravity Drive)
- Unit stats for movement values
- Galaxy adjacency system

## Notable Implementation Details

### Strengths:
1. **Comprehensive Architecture**: Well-structured movement system with validators, executors, and commands
2. **Technology Integration**: Gravity Drive properly integrated with movement validation
3. **Transport Mechanics**: Sophisticated transport system with capacity validation
4. **Joint Validation**: Movement plans validated as complete operations
5. **Event System**: Movement events properly published
6. **Performance Optimized**: Benchmarked movement validation

### Areas Needing Attention:
1. **Enemy System Movement**: Sustain Damage bypass not explicitly tested
2. **Leadership Exception**: Command token movement restriction exception needs verification
3. **Enemy Unit Transport**: Validation for preventing transport of enemy units
4. **Wormhole Movement**: Special movement rules not covered
5. **Fleet Supply**: Integration with fleet supply limits

### Architecture Quality:
- **Excellent**: Separation of concerns with validators, executors, and commands
- **Good**: Technology effects properly integrated
- **Good**: Comprehensive test coverage for core mechanics
- **Needs Work**: Some edge cases and special rules need attention

## Action Items

### High Priority:
1. **Add Enemy System Movement Tests**: Test movement through systems with enemy ships and Sustain Damage bypass
2. **Verify Leadership Exception**: Test movement from commanded systems using Leadership secondary
3. **Add Enemy Unit Transport Validation**: Prevent transport of units belonging to other players

### Medium Priority:
4. **Wormhole Movement Rules**: Implement special movement through wormholes
5. **Fleet Supply Integration**: Ensure movement respects fleet supply limits
6. **Movement Range Display**: UI helpers for showing valid movement ranges

### Low Priority:
7. **Movement Animation**: Visual feedback for movement operations
8. **Movement History**: Track movement history for game replay
9. **Advanced Movement Patterns**: Support for complex multi-step movements

## Priority Assessment
**Overall Priority**: Critical - Movement is fundamental to TI4 gameplay

**Implementation Status**: Well Implemented (85%)
- Core movement mechanics: ✅ Complete
- Transport system: ✅ Complete  
- Technology integration: ✅ Complete
- Tactical action integration: ✅ Complete
- Edge cases and special rules: ⚠️ Partial

**Recommended Focus**: 
1. Complete edge case testing (enemy systems, Leadership exception)
2. Add missing validation rules (enemy unit transport)
3. Implement special movement rules (wormholes)

The movement system is one of the most complete implementations in the codebase, with excellent architecture and comprehensive test coverage for core mechanics. The remaining work focuses on edge cases and special rules rather than fundamental functionality.