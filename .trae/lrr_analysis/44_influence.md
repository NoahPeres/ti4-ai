# LRR Rule Analysis: Rule 44 - INFLUENCE

## Category Overview
**Rule Type**: Resource System & Political Mechanics  
**Complexity**: Medium  
**Scope**: Planet political power and spending mechanics  

## Raw LRR Text
```
47 INFLUENCE
Influence represents a planet's political power. Players spend influence to gain command tokens using the "Leadership" strategy card, and the influence values of planets are used to cast votes during the agenda phase.
47.1 A planet's influence is the rightmost value (surrounded by a blue border) found on the planet's system tile and planet card.
47.2 A player can spend a planet's influence by exhausting that planet's card.
47.3 A player can spend a trade good as if it were one influence.
a Players cannot spend trade goods to cast votes during the agenda phase.
```

## Sub-Rules Analysis

### 47.0 Influence Definition
**Rule**: "Influence represents a planet's political power. Players spend influence to gain command tokens using the 'Leadership' strategy card, and the influence values of planets are used to cast votes during the agenda phase."

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Planet influence values exist in `Planet` class
- **Tests**: Basic planet influence tracking in multiple test files
- **Assessment**: Basic influence values exist but spending mechanics missing
- **Priority**: HIGH
- **Dependencies**: Requires Leadership strategy card and agenda phase systems

### 47.1 Influence Value Location
**Rule**: "A planet's influence is the rightmost value (surrounded by a blue border) found on the planet's system tile and planet card."

**Implementation Status**: ✅ IMPLEMENTED
- **Code**: Planet class has influence property
- **Tests**: Planet creation tests verify influence values
- **Assessment**: Basic influence value storage implemented
- **Priority**: HIGH (COMPLETE)
- **Dependencies**: None

### 47.2 Spending Influence by Exhausting Planets
**Rule**: "A player can spend a planet's influence by exhausting that planet's card."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No planet exhaustion system found
- **Tests**: No tests for planet exhaustion or influence spending
- **Assessment**: Core spending mechanic missing
- **Priority**: HIGH
- **Dependencies**: Requires planet card exhaustion system

### 47.3 Trade Goods as Influence
**Rule**: "A player can spend a trade good as if it were one influence."
**Sub-rule**: "Players cannot spend trade goods to cast votes during the agenda phase."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No trade good to influence conversion system
- **Tests**: No tests for trade good influence spending
- **Assessment**: Alternative influence spending missing
- **Priority**: MEDIUM
- **Dependencies**: Requires trade good system and spending validation

## Related Topics
- **Leadership Strategy Card (Rule 52)**: Primary use of influence spending
- **Agenda Phase (Rule 8)**: Influence used for voting
- **Exhausted (Rule 34)**: Planet exhaustion mechanics
- **Trade Goods (Rule 93)**: Alternative influence source
- **Planets (Rule 64)**: Source of influence values

## Dependencies
- **Core Systems**: Planet card exhaustion system
- **Strategy Cards**: Leadership strategy card implementation
- **Agenda System**: Voting mechanics using influence
- **Trade Good System**: Alternative influence spending
- **Resource Management**: Unified spending system

## Test References
**Current Test Coverage**: ⚠️ PARTIAL
- **Planet Influence Values**: Tested in `test_planet.py`, `test_system.py`
- **Influence in Game Objects**: Used in `test_movement.py`, `test_tactical_action.py`
- **Constants**: Default influence value in `test_constants_usage.py`

**Missing Test Areas**:
- Planet exhaustion for influence spending
- Leadership strategy card influence mechanics
- Trade good to influence conversion
- Agenda phase voting with influence
- Influence spending validation

## Implementation Files
**Current Implementation**: ⚠️ PARTIAL

**Relevant Files**:
- `src/ti4/core/planet.py`: Planet class with influence property
- `tests/test_planet.py`: Basic planet influence tests
- `src/ti4/constants.py`: Default influence constants (inferred)

**Missing Components**:
- Planet card exhaustion system
- Influence spending mechanics
- Leadership strategy card influence abilities
- Trade good to influence conversion
- Agenda phase voting system

## Notable Implementation Details

### Current Planet System
- Planet class has influence property
- Influence values properly stored and accessible
- Basic planet creation with influence values works
- No exhaustion or spending mechanics

### Missing Influence Mechanics
- No planet card exhaustion system
- No influence spending validation
- No Leadership strategy card implementation
- No agenda phase voting system
- No trade good conversion mechanics

### Test Coverage Gaps
- Extensive use of influence values in tests but no spending tests
- No exhaustion mechanics tested
- No strategy card integration tested

## Action Items

### High Priority
1. **Implement Planet Exhaustion System**
   - Add exhausted/readied state to planet cards
   - Implement exhaustion mechanics for spending
   - Add validation for exhausted planet usage

2. **Implement Influence Spending**
   - Create influence spending validation system
   - Add Leadership strategy card influence mechanics
   - Implement command token gain from influence

### Medium Priority
3. **Trade Good Integration**
   - Implement trade good to influence conversion
   - Add spending validation (no voting with trade goods)
   - Create unified influence spending system

4. **Agenda Phase Integration**
   - Implement influence-based voting mechanics
   - Add vote calculation from planet influence
   - Validate trade good restrictions for voting

### Low Priority
5. **Enhanced Testing**
   - Add comprehensive influence spending tests
   - Test planet exhaustion mechanics
   - Test Leadership strategy card integration
   - Test agenda phase voting scenarios

## Priority Assessment
**Overall Priority**: 🟠 HIGH

**Rationale**:
- Influence is fundamental to command token economy
- Leadership strategy card is core gameplay mechanic
- Agenda phase voting requires influence system
- Planet exhaustion affects multiple game systems

**Implementation Effort**: MEDIUM
- Basic influence values already exist
- Need to add exhaustion and spending systems
- Integration with strategy cards and agenda phase
- Moderate complexity for trade good conversion

**Dependencies**: Multiple systems need coordination (strategy cards, agenda phase, trade goods)