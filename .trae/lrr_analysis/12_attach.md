# Rule 12: ATTACH

## Category Overview
**Rule Type:** Card Management Mechanic  
**Priority:** Medium  
**Complexity:** Medium  
**Implementation Status:** Not Implemented  

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

### 12.2 - Control Transfer Behavior  
**Raw LRR Text:**
> "If a player gains or loses control of planet that contains a card with an attach effect, the attached card stays with that planet."

**Analysis:**
- Attached cards remain with the planet when control changes
- Cards maintain their exhausted/readied state during transfer
- If planet card is purged, all attached cards are also purged
- Implementation requires proper card ownership tracking

**Priority:** Medium - Important for planet control mechanics

### 12.3 - Attachment Token Placement
**Raw LRR Text:**
> "When a card is attached to a planet card, place the corresponding attachment token on that planet on the game board."

**Analysis:**
- Physical board representation of attached cards
- Tokens must be removed when cards are purged
- Visual indicator for game state tracking
- Implementation requires token management system

**Priority:** Medium - Visual game state representation

## Related Topics
- **Agenda Card:** Many agenda cards have attach effects
- **Control:** Planet control affects attached card ownership
- **Exploration:** Exploration cards can have attach effects
- **Planets:** Target for attachment mechanics

## Dependencies
- Planet card system and control mechanics
- Card state management (exhausted/readied)
- Token placement and removal system
- Exploration card resolution system
- Agenda card resolution system

## Test References
**Current Test Coverage:** None found
- No existing tests for attach mechanics
- No tests for attachment token management
- No tests for control transfer with attached cards

## Implementation Files
**Current Implementation Status:** Not Implemented
- No dedicated attach system found
- Basic planet control exists in `src/ti4/core/system.py`
- Exploration system partially exists but lacks attach handling
- No attachment token management system

## Action Items

1. **Create Attachment System Architecture**
   - Design card attachment data structure
   - Implement attachment/detachment methods
   - Handle card state preservation during attachment

2. **Implement Planet Card Attachment**
   - Add attachment tracking to planet cards
   - Support multiple attachments per planet
   - Maintain attachment order and positioning

3. **Build Control Transfer Logic**
   - Ensure attached cards transfer with planet control
   - Preserve card states during control changes
   - Handle purging of attached cards when planet is purged

4. **Create Attachment Token System**
   - Design token placement mechanics
   - Implement token-to-card correspondence
   - Handle token removal when cards are detached/purged

5. **Integrate with Exploration System**
   - Support exploration cards with attach effects
   - Handle attachment during exploration resolution
   - Validate attachment targets and conditions

6. **Integrate with Agenda System**
   - Support agenda cards with attach effects
   - Handle attachment during agenda resolution
   - Manage permanent vs temporary attachments

7. **Implement Visual Representation**
   - Design UI for showing attached cards
   - Display attachment tokens on game board
   - Show attachment relationships clearly

8. **Add Comprehensive Testing**
   - Test basic attachment/detachment mechanics
   - Test control transfer scenarios
   - Test token placement and removal
   - Test integration with exploration and agenda systems

9. **Create Attachment Validation**
   - Validate attachment targets (must be planets)
   - Check attachment prerequisites
   - Prevent invalid attachment attempts

10. **Document Attachment API**
    - Create clear interface for attachment operations
    - Document attachment state management
    - Provide examples for common attachment scenarios