# TI4 AI Implementation Roadmap

**Last Updated**: 2025-09-18  
**Current Implementation Status**: 5.7% overall  
**Next Target**: 25% overall (focusing on core spatial mechanics)

## Priority Analysis Summary

Based on comprehensive analysis of all 101 LRR rules, the following implementation order maximizes impact and builds foundational systems that enable higher-level gameplay mechanics.

### Critical Foundation Layer (0% → 15%)
These rules form the spatial and mechanical foundation that all other systems depend on:

1. **Rule 6: ADJACENCY** (0% → 90%) - Core spatial relationships
2. **Rule 60: NEIGHBORS** (0% → 85%) - Neighbor determination system  
3. **Rule 101: WORMHOLES** (0% → 80%) - Special adjacency mechanics

### Victory & Objectives Layer (15% → 20%)
Essential for game completion and AI decision-making:

4. **Rule 61: OBJECTIVE CARDS** (0% → 75%) - Victory condition tracking

### Strategy & Command Layer (20% → 25%)
Core game flow and player actions:

5. **Rule 99: WARFARE STRATEGY CARD** (0% → 70%) - Command token management

---

## Phase 1: Core Spatial Mechanics Foundation

### 🎯 Rule 6: ADJACENCY Implementation Plan

**Target**: 0% → 90% implementation  
**Estimated Effort**: 3-4 days with strict TDD  
**Dependencies**: None (foundational)

#### Step 1: Enhanced Adjacency System (TDD)
```
RED → GREEN → REFACTOR cycle for each feature:

1.1 Basic Physical Adjacency (EXISTING - enhance tests)
   - Test: Adjacent hex coordinates return true
   - Test: Non-adjacent hex coordinates return false  
   - Test: System not adjacent to itself
   - Implementation: Enhance existing Galaxy.are_systems_adjacent()

1.2 Wormhole Adjacency System (NEW)
   - Test: Alpha wormhole systems are adjacent regardless of distance
   - Test: Beta wormhole systems are adjacent regardless of distance
   - Test: Alpha-Beta wormholes are NOT adjacent
   - Test: Systems with multiple wormhole types
   - Implementation: WormholeAdjacencyCalculator class

1.3 Unit/Planet Adjacency Rules (NEW)
   - Test: Unit adjacent to all systems adjacent to containing system
   - Test: Planet adjacent to all systems adjacent to containing system
   - Test: Planet adjacent to its containing system
   - Implementation: Enhanced adjacency checking for units/planets

1.4 Performance & Caching (ENHANCE EXISTING)
   - Test: Adjacency calculations are cached properly
   - Test: Wormhole adjacency cache invalidation
   - Implementation: Enhanced GameStateCache with wormhole support
```

#### Step 2: Wormhole Data Structures (TDD)
```
2.1 Wormhole Types & System Integration
   - Test: System can contain alpha/beta/gamma/delta wormholes
   - Test: System can contain multiple wormhole types
   - Test: Wormhole type validation and constraints
   - Implementation: Wormhole enum, System.wormholes property

2.2 Wormhole Token Management
   - Test: Wormhole tokens can be placed/removed from systems
   - Test: Wormhole token placement validation
   - Implementation: WormholeToken class, placement mechanics
```

#### Step 3: Integration & Edge Cases (TDD)
```
3.1 Complex Adjacency Scenarios
   - Test: Multi-hop adjacency through wormholes
   - Test: Mixed physical and wormhole adjacency
   - Test: Performance with large galaxy configurations
   - Implementation: Comprehensive adjacency resolver

3.2 Movement Integration
   - Test: Movement validation uses enhanced adjacency
   - Test: Wormhole movement mechanics
   - Implementation: Update MovementValidator to use new adjacency
```

---

### 🎯 Rule 60: NEIGHBORS Implementation Plan

**Target**: 0% → 85% implementation  
**Estimated Effort**: 2-3 days with strict TDD  
**Dependencies**: Rule 6 (Adjacency) must be completed first

#### Step 1: Neighbor Determination System (TDD)
```
1.1 Basic Neighbor Queries
   - Test: Get all neighbors of a system
   - Test: Check if two systems are neighbors
   - Test: Neighbor relationships are symmetric
   - Implementation: NeighborCalculator class

1.2 Wormhole Neighbor Integration
   - Test: Wormhole-connected systems are neighbors
   - Test: Neighbor queries include wormhole adjacency
   - Implementation: Integration with wormhole adjacency system

1.3 Performance Optimization
   - Test: Neighbor calculations are cached
   - Test: Bulk neighbor queries are efficient
   - Implementation: Neighbor caching system
```

#### Step 2: Advanced Neighbor Mechanics (TDD)
```
2.1 Range-Based Neighbor Queries
   - Test: Get neighbors within N distance
   - Test: Shortest path between systems
   - Implementation: BFS-based pathfinding with caching

2.2 Conditional Neighbor Queries
   - Test: Get neighbors matching specific criteria
   - Test: Filter neighbors by system properties
   - Implementation: Flexible neighbor query system
```

---

### 🎯 Rule 101: WORMHOLES Implementation Plan

**Target**: 0% → 80% implementation  
**Estimated Effort**: 2-3 days with strict TDD  
**Dependencies**: Rule 6 (Adjacency) foundation

#### Step 1: Wormhole Type System (TDD)
```
1.1 Wormhole Type Definitions
   - Test: Alpha/Beta/Gamma/Delta wormhole types
   - Test: Wormhole type validation and constraints
   - Implementation: WormholeType enum, validation logic

1.2 Wormhole Adjacency Rules
   - Test: Matching wormhole types create adjacency
   - Test: Different wormhole types do NOT create adjacency
   - Test: Multiple wormhole types in same system
   - Implementation: Core wormhole adjacency logic
```

#### Step 2: Faction-Specific Wormholes (TDD)
```
2.1 Delta Wormhole Mechanics (Ghosts of Creuss)
   - Test: Delta wormhole special rules
   - Test: Faction-specific wormhole interactions
   - Implementation: Faction-aware wormhole system

2.2 Wormhole Token Placement
   - Test: Dynamic wormhole token placement
   - Test: Wormhole token removal and effects
   - Implementation: WormholeTokenManager class
```

---

## Phase 2: Victory & Strategy Systems

### 🎯 Rule 61: OBJECTIVE CARDS Implementation Plan

**Target**: 0% → 75% implementation  
**Estimated Effort**: 3-4 days with strict TDD

#### Step 1: Objective Card System (TDD)
```
1.1 Objective Card Types & Structure
   - Test: Stage I and Stage II objective cards
   - Test: Secret objective cards
   - Test: Objective card validation and constraints
   - Implementation: ObjectiveCard class hierarchy

1.2 Objective Tracking & Scoring
   - Test: Objective completion detection
   - Test: Victory point awarding
   - Test: Objective card claiming mechanics
   - Implementation: ObjectiveTracker class
```

#### Step 2: Victory Condition Integration (TDD)
```
2.1 Victory Point Management
   - Test: Victory point accumulation and tracking
   - Test: Victory condition checking (10+ points)
   - Test: Alternative victory conditions
   - Implementation: Enhanced VictoryPointManager

2.2 AI Decision Support
   - Test: Objective evaluation for AI planning
   - Test: Objective priority scoring
   - Implementation: ObjectiveEvaluator for AI systems
```

---

### 🎯 Rule 99: WARFARE STRATEGY CARD Implementation Plan

**Target**: 0% → 70% implementation  
**Estimated Effort**: 2-3 days with strict TDD

#### Step 1: Command Token Management (TDD)
```
1.1 Command Token Redistribution
   - Test: Remove command tokens from game board
   - Test: Redistribute tokens to command sheet pools
   - Test: Token redistribution validation and limits
   - Implementation: CommandTokenRedistributor class

1.2 Strategy Card Integration
   - Test: Warfare primary ability execution
   - Test: Warfare secondary ability (other players)
   - Implementation: WarfareStrategyCard class
```

---

## Implementation Guidelines

### Strict TDD Process
1. **RED**: Write failing test first
2. **GREEN**: Write minimal code to pass test  
3. **REFACTOR**: Clean up code while keeping tests green
4. **REPEAT**: For each small feature increment

### Quality Gates
- **100% test coverage** for all new code
- **Performance benchmarks** for adjacency/neighbor calculations
- **Integration tests** for cross-rule interactions
- **Documentation** for all public APIs

### Success Metrics
- **Overall Implementation**: Track progress toward 25% target
- **Test Coverage**: Maintain 100% for new implementations
- **Performance**: Adjacency queries <1ms, neighbor queries <5ms
- **Integration**: All existing tests continue to pass

---

## Context for Future Development

This roadmap prioritizes **foundational spatial mechanics** that enable all higher-level TI4 gameplay. Once Phase 1 is complete:

- **Movement system** will have proper adjacency foundation
- **Combat system** can use accurate neighbor determination  
- **Ability ranges** will work correctly with wormhole adjacency
- **AI planning** will have spatial awareness for strategic decisions

The **strict TDD approach** ensures each implementation is robust, testable, and maintainable, building toward a production-ready TI4 AI system.

**Next Action**: Begin with Rule 6 (Adjacency) implementation using the detailed TDD plan above.