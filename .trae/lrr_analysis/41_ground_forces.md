# Rule 41: GROUND FORCES

## Category Overview
**Rule Type:** Unit Mechanics  
**Complexity:** Medium  
**Frequency:** High (used in transport, invasion, control)  
**Dependencies:** Transport, Capacity, Invasion, Planets, Units

## Raw LRR Text
```
43 GROUND FORCES
A ground force is a type of unit. All infantry and mech units in the game are ground forces. Some races have unique infantry units.

43.1 Ground forces are always on planets, in a space area with ships that have capacity values, or being transported by those ships.

43.2 Ground forces being transported by a ship are placed in a system's space area along with the ship that is transporting them.

43.3 There is no limit to the number of ground forces a player can have on a planet.
```

## Sub-Rules Analysis

### 43.1 - Ground Force Locations (WELL IMPLEMENTED)
- **Implementation Status:** ✅ COMPLETE
- **Code Location:** `System.place_unit_on_planet()`, `System.place_unit_in_space()`, transport mechanics
- **Test Coverage:** ✅ Comprehensive (`test_movement.py`, `test_tactical_action.py`)
- **Details:** Ground forces can be placed on planets, in space (with capacity), and transported properly

### 43.2 - Transport Mechanics (WELL IMPLEMENTED)
- **Implementation Status:** ✅ COMPLETE  
- **Code Location:** `TransportOperation`, `TransportExecutor`, `MovementCommand`
- **Test Coverage:** ✅ Comprehensive (`test_movement.py`)
- **Details:** Transport system properly handles ground forces in space area with ships

### 43.3 - No Planet Limit (WELL IMPLEMENTED)
- **Implementation Status:** ✅ COMPLETE
- **Code Location:** `Planet.units` list with no artificial limits
- **Test Coverage:** ✅ Implicit (no limit enforcement tests needed)
- **Details:** Planets can hold unlimited ground forces as per rules

## Related Topics
- **Rule 95: TRANSPORT** - How ground forces are transported by ships
- **Rule 16: CAPACITY** - Ship capacity limits for ground forces in space
- **Rule 49: INVASION** - Ground forces participate in invasions
- **Rule 42: GROUND COMBAT** - Ground forces engage in combat
- **Rule 55: MECHS** - Mechs are a type of ground force with special abilities

## Dependencies
- Unit system (infantry, mech unit types)
- Transport mechanics (capacity validation, movement)
- Planet system (ground force placement and storage)
- Space area management (ground forces in space with ships)
- Combat system (ground forces participate in ground combat)

## Test References

### Existing Tests ✅
- `test_movement.py::test_ground_force_transport_from_planet()` - Transport mechanics
- `test_tactical_action.py::test_commit_ground_forces_step()` - Ground force commitment
- `test_tactical_action.py::test_ground_forces_cannot_move_directly_between_planets()` - Movement restrictions
- `test_system.py` - Ground force placement on planets
- `test_unit.py::test_deploy_ability()` - Mech deploy ability
- `test_fleet_management.py` - Ground force capacity validation

### Missing Tests ❌
- Ground force limit validation (should be unlimited on planets)
- Ground force type validation (infantry vs mech distinction)
- Faction-specific ground force abilities (unique infantry)
- Ground force interaction with planet control
- Ground force removal from reinforcements

## Implementation Files

### Core Implementation ✅
- `src/ti4/core/unit.py` - Ground force unit types (infantry, mech)
- `src/ti4/core/movement.py` - `TransportOperation`, ground force movement
- `src/ti4/core/system.py` - Ground force placement on planets and in space
- `src/ti4/core/planet.py` - Planet ground force storage
- `src/ti4/actions/tactical_action.py` - `CommitGroundForcesPlan`

### Well Implemented Features ✅
- `Unit` class with proper ground force types
- Transport system with capacity validation
- Planet placement and space area management
- Movement validation for ground forces
- Deploy ability for mechs

## Notable Implementation Details

### Well Implemented ✅
1. **Unit Types** - Infantry and mech properly implemented as ground force types
2. **Transport System** - Complete transport mechanics with capacity validation
3. **Placement System** - Ground forces can be placed on planets and in space areas
4. **Movement Validation** - Proper validation that ground forces can't move directly between planets
5. **Capacity Integration** - Ground forces count against ship capacity in space areas
6. **Deploy Ability** - Mechs have deploy ability properly implemented

### Implementation Gaps ❌
1. **Faction-Specific Infantry** - No system for unique infantry units per faction
2. **Ground Force Limits** - No explicit validation that planets have unlimited capacity
3. **Control Integration** - Limited integration between ground forces and planet control
4. **Reinforcement Management** - Basic reinforcement system but could be more robust
5. **Ground Force Abilities** - Limited special abilities beyond basic mech deploy

## Action Items

1. **MEDIUM PRIORITY** - Implement faction-specific infantry variants (Sol Spec Ops, etc.)
2. **MEDIUM PRIORITY** - Add explicit tests for unlimited planet capacity
3. **MEDIUM PRIORITY** - Enhance ground force integration with planet control mechanics
4. **LOW PRIORITY** - Implement additional ground force special abilities
5. **LOW PRIORITY** - Add ground force production tracking and limits
6. **LOW PRIORITY** - Create ground force UI components for better visualization
7. **LOW PRIORITY** - Add ground force statistics and analytics
8. **LOW PRIORITY** - Implement ground force upgrade mechanics
9. **LOW PRIORITY** - Add ground force formation and grouping features
10. **LOW PRIORITY** - Create ground force AI decision-making enhancements

## Priority Assessment
**PRIORITY: MEDIUM-HIGH**

Ground forces are fundamental units that participate in many core game mechanics including transport, invasion, and planet control. The current implementation is quite solid with good transport mechanics, proper placement systems, and basic unit functionality. 

The main gaps are in faction-specific variants and some edge case validations, but the core functionality is well-implemented and tested. This represents a strong foundation that supports the primary use cases effectively.

The system successfully handles the key requirements: ground forces can be on planets or in space (with capacity), they can be transported by ships, and there are no artificial limits on planet capacity. The integration with the transport and tactical action systems is particularly well done.