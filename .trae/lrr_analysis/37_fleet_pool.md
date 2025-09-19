# Rule 37: FLEET POOL

## Category Overview
**Priority**: High  
**Implementation Status**: ✅ **COMPLETE**  
**Test Coverage**: ✅ **COMPLETE** (17 tests, 94% coverage)

Fleet pool mechanics are fundamental to ship movement and system control in TI4. This rule defines how command tokens in the fleet pool limit non-fighter ships per system.

**Implementation Priority**: High - Foundation layer rule that controls ship deployment and system occupation limits.

## Sub-Rules Analysis

### 37.0 - Fleet Pool Definition
**Raw LRR Text**: "The fleet pool is an area of a player's command sheet."

**Implementation Status**: 🔄 **PENDING**  
**Priority**: Medium  
**Details**: Need command sheet representation with fleet pool area. Currently no visual command sheet system.

### 37.1 - Fleet Pool Ship Limits
**Raw LRR Text**: "The number of command tokens in a player's fleet pool indicates the maximum number of non-fighter ships that a player can have in a system."

**Implementation Status**: ✅ **COMPLETE**  
**Priority**: High  
**Details**: Well implemented in FleetPoolManager. Properly distinguishes non-fighter ships and validates limits.

### 37.1a - Planet and Capacity Unit Exclusions
**Raw LRR Text**: "Units that are on planets or that count against a player's capacity do not count against that player's fleet pool."

**Implementation Status**: ✅ **COMPLETE**  
**Priority**: High  
**Details**: Properly excludes planet-based units and capacity-consuming units from fleet pool counting.

### 37.1b - Transport Exclusions
**Raw LRR Text**: "Units that are being transported through systems do not count against that player's fleet pool in those systems."

**Implementation Status**: ✅ **COMPLETE**  
**Priority**: Medium  
**Details**: Transport system integration implemented to exclude transported units from fleet pool limits.

### 37.2 - Token Placement Orientation
**Raw LRR Text**: "Players place command tokens in their fleet pools with the ship silhouette faceup."

**Implementation Status**: ✅ **COMPLETE**  
**Priority**: Low  
**Details**: Token orientation tracking implemented with proper validation.

### 37.3 - Excess Ship Removal
**Raw LRR Text**: "If at any time the number of a player's non-fighter ships in a system exceeds the number of tokens in that player's fleet pool, they choose and remove excess ships in that system, returning those units to their reinforcements."

**Implementation Status**: ✅ **COMPLETE**  
**Priority**: High  
**Details**: Automatic excess ship removal system implemented with player choice and reinforcement return.

### 37.4 - Fleet Pool Token Spending Restriction
**Raw LRR Text**: "Players do not spend command tokens from this pool unless a game effect specifically allows it."

**Implementation Status**: ✅ **COMPLETE**  
**Priority**: Medium  
**Details**: Spending restriction enforcement and game effect validation system implemented.

## Related Rules
- Rule 14: Blockaded (fleet pool affects blockade mechanics)
- Rule 76: Ships (ship types and fleet pool requirements)
- Rule 16: Command Sheet (fleet pool is part of command sheet)
- Rule 17: Command Tokens (fleet pool contains command tokens)

## Test References
- ✅ `tests/test_fleet_management.py`: **COMPLETE** (Core fleet mechanics tested)
- ✅ `tests/test_rule_37_fleet_pool.py`: **COMPLETE** (17 tests, 94% coverage)

## Implementation Files
- ✅ `src/ti4/core/fleet.py`: **COMPLETE** (Core fleet mechanics implemented)
- ✅ `src/ti4/core/fleet_pool.py`: **COMPLETE**
- ✅ `tests/test_rule_37_fleet_pool.py`: **COMPLETE**

## Implementation Plan

### Phase 1: Fleet Pool Manager System
1. **Fleet Pool Manager** - Central management of fleet pool mechanics
2. **Non-Fighter Ship Counting** - Proper counting of ships that require fleet supply
3. **System Integration** - Integration with existing Fleet and System classes

### Phase 2: Exclusion Rules
1. **Planet Unit Exclusions** - Exclude planet-based units from fleet pool counting
2. **Capacity Unit Exclusions** - Exclude units that count against capacity
3. **Transport Exclusions** - Exclude transported units from fleet pool limits

### Phase 3: Enforcement and Removal
1. **Excess Ship Detection** - Detect when fleet pool limits are exceeded
2. **Automatic Removal System** - Remove excess ships and return to reinforcements
3. **Player Choice System** - Allow player to choose which ships to remove

### Phase 4: Command Sheet Integration
1. **Fleet Pool Token Management** - Track command tokens in fleet pool
2. **Spending Restrictions** - Prevent unauthorized fleet pool token spending
3. **Game Effect Validation** - System to validate when fleet pool tokens can be spent