# Rule 32: DIPLOMACY (STRATEGY CARD) - Analysis

## Category Overview
**Rule Type:** Strategy Card Mechanic
**Priority:** MEDIUM
**Status:** PARTIALLY IMPLEMENTED
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
- **Status:** IMPLEMENTED
- **Description:** Basic strategic action framework for Diplomacy card
- **Implementation:** Found in `game_controller.py` with strategic action handling

### 32.2 Primary Ability Resolution
- **Status:** NOT IMPLEMENTED
- **Description:** System selection, command token placement, planet readying
- **Gap:** No implementation of Diplomacy-specific primary ability logic

### 32.3 Secondary Ability Resolution
- **Status:** NOT IMPLEMENTED
- **Description:** Other players spending command tokens to ready planets
- **Gap:** No secondary ability system for strategy cards

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

### Missing Tests
- Diplomacy primary ability execution
- Command token placement in systems
- Planet readying mechanics
- Secondary ability usage
- System activation prevention
- Reinforcement vs command sheet token logic

## Implementation Files

### Core Implementation
- `src/ti4/core/strategy_card.py`: Basic strategy card definitions
- `src/ti4/core/game_controller.py`: Strategy card selection and basic strategic actions
- Command token management (referenced but not fully visible)

### Missing Implementation
- Diplomacy-specific primary ability logic
- Planet readying system
- System activation prevention mechanics
- Secondary ability framework
- Command token placement validation
- Reinforcement pool integration

## Notable Implementation Details

### Well Implemented
- Basic strategy card framework
- Strategy card selection system
- Initiative order determination
- Strategic action triggering
- Command token resource tracking

### Gaps and Issues
- No specific strategy card ability implementations
- Missing planet readying mechanics
- No system activation prevention
- Limited command token placement logic
- No secondary ability system
- Missing reinforcement pool integration

## Action Items

1. **Implement Diplomacy primary ability** - System selection and command token placement logic
2. **Add planet readying mechanics** - System for readying exhausted planets
3. **Create system activation prevention** - Block other players from activating chosen system
4. **Implement secondary ability framework** - Allow other players to use secondary abilities
5. **Add command token placement validation** - Handle reinforcements vs command sheet logic
6. **Create reinforcement pool system** - Track and manage player reinforcement tokens
7. **Add Mecatol Rex restriction logic** - Prevent selection of Mecatol Rex system
8. **Implement turn order for secondary abilities** - Clockwise resolution from active player
9. **Add comprehensive Diplomacy tests** - Cover all primary and secondary ability scenarios
10. **Create planet control validation** - Ensure player controls planets in chosen system

## Priority Assessment
**MEDIUM** - Important strategic card but not critical for basic gameplay. Missing implementation affects strategic depth and player interaction but doesn't break core game mechanics.
