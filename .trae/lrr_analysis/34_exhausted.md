# Rule 34: EXHAUSTED - Analysis

## Category Overview
**Rule Type:** Core Game Mechanic  
**Priority:** HIGH  
**Status:** NOT IMPLEMENTED  
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
- **Status:** NOT IMPLEMENTED
- **Description:** Physical card flipping to facedown state
- **Gap:** No card state management system

### 34.2 Ready Cards Step
- **Status:** NOT IMPLEMENTED
- **Description:** Status phase step to ready all exhausted cards
- **Gap:** No status phase implementation or card readying system

### 34.3 Planet Card Exhaustion
- **Status:** NOT IMPLEMENTED
- **Description:** Exhausting planets to spend resources/influence
- **Gap:** No planet card state or resource spending mechanics

### 34.4 Ability-Triggered Exhaustion
- **Status:** NOT IMPLEMENTED
- **Description:** Technology and other abilities requiring card exhaustion
- **Gap:** No ability cost system or exhaustion validation

### 34.5 Strategy Card Exhaustion
- **Status:** NOT IMPLEMENTED
- **Description:** Exhausting strategy cards after strategic actions
- **Gap:** No strategy card state management

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

### Existing Tests
- No specific exhausted state tests found
- Limited status phase references
- No card state management tests

### Missing Tests
- Card exhaustion mechanics
- Ready cards step functionality
- Planet exhaustion for resource spending
- Technology card exhaustion
- Strategy card exhaustion
- Passive ability persistence on exhausted cards
- Double exhaustion prevention

## Implementation Files

### Core Implementation
- No exhausted state system found
- No card state management
- No status phase implementation

### Missing Implementation
- Card state management system
- Exhausted/ready state tracking
- Status phase "Ready Cards" step
- Planet card exhaustion mechanics
- Technology card exhaustion
- Strategy card state management
- Resource/influence spending validation

## Notable Implementation Details

### Well Implemented
- Basic strategy card framework exists
- Some resource tracking mechanisms

### Gaps and Issues
- No card state management system
- Missing exhausted/ready state tracking
- No status phase implementation
- No planet card exhaustion mechanics
- Missing technology card exhaustion
- No validation for exhausted card usage
- No passive ability persistence logic

## Action Items

1. **Implement card state management system** - Track exhausted/ready states for all card types
2. **Create status phase framework** - Implement status phase with "Ready Cards" step
3. **Add planet card exhaustion mechanics** - Handle resource/influence spending exhaustion
4. **Implement technology card exhaustion** - Support ability costs requiring exhaustion
5. **Add strategy card state management** - Track exhaustion after strategic actions
6. **Create exhaustion validation system** - Prevent usage of exhausted cards
7. **Implement passive ability persistence** - Maintain passive effects on exhausted cards
8. **Add double exhaustion prevention** - Block exhausting already exhausted cards
9. **Create comprehensive exhaustion tests** - Cover all exhaustion scenarios and edge cases
10. **Add visual state indicators** - Support for faceup/facedown card representation

## Priority Assessment
**HIGH** - Fundamental game mechanic affecting resource management, ability usage, and game flow. Critical for proper resource economy and strategic decision-making.