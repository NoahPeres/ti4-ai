# Rule 37: FLEET POOL - Analysis

## Category Overview
**Rule Type:** Core Resource Management  
**Priority:** HIGH  
**Status:** WELL IMPLEMENTED  
**Complexity:** Medium  

## Raw LRR Text
```
37 FLEET POOL
The fleet pool is an area of a player's command sheet.

37.1 The number of command tokens in a player's fleet pool indicates the maximum number of non-fighter ships that a player can have in a system.
a Units that are on planets or that count against a player's capacity do not count against that player's fleet pool.
b Units that are being transported through systems do not count against a player's fleet pool in those systems.

37.2 Players place command tokens in their fleet pools with the ship silhouette faceup.

37.3 If at any time the number of a player's non-fighter ships in a system exceeds the number of tokens in that player's fleet pool, they choose and remove excess ships in that system, returning those units to their reinforcements.

37.4 Players do not spend command tokens from this pool unless a game effect specifically allows it.

RELATED TOPICS: Capacity, Command Sheet, Command Tokens, Ships, System Tiles
```

## Sub-Rules Analysis

### 37.1 Fleet Pool Limit System
- **Status:** WELL IMPLEMENTED
- **Description:** Command tokens in fleet pool limit non-fighter ships per system
- **Implementation:** Fleet supply validation system exists with proper exclusions

### 37.2 Token Placement Orientation
- **Status:** NOT IMPLEMENTED
- **Description:** Fleet pool tokens placed with ship silhouette faceup
- **Gap:** No token orientation tracking or visual representation

### 37.3 Excess Ship Removal
- **Status:** PARTIALLY IMPLEMENTED
- **Description:** Automatic removal of excess ships when fleet pool exceeded
- **Gap:** Validation exists but automatic removal system not fully implemented

### 37.4 Fleet Pool Token Spending Restriction
- **Status:** NOT IMPLEMENTED
- **Description:** Fleet pool tokens cannot be spent unless specifically allowed
- **Gap:** No spending restriction enforcement or game effect validation

## Related Topics
- Capacity
- Command Sheet
- Command Tokens
- Ships
- System Tiles

## Dependencies
- Command token system
- Command sheet management
- Ship unit system
- System validation
- Reinforcement pool management
- Fleet capacity validation
- Unit removal mechanics
- Game effect validation system

## Test References

### Existing Tests
- Comprehensive fleet supply validation tests
- Fleet capacity management tests
- Fleet pool limit enforcement tests
- Fighter II fleet supply requirements
- Non-fighter ship counting tests
- Fleet supply within/exceeding limits tests

### Missing Tests
- Token orientation (ship silhouette) tests
- Automatic excess ship removal tests
- Fleet pool token spending restriction tests
- Game effect override for token spending
- Transport exclusion from fleet pool tests
- Planet-based unit exclusion tests

## Implementation Files

### Core Implementation
- <mcfile name="fleet.py" path="/Users/noahperes/Developer/Code/kiro_test/ti4_ai/src/ti4/core/fleet.py"></mcfile> - Fleet management and validation
- <mcfile name="exceptions.py" path="/Users/noahperes/Developer/Code/kiro_test/ti4_ai/src/ti4/core/exceptions.py"></mcfile> - Fleet supply error handling
- <mcfile name="test_fleet_management.py" path="/Users/noahperes/Developer/Code/kiro_test/ti4_ai/tests/test_fleet_management.py"></mcfile> - Comprehensive fleet tests

### Missing Implementation
- Command sheet visual representation
- Token orientation tracking
- Automatic ship removal system
- Fleet pool token spending restrictions
- Game effect validation for token spending
- Transport system integration

## Notable Implementation Details

### Well Implemented
- <mcsymbol name="FleetCapacityValidator" filename="fleet.py" path="/Users/noahperes/Developer/Code/kiro_test/ti4_ai/src/ti4/core/fleet.py" startline="67" type="class"></mcsymbol> - Comprehensive fleet validation
- <mcsymbol name="is_fleet_supply_valid" filename="fleet.py" path="/Users/noahperes/Developer/Code/kiro_test/ti4_ai/src/ti4/core/fleet.py" startline="82" type="function"></mcsymbol> - Fleet supply limit checking
- <mcsymbol name="requires_fleet_supply" filename="fleet.py" path="/Users/noahperes/Developer/Code/kiro_test/ti4_ai/src/ti4/core/fleet.py" startline="63" type="function"></mcsymbol> - Fleet supply requirement detection
- Fighter vs non-fighter ship distinction
- Fleet pool token limit enforcement
- Comprehensive test coverage for core mechanics

### Gaps and Issues
- No visual command sheet representation
- Missing token orientation tracking
- No automatic excess ship removal
- Missing fleet pool token spending restrictions
- No game effect validation system
- Transport system not integrated with fleet pool rules

## Action Items

1. **Implement command sheet visual system** - Create command sheet representation with fleet pool area
2. **Add token orientation tracking** - Track ship silhouette orientation for fleet pool tokens
3. **Create automatic ship removal system** - Implement excess ship removal when fleet pool exceeded
4. **Add fleet pool spending restrictions** - Prevent token spending unless game effect allows
5. **Implement game effect validation** - System to validate when fleet pool tokens can be spent
6. **Integrate transport system** - Exclude transported units from fleet pool counting
7. **Add planet unit exclusion** - Ensure planet-based units don't count against fleet pool
8. **Create command sheet UI** - Visual representation of command sheet with pools
9. **Implement token management interface** - UI for managing command tokens in pools
10. **Add comprehensive integration tests** - Test fleet pool with transport and planet systems

## Priority Assessment
**HIGH** - Core resource management system that's mostly well implemented. The fleet supply validation is excellent, but missing some UI and automatic enforcement features. Critical for proper game flow and resource management.