# Rule 2: ACTION CARDS

## Category Overview
Action cards provide players with various abilities that they can resolve as described on the cards.

## Sub-Rules Analysis

### 2.1 - Status Phase Card Draw
**Raw LRR Text**: "Each player draws one action card during each status phase."

**Priority**: HIGH - Core game flow
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Fundamental game mechanic - every player gets one card per round. Requires status phase implementation.

### 2.2 - Politics Strategy Card Drawing
**Raw LRR Text**: "Players can draw action cards by resolving the primary and secondary abilities of the 'Politics' strategy card."

**Priority**: HIGH - Strategy card integration
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Additional card draw mechanism. Politics strategy card exists in basic form but drawing mechanics not implemented.

### 2.3 - Card Drawing Mechanics
**Raw LRR Text**: "When a player draws an action card, they take the top card from the action card deck and add it to their hand of action cards."

**Priority**: HIGH - Basic deck mechanics
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Standard deck operations - draw from top, add to hand. Need action card deck system.

### 2.4 - Hand Size Limit
**Raw LRR Text**: "Each player's hand can have a maximum of seven action cards. If a player ever has more than seven action cards, that player must choose seven cards to keep and discard the rest."
**Sub-rule**: "A game effect can increase or decrease the number of cards a player's hand can have."

**Priority**: MEDIUM - Hand management
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Hand size enforcement with player choice for discarding. Variable hand size based on game effects.

### 2.5 - Hidden Information
**Raw LRR Text**: "A player's action cards remain hidden from other players until those cards are played."

**Priority**: MEDIUM - Information hiding
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Critical for game balance - need player-specific information visibility system.

### 2.6 - Action Card Timing Format
**Raw LRR Text**: "The first paragraph of each action card is presented in bold text and describes the timing of when that card's ability can be resolved."

**Priority**: MEDIUM - Card structure
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Action cards need structured timing information. Related to component actions and timing windows.

### 2.7 - Playing Action Cards
**Raw LRR Text**: "To play an action card, a player reads and resolves the card's ability text, making any decisions as prompted by the card. Then, that player discards the card, placing it in the action discard pile."

**Priority**: HIGH - Core card mechanics
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Core action card mechanic - play, resolve, discard. Requires ability resolution system and discard pile.

### 2.8 - Action Card Cancellation
**Raw LRR Text**: "If an action card is canceled, that card has no effect and is discarded."

**Priority**: MEDIUM - Cancellation system
**Implementation Status**: ❌ NOT IMPLEMENTED
**Test References**: None found
**Notes**: Some abilities can cancel other abilities. Need cancellation mechanics integrated with ability system.

## Dependencies Summary
- **Status Phase**: Required for regular card draw (2.1)
- **Strategy Card System**: Politics card for additional draws (2.2)
- **Deck Management**: Action card deck, shuffling, drawing (2.3)
- **Hand Management**: Hand size limits, discard selection (2.4)
- **Information System**: Hidden information, player perspectives (2.5)
- **Ability System**: Card resolution, timing, cancellation (2.6, 2.7, 2.8)
- **Discard System**: Action discard pile management (2.7, 2.8)

## Action Items for Full Implementation
1. **CRITICAL**: Implement action card deck and drawing system (2.1, 2.2, 2.3)
2. **HIGH**: Create action card resolution and discard mechanics (2.7)
3. **HIGH**: Build hand management with size limits (2.4)
4. **MEDIUM**: Implement hidden information system (2.5)
5. **MEDIUM**: Add action card timing structure (2.6)
6. **MEDIUM**: Create cancellation system (2.8)
7. **LOW**: Integrate with Politics strategy card (2.2)

## Related Rules
- Rule 1: Abilities (ability resolution)
- Rule 3: Action Phase (component actions)
- Rule 66: Politics (strategy card)
- Rule 85: Status Phase (card draw timing)
