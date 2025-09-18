# LRR Rule Analysis: Rule 60 - NEIGHBORS

## Rule Category Overview
**Rule 60: NEIGHBORS** - Defines when two players are considered neighbors for the purposes of transactions and other game effects.

## Raw LRR Text
```
60 NEIGHBORS	
Two players are neighbors if they both have a unit or control a planet in the same system. They are also neighbors if they both have a unit or control a planet in systems that are adjacent to each other.
60.1 Players can resolve transactions with their neighbors.
60.2 Players are neighbors if the adjacency of systems is granted by a wormhole.
60.3 Players are neighbors with the Ghosts of Creuss if the Ghosts of Creuss' "Quantum Entanglement" faction ability is causing adjacency from the perspective of the Ghosts of Creuss player.
RELATED TOPICS: Promissory Notes, Transactions
```

## Sub-Rules Analysis

### 60.0 Basic Neighbor Definition
**Rule**: "Two players are neighbors if they both have a unit or control a planet in the same system. They are also neighbors if they both have a unit or control a planet in systems that are adjacent to each other."

**Implementation Status**: ✅ IMPLEMENTED
- **Code**: `Galaxy.are_players_neighbors()` method in `src/ti4/core/galaxy.py` with comprehensive neighbor detection
- **Tests**: Full test coverage in `tests/test_neighbor_detection.py` with 5 test scenarios
- **Assessment**: Complete implementation with same system, adjacent system, wormhole, and edge case coverage
- **Priority**: COMPLETED
- **Dependencies**: Uses existing adjacency system and unit/planet tracking
- **Notes**: Core mechanic for transactions and many game effects - READY FOR USE

### 60.1 Transaction Eligibility
**Rule**: "Players can resolve transactions with their neighbors."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No transaction system or neighbor validation
- **Tests**: No transaction or neighbor validation tests
- **Assessment**: Critical for diplomatic gameplay - transactions are core mechanic
- **Priority**: HIGH
- **Dependencies**: Requires neighbor detection and transaction system
- **Notes**: Transactions include trade goods, commodities, promissory notes

### 60.2 Wormhole Neighbor Adjacency
**Rule**: "Players are neighbors if the adjacency of systems is granted by a wormhole."

**Implementation Status**: ✅ IMPLEMENTED
- **Code**: Integrated into `Galaxy.are_players_neighbors()` method using existing wormhole adjacency system
- **Tests**: Covered in `tests/test_neighbor_detection.py` with wormhole connection test scenario
- **Assessment**: Wormhole adjacency properly extends neighbor relationships beyond physical adjacency
- **Priority**: COMPLETED
- **Dependencies**: Uses existing wormhole system and adjacency calculation
- **Notes**: Extends neighbor relationships beyond physical adjacency - READY FOR USE

### 60.3 Ghosts of Creuss Special Case
**Rule**: "Players are neighbors with the Ghosts of Creuss if the Ghosts of Creuss' 'Quantum Entanglement' faction ability is causing adjacency from the perspective of the Ghosts of Creuss player."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No faction-specific abilities or Ghosts of Creuss implementation
- **Tests**: No faction ability tests
- **Assessment**: Faction-specific neighbor rule for Ghosts of Creuss
- **Priority**: LOW
- **Dependencies**: Requires faction abilities and Ghosts of Creuss implementation
- **Notes**: Special case that extends neighbor relationships for specific faction

## Related Topics
- **Adjacency (Rule 6)**: Foundation for neighbor determination
- **Transactions**: Primary use case for neighbor relationships
- **Promissory Notes**: Diplomatic tools exchanged between neighbors
- **Wormholes**: Create virtual adjacency for neighbor purposes
- **Faction Abilities**: Special cases like Ghosts of Creuss

## Test References

### Current Test Coverage
- **Adjacency Tests**: `test_performance_cache.py`, `test_movement.py`, `test_hex_coordinate.py`
- **System Tests**: Basic system structure and unit placement
- **Galaxy Tests**: Basic adjacency checking between systems

### Missing Test Scenarios
- Player neighbor detection based on unit/planet presence
- Neighbor validation for transaction eligibility
- Wormhole-based neighbor relationships
- Ghosts of Creuss special neighbor rules
- Multi-system neighbor scenarios
- Dynamic neighbor changes during gameplay

## Implementation Files

### Core Implementation
- `src/ti4/core/galaxy.py` - Basic system adjacency (partial)
- `src/ti4/performance/cache.py` - Adjacency caching (partial)
- **MISSING**: Player neighbor detection system
- **MISSING**: Transaction validation system

### Supporting Files
- `src/ti4/core/system.py` - System structure with units/planets
- `src/ti4/core/hex_coordinate.py` - Coordinate-based adjacency
- **MISSING**: Wormhole system
- **MISSING**: Faction ability system
- **MISSING**: Transaction system

## Notable Details

### Strengths
- Basic system adjacency calculation implemented
- Efficient adjacency caching system
- Hex coordinate system supports adjacency detection
- Test utilities for adjacent system scenarios

### Areas Needing Attention
- No player neighbor detection logic
- Missing transaction system integration
- No wormhole adjacency support
- No faction-specific neighbor rules
- Limited test coverage for neighbor scenarios

## Action Items

### High Priority
1. **Implement Player Neighbor Detection**: Create system to determine when players are neighbors
2. **Transaction System Integration**: Build transaction validation using neighbor relationships
3. **Comprehensive Neighbor Tests**: Test all neighbor determination scenarios

### Medium Priority
1. **Wormhole Adjacency Support**: Implement wormhole-based neighbor relationships
2. **Dynamic Neighbor Tracking**: Track neighbor changes during gameplay
3. **Neighbor Validation API**: Provide clean interface for neighbor checking

### Low Priority
1. **Faction-Specific Rules**: Implement Ghosts of Creuss special neighbor rules
2. **Neighbor Optimization**: Optimize neighbor detection for performance
3. **Neighbor Analytics**: Track neighbor relationships for game analysis

## Priority Assessment
- **Overall Priority**: HIGH
- **Implementation Status**: ~20% (basic adjacency only)
- **Blocking Dependencies**: Transaction system, player unit tracking
- **Impact**: Critical for diplomatic gameplay and many game mechanics