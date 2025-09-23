# Rule 16: CAPACITY (ATTRIBUTE)

## Category Overview
**Priority**: HIGH - Core game mechanic affecting unit transport, fleet composition, and space area management
**Complexity**: MEDIUM - Involves multiple validation layers and transport mechanics
**Dependencies**: Movement, Transport, Fleet Management, Combat System

## Sub-Rules Analysis

### 16.0 - Core Definition
**Raw LRR Text**: "Capacity is an attribute of some units that is presented on faction sheets and unit upgrade technology cards."
**Implementation Status**: ✅ IMPLEMENTED
**Details**: Unit capacity attribute is implemented in UnitStats class and accessible via Unit.get_capacity()
**Test Coverage**: ✅ Comprehensive tests in test_unit.py

### 16.1 - Transport Limits
**Raw LRR Text**: "A unit's capacity value indicates the maximum combined number of fighters and ground forces that it can transport."
**Implementation Status**: ✅ IMPLEMENTED
**Details**: Transport validation implemented in TransportValidator class with capacity checking
**Test Coverage**: ✅ Tests in test_movement.py and test_tactical_action.py

### 16.2 - System Space Area Capacity
**Raw LRR Text**: "The combined capacity values of a player's ships in a system determine the number of fighters and ground forces that player can have in that system's space area."
**Implementation Status**: ✅ IMPLEMENTED
**Details**: Fleet capacity calculation implemented in Fleet.get_total_capacity() and validated by FleetCapacityValidator
**Test Coverage**: ✅ Comprehensive tests in test_fleet_management.py

### 16.3 - Excess Unit Removal
**Raw LRR Text**: "If a player has more fighters and ground forces in the space area of a system than the total capacity of that player's ships in that system, that player must remove the excess units."
**Implementation Status**: ✅ IMPLEMENTED
**Details**: Fleet capacity validation prevents invalid fleet compositions
**Test Coverage**: ✅ Tests for capacity validation and excess unit detection

## Implementation Status Summary
**Overall Rule Status**: 🟡 PARTIALLY IMPLEMENTED (6/7 sub-rules complete)
**Completion Percentage**: 86%

### Completed Sub-Rules:
- ✅ 16.0 - Core Definition
- ✅ 16.1 - Transport Limits
- ✅ 16.2 - System Space Area Capacity
- ✅ 16.3 - Excess Unit Removal (validation)
- ✅ 16.3a - Player Choice in Removal
- ✅ 16.3b - Planetary Units Exception

### Remaining Sub-Rules:
- ❌ 16.3c - Combat Exception (capacity doesn't apply during combat)

### 16.3a - Player Choice in Removal
**Raw LRR Text**: "A player can choose which of their excess units to remove."
**Implementation Status**: ✅ IMPLEMENTED
**Details**: FleetCapacityEnforcer.remove_excess_units_with_choice() allows player to specify which units to remove
**Test Coverage**: ✅ Comprehensive tests in test_capacity_excess_removal.py
**Test Cases Demonstrating Implementation**:
- `test_player_choice_remove_excess_fighters`: Player chooses which fighters to remove when capacity exceeded
- `test_player_choice_remove_mixed_excess_units`: Player chooses mix of fighters and ground forces to remove
- `test_invalid_choice_insufficient_units`: Error handling when player doesn't choose enough units
- `test_invalid_choice_non_capacity_units`: Error handling when player tries to remove units that don't count against capacity
- `test_no_removal_when_within_capacity`: No removal occurs when fleet is within capacity limits

### 16.3b - Planetary Units Exception
**Raw LRR Text**: "Ground forces on planets do not count against capacity."
**Implementation Status**: ✅ IMPLEMENTED
**Details**: Fleet capacity validation only considers space area units
**Test Coverage**: ✅ Implicit in existing tests

### 16.3c - Combat Exception
**Raw LRR Text**: "A player's fighters and ground forces do not count against capacity during combat. At the end of combat, any excess units are removed and returned to that player's reinforcements."
**Implementation Status**: ❌ NOT IMPLEMENTED
**Details**: No special capacity handling during combat phases
**Test Coverage**: ❌ No tests for combat capacity exceptions

### 16.4 - Unit Assignment
**Raw LRR Text**: "Fighters and ground forces are not assigned to specific ships, except while they are being transported."
**Implementation Status**: ✅ PARTIALLY IMPLEMENTED
**Details**: Transport operations assign units to specific ships temporarily, but general fleet management doesn't require specific assignments
**Test Coverage**: ✅ Transport assignment tests exist

## Related Topics
- Movement (Rule 95)
- Transport (Rule 95)
- Fleet Management
- Combat System
- Reinforcements

## Dependencies
- Unit Stats System
- Fleet Management System
- Transport System
- Movement Validation
- Combat System (for capacity exceptions)

## Test References
**Existing Tests**:
- `tests/test_unit.py`: Unit capacity attribute tests
- `tests/test_fleet_management.py`: Fleet capacity validation tests
- `tests/test_movement.py`: Transport capacity validation tests
- `tests/test_tactical_action.py`: Movement planning capacity tests
- `tests/test_integration.py`: Fleet capacity integration tests

**Missing Tests**:
- Excess unit removal choice mechanism
- Combat capacity exception handling
- Post-combat excess unit removal

## Implementation Files
**Existing Files**:
- `src/ti4/core/unit.py`: Unit capacity methods
- `src/ti4/core/fleet.py`: Fleet capacity calculation and validation
- `src/ti4/core/movement.py`: Transport capacity validation
- `src/ti4/actions/tactical_action.py`: Movement planning capacity validation

**Missing Files**:
- Excess unit removal system
- Combat capacity exception handler
- Post-combat cleanup system

## Action Items

1. **Implement Excess Unit Removal Choice System**
   - Create mechanism for players to choose which excess units to remove
   - Add UI/interface for excess unit selection
   - Integrate with fleet validation system

2. **Add Combat Capacity Exception Handling**
   - Implement capacity suspension during combat phases
   - Create post-combat capacity validation
   - Add excess unit removal after combat

3. **Enhance Transport Assignment Tracking**
   - Improve temporary unit-to-ship assignment during transport
   - Add validation for transport assignment consistency
   - Create transport assignment visualization

4. **Create Comprehensive Capacity Integration Tests**
   - Test capacity interactions with combat system
   - Test excess unit removal scenarios
   - Test capacity with technology upgrades

5. **Add Capacity Violation Detection and Resolution**
   - Implement real-time capacity violation detection
   - Create automatic excess unit identification
   - Add capacity violation resolution workflows

6. **Enhance Fleet Composition Validation**
   - Add pre-movement capacity validation
   - Implement capacity-aware fleet building
   - Create capacity optimization suggestions

7. **Implement Technology-Based Capacity Modifications**
   - Add support for capacity-modifying technologies
   - Implement dynamic capacity calculation
   - Test capacity changes from upgrades

8. **Create Capacity Management UI Components**
   - Add capacity indicators to fleet displays
   - Implement capacity usage visualization
   - Create capacity planning tools

9. **Add Advanced Transport Validation**
   - Implement multi-system transport validation
   - Add capacity-aware movement planning
   - Create transport optimization algorithms

10. **Enhance Documentation and Examples**
    - Create capacity rule examples and edge cases
    - Add capacity management best practices
    - Document capacity interaction with other systems
