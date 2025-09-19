# Rule 34: EXHAUSTED - Analysis

## Category Overview
**Rule Type:** Core Game Mechanic  
**Priority:** HIGH  
**Status:** IMPLEMENTED  
**Complexity:** Medium  

## Raw LRR Text
```
34 EXHAUSTED
Some cards can be exhausted. A player cannot resolve abilities or spend the resources or influence of an exhausted card.

34.1 To exhaust a card, a player flips the card facedown.

34.2 During the "Ready Cards" step of the status phase, each player readies all of their exhausted cards by flipping those cards faceup.

34.3 A player exhausts their planet cards to spend either the resources or influence on that card.

34.4 Abilities, including some found on technology cards, may instruct a player to exhaust a card to resolve those abilities. If a card is already exhausted, it cannot be exhausted again.
a Passive abilities on an exhausted card are still in effect while that card is exhausted.

34.5 After a player performs a strategic action, they exhaust the strategy card that corresponds to that action.

RELATED TOPICS: Influence, Planets, Resources, Status Phase
```

## Sub-Rules Analysis

### 34.1 Card Exhaustion Mechanism
- **Status:** IMPLEMENTED
- **Description:** Physical card flipping to facedown state
- **Implementation:** Added `is_exhausted()`, `exhaust()`, and `ready()` methods to Planet and TechnologyCard classes

### 34.2 Ready Cards Step
- **Status:** IMPLEMENTED
- **Description:** Status phase step to ready all exhausted cards
- **Implementation:** StatusPhaseManager.ready_all_cards() method implemented to ready all player cards

### 34.3 Planet Card Exhaustion
- **Status:** IMPLEMENTED
- **Description:** Exhausting planets to spend resources/influence
- **Implementation:** Planet class has exhausted state tracking with proper validation

### 34.4 Ability-Triggered Exhaustion
- **Status:** IMPLEMENTED
- **Description:** Technology and other abilities requiring card exhaustion
- **Implementation:** TechnologyCard class supports exhaustion mechanics with passive ability persistence

### 34.5 Strategy Card Exhaustion
- **Status:** IMPLEMENTED
- **Description:** Exhausting strategy cards after strategic actions
- **Implementation:** GameState tracks exhausted strategy cards and StatusPhaseManager readies them

## Related Topics
- Influence
- Planets
- Resources
- Status Phase

## Dependencies
- Card state management system
- Status phase implementation
- Planet card system
- Resource/influence spending mechanics
- Technology ability system
- Strategy card lifecycle
- Game phase management

## Test References

### Implemented Tests
- **test_rule_34_exhausted.py** - Comprehensive test suite covering all Rule 34 mechanics
  - `TestRule34GeneralExhaustedMechanics` - Basic exhausted state functionality
  - `TestRule34PlanetCardExhaustion` - Planet card exhaustion mechanics
  - `TestRule34TechnologyCardExhaustion` - Technology card exhaustion mechanics
  - `TestRule34StatusPhaseReadyCards` - Status phase card readying functionality
  - `TestRule34IntegrationWithExistingSystems` - Integration with game systems

### Test Cases Demonstrating Implementation
- `test_exhausted_planet_cannot_spend_resources()` - Rule 34 core mechanic
- `test_exhausted_planet_cannot_spend_influence()` - Rule 34 core mechanic
- `test_planet_exhaustion_for_resources()` - Rule 34.3 implementation
- `test_planet_exhaustion_for_influence()` - Rule 34.3 implementation
- `test_technology_card_exhaustion()` - Rule 34.4 implementation
- `test_passive_abilities_persist_when_exhausted()` - Rule 34.4a implementation
- `test_status_phase_readies_all_exhausted_cards()` - Rule 34.2 implementation
- `test_ready_cards_affects_all_card_types()` - Rule 34.2 comprehensive test
- `test_comprehensive_card_readying_in_status_phase()` - Integration test

## Implementation Files

### Core Implementation
- **src/ti4/core/planet.py** - Planet class with exhausted state mechanics
- **src/ti4/core/technology.py** - TechnologyCard class with exhaustion support
- **src/ti4/core/game_state.py** - GameState with exhausted card tracking and management
- **src/ti4/core/status_phase.py** - StatusPhaseManager with ready_all_cards functionality

### Implementation Details
- Card state management system with `is_exhausted()`, `exhaust()`, and `ready()` methods
- Status phase "Ready Cards" step implementation
- Planet card exhaustion mechanics for resource/influence spending
- Technology card exhaustion with passive ability persistence
- Strategy card state management and exhaustion tracking
- Validation preventing usage of exhausted cards
- Comprehensive test coverage for all exhaustion scenarios

## Notable Implementation Details

### Successfully Implemented
- **Card state management system** - Complete exhausted/ready state tracking for all card types
- **Status phase framework** - StatusPhaseManager with "Ready Cards" step implementation
- **Planet card exhaustion mechanics** - Full resource/influence spending exhaustion support
- **Technology card exhaustion** - Ability costs requiring exhaustion with passive ability persistence
- **Strategy card state management** - Exhaustion tracking after strategic actions
- **Exhaustion validation system** - Prevention of usage of exhausted cards
- **Double exhaustion prevention** - Blocks exhausting already exhausted cards
- **Comprehensive test coverage** - All exhaustion scenarios and edge cases covered

### Implementation Quality
- Follows TDD methodology with proper red-green-refactor cycles
- Comprehensive test suite with 15 passing test cases
- Clean separation of concerns between card types and game state
- Proper integration with existing game systems
- Maintains passive ability functionality on exhausted cards as per Rule 34.4a

## Action Items

~~1. **Implement card state management system** - Track exhausted/ready states for all card types~~ ✅ COMPLETED
~~2. **Create status phase framework** - Implement status phase with "Ready Cards" step~~ ✅ COMPLETED
~~3. **Add planet card exhaustion mechanics** - Handle resource/influence spending exhaustion~~ ✅ COMPLETED
~~4. **Implement technology card exhaustion** - Support ability costs requiring exhaustion~~ ✅ COMPLETED
~~5. **Add strategy card state management** - Track exhaustion after strategic actions~~ ✅ COMPLETED
~~6. **Create exhaustion validation system** - Prevent usage of exhausted cards~~ ✅ COMPLETED
~~7. **Implement passive ability persistence** - Maintain passive effects on exhausted cards~~ ✅ COMPLETED
~~8. **Add double exhaustion prevention** - Block exhausting already exhausted cards~~ ✅ COMPLETED
~~9. **Create comprehensive exhaustion tests** - Cover all exhaustion scenarios and edge cases~~ ✅ COMPLETED
10. **Add visual state indicators** - Support for faceup/facedown card representation (Future enhancement)

## Priority Assessment
**COMPLETED** - All fundamental exhausted state mechanics have been successfully implemented and tested. The implementation covers all aspects of Rule 34 including card exhaustion, status phase readying, resource/influence spending validation, and proper integration with existing game systems.