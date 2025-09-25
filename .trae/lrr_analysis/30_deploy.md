# Rule 30: DEPLOY - Analysis

## Category Overview
**Rule Type:** Unit Abilities
**Priority:** MEDIUM-HIGH
**Implementation Status:** ✅ **COMPLETED**

## Raw LRR Text
```
30 DEPLOY
Some units have deploy abilities. Deploy abilities are indicated by the "Deploy" header and provide the means to place specific units on the game board without producing them as normal.

30.1 A player can use a unit's deploy ability when the ability's conditions are met to place that unit on the game board.
a A player does not have to spend resources to deploy a unit unless otherwise specified.

30.2 A player can only resolve a deploy ability to place a unit that is in their reinforcements.
a If there are no units that have a deploy ability in a player's reinforcements, the deploy ability cannot be used.

30.3 A unit's deploy ability can be resolved only once per timing window.

RELATED TOPICS: Abilities, Mechs, Reinforcements
```

## Sub-Rules Analysis

### 30.1 Deploy Ability Usage
**Status:** ✅ **COMPLETED**
**Implementation:** Player.deploy_unit() method with full validation
**Details:** Validates unit has deploy ability, planet control, and placement logic

### 30.1.a Resource-Free Deployment
**Status:** ✅ **COMPLETED**
**Implementation:** Deploy bypasses resource costs entirely
**Details:** No resource spending required for deploy abilities

### 30.2 Reinforcement Requirement
**Status:** ✅ **COMPLETED**
**Implementation:** Validates unit availability in reinforcements
**Details:** Checks specific unit type availability before deployment

### 30.2.a Availability Check
**Status:** ✅ **COMPLETED**
**Implementation:** Validates deployable units exist in reinforcements
**Details:** Raises ReinforcementError if no units with deploy ability available

### 30.3 Timing Window Restriction
**Status:** ✅ **COMPLETED**
**Implementation:** Player tracks timing windows and deploy usage
**Details:** Each deploy ability limited to once per timing window with advance_timing_window()

## Related Topics
- **Abilities:** General ability system framework
- **Mechs (Rule 55):** Primary units with deploy abilities
- **Reinforcements:** Unit pool management system

## Dependencies
- **Unit Abilities System:** Must support deploy ability detection
- **Reinforcements System:** Must track available units
- **Timing System:** Must track timing windows for ability usage
- **Resource System:** Must handle resource-free placement

## Test References

### Implemented Tests
- `tests/test_rule_30_deploy.py`: Complete deploy ability testing
  - `test_rule_30_1_deploy_ability_usage`: Basic deploy functionality
  - `test_rule_30_1a_no_resource_cost`: Resource-free deployment
  - `test_rule_30_2_reinforcement_requirement`: Reinforcement validation
  - `test_rule_30_2a_no_deploy_units_available`: Deployable unit availability check
  - `test_rule_30_3_timing_window_restriction`: Once per timing window restriction
  - `test_rule_30_3_timing_window_reset`: Timing window advancement
  - `test_deploy_ability_multiple_planets_same_system`: Multi-planet deployment

### Unit Ability Tests
- `test_unit.py`: Deploy ability detection
  - Lines 105-116: Basic deploy ability identification for mechs
  - Lines 232-233: Deploy ability verification in comprehensive tests

## Implementation Files

### Core Implementation
- `src/ti4/core/player.py`: Deploy ability system
  - `Player.deploy_unit()`: Main deployment method with full validation
  - `Player.advance_timing_window()`: Timing window management
  - `Player._timing_window_id`: Current timing window tracking
  - `Player._deploy_used_this_window`: Deploy usage tracking per window

### Supporting Implementation
- `src/ti4/core/unit.py`: Deploy ability detection
  - `Unit.has_deploy()`: Returns boolean for deploy capability
- `src/ti4/core/unit_stats.py`: Deploy ability flag
  - `UnitStats.deploy`: Boolean flag for deploy capability
  - Mech units have deploy=True in stats
- `src/ti4/core/reinforcements.py`: Unit availability validation
- `src/ti4/core/exceptions.py`: DeployError and ReinforcementError

## Notable Implementation Details

### Successfully Implemented
- **Deploy ability activation system** with full condition checking
- **Reinforcement validation logic** for unit availability
- **Timing window tracking** with once-per-window enforcement
- **Deploy placement mechanics** for planet-based deployment
- **Resource-free deployment** bypassing normal production costs
- **Comprehensive error handling** with specific exception types
- **Complete test coverage** for all rule aspects

### Key Features
- **Planet control validation:** Must control target planet to deploy
- **Unit type validation:** Only units with deploy ability can be deployed
- **Reinforcement checking:** Validates both specific unit and deployable unit availability
- **Timing window management:** Tracks and enforces deployment restrictions
- **Error messaging:** Clear feedback for deployment failures

## Test Case Coverage

The following test cases demonstrate complete Rule 30 implementation:

1. **test_rule_30_1_deploy_ability_usage**: Validates basic deploy functionality
2. **test_rule_30_1a_no_resource_cost**: Confirms resource-free deployment
3. **test_rule_30_2_reinforcement_requirement**: Tests reinforcement validation
4. **test_rule_30_2a_no_deploy_units_available**: Validates deployable unit availability
5. **test_rule_30_3_timing_window_restriction**: Enforces once-per-window limit
6. **test_rule_30_3_timing_window_reset**: Tests timing window advancement
7. **test_deploy_ability_multiple_planets_same_system**: Multi-planet scenarios

## Priority Assessment
**✅ COMPLETED** - Deploy abilities are fully implemented with:
- Complete rule compliance for all sub-rules (30.1, 30.1.a, 30.2, 30.2.a, 30.3)
- Comprehensive validation and error handling
- Full test coverage demonstrating correct behavior
- Integration with existing game systems (reinforcements, planets, units)
- Proper timing window management for strategic gameplay
