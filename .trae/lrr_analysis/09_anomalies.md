# LRR Rule Analysis: Section 9 - ANOMALIES

## Category Overview
Anomalies are special system tiles with unique rules that affect movement and gameplay. There are four types: asteroid fields, nebulae, supernovas, and gravity rifts. Each anomaly type has distinct effects on ship movement and combat, and some may contain planets while still maintaining their anomaly properties.

## Sub-Rules Analysis

### 9.1 Anomaly Identification 🟡 MEDIUM
**Raw LRR Text**: "An anomaly is identified by a red border located on the tile's corners."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No anomaly identification system
- **Tests**: No anomaly identification tests
- **Assessment**: Visual identification system not implemented
- **Priority**: MEDIUM
- **Dependencies**: Requires system tile visual properties and anomaly type system
- **Notes**: Red border is the visual indicator for anomaly tiles

### 9.2 Anomaly Types 🔴 HIGH
**Raw LRR Text**: "There are four types of anomalies: asteroid fields, nebulae, supernovas, and gravity rifts."

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Basic anomaly rule stub exists in `movement_rules.py`
- **Tests**: No specific anomaly type tests
- **Assessment**: Framework exists but specific anomaly types not implemented
- **Priority**: HIGH
- **Dependencies**: Requires individual anomaly type implementations
- **Notes**: Four distinct anomaly types with different effects

### 9.2a Anomalies with Planets 🟡 MEDIUM
**Raw LRR Text**: "Some anomalies contain planets; those systems are still anomalies."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No planet-anomaly combination system
- **Tests**: No tests for anomalies with planets
- **Assessment**: Dual nature systems (anomaly + planets) not handled
- **Priority**: MEDIUM
- **Dependencies**: Requires system tile properties and planet system integration
- **Notes**: Systems can be both anomalies and contain planets simultaneously

### 9.3 Anomaly Art Identification 🟢 LOW
**Raw LRR Text**: "Each type of anomaly is identified by its art, as follows: [Asteroid Field, Supernova, Nebula, Gravity Rift artwork descriptions]"

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No artwork identification system
- **Tests**: No art-based identification tests
- **Assessment**: Visual art identification not implemented
- **Priority**: LOW
- **Dependencies**: Requires asset management and visual identification system
- **Notes**: Each anomaly has distinct artwork for identification

### 9.4 Ability-Created Anomalies 🟡 MEDIUM
**Raw LRR Text**: "Abilities can cause a system tile to become an anomaly; that system tile is an anomaly in addition to its other properties."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No dynamic anomaly creation system
- **Tests**: No ability-created anomaly tests
- **Assessment**: Dynamic anomaly transformation not implemented
- **Priority**: MEDIUM
- **Dependencies**: Requires ability system and system property modification
- **Notes**: Systems can gain anomaly properties through game effects

### 9.5 Multiple Anomaly Types 🟡 MEDIUM
**Raw LRR Text**: "Abilities can cause a system to be two different anomalies; that system has the properties of both anomalies."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No multiple anomaly type system
- **Tests**: No multiple anomaly tests
- **Assessment**: Stacking anomaly effects not implemented
- **Priority**: MEDIUM
- **Dependencies**: Requires anomaly effect stacking and combination rules
- **Notes**: Systems can have multiple anomaly types simultaneously

## Related Anomaly Types (Cross-References)

### Asteroid Field (Rule 11) 🔴 HIGH
**Effect**: "A ship cannot move through or into an asteroid field."
- **Implementation Status**: ❌ NOT IMPLEMENTED
- **Priority**: HIGH - Blocks all movement
- **Dependencies**: Movement validation system

### Nebula (Rule 59) 🔴 HIGH
**Effects**: 
- Ships can only move into nebula if it's the active system
- Ships in nebula have move value of 1
- Defender gets +1 to combat rolls in nebula
- **Implementation Status**: ❌ NOT IMPLEMENTED
- **Priority**: HIGH - Affects movement and combat
- **Dependencies**: Movement rules and combat system

### Supernova (Rule 86) 🔴 HIGH
**Effect**: "A ship cannot move through or into a supernova."
- **Implementation Status**: ❌ NOT IMPLEMENTED
- **Priority**: HIGH - Blocks all movement
- **Dependencies**: Movement validation system

### Gravity Rift (Rule 41) 🔴 HIGH
**Effects**:
- Ships moving out/through get +1 move value
- Roll die when exiting: 1-3 destroys ship
- Can affect same ship multiple times
- **Implementation Status**: ❌ NOT IMPLEMENTED
- **Priority**: HIGH - Affects movement and unit survival
- **Dependencies**: Movement rules and unit destruction system

## Dependencies Summary

### Critical Dependencies
- **System Tile System**: Base system for anomaly properties (Rule 88)
- **Movement System**: All anomalies affect movement in some way (Rule 58)
- **Combat System**: Nebulae affect combat rolls (Rule 78)
- **Ability System**: For dynamic anomaly creation (Rule 1)
- **Unit Destruction**: Gravity rifts can destroy units

### Related Systems
- **Planet System**: Some anomalies contain planets (Rule 64)
- **Active System**: Nebulae interact with active system rules (Rule 5)
- **Visual Assets**: Anomaly identification through artwork
- **Effect Stacking**: Multiple anomaly types on same system
- **Property Modification**: Dynamic anomaly assignment

## Test References
- **Movement Rules**: Basic `AnomalyRule` stub in `movement_rules.py`
- **No Anomaly Tests**: No specific tests found for any anomaly type
- **No Movement Restriction Tests**: No tests for anomaly movement blocking
- **No Combat Effect Tests**: No tests for nebula combat bonuses

## Action Items
1. **Implement core anomaly system** with four anomaly types
2. **Create movement restriction validation** for asteroid fields and supernovas
3. **Implement nebula movement rules** (active system only, move value 1)
4. **Add nebula combat effects** (+1 defender bonus)
5. **Implement gravity rift mechanics** (movement bonus and destruction risk)
6. **Create dynamic anomaly assignment** system for abilities
7. **Add anomaly stacking support** for multiple types per system
8. **Integrate with planet system** for anomalies containing planets
9. **Add comprehensive test suite** for all anomaly types and interactions
10. **Implement visual identification** system for anomaly recognition