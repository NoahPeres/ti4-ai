# LRR Rule Analysis: Section 6 - ADJACENCY

## 6. ADJACENCY

**Rule Category Overview**: Two system tiles are adjacent to each other if any of the tiles' sides are touching each other.

### 6.1 Wormhole Adjacency
**Rule**: "A system that has a wormhole is treated as being adjacent to a system that has a matching wormhole."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: Basic adjacency exists in galaxy system but no wormhole rules
- **Tests**: No wormhole adjacency tests
- **Assessment**: Special adjacency rules missing - wormholes create virtual adjacency
- **Priority**: MEDIUM
- **Dependencies**: Requires wormhole system and adjacency calculation
- **Notes**: Wormholes effectively make distant systems adjacent for movement and other purposes

### 6.2 Unit/Planet Adjacency to Systems
**Rule**: "A unit or planet is adjacent to all system tiles that are adjacent to the system tile that contains that unit or planet."

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Basic system structure exists in `src/ti4/core/system.py`
- **Tests**: Some system tests exist
- **Assessment**: Basic planet-system relationship exists but adjacency rules incomplete
- **Priority**: MEDIUM
- **Dependencies**: Requires complete adjacency calculation system
- **Notes**: Sub-rule: "A system is not adjacent to itself."

### 6.3 Planet Adjacency to Containing System
**Rule**: "A planet is treated as being adjacent to the system that contains that planet."

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Basic planet-system relationship exists in `src/ti4/core/system.py`
- **Tests**: Some system/planet tests exist
- **Assessment**: Basic structure exists but may need verification of adjacency rules
- **Priority**: MEDIUM
- **Dependencies**: Requires planet-system relationship validation
- **Notes**: This establishes that planets are adjacent to their own system

### 6.4 Hyperlane Adjacency
**Rule**: "Systems that are connected by lines drawn across one or more hyperlane tiles are adjacent for all purposes."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No hyperlane system
- **Tests**: No hyperlane tests
- **Assessment**: Hyperlanes create additional adjacency connections beyond physical touching
- **Priority**: LOW
- **Dependencies**: Requires hyperlane tile system and adjacency calculation
- **Notes**: Hyperlanes are an expansion feature that creates new adjacency paths