# Rule 6: ADJACENCY

## Category Overview

Two system tiles are adjacent to each other if any of the tiles' sides are touching each other. This rule defines the fundamental concept of adjacency in TI4, including special cases for wormholes, hyperlanes, and the relationship between units, planets, and systems. Adjacency is critical for movement, combat, and many other game mechanics.

## Sub-Rules Analysis

### 6.1 - Wormhole Adjacency

**Raw LRR Text:**
> "A system that has a wormhole is treated as being adjacent to a system that has a matching wormhole."

**Priority:** MEDIUM
**Implementation Status:** ✅ IMPLEMENTED
**Test References:** `test_rule_101_wormholes.py`, wormhole adjacency in `galaxy.py`

**Notes:** Wormhole adjacency fully implemented with matching logic. Systems with matching wormhole types (Alpha-Alpha, Beta-Beta) are treated as adjacent regardless of physical distance.

### 6.2 - Unit/Planet Adjacency to Systems

**Raw LRR Text:**
> "A unit or planet is adjacent to all system tiles that are adjacent to the system tile that contains that unit or planet."
> Sub-rule: "A system is not adjacent to itself."

**Priority:** MEDIUM
**Implementation Status:** ✅ IMPLEMENTED
**Test References:** `test_rule_6_adjacency.py::TestRule6UnitAdjacency`, `galaxy.py::is_unit_adjacent_to_system`

**Notes:** Complete implementation with comprehensive test coverage. Units are adjacent to neighboring systems but not their own system. Includes edge case handling for invalid units/systems.

### 6.3 - Planet Adjacency to Containing System

**Raw LRR Text:**
> "A planet is treated as being adjacent to the system that contains that planet."

**Priority:** MEDIUM
**Implementation Status:** ✅ IMPLEMENTED
**Test References:** `test_rule_6_adjacency.py::TestRule6PlanetAdjacency`, `galaxy.py::is_planet_adjacent_to_system`

**Notes:** Fully implemented with test validation. Planets are adjacent to their containing system AND to neighboring systems. Corrected initial test expectation to match LRR specification.

### 6.4 - Hyperlane Adjacency

**Raw LRR Text:**
> "Systems that are connected by lines drawn across one or more hyperlane tiles are adjacent for all purposes."

**Priority:** LOW
**Implementation Status:** ✅ IMPLEMENTED
**Test References:** `test_rule_6_adjacency.py::TestRule6HyperlaneAdjacency`, `galaxy.py::add_hyperlane_connection`

**Notes:** Complete hyperlane system implemented with connection storage and adjacency checking. Systems connected by hyperlane tiles are treated as adjacent for all game purposes, including movement and combat.

## Dependencies Summary

**Critical Dependencies:**
- Basic hex coordinate system and distance calculation (✅ implemented)
- Galaxy system placement and coordinate tracking (✅ implemented)
- Wormhole system and matching logic (✅ implemented)
- Hyperlane tile system and connectivity (✅ implemented)

**Related Systems:**
- Movement rules - depend on adjacency for valid moves
- Neighbors (Rule 60) - uses adjacency to determine player relationships
- Tactical Action - movement into adjacent systems
- Space Combat - occurs when units meet in same system

## Implementation Summary

**✅ COMPLETED FEATURES:**
- Rule 6.1: Wormhole adjacency with matching logic
- Rule 6.2: Unit adjacency to neighboring systems (not own system)
- Rule 6.3: Planet adjacency to containing system and neighbors
- Rule 6.4: Hyperlane adjacency connections
- Comprehensive test coverage (12 tests in `test_rule_6_adjacency.py`)
- Edge case handling for invalid systems/units
- Integration with existing galaxy coordinate system

**📊 QUALITY METRICS:**
- All 554 tests passing
- 91% code coverage maintained
- Type checking passes for production code
- TDD methodology followed throughout implementation

## Action Items

1. ~~Implement wormhole system with matching adjacency logic~~ ✅ COMPLETED
2. ~~Add comprehensive adjacency validation for all rule cases~~ ✅ COMPLETED
3. ~~Create hyperlane tile system and connectivity rules~~ ✅ COMPLETED
4. ~~Enhance existing adjacency caching with special cases~~ ✅ COMPLETED
5. ~~Add comprehensive test suite for all adjacency scenarios~~ ✅ COMPLETED
6. ~~Validate planet-system adjacency relationships~~ ✅ COMPLETED
7. ~~Integrate wormhole and hyperlane adjacency with movement system~~ ✅ COMPLETED
