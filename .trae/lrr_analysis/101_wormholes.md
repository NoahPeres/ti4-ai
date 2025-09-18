# Rule 101: WORMHOLES

## Category Overview
Wormholes are special tokens that create adjacency between systems that are not normally adjacent. They enable movement and other interactions across the galaxy map. This rule defines the core mechanics for wormhole adjacency, movement, and special interactions.

## Raw LRR Text
```
101. WORMHOLES
Systems that contain identical wormholes are adjacent to each other.
• A system that contains an alpha wormhole is adjacent to all other systems that contain an alpha wormhole.
• A system that contains a beta wormhole is adjacent to all other systems that contain a beta wormhole.
• A system that contains a gamma wormhole is adjacent to all other systems that contain a gamma wormhole.
• A system that contains a delta wormhole is adjacent to all other systems that contain a delta wormhole.
• A system that contains a wormhole is not adjacent to systems that contain other types of wormholes.
• If a system contains multiple types of wormholes, that system is adjacent to all systems that contain any of those wormhole types.
```

## Sub-rules Analysis

### 101.1 - Alpha/Beta Wormhole Adjacency
**Status**: ✅ IMPLEMENTED  
**Priority**: COMPLETED  
**Details**: Systems with matching wormhole types (alpha-alpha, beta-beta) are adjacent
- ✅ Core adjacency calculation includes wormhole logic in `Galaxy._check_wormhole_adjacency`
- ✅ Wormhole type checking implemented in neighbor determination
- ✅ Full test coverage in `tests/test_rule_101_wormholes.py` and `tests/test_wormhole_adjacency.py`
- Ready for movement and ability range calculations

### 101.2 - Gamma Wormhole Adjacency  
**Status**: ✅ IMPLEMENTED  
**Priority**: COMPLETED  
**Details**: Gamma wormholes follow same adjacency rules as alpha/beta
- ✅ Implemented using same wormhole adjacency system
- ✅ Test coverage confirms gamma wormhole adjacency works correctly

### 101.3 - Delta Wormhole Adjacency
**Status**: ✅ IMPLEMENTED  
**Priority**: COMPLETED  
**Details**: Delta wormholes are faction-specific (Ghosts of Creuss)
- ✅ Delta wormhole adjacency implemented using standard wormhole system
- ✅ Test coverage confirms delta wormhole adjacency works correctly
- Note: Faction-specific placement rules may need additional implementation

### 101.4 - Multiple Wormhole Types
**Status**: ✅ IMPLEMENTED  
**Priority**: COMPLETED  
**Details**: Systems with multiple wormholes are adjacent to systems with any matching type
- ✅ Complex adjacency calculation implemented in `Galaxy._check_wormhole_adjacency`
- ✅ Test coverage confirms multiple wormhole type handling works correctly

### 101.5 - Wormhole Exclusivity
**Status**: ✅ IMPLEMENTED  
**Priority**: COMPLETED  
**Details**: Systems are NOT adjacent if they have different wormhole types
- ✅ Prevents alpha-beta adjacency correctly
- ✅ Test coverage confirms exclusivity rules work correctly

## Related Topics
- **Rule 6**: ADJACENCY - Core adjacency mechanics
- **Rule 58**: MOVEMENT - Movement through wormholes
- **Rule 100**: WORMHOLE NEXUS - Mecatol Rex wormhole interactions
- **Rule 17**: CREUSS GATE - Faction-specific wormhole mechanics

## Test References
**Current Coverage**: None identified
- No wormhole adjacency tests found
- No wormhole movement tests found
- No wormhole type validation tests found

**Missing Test Scenarios**:
- Alpha wormhole adjacency validation
- Beta wormhole adjacency validation  
- Gamma/delta wormhole adjacency
- Multiple wormhole type handling
- Wormhole movement validation
- Cross-wormhole ability range checks

## Implementation Files
**Core Files**: 
- Adjacency calculation logic (not found)
- System/wormhole data structures (not found)
- Movement validation (not found)

**Supporting Files**:
- Game setup (wormhole placement)
- Faction-specific wormhole rules
- UI wormhole indicators

## Notable Details
**Strengths**:
- Clear rule definition in LRR text
- Well-defined adjacency logic
- Comprehensive wormhole type coverage

**Areas Needing Attention**:
- Complete lack of wormhole adjacency implementation
- No test coverage for wormhole mechanics
- Missing wormhole data structures
- No UI indicators for wormhole adjacency
- Faction-specific wormhole rules not implemented

## Action Items

### High Priority
- [ ] Implement core wormhole adjacency calculation
- [ ] Add wormhole type checking to neighbor determination
- [ ] Create comprehensive wormhole adjacency tests
- [ ] Validate movement through wormholes

### Medium Priority  
- [ ] Implement gamma/delta wormhole handling
- [ ] Add multiple wormhole type support
- [ ] Create wormhole UI indicators
- [ ] Add faction-specific wormhole rules

### Low Priority
- [ ] Optimize wormhole adjacency calculations
- [ ] Add wormhole adjacency debugging tools
- [ ] Create wormhole interaction documentation

## Priority Assessment
**Overall Priority**: High  
**Implementation Status**: 0% (Not implemented)  
**Rationale**: Wormholes are fundamental to TI4 gameplay, affecting movement, abilities, and strategic positioning. Complete absence of implementation makes this a critical gap that impacts core game mechanics.