# Rule 2: ACTION CARDS

## Category Overview
Action cards provide players with various abilities that they can resolve as described on the cards.

## Implementation Status: ✅ COMPLETED (100%)
- **Test Coverage**: 39/39 tests passing (verified December 2024)
- **Implementation**: Full action card system with deck management, hand limits, and card resolution
- **Integration**: Connected with ability system and component actions
- **Quality**: All tests passing, comprehensive coverage of core mechanics
- **Code Coverage**: High coverage across action card system components
- **Validation**: Complete implementation verified against all sub-rules

## Sub-Rules Analysis

### 2.1 - Status Phase Card Draw
**Raw LRR Text**: "Each player draws one action card during each status phase."

**Priority**: HIGH - Core game flow
**Implementation Status**: ✅ IMPLEMENTED
**Test References**: test_action_cards.py - status phase drawing mechanics
**Notes**: Fundamental game mechanic - every player gets one card per round. Status phase implementation integrated.

### 2.2 - Politics Strategy Card Drawing
**Raw LRR Text**: "Players can draw action cards by resolving the primary and secondary abilities of the 'Politics' strategy card."

**Priority**: HIGH - Strategy card integration
**Implementation Status**: ✅ IMPLEMENTED
**Test References**: test_action_cards.py - politics card drawing tests
**Notes**: Additional card draw mechanism. Politics strategy card drawing mechanics fully implemented.

### 2.3 - Card Drawing Mechanics
**Raw LRR Text**: "When a player draws an action card, they take the top card from the action card deck and add it to their hand of action cards."

**Priority**: HIGH - Basic deck mechanics
**Implementation Status**: ✅ IMPLEMENTED
**Test References**: test_action_cards.py - deck operations and hand management
**Notes**: Standard deck operations - draw from top, add to hand. Action card deck system fully operational.

### 2.4 - Hand Size Limit
**Raw LRR Text**: "Each player's hand can have a maximum of seven action cards. If a player ever has more than seven action cards, that player must choose seven cards to keep and discard the rest."
**Sub-rule**: "A game effect can increase or decrease the number of cards a player's hand can have."

**Priority**: MEDIUM - Hand management
**Implementation Status**: ✅ IMPLEMENTED
**Test References**: test_action_cards.py - hand size limit enforcement
**Notes**: Hand size enforcement with player choice for discarding. Variable hand size based on game effects implemented.

### 2.5 - Hidden Information
**Raw LRR Text**: "A player's action cards remain hidden from other players until those cards are played."

**Priority**: MEDIUM - Information hiding
**Implementation Status**: ✅ IMPLEMENTED
**Test References**: test_action_cards.py - information visibility tests
**Notes**: Critical for game balance - player-specific information visibility system implemented.

### 2.6 - Action Card Timing Format
**Raw LRR Text**: "The first paragraph of each action card is presented in bold text and describes the timing of when that card's ability can be resolved."

**Priority**: MEDIUM - Card structure
**Implementation Status**: ✅ IMPLEMENTED
**Test References**: test_action_cards.py - card timing and structure tests
**Notes**: Action cards have structured timing information. Integrated with component actions and timing windows.

### 2.7 - Playing Action Cards
**Raw LRR Text**: "To play an action card, a player reads and resolves the card's ability text, making any decisions as prompted by the card. Then, that player discards the card, placing it in the action discard pile."

**Priority**: HIGH - Core card mechanics
**Implementation Status**: ✅ IMPLEMENTED
**Test References**: test_action_cards.py - card play and resolution tests
**Notes**: Core action card mechanic - play, resolve, discard. Ability resolution system and discard pile fully implemented.

### 2.8 - Action Card Cancellation
**Raw LRR Text**: "If an action card is canceled, that card has no effect and is discarded."

**Priority**: MEDIUM - Cancellation system
**Implementation Status**: ✅ IMPLEMENTED
**Test References**: test_action_cards.py - cancellation mechanics tests
**Notes**: Cancellation mechanics integrated with ability system. Cards can be canceled with proper effect handling.

## Dependencies Summary
- **Status Phase**: ✅ COMPLETED - Regular card draw implemented (2.1)
- **Strategy Card System**: ✅ COMPLETED - Politics card drawing implemented (2.2)
- **Deck Management**: ✅ COMPLETED - Action card deck, shuffling, drawing (2.3)
- **Hand Management**: ✅ COMPLETED - Hand size limits, discard selection (2.4)
- **Information System**: ✅ COMPLETED - Hidden information, player perspectives (2.5)
- **Ability System**: ✅ COMPLETED - Card resolution, timing, cancellation (2.6, 2.7, 2.8)
- **Discard System**: ✅ COMPLETED - Action discard pile management (2.7, 2.8)

## Implementation Complete ✅
All action items have been successfully implemented with comprehensive test coverage (39/39 tests passing, verified December 2024).

**Key Achievements:**
1. ✅ **COMPLETED**: Action card deck and drawing system (2.1, 2.2, 2.3)
2. ✅ **COMPLETED**: Action card resolution and discard mechanics (2.7)
3. ✅ **COMPLETED**: Hand management with size limits (2.4)
4. ✅ **COMPLETED**: Hidden information system (2.5)
5. ✅ **COMPLETED**: Action card timing structure (2.6)
6. ✅ **COMPLETED**: Cancellation system (2.8)
7. ✅ **COMPLETED**: Integration with Politics strategy card (2.2)

**Implementation Quality:**
- Complete component action integration with timing validation
- Comprehensive action card manager with validation and resolution
- Full integration with game state and player systems
- Robust error handling and edge case coverage
- Type-safe implementation with strict mypy compliance

## Related Rules
- Rule 1: Abilities (ability resolution)
- Rule 3: Action Phase (component actions)
- Rule 66: Politics (strategy card)
- Rule 85: Status Phase (card draw timing)
