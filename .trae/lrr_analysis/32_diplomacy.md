# Rule 32: DIPLOMACY (STRATEGY CARD) - Analysis

## Category Overview
**Rule Type:** Strategy Card Mechanic
**Priority:** MEDIUM
**Status:** COMPLETED ✅
**Complexity:** Medium-High

## Raw LRR Text
```
32 DIPLOMACY (STRATEGY CARD)
The "Diplomacy" strategy card can be used to preemptively prevent other players from activating a specific system. It can also be used to ready planets. This card's initiative value is "2."

32.1 During the action phase, if the active player has the "Diplomacy" strategy card, they can perform a strategic action to resolve that card's primary ability.

32.2 To resolve the primary ability on the "Diplomacy" strategy card, the active player chooses a system that contains a planet they control other than the Mecatol Rex system; each other player places one command token from their reinforcements in that system. Then, the active player readies any two of their exhausted planets.
a If a player has no command tokens in their reinforcements, that player places one command token of their choice from their command sheet.
b If a player already has a command token in the chosen system, they do not place a command token there.

32.3 After the active player resolves the primary ability of the "Diplomacy" strategy card, each other player, beginning with the player to the left of the active player and proceeding clockwise, may spend one command token from their strategy pool to ready up to two exhausted planets they control.

RELATED TOPICS: Active System, Command Tokens, Initiative Order, Planets, Readied, Strategic Action, Strategy Card
```

## Sub-Rules Analysis

### 32.1 Strategic Action Trigger
- **Status:** IMPLEMENTED ✅
- **Description:** Basic strategic action framework for Diplomacy card
- **Implementation:** Found in `game_controller.py` with strategic action handling

### 32.2 Primary Ability Resolution
- **Status:** IMPLEMENTED ✅
- **Description:** System selection, command token placement, planet readying
- **Implementation:** Fully implemented in `DiplomacyStrategyCard.execute_primary_ability()`
- **Test Coverage:** `test_diplomacy_primary_ability_*` test cases

### 32.3 Secondary Ability Resolution
- **Status:** IMPLEMENTED ✅
- **Description:** Other players spending command tokens to ready planets
- **Implementation:** Fully implemented in `DiplomacyStrategyCard.execute_secondary_ability()`
- **Test Coverage:** `test_diplomacy_secondary_ability_*` test cases

## Implementation Details

### Test Cases Demonstrating Rule Implementation

1. **Primary Ability Tests:**
   - `test_diplomacy_primary_ability_system_selection_and_command_token_placement`: Validates system selection and command token placement mechanics
   - `test_diplomacy_primary_ability_requires_controlled_planet`: Ensures system must contain controlled planet
   - `test_diplomacy_primary_ability_requires_system_id`: Validates system_id parameter requirement
   - `test_diplomacy_primary_ability_requires_game_state`: Validates game_state parameter requirement
   - `test_diplomacy_primary_ability_invalid_system`: Handles invalid system scenarios

2. **Secondary Ability Tests:**
   - `test_diplomacy_secondary_ability_ready_planets`: Validates planet readying functionality
   - `test_diplomacy_secondary_ability_requires_strategy_token`: Ensures strategy token cost
   - `test_diplomacy_secondary_ability_max_two_planets`: Enforces maximum two planets limit
   - `test_diplomacy_secondary_ability_only_controlled_planets`: Validates player control requirement

3. **Card Properties Tests:**
   - `test_diplomacy_card_type`: Validates card type identification
   - `test_diplomacy_initiative_value`: Validates initiative value of 2

### Key Implementation Features

- **System Selection Validation:** Ensures selected system contains controlled planets (excluding Mecatol Rex)
- **Command Token Placement:** Places tokens from reinforcements or command sheet as per LRR 32.2.a
- **Duplicate Token Prevention:** Prevents placing tokens in systems already containing player tokens (LRR 32.2.b)
- **Planet Readying:** Implements both primary (2 planets) and secondary (up to 2 planets) readying
- **Strategy Token Cost:** Enforces strategy pool token cost for secondary ability
- **Player Control Validation:** Ensures only controlled planets can be readied

## Related Topics
- Active System
- Command Tokens
- Initiative Order
- Planets
- Readied
- Strategic Action
- Strategy Card

## Dependencies
- Strategy card system (basic framework exists)
- Command token management
- Planet control and readying mechanics
- System activation prevention
- Player turn order system
- Reinforcement pool management

## Test References

### Existing Tests
- `test_game_controller.py`: Strategy card selection, initiative order, strategic actions
- `test_integration_scenarios.py`: Strategy card selection in game flow
- Multiple tests for command token management
- Strategy card framework tests
- `test_rule_32_diplomacy.py`: Complete test coverage for Diplomacy strategy card including primary ability execution, command token placement, planet readying mechanics, secondary ability usage, and all edge cases

## Implementation Files

### Core Implementation
- `src/ti4/core/strategy_cards/cards/diplomacy.py`: Complete Diplomacy strategy card implementation
- `src/ti4/core/strategy_cards/base_strategy_card.py`: Base strategy card framework
- `src/ti4/core/game_controller.py`: Strategy card selection and strategic actions
- `src/ti4/core/command_sheet.py`: Command token management and spending APIs
- `tests/test_rule_32_diplomacy.py`: Comprehensive test coverage for all Diplomacy mechanics

## Notable Implementation Details

### Fully Implemented ✅
- Complete Diplomacy strategy card with primary and secondary abilities
- System selection with Mecatol Rex restriction enforcement
- Command token placement from reinforcements or command sheet
- Planet readying mechanics for both primary (2 planets) and secondary (up to 2 planets) abilities
- Strategy token spending validation using proper APIs
- Player control validation for planets and systems
- Comprehensive test coverage including edge cases
- Error handling for invalid scenarios (double exhaustion, already ready planets, etc.)

## Priority Assessment
**COMPLETED** ✅ - All Diplomacy strategy card functionality has been fully implemented and tested. The implementation correctly handles all LRR rules including system selection, command token placement, planet readying, and secondary ability mechanics.
