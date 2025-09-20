# LRR Rule Analysis: Section 2 - ACTION CARDS

## 2. ACTION CARDS

**Rule Category Overview**: Action cards provide players with various abilities that they can resolve as described on the cards.

### 2.1 Draw One Card Per Status Phase
**Rule**: "Each player draws one action card during each status phase."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No status phase implementation
- **Tests**: No action card drawing tests
- **Assessment**: Core game flow missing - status phase doesn't exist
- **Priority**: HIGH
- **Dependencies**: Requires status phase, action card deck, and drawing mechanics
- **Notes**: This is fundamental game flow - every round players get new cards

### 2.2 Politics Strategy Card Drawing
**Rule**: "Players can draw action cards by resolving the primary and secondary abilities of the 'Politics' strategy card."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No Politics strategy card implementation
- **Tests**: No Politics strategy card tests
- **Assessment**: Strategy cards exist in basic form but Politics not implemented
- **Priority**: HIGH
- **Dependencies**: Requires Politics strategy card and action card drawing system
- **Notes**: This provides additional card draw beyond the status phase

### 2.3 Card Drawing Mechanics
**Rule**: "When a player draws an action card, they take the top card from the action card deck and add it to their hand of action cards."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No action card deck system
- **Tests**: No card drawing tests
- **Assessment**: Basic deck and hand management system needed
- **Priority**: HIGH
- **Dependencies**: Requires action card deck, shuffling, and hand management
- **Notes**: Standard deck mechanics - draw from top, add to hand

### 2.4 Hand Size Limit
**Rule**: "Each player's hand can have a maximum of seven action cards. If a player ever has more than seven action cards, that player must choose seven cards to keep and discard the rest."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No hand management system
- **Tests**: No hand size tests
- **Assessment**: Need hand size enforcement and discard selection
- **Priority**: MEDIUM
- **Dependencies**: Requires hand management and player choice system
- **Notes**: Sub-rule: "A game effect can increase or decrease the number of cards a player's hand can have."

### 2.5 Hidden Information
**Rule**: "A player's action cards remain hidden from other players until those cards are played."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No hidden information system
- **Tests**: No hidden information tests
- **Assessment**: Need player-specific information visibility
- **Priority**: MEDIUM
- **Dependencies**: Requires player perspective system and information hiding
- **Notes**: Critical for game balance - opponents shouldn't see your cards

### 2.6 Action Card Timing Format
**Rule**: "The first paragraph of each action card is presented in bold text and describes the timing of when that card's ability can be resolved."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No action card format system
- **Tests**: No action card format tests
- **Assessment**: Action cards need structured timing information
- **Priority**: MEDIUM
- **Dependencies**: Requires action card data structure and timing parsing
- **Notes**: Sub-rule about component actions: "If an action card contains the word 'Action,' a player must use a component action during the action phase to resolve the ability. A player cannot resolve a component action if they cannot completely resolve its ability."
- **Additional Note**: "Multiple action cards with the same name cannot be played during a single timing window to affect the same units or game effect. Canceled cards are not treated as being played."

### 2.7 Playing Action Cards
**Rule**: "To play an action card, a player reads and resolves the card's ability text, making any decisions as prompted by the card. Then, that player discards the card, placing it in the action discard pile."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No action card resolution system
- **Tests**: No action card playing tests
- **Assessment**: Need card resolution, decision prompts, and discard mechanics
- **Priority**: HIGH
- **Dependencies**: Requires action card system, ability resolution, and discard pile
- **Notes**: This is the core action card mechanic - play, resolve, discard

### 2.8 Action Card Cancellation
**Rule**: "If an action card is canceled, that card has no effect and is discarded."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No cancellation system
- **Tests**: No cancellation tests
- **Assessment**: Need ability cancellation mechanics
- **Priority**: MEDIUM
- **Dependencies**: Requires action card system and cancellation effects
- **Notes**: Some abilities can cancel other abilities - need to handle this
