# Rule 65: PLANETARY SHIELD (UNIT ABILITY)

## Category Overview
**Rule Type**: Unit Ability  
**Complexity**: Medium  
**Dependencies**: Bombardment, Unit Abilities, L1Z1X Harrow, X-89 Bacterial Weapon, War Sun, Magen Defense Grid  

## Raw LRR Text
```
65 PLANETARY SHIELD (UNIT ABILITY)	
Units cannot use the "Bombardment" ability against a planet that contains a unit that has the "Planetary Shield" ability.
65.1 The "Planetary Shield" ability does not prevent a planet from being affected by the "X-89 Bacterial Weapon" technology.
65.2 The "Planetary Shield" ability prevents an L1Z1X player from using their "Harrow" faction ability.
65.3 If a war sun is in a system with any number of other players' units that have the "Planetary Shield" ability, those units are treated as if they do not have that ability.
a	Units treated as if they do not have a "Planetary Shield" ability cannot use the "Magen Defense Grid" technology.
b  A war sun can use its "Bombardment" ability against planets that contain units that have the "Planetary Shield" ability.
RELATED TOPICS: Bombardment
```

## Sub-Rules Analysis

### 65.0 - Basic Bombardment Prevention ✅ IMPLEMENTED
**Status**: Implemented in unit ability system  
**Implementation**: PDS units have planetary_shield ability flag  
**Test Coverage**: Unit tests verify planetary shield ability detection  

### 65.1 - X-89 Bacterial Weapon Exception ❌ NOT IMPLEMENTED
**Status**: Not implemented  
**Implementation**: No X-89 Bacterial Weapon technology or exception handling  
**Test Coverage**: No tests for X-89 Bacterial Weapon interactions  

### 65.2 - L1Z1X Harrow Prevention ❌ NOT IMPLEMENTED
**Status**: Not implemented  
**Implementation**: No L1Z1X faction abilities or Harrow ability system  
**Test Coverage**: No tests for L1Z1X Harrow interactions  

### 65.3 - War Sun Override ❌ NOT IMPLEMENTED
**Status**: Not implemented  
**Implementation**: No war sun override mechanics for planetary shield  
**Test Coverage**: No tests for war sun bombardment override  

### 65.3a - Magen Defense Grid Restriction ❌ NOT IMPLEMENTED
**Status**: Not implemented  
**Implementation**: No Magen Defense Grid technology or restriction system  
**Test Coverage**: No tests for Magen Defense Grid interactions  

### 65.3b - War Sun Bombardment Override ❌ NOT IMPLEMENTED
**Status**: Not implemented  
**Implementation**: No bombardment system with war sun exceptions  
**Test Coverage**: No tests for war sun bombardment mechanics  

## Related Topics
- **Bombardment**: Core combat mechanic that planetary shield blocks
- **Unit Abilities**: Framework for special unit capabilities
- **L1Z1X Harrow**: Faction-specific ability affected by planetary shield
- **X-89 Bacterial Weapon**: Technology that bypasses planetary shield
- **War Sun**: Unit that overrides planetary shield protection
- **Magen Defense Grid**: Technology affected by war sun override
- **PDS**: Primary unit with planetary shield ability

## Test References

### Current Coverage
- `test_unit.py`: Basic planetary shield ability detection for PDS units
- Unit ability matrix validation for planetary shield presence
- Multiple ability testing including planetary shield on PDS

### Missing Test Scenarios
- Bombardment prevention mechanics
- X-89 Bacterial Weapon exception handling
- L1Z1X Harrow ability prevention
- War sun override of planetary shield
- Magen Defense Grid restriction when overridden
- Integration with bombardment combat system
- Planet-level protection validation

## Implementation Files

### Core Implementation
- `src/ti4/core/unit.py`: Basic planetary shield ability flag
- `src/ti4/core/unit_stats.py`: Planetary shield attribute definition
- Bombardment prevention system (not yet implemented)
- Technology exception system (not yet implemented)

### Supporting Systems
- Bombardment combat system integration
- Faction ability system (L1Z1X Harrow)
- Technology system (X-89 Bacterial Weapon, Magen Defense Grid)
- War sun override mechanics
- Planet protection validation system

## Notable Details

### Strengths
- Solid foundation for unit ability detection
- Comprehensive unit ability matrix implementation
- Good test coverage for basic ability presence
- Clear unit ability framework structure

### Areas Needing Attention
- **Bombardment Integration**: No actual bombardment prevention mechanics
- **Technology Exceptions**: Missing X-89 Bacterial Weapon and Magen Defense Grid
- **Faction Abilities**: No L1Z1X Harrow implementation
- **War Sun Override**: Missing war sun special bombardment rules
- **Combat Integration**: No integration with bombardment combat system
- **Planet Protection**: No planet-level protection validation

## Action Items
1. **HIGH**: Implement bombardment prevention mechanics for planetary shield
2. **HIGH**: Add war sun override system for planetary shield
3. **MEDIUM**: Implement X-89 Bacterial Weapon exception handling
4. **MEDIUM**: Add L1Z1X Harrow faction ability and prevention
5. **MEDIUM**: Implement Magen Defense Grid technology and restrictions
6. **MEDIUM**: Create planet-level protection validation system
7. **LOW**: Add comprehensive bombardment integration tests

## Priority Assessment
**Priority**: Medium  
**Implementation Status**: 20%  
**Rationale**: While the basic unit ability is implemented, the actual protective mechanics and all exceptions are missing. Planetary shield is important for defensive strategy but not as critical as core economic or movement systems.