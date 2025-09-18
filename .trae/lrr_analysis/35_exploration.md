# Rule 35: EXPLORATION - Analysis

## Category Overview
**Rule Type:** Core Game Mechanic  
**Priority:** MEDIUM  
**Status:** NOT IMPLEMENTED  
**Complexity:** High  

## Raw LRR Text
```
35 EXPLORATION
Planets and some space areas can be explored, yielding varying results determined by the cards drawn from the exploration decks.

35.1 When a player takes control of a planet that is not already controlled by another player, they explore that planet.

35.2 When a player explores a planet, they draw and resolve a card from the exploration deck that corresponds to that planet's trait.
a There are three planetary exploration decks, each of which corresponds to a planet trait: cultural, hazardous, and industrial.
b Planets that do not have traits, such as Mecatol Rex and planets in home systems, cannot be explored.
c If a planet has multiple traits, the player exploring the planet chooses which of the corresponding exploration decks to draw from.
d If a player gains control of multiple planets or resolves multiple explore effects at the same time, they choose the order in which they resolve those explorations, completely resolving each exploration card before resolving the next.

35.3 Certain abilities may allow a planet to be explored multiple times.

35.4 Players can explore space areas that contain frontier tokens if they own the "Dark Energy Tap" technology or if another game effect allows them to.
a Frontier tokens are placed in systems during setup and by specific abilities.

35.5 When a player explores a frontier token, they draw and resolve a card from the frontier exploration deck.

35.6 After a frontier token is explored, it is discarded and returned to the supply.

35.7 To resolve an exploration card, a player reads the card, makes any necessary decisions, and resolves its ability. If the card was not a relic fragment or an attachment, it is discarded into its respective discard pile.
a If there are no cards in an exploration deck, its discard pile is shuffled to form a new exploration deck.

35.8 If a player resolves an exploration card that has an "attach" header, they attach that card to the planet card of the planet being explored.

35.9 If a player resolves an exploration card that has "relic fragment" in the title, they place that card faceup in their play area.
a Players can resolve the ability of relic fragments that are in their play area. Resolving these abilities allows players to draw cards from the relic deck.
b Relic fragments can be exchanged as part of transactions.

RELATED TOPICS: Attach, Control, Planets, Relics
```

## Sub-Rules Analysis

### 35.1 Planet Control Exploration Trigger
- **Status:** NOT IMPLEMENTED
- **Description:** Automatic exploration when taking control of uncontrolled planets
- **Gap:** No planet control change detection or exploration triggering

### 35.2 Planet Trait-Based Exploration
- **Status:** NOT IMPLEMENTED
- **Description:** Draw from trait-specific exploration decks (cultural, hazardous, industrial)
- **Gap:** No planet trait system or exploration deck management

### 35.3 Multiple Exploration Abilities
- **Status:** NOT IMPLEMENTED
- **Description:** Some abilities allow repeated planet exploration
- **Gap:** No exploration tracking or repeat exploration mechanics

### 35.4 Frontier Token Exploration Prerequisites
- **Status:** NOT IMPLEMENTED
- **Description:** Requires "Dark Energy Tap" technology or other game effects
- **Gap:** No frontier token system or technology prerequisite checking

### 35.5 Frontier Exploration Deck
- **Status:** NOT IMPLEMENTED
- **Description:** Draw from frontier exploration deck when exploring frontier tokens
- **Gap:** No frontier exploration deck or resolution system

### 35.6 Frontier Token Cleanup
- **Status:** NOT IMPLEMENTED
- **Description:** Discard and return frontier tokens to supply after exploration
- **Gap:** No frontier token lifecycle management

### 35.7 Exploration Card Resolution
- **Status:** NOT IMPLEMENTED
- **Description:** Resolve card abilities and handle discard/deck reshuffling
- **Gap:** No exploration card resolution system or deck management

### 35.8 Attachment Cards
- **Status:** NOT IMPLEMENTED
- **Description:** Attach exploration cards with "attach" header to planet cards
- **Gap:** No card attachment system or planet card modification

### 35.9 Relic Fragment Handling
- **Status:** NOT IMPLEMENTED
- **Description:** Place relic fragments in play area and enable relic deck drawing
- **Gap:** No relic fragment system or relic deck mechanics

## Related Topics
- Attach
- Control
- Planets
- Relics

## Dependencies
- Planet control system
- Planet trait system (cultural, hazardous, industrial)
- Exploration deck management (4 decks total)
- Frontier token system
- Technology system ("Dark Energy Tap")
- Card attachment mechanics
- Relic fragment and relic deck systems
- Discard pile management
- Deck reshuffling mechanics
- Transaction system (for relic fragment trading)

## Test References

### Existing Tests
- No exploration-related tests found
- No planet trait tests
- No frontier token tests
- No relic fragment tests

### Missing Tests
- Planet control exploration triggering
- Trait-based exploration deck selection
- Multiple trait planet exploration choice
- Frontier token exploration prerequisites
- Exploration card resolution
- Attachment card mechanics
- Relic fragment placement and abilities
- Deck reshuffling when empty
- Multiple exploration ordering
- Repeat exploration abilities

## Implementation Files

### Core Implementation
- Basic planet system exists
- Some technology framework
- No exploration system found

### Missing Implementation
- Exploration trigger system
- Planet trait definitions and tracking
- Exploration deck management (cultural, hazardous, industrial, frontier)
- Frontier token system
- Exploration card resolution engine
- Card attachment mechanics
- Relic fragment system
- Relic deck management
- Discard pile and reshuffling system
- Technology prerequisite checking for exploration

## Notable Implementation Details

### Well Implemented
- Basic planet and technology frameworks exist
- Some card management infrastructure

### Gaps and Issues
- No exploration system whatsoever
- Missing planet trait system
- No exploration deck infrastructure
- Missing frontier token mechanics
- No card attachment system
- Missing relic fragment and relic deck systems
- No exploration triggering on planet control
- Missing technology prerequisite validation

## Action Items

1. **Implement planet trait system** - Add cultural, hazardous, and industrial traits to planets
2. **Create exploration deck management** - Implement 4 exploration decks with discard piles and reshuffling
3. **Add exploration triggering system** - Trigger exploration on planet control changes
4. **Implement frontier token system** - Add frontier tokens with placement and exploration mechanics
5. **Create exploration card resolution engine** - Handle card drawing, resolution, and effects
6. **Add card attachment mechanics** - Support attaching exploration cards to planet cards
7. **Implement relic fragment system** - Handle relic fragment placement and abilities
8. **Create relic deck management** - Support relic deck drawing from fragment abilities
9. **Add technology prerequisite checking** - Validate "Dark Energy Tap" for frontier exploration
10. **Implement exploration ordering system** - Handle multiple simultaneous explorations with player choice

## Priority Assessment
**MEDIUM** - Adds significant gameplay depth and variety but not essential for core game mechanics. Important for complete game experience and strategic diversity.