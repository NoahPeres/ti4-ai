# Rule 50: NEIGHBORS

## Category Overview
**Rule Type**: Core Game Mechanics  
**Complexity**: Medium  
**Implementation Priority**: High  
**Dependencies**: Systems, Adjacency, Wormholes, Units, Planets  

## Raw LRR Text
From `lrr.txt` section 60:

**60** Two players are neighbors if they both have a unit or control a planet in the same system. They are also neighbors if they both have a unit or control a planet in systems that are adjacent to each other.

**60.1** Players can resolve transactions with their neighbors.

**60.2** Players are neighbors if the adjacency of systems is granted by a wormhole.

**60.3** Players are neighbors with the Ghosts of Creuss if the Ghosts of Creuss' "Quantum Entanglement" faction ability is causing adjacency from the perspective of the Ghosts of Creuss player.

## Sub-Rules Analysis

### 60 - Basic Neighbor Definition
- **Status**: ⚠️ Partially Implemented
- **Location**: Basic adjacency system exists in `galaxy.py`
- **Test Coverage**: Limited - adjacency testing exists but not neighbor relationships
- **Implementation Notes**: Adjacency mechanics exist but neighbor relationship logic missing

### 60.1 - Transaction Permissions
- **Status**: ❓ Unknown
- **Location**: Transaction system not found
- **Test Coverage**: None found
- **Implementation Notes**: Requires transaction system and neighbor validation

### 60.2 - Wormhole Neighbors
- **Status**: ❌ Not Implemented
- **Location**: No wormhole adjacency system
- **Test Coverage**: None found
- **Implementation Notes**: Wormhole adjacency rules missing entirely

### 60.3 - Ghosts of Creuss Special Case
- **Status**: ❌ Not Implemented
- **Location**: No faction-specific adjacency rules
- **Test Coverage**: None found
- **Implementation Notes**: Faction-specific neighbor rules not implemented

## Related Topics
- **Rule 6**: ADJACENCY (system adjacency mechanics)
- **Rule 101**: WORMHOLES (wormhole adjacency)
- **Rule 44**: HYPERLANES (hyperlane adjacency)
- **Rule 92**: TRANSACTIONS (neighbor-based trading)
- **Rule 17**: COMMAND TOKENS (system control)
- **Rule 69**: PROMISSORY NOTES (neighbor transactions)

## Dependencies
- **Systems**: System placement and identification
- **Adjacency**: Physical and special adjacency rules
- **Units**: Unit presence in systems
- **Planets**: Planet control mechanics
- **Wormholes**: Wormhole adjacency rules
- **Factions**: Faction-specific adjacency abilities

## Test References
### Limited Test Coverage Found:
- `test_hex_coordinate.py`: Basic hex coordinate neighbor calculation
- `test_performance_cache.py`: Adjacency caching functionality
- `test_utils.py`: Adjacent system creation utilities
- `test_movement.py`: Adjacent system movement validation
- `test_integration.py`: Basic adjacency in movement tests

### Missing Test Scenarios:
1. **Player Neighbor Detection**: No tests for determining if players are neighbors
2. **Transaction Validation**: No tests for neighbor-based transaction permissions
3. **Wormhole Neighbors**: No tests for wormhole-based neighbor relationships
4. **Faction-Specific Rules**: No tests for Ghosts of Creuss special adjacency

## Implementation Files
### Core Implementation:
- `src/ti4/core/galaxy.py`: Basic system adjacency (`are_systems_adjacent`)
- `src/ti4/core/hex_coordinate.py`: Hex coordinate distance and neighbor calculation
- `src/ti4/performance/concurrent.py`: Thread-safe adjacency checking
- `src/ti4/performance/cache.py`: Adjacency result caching

### Missing Implementation:
- Player neighbor relationship detection
- Transaction permission validation
- Wormhole adjacency rules
- Faction-specific adjacency abilities

## Notable Implementation Details

### Strengths:
1. **Basic Adjacency System**: Solid foundation with hex coordinate system
2. **Performance Optimization**: Adjacency caching implemented
3. **Thread Safety**: Concurrent adjacency checking supported
4. **Distance Calculation**: Proper hex distance calculation

### Areas Needing Attention:
1. **Player Relationship Logic**: No system to determine player neighbors
2. **Wormhole Adjacency**: Special adjacency rules not implemented
3. **Transaction Integration**: No connection between neighbors and transactions
4. **Faction Abilities**: Special faction adjacency rules missing
5. **Unit/Planet Tracking**: No system to track player presence in systems

### Architecture Quality:
- **Good**: Basic adjacency infrastructure is solid
- **Needs Work**: Higher-level neighbor relationship logic missing
- **Missing**: Special adjacency rules (wormholes, hyperlanes, factions)
- **Missing**: Integration with transaction and diplomacy systems

## Action Items

### High Priority:
1. **Implement Player Neighbor Detection**: Create system to determine if two players are neighbors based on unit/planet presence
2. **Add Wormhole Adjacency Rules**: Implement wormhole-based adjacency for neighbor determination
3. **Create Transaction Validation**: Link neighbor relationships to transaction permissions

### Medium Priority:
4. **Add Faction-Specific Rules**: Implement Ghosts of Creuss "Quantum Entanglement" adjacency
5. **Implement Hyperlane Adjacency**: Add hyperlane-based adjacency rules
6. **Add Comprehensive Testing**: Test all neighbor relationship scenarios

### Low Priority:
7. **Neighbor Relationship Caching**: Cache neighbor relationships for performance
8. **Neighbor Change Events**: Publish events when neighbor relationships change
9. **Neighbor Visualization**: UI helpers for showing neighbor relationships

## Priority Assessment
**Overall Priority**: High - Neighbor relationships are fundamental to diplomacy and transactions

**Implementation Status**: Partial (30%)
- Basic adjacency mechanics: ✅ Complete
- Hex coordinate system: ✅ Complete
- Player neighbor detection: ❌ Missing
- Wormhole adjacency: ❌ Missing
- Transaction integration: ❌ Missing
- Faction-specific rules: ❌ Missing

**Recommended Focus**: 
1. Build player neighbor detection system on existing adjacency foundation
2. Implement wormhole adjacency rules
3. Connect neighbor relationships to transaction system
4. Add comprehensive test coverage

The neighbor system has a solid foundation with the adjacency mechanics, but lacks the higher-level logic to determine player relationships and integrate with game systems like transactions and diplomacy. This is a critical gap that affects multiple game mechanics.