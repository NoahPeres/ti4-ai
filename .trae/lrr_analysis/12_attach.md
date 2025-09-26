# Rule 12: ATTACH

## Category Overview
**Rule Type:** Card Management Mechanic
**Priority:** Medium
**Complexity:** Medium
**Implementation Status:** ✅ COMPLETED

Rule 12 defines the mechanics for attaching cards to planet cards, including physical placement, control transfer behavior, and attachment token management on the game board.

## Sub-Rules Analysis

### 12.1 - Card Attachment Process
**Raw LRR Text:**
> "To attach a card to a planet card, a player places the card with the attach effect partially underneath the planet card."

**Analysis:**
- Defines the physical placement method for attaching cards
- Cards are placed "partially underneath" the planet card
- Attached cards maintain their exhausted/readied state
- Implementation requires card positioning and visual representation

**Priority:** Medium - Core mechanic for exploration and agenda effects
**Status:** ✅ IMPLEMENTED

### 12.2 - Control Transfer Behavior
**Raw LRR Text:**
> "If a player gains or loses control of planet that contains a card with an attach effect, the attached card stays with that planet."

**Analysis:**
- Attached cards remain with the planet when control changes
- Cards maintain their exhausted/readied state during transfer
- If planet card is purged, all attached cards are also purged
- Implementation requires proper card ownership tracking

**Priority:** Medium - Important for planet control mechanics
**Status:** ✅ IMPLEMENTED

### 12.3 - Attachment Token Placement
**Raw LRR Text:**
> "When a card is attached to a planet card, place the corresponding attachment token on that planet on the game board."

**Analysis:**
- Physical board representation of attached cards
- Tokens must be removed when cards are purged
- Visual indicator for game state tracking
- Implementation requires token management system

**Priority:** Medium - Visual game state representation
**Status:** ✅ IMPLEMENTED

## Related Topics
- **Agenda Card:** Many agenda cards have attach effects
- **Control:** Planet control affects attached card ownership
- **Exploration:** Exploration cards can have attach effects
- **Planets:** Target for attachment mechanics

## Dependencies
- Planet card system and control mechanics ✅
- Card state management (exhausted/readied) ✅
- Token placement and removal system ✅
- Exploration card resolution system (partial)
- Agenda card resolution system (partial)

## Test References
**Current Test Coverage:** ✅ COMPREHENSIVE

### Core Attachment Tests
- `test_attach_card_to_planet_card_basic` - Basic attachment functionality
- `test_attach_card_preserves_exhausted_state` - State preservation during attachment
- `test_multiple_attachments_per_planet` - Multiple attachments support

### Control Transfer Tests
- `test_attached_cards_stay_with_planet_on_control_change` - Control transfer behavior
- `test_purged_planet_card_purges_attachments` - Purging behavior

### Token Management Tests
- `test_attachment_token_placed_on_game_board` - Token placement (Rule 12.3)
- `test_attachment_token_removed_when_card_detached` - Token removal
- `test_multiple_attachment_tokens_per_planet` - Multiple token support

### Validation Tests
- `test_attachment_validation_only_planets_can_have_attachments` - Target validation
- `test_attachment_order_preservation` - Attachment order maintenance

### Integration Tests
- `test_attachment_system_integration_with_exploration` - Exploration integration (placeholder)
- `test_attachment_system_integration_with_agenda_cards` - Agenda integration (placeholder)

## Implementation Files
**Current Implementation Status:** ✅ COMPLETED

### Core Implementation
- `src/ti4/core/planet_card.py` - PlanetCard class with attachment methods
  - `attach_card()` - Attach cards to planet with token management
  - `detach_card()` - Detach cards and remove tokens
  - `get_attached_cards()` - Retrieve attached cards
  - `has_attached_cards()` - Check for attachments
  - `purge_attachments()` - Remove all attachments (for control transfer)

- `src/ti4/core/game_state.py` - GameState with attachment token tracking
  - `planet_attachment_tokens` - Dict mapping planet names to token sets
  - `_get_or_create_planet_card()` - Updated to pass game_state reference

### Test Implementation
- `tests/test_rule_12_attach.py` - Comprehensive test suite (12 tests, all passing)

## Implementation Details

### Data Structures
- `PlanetCard._attached_cards: List[Any]` - Stores attached cards in order
- `GameState.planet_attachment_tokens: dict[str, set[str]]` - Maps planet names to token IDs
- `PlanetCard._game_state: Optional[GameState]` - Reference for token management

### Key Features Implemented
1. **Attachment System Architecture** ✅
   - Card attachment data structure implemented
   - Attachment/detachment methods with validation
   - Card state preservation during attachment

2. **Planet Card Attachment** ✅
   - Attachment tracking on planet cards
   - Multiple attachments per planet supported
   - Attachment order preservation

3. **Control Transfer Logic** ✅
   - Attached cards transfer with planet control
   - Card states preserved during control changes
   - Purging of attached cards when planet is purged

4. **Attachment Token System** ✅
   - Token placement mechanics implemented
   - Token-to-card correspondence maintained
   - Token removal when cards are detached/purged

5. **Comprehensive Testing** ✅
   - Basic attachment/detachment mechanics tested
   - Control transfer scenarios covered
   - Token placement and removal validated
   - Integration placeholders for exploration and agenda systems

6. **Attachment Validation** ✅
   - Validation that only planets can have attachments
   - Prevention of duplicate attachments
   - Proper error handling for invalid operations

## Raw LRR Text
```
12. ATTACH
To attach a card to a planet card, a player places the card with the attach effect partially underneath the planet card.

• If a player gains or loses control of planet that contains a card with an attach effect, the attached card stays with that planet.

• When a card is attached to a planet card, place the corresponding attachment token on that planet on the game board.
```
