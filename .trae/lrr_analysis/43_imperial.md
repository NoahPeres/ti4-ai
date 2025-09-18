# LRR Rule Analysis: Rule 43 - IMPERIAL (STRATEGY CARD)

## Category Overview
**Rule Type**: Strategy Card Mechanics  
**Complexity**: Medium  
**Scope**: Victory point scoring and secret objective management  

## Raw LRR Text
```
45 IMPERIAL (STRATEGY CARD)
The "Imperial" strategy card allows players to score victory points and draw secret objectives. This card's initiative value is "8."

45.2 To resolve the primary ability on the "Imperial" strategy card, the active player can score one public objective of their choice if they meet that objective's requirements as described on its card. Then, if the active player controls Mecatol Rex, they gain one victory point; if they do not control Mecatol Rex, they can draw one secret objective card.

45.3 After the active player resolves the primary ability of the "Imperial" strategy card, each other player, beginning with the player to the left of the active player and proceeding clockwise, may spend one command token from their strategy pool to draw one secret objective card.

45.4 If a player has more than three secret objective cards after drawing a secret objective, they must choose one of their unscored secret objectives and return it to the secret objective deck. This number includes the secret objective cards in the player's hand and the cards that player has already scored. Then, they shuffle the secret objective deck.
```

## Sub-Rules Analysis

### 45.1 Imperial Card Properties
**Rule**: "The 'Imperial' strategy card allows players to score victory points and draw secret objectives. This card's initiative value is '8.'"

**Implementation Status**: ⚠️ PARTIAL
- **Code**: Strategy card system exists in `test_game_controller.py`
- **Tests**: Strategy card selection and initiative order tests exist
- **Assessment**: Basic strategy card framework exists but Imperial-specific mechanics missing
- **Priority**: HIGH
- **Dependencies**: Requires strategy card resolution system and Imperial-specific abilities

### 45.2 Primary Ability - Objective Scoring & Mecatol Rex Bonus
**Rule**: "To resolve the primary ability on the 'Imperial' strategy card, the active player can score one public objective of their choice if they meet that objective's requirements as described on its card. Then, if the active player controls Mecatol Rex, they gain one victory point; if they do not control Mecatol Rex, they can draw one secret objective card."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No Imperial primary ability implementation found
- **Tests**: No Imperial-specific ability tests
- **Assessment**: Core Imperial mechanics missing - objective scoring and Mecatol Rex control bonus
- **Priority**: HIGH
- **Dependencies**: Requires objective system, Mecatol Rex control tracking, victory point system

### 45.3 Secondary Ability - Secret Objective Draw
**Rule**: "After the active player resolves the primary ability of the 'Imperial' strategy card, each other player, beginning with the player to the left of the active player and proceeding clockwise, may spend one command token from their strategy pool to draw one secret objective card."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No secondary ability system for Imperial
- **Tests**: No secondary ability tests
- **Assessment**: Secondary ability mechanics missing
- **Priority**: HIGH
- **Dependencies**: Requires command token system, secret objective deck management

### 45.4 Secret Objective Hand Limit
**Rule**: "If a player has more than three secret objective cards after drawing a secret objective, they must choose one of their unscored secret objectives and return it to the secret objective deck. This number includes the secret objective cards in the player's hand and the cards that player has already scored. Then, they shuffle the secret objective deck."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No secret objective hand limit enforcement
- **Tests**: No hand limit tests
- **Assessment**: Hand management mechanics missing
- **Priority**: MEDIUM
- **Dependencies**: Requires secret objective tracking system

## Related Topics
- **Strategy Cards (Rule 83)**: Imperial is one of eight strategy cards
- **Objective Cards (Rule 61)**: Imperial allows scoring public objectives
- **Victory Points (Rule 98)**: Imperial provides victory point scoring
- **Command Tokens**: Required for secondary ability
- **Mecatol Rex**: Central to Imperial's primary ability bonus

## Dependencies
- **Core Systems**: Strategy card resolution framework
- **Objective System**: Public and secret objective management
- **Victory Point System**: Point tracking and awarding
- **Command Token System**: For secondary ability costs
- **Planet Control System**: For Mecatol Rex control detection
- **Turn Order System**: For secondary ability resolution order

## Test References
**Current Test Coverage**: ⚠️ PARTIAL
- **Strategy Card Tests**: Basic selection and initiative in `test_game_controller.py`
- **Victory Point Tests**: Basic tracking in `test_victory_conditions.py`
- **Objective Tests**: Basic objective system in `test_victory_conditions.py`

**Missing Test Areas**:
- Imperial primary ability resolution
- Mecatol Rex control bonus
- Secret objective drawing mechanics
- Hand limit enforcement
- Secondary ability resolution

## Implementation Files
**Current Implementation**: ⚠️ PARTIAL

**Relevant Files**:
- `tests/test_game_controller.py`: Strategy card selection system
- `tests/test_victory_conditions.py`: Victory point tracking
- `src/ti4/core/game_state.py`: Basic game state (inferred)

**Missing Components**:
- Imperial strategy card class with specific abilities
- Objective scoring validation system
- Mecatol Rex control detection
- Secret objective hand management
- Strategy card ability resolution framework

## Notable Implementation Details

### Current Strategy Card System
- Basic strategy card selection exists
- Initiative order calculation implemented
- Turn order based on strategy card initiative values
- Multiple strategy card selection supported (for fewer players)

### Victory Point System
- Basic victory point tracking exists
- Victory point awarding functionality present
- Win condition detection implemented

### Missing Imperial-Specific Features
- No Imperial primary ability implementation
- No Mecatol Rex control bonus system
- No secret objective drawing mechanics
- No hand limit enforcement

## Action Items

### High Priority
1. **Implement Imperial Primary Ability**
   - Create Imperial strategy card class
   - Implement public objective scoring validation
   - Add Mecatol Rex control detection and bonus
   - Add alternative secret objective draw

2. **Implement Imperial Secondary Ability**
   - Add command token cost validation
   - Implement secret objective drawing for other players
   - Add turn order resolution for secondary abilities

### Medium Priority
3. **Secret Objective Hand Management**
   - Implement 3-card hand limit enforcement
   - Add objective selection and return mechanics
   - Implement deck shuffling after returns

4. **Integration Testing**
   - Test Imperial with full objective system
   - Test Mecatol Rex control scenarios
   - Test hand limit edge cases

### Low Priority
5. **Strategy Card Framework Enhancement**
   - Generalize strategy card ability resolution
   - Add strategy card state management
   - Implement exhaustion mechanics

## Priority Assessment
**Overall Priority**: 🟠 HIGH

**Rationale**:
- Imperial is a core strategy card affecting victory conditions
- Victory point scoring is fundamental to game progression
- Secret objective management is essential for player strategy
- Mecatol Rex control is a key strategic element

**Implementation Effort**: MEDIUM-HIGH
- Requires integration with multiple systems
- Complex interaction between objectives, victory points, and control
- Hand management adds complexity

**Dependencies**: Multiple core systems need coordination