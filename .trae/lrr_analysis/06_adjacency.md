# Rule 6: ADJACENCY

## Category Overview

Two system tiles are adjacent to each other if any of the tiles' sides are touching each other. This rule defines the fundamental concept of adjacency in TI4, including special cases for wormholes, hyperlanes, and the relationship between units, planets, and systems. Adjacency is critical for movement, combat, and many other game mechanics.

## Sub-Rules Analysis

### 6.1 - Wormhole Adjacency

**Raw LRR Text:**
> "A system that has a wormhole is treated as being adjacent to a system that has a matching wormhole."

**Priority:** MEDIUM  
**Implementation Status:** ❌ NOT IMPLEMENTED  
**Test References:** No wormhole adjacency tests found  

**Notes:** Special adjacency rules missing - wormholes create virtual adjacency. Wormholes effectively make distant systems adjacent for movement and other purposes.

### 6.2 - Unit/Planet Adjacency to Systems

**Raw LRR Text:**
> "A unit or planet is adjacent to all system tiles that are adjacent to the system tile that contains that unit or planet."
> Sub-rule: "A system is not adjacent to itself."

**Priority:** MEDIUM  
**Implementation Status:** ⚠️ PARTIAL  
**Test References:** Basic system tests in `test_utils.py`, adjacency caching tests in `test_performance_cache.py`  

**Notes:** Basic system structure exists but adjacency rules incomplete. The sub-rule clarifies that systems are not self-adjacent.

### 6.3 - Planet Adjacency to Containing System

**Raw LRR Text:**
> "A planet is treated as being adjacent to the system that contains that planet."

**Priority:** MEDIUM  
**Implementation Status:** ⚠️ PARTIAL  
**Test References:** Some system/planet tests exist  

**Notes:** Basic planet-system relationship exists but may need verification of adjacency rules. This establishes that planets are adjacent to their own system.

### 6.4 - Hyperlane Adjacency

**Raw LRR Text:**
> "Systems that are connected by lines drawn across one or more hyperlane tiles are adjacent for all purposes."

**Priority:** LOW  
**Implementation Status:** ❌ NOT IMPLEMENTED  
**Test References:** No hyperlane tests found  

**Notes:** Hyperlanes are an expansion feature that creates new adjacency paths beyond physical touching. Creates additional adjacency connections.

## Dependencies Summary

**Critical Dependencies:**
- Basic hex coordinate system and distance calculation (✅ implemented)
- Galaxy system placement and coordinate tracking (✅ implemented)
- Wormhole system and matching logic
- Hyperlane tile system and connectivity

**Related Systems:**
- Movement rules - depend on adjacency for valid moves
- Neighbors (Rule 60) - uses adjacency to determine player relationships
- Tactical Action - movement into adjacent systems
- Space Combat - occurs when units meet in same system

## Action Items

1. Implement wormhole system with matching adjacency logic
2. Add comprehensive adjacency validation for all rule cases
3. Create hyperlane tile system and connectivity rules
4. Enhance existing adjacency caching with special cases
5. Add comprehensive test suite for all adjacency scenarios
6. Validate planet-system adjacency relationships
7. Integrate wormhole and hyperlane adjacency with movement system