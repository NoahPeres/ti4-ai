# Rule 64: PLANETS

## Category Overview
**Rule Type**: Core Game Mechanics  
**Complexity**: High  
**Dependencies**: Resources, Influence, Control, Exhausted/Readied States, Technology Specialties, Legendary Planets  

## Raw LRR Text
```
64 PLANETS	
Planets provide players with resources and influence. Planets are on system tiles and each has a name, a resource value, and an influence value. Some planets also have traits.
64.1 A planet's resources are indicated by the value on its planet card and system tile that is surrounded by a yellow triangular border.
64.2 A planet's influence is indicated by the value on its planet card and system tile that is surrounded by a blue hexagonal border.
64.3 A planet's trait has no inherent effects, but some game effects refer to a planet's trait. There are three traits: cultural, hazardous, and industrial.
64.4 Some planets have a technology specialty, which allows those planets to be exhausted to satisfy a prerequisite when researching technology.
64.5 Some planets are legendary planets, as indicated by the legendary planet icon. When a player gains control of a legendary planet, they also gain control of its legendary planet ability card.
64.6 PLANET CARD
Each planet has a corresponding planet card that displays its name, resource value, influence value, and trait, if it has one. If a player controls a planet, they keep that planet's card in their play area.
64.7 A planet card has both a readied and exhausted state. When a planet is readied, it is placed faceup. When a planet is exhausted, it is placed facedown.
64.8 A player can spend a readied planet's resources or influence.
64.9 A player cannot spend an exhausted planet's resources or influence.
RELATED TOPICS: Control, Exhausted, Influence, Legendary Planets, Readied, Resources, System Tiles, Technology
```

## Sub-Rules Analysis

### 64.1 - Resource Values ⚠️ PARTIALLY IMPLEMENTED
**Status**: Basic structure exists, display mechanics unclear  
**Implementation**: Planet class has resources field, but no yellow border display system  
**Test Coverage**: Basic planet creation tests verify resource values  

### 64.2 - Influence Values ⚠️ PARTIALLY IMPLEMENTED
**Status**: Basic structure exists, display mechanics unclear  
**Implementation**: Planet class has influence field, but no blue hexagonal border display system  
**Test Coverage**: Basic planet creation tests verify influence values  

### 64.3 - Planet Traits ❌ NOT IMPLEMENTED
**Status**: Not implemented  
**Implementation**: No trait system for cultural, hazardous, and industrial planets  
**Test Coverage**: No tests for planet traits or trait-based effects  

### 64.4 - Technology Specialties ❌ NOT IMPLEMENTED
**Status**: Not implemented  
**Implementation**: No technology specialty system for prerequisite satisfaction  
**Test Coverage**: No tests for technology specialty mechanics  

### 64.5 - Legendary Planets ❌ NOT IMPLEMENTED
**Status**: Not implemented  
**Implementation**: No legendary planet system or ability card integration  
**Test Coverage**: No tests for legendary planet mechanics  

### 64.6 - Planet Cards ⚠️ PARTIALLY IMPLEMENTED
**Status**: Basic planet representation exists, card management unclear  
**Implementation**: Planet class exists but no player play area integration  
**Test Coverage**: Basic planet tests but no card management tests  

### 64.7 - Readied/Exhausted States ❌ NOT IMPLEMENTED
**Status**: Not implemented  
**Implementation**: No exhausted/readied state tracking for planets  
**Test Coverage**: No tests for planet state management  

### 64.8 - Spending Readied Resources ❌ NOT IMPLEMENTED
**Status**: Not implemented  
**Implementation**: No resource spending system tied to planet states  
**Test Coverage**: No tests for resource spending mechanics  

### 64.9 - Exhausted Spending Restriction ❌ NOT IMPLEMENTED
**Status**: Not implemented  
**Implementation**: No validation preventing exhausted planet resource use  
**Test Coverage**: No tests for exhausted planet restrictions  

## Related Topics
- **Resources**: Core economic system for unit production and abilities
- **Influence**: Used for command tokens, voting, and various abilities
- **Control**: Planet ownership and control mechanics
- **Exhausted/Readied**: Card state system for resource management
- **Technology Specialties**: Research prerequisite satisfaction system
- **Legendary Planets**: Special planets with unique abilities
- **System Tiles**: Physical board representation of planets
- **Exploration**: Planet trait-based exploration mechanics

## Test References

### Current Coverage
- `test_planet.py`: Basic planet creation, control tracking, unit placement
- `test_system.py`: Planet integration within systems
- `test_movement.py`: Planet-based unit movement and placement
- `test_tactical_action.py`: Ground force planet interactions

### Missing Test Scenarios
- Planet trait system (cultural, hazardous, industrial)
- Technology specialty mechanics and prerequisite satisfaction
- Legendary planet abilities and card management
- Planet card readied/exhausted state transitions
- Resource and influence spending validation
- Exhausted planet spending restrictions
- Planet card display and management in play areas

## Implementation Files

### Core Implementation
- `src/ti4/core/planet.py`: Basic planet structure with resources and influence
- Planet card system (not yet implemented)
- Technology specialty system (not yet implemented)
- Legendary planet system (not yet implemented)

### Supporting Systems
- Resource spending and validation system
- Card state management (exhausted/readied)
- Player play area management
- Technology research system integration
- Exploration system integration

## Notable Details

### Strengths
- Solid foundation for basic planet structure (name, resources, influence)
- Good integration with system and unit placement mechanics
- Control tracking system in place
- Comprehensive test coverage for basic planet operations

### Areas Needing Attention
- **Planet Traits**: No implementation of cultural/hazardous/industrial traits
- **State Management**: Missing exhausted/readied state system
- **Resource Spending**: No validation or spending mechanics
- **Technology Integration**: Missing technology specialty system
- **Legendary Planets**: No special planet ability system
- **Card Management**: No planet card play area integration

## Action Items
1. **HIGH**: Implement planet exhausted/readied state system
2. **HIGH**: Add resource and influence spending validation
3. **HIGH**: Create planet trait system (cultural, hazardous, industrial)
4. **MEDIUM**: Implement technology specialty mechanics
5. **MEDIUM**: Add legendary planet system and ability cards
6. **MEDIUM**: Create planet card management in player play areas
7. **LOW**: Add visual display systems for resource/influence borders

## Priority Assessment
**Priority**: High  
**Implementation Status**: 25%  
**Rationale**: Planets are fundamental to TI4's economic and strategic systems. While basic structure exists, critical mechanics like resource spending, state management, and trait systems are missing. These are essential for proper gameplay.