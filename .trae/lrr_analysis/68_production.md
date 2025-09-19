# Rule 68: PRODUCTION (UNIT ABILITY)

## Category Overview
**Priority**: High  
**Implementation Status**: ✅ **COMPLETE**  
**Test Coverage**: ✅ **COMPLETE** (25 tests, 98% coverage) 

Production ability mechanics are fundamental to unit production during tactical actions. This rule defines how production values work, placement restrictions, and special cases for different unit types.

**Implementation Priority**: High - Core game layer rule that integrates with existing production system (Rule 67) and space dock mechanics (Rule 79).

## Sub-Rules Analysis

### 68.0 - Production Ability Definition
**Raw LRR Text**: "During the 'Production' step of a tactical action, the active player can resolve the 'Production' ability of each of their units that are in the active system to produce units."

**Implementation Status**: ✅ **COMPLETE**  
**Priority**: High  
**Details**: Core production ability mechanics during tactical action production step. Integration with existing tactical action system.

### 68.1 - Production Value and Limits
**Raw LRR Text**: "A unit's 'Production' ability, which is presented on a faction sheet or unit upgrade technology card, is always followed by a value. This value is the maximum number of units that this unit can produce."

**Implementation Status**: ✅ **COMPLETE**  
**Priority**: High  
**Details**: Production value mechanics and unit production limits. Integration with UnitStats system.

### 68.1a - Combined Production Values
**Raw LRR Text**: "If the active player has multiple units in the active system that have the 'Production' ability, that player can produce a number of units up to the combined total of their units' production values in that system."

**Implementation Status**: 🔄 **PENDING**  
**Priority**: High  
**Details**: Multiple production units combine their values. System-wide production calculation.

### 68.1b - Fighter/Infantry Production Counting
**Raw LRR Text**: "When producing fighters or infantry, each individual unit counts toward the producing unit's production limit."

**Implementation Status**: 🔄 **PENDING**  
**Priority**: High  
**Details**: Fighter and infantry tokens count individually against production limits, not as pairs.

### 68.1c - Partial Fighter/Infantry Production
**Raw LRR Text**: "A player can choose to produce one fighter or infantry instead of two, but must still pay the entire cost."

**Implementation Status**: 🔄 **PENDING**  
**Priority**: Medium  
**Details**: Optional partial production with full cost payment for fighters/infantry.

### 68.1d - Arborec Space Dock Restriction
**Raw LRR Text**: "'Production' value from Arborec space docks cannot be used to produce infantry, even if the Arborec player controls other units that have 'Production' in the same system."

**Implementation Status**: 🔄 **PENDING**  
**Priority**: Low  
**Details**: Faction-specific production restriction for Arborec space docks.

### 68.2 - Ship Production Placement
**Raw LRR Text**: "When a player produces ships by using 'Production,' that player must place them in the active system."

**Implementation Status**: 🔄 **PENDING**  
**Priority**: High  
**Details**: Ships produced via production must be placed in the active system space area.

### 68.3 - Ground Force Production Placement
**Raw LRR Text**: "When a player produces ground forces, that player must place those unit on planets that contain a unit that used its 'Production' ability."

**Implementation Status**: 🔄 **PENDING**  
**Priority**: High  
**Details**: Ground forces must be placed on planets with production units.

### 68.4 - Space Area Production Options
**Raw LRR Text**: "If a player uses the 'Production' ability of a unit in a space area of a system to produce ground forces, those ground forces may either be placed on a planet the player controls in that system or in the space area of that system."

**Implementation Status**: 🔄 **PENDING**  
**Priority**: High  
**Details**: Space-based production units can place ground forces on controlled planets or in space.

## Related Rules
- Rule 67: Producing Units
- Rule 79: Space Dock
- Rule 14: Blockaded (production blockade mechanics)
- Rule 76: Ships (ship production validation)

## Test References
- ✅ `tests/test_rule_68_production.py`: **COMPLETE** (25 tests, 98% coverage)

## Implementation Files
- ✅ `src/ti4/core/production_ability.py`: **COMPLETE**
- ✅ `tests/test_rule_68_production.py`: **COMPLETE**

## Implementation Plan

### Phase 1: Production Ability System
1. **Production Value System** - Unit production values and limits
2. **Combined Production** - Multiple units combining production values
3. **Unit Integration** - Integration with existing Unit and UnitStats systems

### Phase 2: Production Counting and Limits
1. **Fighter/Infantry Counting** - Individual unit counting for production limits
2. **Partial Production** - Optional partial fighter/infantry production
3. **Production Validation** - Validate production against limits

### Phase 3: Placement Rules
1. **Ship Placement** - Ships must be placed in active system
2. **Ground Force Placement** - Ground forces on planets with production units
3. **Space Area Production** - Special placement rules for space-based production

### Phase 4: Special Cases and Integration
1. **Faction Restrictions** - Arborec space dock infantry restriction
2. **Blockade Integration** - Production blockade mechanics
3. **Tactical Action Integration** - Integration with tactical action system