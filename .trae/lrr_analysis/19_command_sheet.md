# Rule 19: COMMAND SHEET

## Category Overview
**Priority**: HIGH  
**Implementation Status**: PARTIALLY IMPLEMENTED  
**Complexity**: MEDIUM  

Rule 19 defines the command sheet structure and its components: strategy pool, tactic pool, fleet pool, trade good area, and quick reference. This is a fundamental player resource management system.

## Raw LRR Text

### 19 COMMAND SHEET
Each player has a command sheet that contains a strategy pool, a tactic pool, a fleet pool, a trade good area, and a quick reference.

**19.1** The pools on the command sheet are where players place their command tokens. Command tokens in a player's pools are used by that player to perform strategic and tactical actions and to increase the number of ships that player can have in each system.

**19.2** The trade good area on the command sheet is where a player places their trade good tokens; trade tokens in a player's trade good area can be spent by that player as resources, influence, or to resolve certain game effects that require trade goods.

**19.3** Players who are familiar with the game can hide the quick reference by placing that portion of the command sheet under their faction sheets.

## Sub-Rules Analysis

### 19.0 - Command Sheet Structure
- **Status**: PARTIALLY IMPLEMENTED
- **Description**: Command sheet with five areas: strategy pool, tactic pool, fleet pool, trade good area, quick reference
- **Implementation**: Basic structure exists but not fully modeled

### 19.1 - Command Token Pools
- **Status**: PARTIALLY IMPLEMENTED
- **Description**: Three pools for command tokens with specific uses
- **Implementation**: Constants defined, fleet pool validation exists, but no complete pool management

### 19.2 - Trade Good Area
- **Status**: PARTIALLY IMPLEMENTED
- **Description**: Area for trade good tokens that can be spent as resources/influence
- **Implementation**: Trade goods exist in player resources but no dedicated area modeling

### 19.3 - Quick Reference
- **Status**: NOT IMPLEMENTED
- **Description**: Hideable quick reference section
- **Implementation Needed**: UI component for quick reference display/hiding

## Related Topics
- Command Tokens
- Fleet Pool
- Strategic Action
- Tactical Action
- Trade Goods

## Dependencies
- **Command Token System**: Token management and pool allocation
- **Player Resource System**: Integration with player resources
- **Trade Good System**: Trade good token management
- **Action System**: Strategic and tactical action integration
- **UI System**: Command sheet display and interaction

## Test References

### Existing Tests
- `test_fleet_management.py` - Fleet pool token validation
  - `test_validate_fleet_supply_limit()` - Fleet token limits
  - `test_validate_fleet_supply_within_limit()` - Fleet token validation
- `test_scenario_library.py` - Command token resource management
- `test_integration_with_builder.py` - Player resource setup with command tokens
- `test_game_scenario_builder.py` - Command token initialization

### Missing Tests Needed
- `test_command_sheet_structure.py` - Command sheet component validation
- `test_command_token_pools.py` - Pool management and token allocation
- `test_trade_good_area.py` - Trade good area functionality
- `test_quick_reference.py` - Quick reference display/hiding
- `test_command_sheet_integration.py` - Integration with actions and resources

## Implementation Files

### Existing Files
- `src/ti4/core/constants.py` - Command token starting values
  - `STARTING_TACTIC_TOKENS = 3`
  - `STARTING_FLEET_TOKENS = 3`
  - `STARTING_STRATEGY_TOKENS = 2`
- `src/ti4/core/fleet.py` - Fleet pool concept mentioned
- `src/ti4/actions/tactical_action.py` - Tactical action framework
- `tests/test_fleet_management.py` - Fleet pool validation

### Missing Files Needed
- `src/ti4/core/command_sheet.py` - Command sheet data structure
- `src/ti4/core/command_token_pools.py` - Pool management system
- `src/ti4/ui/command_sheet_display.py` - Command sheet UI component
- `src/ti4/mechanics/trade_good_area.py` - Trade good area management

## Notable Implementation Details

### Well-Implemented Areas
1. **Fleet Pool Validation** - Fleet supply limits properly enforced
2. **Command Token Constants** - Starting token counts defined correctly
3. **Resource Integration** - Command tokens tracked in player resources
4. **Test Coverage** - Good coverage for fleet pool mechanics

### Implementation Gaps
1. **Command Sheet Structure** - No unified command sheet data model
2. **Pool Management** - No system for moving tokens between pools
3. **Trade Good Area** - No dedicated trade good area implementation
4. **Quick Reference** - No quick reference system
5. **UI Integration** - No command sheet display components

### Integration Points
- **Tactical Actions**: Use tactic pool tokens for system activation
- **Strategic Actions**: Use strategy pool tokens for secondary abilities
- **Fleet Management**: Fleet pool tokens limit ship deployment
- **Resource Management**: Trade good area integrates with player resources

## Action Items

1. **Create Command Sheet Data Model** - Unified structure for all command sheet components
2. **Implement Pool Management System** - Token allocation and movement between pools
3. **Create Trade Good Area Component** - Dedicated trade good token management
4. **Add Quick Reference System** - Hideable reference display functionality
5. **Build Command Sheet UI** - Visual representation of command sheet
6. **Integrate with Action System** - Connect pools to tactical/strategic actions
7. **Add Pool Validation** - Ensure proper token limits and allocation
8. **Create Command Sheet Tests** - Comprehensive testing for all components
9. **Add Token Movement Mechanics** - System for gaining and spending tokens
10. **Document Command Sheet API** - Clear interface for command sheet operations