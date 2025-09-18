# Rule 48: MECHS

## Category Overview
**Rule Type**: Core Mechanics - Unit Type  
**Complexity**: Medium  
**Dependencies**: High (Ground Forces, Production, Deploy, Leaders)  
**Implementation Priority**: Medium

## Raw LRR Text
```
55 MECHS	
Mechs are unique, faction-specific heavy ground forces.

55.1 Mechs are a type of ground force and can be transported and participate in ground combat.

55.2 Each player begins with their mech unit card in play on their leader sheet and can produce mechs for the cost presented on the card.

55.3 Some mechs have "Deploy" abilities which allow a player to place them on the game board without producing them normally.

55.4 Mech unit cards are not technologies.

RELATED TOPICS: Deploy, Ground Combat, Ground Forces, Producing Units, Units
```

## Sub-Rules Analysis

### 55.1 - Mech as Ground Force
- **Status**: ✅ Partially Implemented
- **Description**: Mechs are ground forces that can be transported and participate in ground combat
- **Implementation**: Basic mech unit type exists with ground force properties
- **Priority**: High

### 55.2 - Mech Unit Cards and Production
- **Status**: ❌ Not Implemented
- **Description**: Players start with mech unit card on leader sheet, can produce for cost
- **Implementation Need**: 
  - Mech unit card system on leader sheet
  - Production cost system for mechs
  - Starting mech card placement
- **Priority**: High

### 55.3 - Deploy Abilities
- **Status**: ✅ Partially Implemented
- **Description**: Some mechs have Deploy abilities for special placement
- **Implementation**: Deploy ability exists and is tested for mechs
- **Priority**: Medium

### 55.4 - Mechs Not Technologies
- **Status**: ✅ Implemented
- **Description**: Mech unit cards are distinct from technology cards
- **Implementation**: Mechs handled separately from technology system
- **Priority**: Low

## Related Topics
- **Deploy (30)**: Special placement abilities for mechs
- **Ground Combat (42)**: Combat mechanics involving mechs
- **Ground Forces (43)**: General ground force mechanics
- **Producing Units (67)**: Unit production system
- **Units (96)**: General unit mechanics
- **Leader Sheet (50)**: Where mech unit cards are placed

## Dependencies
- Ground force system must be implemented
- Production system for unit creation
- Leader sheet system for mech card placement
- Deploy ability system
- Combat system for ground combat participation

## Test References
**Current Test Coverage**: ✅ Partial Coverage
- `test_unit.py`: Tests for mech abilities (sustain damage, deploy)
- Mech unit creation and ability verification
- Deploy ability testing specifically for mechs

**Test Coverage Details**:
```python
# From test_unit.py
mech = Unit(unit_type="mech", owner="player1")
assert mech.has_sustain_damage() is True
assert mech.has_deploy() is True
assert mech.has_bombardment() is False
```

**Missing Test Areas**:
- Mech unit card system on leader sheet
- Mech production cost mechanics
- Faction-specific mech abilities
- Mech participation in ground combat
- Transport mechanics for mechs

## Implementation Files
**Core Files**:
- `src/ti4/core/unit.py` - Basic mech unit implementation
- `tests/test_unit.py` - Mech ability testing

**Implementation Status**:
- ✅ Basic mech unit type with abilities (sustain damage, deploy)
- ❌ Mech unit card system
- ❌ Leader sheet integration
- ❌ Production cost system for mechs
- ❌ Faction-specific mech variations

## Notable Implementation Details

### Current Mech Implementation
- Mech units have sustain damage ability
- Mech units have deploy ability
- Basic unit creation and ability testing
- Proper identification as ground forces

### Key Implementation Gaps
1. **Mech Unit Cards**: No system for mech unit cards on leader sheet
2. **Production Costs**: No specific production cost system for mechs
3. **Faction Specificity**: No faction-specific mech variations
4. **Leader Sheet Integration**: No connection between mechs and leader sheet

### Unit Ability Matrix (From Documentation)
```
| Unit Type | Sustain Damage | Deploy | Bombardment | Space Cannon | Planetary Shield |
|-----------|:--------------:|:------:|:-----------:|:------------:|:----------------:|
| Mech      |       ✅       |   ✅   |     ❌      |      ❌      |        ❌        |
```

## Action Items

### High Priority
1. **Implement Mech Unit Card System**
   - Create mech unit card data structure
   - Integrate with leader sheet system
   - Add starting mech card placement during setup

2. **Add Mech Production System**
   - Implement production cost system for mechs
   - Connect to general unit production mechanics
   - Add cost validation and resource spending

### Medium Priority
3. **Enhance Faction-Specific Mechs**
   - Add faction-specific mech abilities
   - Implement unique mech characteristics per faction
   - Add faction-specific mech unit cards

4. **Improve Ground Combat Integration**
   - Ensure mechs participate properly in ground combat
   - Test mech combat abilities (sustain damage)
   - Add transport mechanics for mechs

### Low Priority
5. **Add Comprehensive Testing**
   - Test mech unit card system
   - Test production cost mechanics
   - Test faction-specific mech abilities
   - Test ground combat participation

## Priority Assessment
**Overall Priority**: Medium
- Mechs are important faction-specific units but not core to basic gameplay
- Current implementation covers basic unit mechanics
- Missing systems (unit cards, production costs) are important for complete experience
- Deploy abilities already implemented provide key mech functionality

**Implementation Complexity**: Medium
- Requires integration with leader sheet system
- Production cost system needs development
- Faction-specific variations add complexity
- Ground combat integration mostly exists

**Dependencies**: High
- Depends on leader sheet system implementation
- Requires production system enhancements
- Needs faction system for unique abilities
- Ground combat system integration required