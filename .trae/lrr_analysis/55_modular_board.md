# Rule 55: MODULAR BOARD

## Category Overview
**Rule Type**: Game Setup & Board Mechanics  
**Complexity**: High  
**Implementation Priority**: High  
**Dependencies**: Galaxy System, System Tiles, Hex Coordinates  

## Raw LRR Text
From `lrr.txt` setup section and related rules:

**STEP 6-CREATE GAME BOARD**: Place the Mecatol Rex system tile in the center of the common play area-this is the center of the galaxy. The galaxy will consist of either three or four rings around Mecatol Rex. Each player's home systems will be in a set position in the third ring.

**Board Setup Process**:
1. **Separate Systems**: Separate system tiles into blue-backed and red-backed piles
2. **Deal System Tiles**: Deal tiles to players based on player count and setup
3. **Place System Tiles**: Players place tiles in rings around Mecatol Rex
4. **Hyperlane Setup**: Place hyperlane tiles for specific configurations
5. **Token Placement**: Place custodians token and frontier tokens

**Player Count Configurations**:
- **THREE-PLAYER**: Six blue and two red tiles per player
- **FOUR-PLAYER**: Five blue and three red tiles per player  
- **FIVE-PLAYER (NO HYPERLANES)**: Four blue and two red tiles per player + speaker places one red
- **FIVE-PLAYER (HYPERLANES)**: Three blue and two red tiles per player
- **SIX-PLAYER**: Three blue and two red tiles per player
- **SIX-PLAYER (LARGE GALAXY)**: Six blue and three red tiles per player
- **SEVEN-PLAYER**: Four blue and two red tiles per player + speaker places two red and three blue
- **EIGHT-PLAYER**: Four blue and two red tiles per player + speaker places two red and two blue
- **EIGHT-PLAYER (ALTERNATE)**: Three blue and two red tiles per player

**Hyperlane Configurations**:
- **FIVE-PLAYER (HYPERLANES)**: 83A, 84A, 85A, 86A, 87A, and 88A
- **SEVEN-PLAYER**: 83A, 84A, 85A, 86A, 87A, and 88A
- **SEVEN-PLAYER (ALTERNATE)**: 83B, 84B, 85B, 86B, 88B, and 90B
- **EIGHT-PLAYER (ALTERNATE)**: 83B, 85B, 87A, 88A, 89B, and 90B

**System Tile Properties**:
- **88.6**: Any area on a system tile that is not a planet is space
- **88.7**: Double-sided tiles with lines crossing edges are hyperlane tiles (not systems)

**Related Topics**: Adjacency, Anomalies, Planets, Ships, Wormholes

## Sub-Rules Analysis

### Board Creation Process
- **Status**: ⚠️ Partially Implemented
- **Location**: `src/ti4/core/galaxy.py` - Basic galaxy structure
- **Test Coverage**: `test_galaxy.py` - Basic galaxy creation
- **Implementation Notes**: Basic hex coordinate system exists but no setup process

### System Tile Management
- **Status**: ❌ Not Implemented
- **Location**: No system tile management found
- **Test Coverage**: None found
- **Implementation Notes**: No tile separation, dealing, or placement system

### Player Count Configurations
- **Status**: ❌ Not Implemented
- **Location**: No configuration system found
- **Test Coverage**: None found
- **Implementation Notes**: No player count-based setup logic

### Hyperlane System
- **Status**: ❌ Not Implemented
- **Location**: No hyperlane system found
- **Test Coverage**: None found
- **Implementation Notes**: No hyperlane tile placement or connectivity

### Ring-Based Placement
- **Status**: ❌ Not Implemented
- **Location**: No ring placement system found
- **Test Coverage**: None found
- **Implementation Notes**: No structured tile placement around Mecatol Rex

### Token Placement
- **Status**: ❌ Not Implemented
- **Location**: No token placement system found
- **Test Coverage**: None found
- **Implementation Notes**: No custodians or frontier token placement

## Related Topics
- **Rule 6**: ADJACENCY (system adjacency rules)
- **Rule 9**: ANOMALIES (special system tiles)
- **Rule 88**: SYSTEM TILES (system tile properties)
- **Rule 50**: NEIGHBORS (adjacency relationships)
- **Rule 96**: WORMHOLES (wormhole connectivity)

## Dependencies
- **Hex Coordinate System**: For tile positioning (✅ Implemented)
- **Galaxy Structure**: For board representation (⚠️ Basic Implementation)
- **System Tiles**: For tile properties and types (❌ Missing)
- **Player Management**: For player count configurations (⚠️ Basic Implementation)
- **Hyperlane System**: For hyperlane connectivity (❌ Missing)
- **Token System**: For board tokens (❌ Missing)

## Test References
### Current Test Coverage:
- `test_galaxy.py`: Basic galaxy structure testing
  - Galaxy creation
  - System placement at coordinates
  - Basic hex coordinate usage

### Test Scenarios Covered:
1. **Basic Galaxy Creation**: Galaxy object instantiation
2. **System Placement**: Placing systems at hex coordinates
3. **Coordinate System**: Basic hex coordinate functionality

### Missing Test Scenarios:
1. **Board Setup Process**: No tests for complete board creation
2. **Player Count Configurations**: No tests for different player counts
3. **System Tile Management**: No tests for tile separation and dealing
4. **Ring Placement**: No tests for structured tile placement
5. **Hyperlane Setup**: No tests for hyperlane configurations
6. **Token Placement**: No tests for board token placement
7. **Configuration Validation**: No tests for valid board configurations
8. **Adjacency Integration**: No tests for board-wide adjacency

## Implementation Files
### Core Implementation:
- `src/ti4/core/galaxy.py`: Basic Galaxy class with hex coordinate system
- `src/ti4/core/system.py`: Basic System class structure
- `src/ti4/core/hex_coordinate.py`: Hex coordinate mathematics

### Supporting Files:
- `src/ti4/testing/scenario_builder.py`: Basic galaxy configuration in test builder
- `tests/test_utils.py`: Utility for creating adjacent systems

### Missing Implementation:
- System tile management system
- Board setup process
- Player count configurations
- Hyperlane system
- Ring-based placement logic
- Token placement system
- Board validation system
- Configuration templates

## Notable Implementation Details

### Strengths:
1. **Hex Coordinate System**: Solid mathematical foundation for hex-based board
2. **Basic Galaxy Structure**: Galaxy class with system placement capability
3. **Adjacency Calculation**: Basic adjacency checking between systems
4. **System Structure**: Basic system representation with planets and units

### Areas Needing Attention:
1. **Setup Process**: No automated board creation process
2. **Configuration System**: No player count-based configurations
3. **System Tiles**: No tile type management or properties
4. **Hyperlanes**: No hyperlane connectivity system
5. **Validation**: No board configuration validation
6. **Token Management**: No board token placement system

### Architecture Quality:
- **Good**: Hex coordinate mathematics and basic galaxy structure
- **Needs Work**: Board setup automation and configuration management
- **Missing**: System tile management and hyperlane system

## Action Items

### High Priority:
1. **Implement Board Setup Process**: Automated board creation for different player counts
2. **Create System Tile Management**: Tile separation, dealing, and placement system
3. **Add Configuration Templates**: Player count-based setup configurations
4. **Implement Ring Placement**: Structured tile placement around Mecatol Rex

### Medium Priority:
5. **Add Hyperlane System**: Hyperlane tile placement and connectivity
6. **Create Token Placement**: Custodians and frontier token management
7. **Add Board Validation**: Validate board configurations and adjacency
8. **Implement Setup Automation**: Complete automated board generation

### Low Priority:
9. **Add Visual Board Representation**: Board visualization system
10. **Create Setup Variants**: Alternative board configurations
11. **Add Board Analysis**: Board balance and fairness analysis
12. **Implement Board Persistence**: Save/load board configurations

## Priority Assessment
**Overall Priority**: High - Board setup is fundamental to game initialization

**Implementation Status**: Basic Foundation (20%)
- Hex coordinate system: ✅ Complete
- Basic galaxy structure: ✅ Complete
- System placement: ✅ Complete
- Board setup process: ❌ Missing
- System tile management: ❌ Missing
- Player configurations: ❌ Missing
- Hyperlane system: ❌ Missing
- Token placement: ❌ Missing

**Recommended Focus**: 
1. Design and implement board setup process for different player counts
2. Create system tile management system with tile types and properties
3. Add configuration templates for all supported player counts
4. Implement ring-based tile placement logic around Mecatol Rex

The current implementation provides a solid foundation with hex coordinates and basic galaxy structure, but lacks the complete board setup process that's essential for game initialization. This is a high-priority system since every game requires proper board setup, and the modular nature is a core feature of TI4. The implementation would build well on the existing hex coordinate system but requires significant work on the setup automation and configuration management.