# LRR Rule Analysis: Rule 42 - HYPERLANES

## Category Overview
**Rule Type**: Board Setup & Adjacency  
**Complexity**: Medium  
**Scope**: Expansion feature for creating non-physical adjacency connections  

## Raw LRR Text
```
44 HYPERLANES
Hyperlanes are tiles that are used in some game board setups to create adjacency of system tiles that are not touching each other.
44.1 Systems that are connected by lines drawn across one or more hyperlane tiles are adjacent for all purposes.
44.2 Hyperlane tiles are not systems. They cannot have units on them and they cannot be targets for effects or abilities.
```

## Sub-Rules Analysis

### 44.1 Hyperlane Adjacency
**Rule**: "Systems that are connected by lines drawn across one or more hyperlane tiles are adjacent for all purposes."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: Basic adjacency exists in `galaxy.py` but no hyperlane system
- **Tests**: No hyperlane adjacency tests found
- **Assessment**: Core hyperlane adjacency mechanics missing
- **Priority**: LOW (expansion feature)
- **Dependencies**: Requires hyperlane tile system and enhanced adjacency calculation

### 44.2 Hyperlane Tile Properties
**Rule**: "Hyperlane tiles are not systems. They cannot have units on them and they cannot be targets for effects or abilities."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No hyperlane tile system exists
- **Tests**: No hyperlane tile tests
- **Assessment**: Hyperlane tiles need special handling as non-system tiles
- **Priority**: LOW
- **Dependencies**: Requires tile type system and unit placement restrictions

## Related Topics
- **Adjacency (Rule 6)**: Hyperlanes create special adjacency rules
- **Movement**: Hyperlane adjacency affects ship movement
- **System Tiles**: Hyperlanes are special tiles but not systems
- **Game Board Setup**: Hyperlanes used in specific player count configurations

## Dependencies
- **Core Systems**: Adjacency calculation system
- **Board Setup**: Galaxy configuration and tile placement
- **Movement System**: Enhanced adjacency checking for movement validation
- **Tile System**: Distinction between system tiles and hyperlane tiles

## Test References
**Current Test Coverage**: ❌ NONE
- No hyperlane-specific tests found
- Basic adjacency tests exist in `test_performance_cache.py` and `test_naming_improvements.py`
- No board setup tests with hyperlanes

**Missing Test Areas**:
- Hyperlane adjacency calculation
- Board setup with hyperlane configurations
- Movement through hyperlane connections
- Unit placement restrictions on hyperlane tiles

## Implementation Files
**Current Implementation**: ❌ NOT IMPLEMENTED

**Relevant Files**:
- `src/ti4/core/galaxy.py`: Basic adjacency system (needs enhancement)
- `src/ti4/core/system.py`: System structure (needs hyperlane distinction)
- `docs/lrr_analysis_06_adjacency.md`: Documents missing hyperlane implementation

**Missing Components**:
- Hyperlane tile class
- Enhanced adjacency calculation with hyperlane support
- Board setup configurations with hyperlanes
- Hyperlane-specific movement validation

## Notable Implementation Details

### Setup Information from LRR
- **5-Player (Hyperlanes)**: Uses tiles 83A, 84A, 85A, 86A, 87A, 88A
- **7-Player**: Uses tiles 83A, 84A, 85A, 86A, 87A, 88A
- **7-Player (Alternate)**: Uses tiles 83B, 84B, 85B, 86B, 88B, 90B
- **8-Player (Alternate)**: Uses tiles 83B, 85B, 87A, 88A, 89B, 90B

### Current Adjacency System
- Basic hex coordinate distance calculation exists
- No support for virtual adjacency through hyperlanes
- Performance caching exists for adjacency checks

## Action Items

### High Priority (if implementing hyperlanes)
1. **Create Hyperlane Tile System**
   - Define hyperlane tile class
   - Implement tile placement and configuration
   - Add board setup support for hyperlane configurations

2. **Enhance Adjacency System**
   - Extend adjacency calculation to include hyperlane connections
   - Update performance caching for hyperlane adjacency
   - Ensure "adjacent for all purposes" rule compliance

### Medium Priority
3. **Movement Integration**
   - Update movement validation to use hyperlane adjacency
   - Test movement through hyperlane connections
   - Verify tactical action system compatibility

4. **Unit Placement Restrictions**
   - Implement restrictions preventing units on hyperlane tiles
   - Add validation for targeting restrictions
   - Update system vs. non-system tile distinction

### Low Priority
5. **Board Setup Configurations**
   - Implement specific hyperlane configurations for different player counts
   - Add setup validation for hyperlane placement
   - Create board setup utilities for hyperlane games

## Priority Assessment
**Overall Priority**: 🟢 LOW

**Rationale**:
- Hyperlanes are an expansion feature, not core gameplay
- Basic adjacency system works for core game
- Implementation would be complex but not essential
- No current demand or usage in existing codebase

**Implementation Effort**: HIGH
- Requires significant changes to adjacency system
- Complex board setup configurations
- Extensive testing needed for edge cases

**Dependencies**: Multiple core systems need enhancement