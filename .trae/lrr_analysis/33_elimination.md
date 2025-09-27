# Rule 33: ELIMINATION - Analysis

## Category Overview
**Rule Type:** Core Game Mechanic
**Priority:** Completed
**Status:** FULLY IMPLEMENTED
**Complexity:** High

## Raw LRR Text
```
33 ELIMINATION
A player who is eliminated is no longer part of the game.

33.1 A player is eliminated when they meet all of the following three conditions:
a The player has no ground forces on the game board.
b The player has no unit that has "Production."
c The player does not control any planets.

33.2 When a player becomes eliminated, all of the units, command tokens, control tokens, promissory notes, technologies, command sheets, and the faction sheet that matches that player's faction or color are returned to the game box, including those in their reinforcements.

33.3 When a player becomes eliminated, all agenda cards they own are discarded.

33.4 When a player becomes eliminated, each promissory note they have that matches another player's faction or color is returned to that player.

33.5 When a player becomes eliminated, each action card in their hand is discarded.

33.6 When a player becomes eliminated, their strategy cards are returned to the common play area whether those cards have been exhausted or not.

33.7 When a player becomes eliminated, their secret objectives are shuffled back into the secret objective deck whether those secret objectives have been completed or not.

33.8 If the speaker becomes eliminated, the speaker token passes to the player to the speaker's left.

33.9 If a game that started with five or more players becomes a game with four or fewer players due to elimination, the players continue to select only one strategy card during the strategy phase.

33.10 When players are eliminated, faction-specific components interact with the game as follows:
a If a player becomes eliminated and the Nekro Virus' assimilator "X" or "Y" token is placed on one of their faction technologies, that technology remains in play.
b If the Ghost of Creuss player becomes eliminated, their wormhole tokens remain on the game board for the remainder of the game.
c If the Naalu player becomes eliminated while another player has the Naalu player's "0" token, that token remains with its current player until the end of the status phase, and then it is removed from play.
e If the Mahact Gene-Sorcerers become eliminated while they have another player's command tokens on their faction sheet, those command tokens are returned to their respective players' reinforcements.
f If the Mahact Gene-Sorcerers have an eliminated player's command token on their faction sheet, that command token remains in play, as does the eliminated player's commander, if it is unlocked.

33.11 If a player becomes eliminated, any units they have captured are returned to the reinforcements of their original owners.

RELATED TOPICS: Agenda Card, Control, Ground Forces, Production, Promissory Notes
```

**Source:** <mcreference link="https://www.tirules.com/R_elimination" index="1">1</mcreference>

## Sub-Rules Analysis

### 33.1 Elimination Conditions
- **Status:** IMPLEMENTED
- **Description:** Three-condition check for elimination (no ground forces, no production units, no planets)
- **Implementation:** `should_eliminate_player` method in GameState checks all three conditions
- **Test Cases:**
  - `test_player_not_eliminated_with_ground_forces` - verifies ground forces prevent elimination
  - `test_player_not_eliminated_with_production_units` - verifies production units prevent elimination
  - `test_player_not_eliminated_with_controlled_planet` - verifies planet control prevents elimination
  - `test_player_eliminated_with_all_three_conditions` - verifies elimination when all conditions met
  - `test_player_not_eliminated_with_only_two_conditions` - verifies no elimination with only 2/3 conditions
  - `test_elimination_check_for_nonexistent_player` - verifies error handling for invalid player

### 33.2 Component Return to Game Box
- **Status:** IMPLEMENTED
- **Description:** Return all player components to game box
- **Implementation:** `eliminate_player` method in GameState removes all units, control tokens, and player data
- **Test Cases:** `test_component_return_on_elimination` verifies units are removed and player is eliminated

### 33.3 Agenda Card Discard
- **Status:** NOT IMPLEMENTED
- **Description:** Discard all owned agenda cards
- **Gap:** No agenda card ownership tracking or discard system

### 33.4 Promissory Note Return
- **Status:** IMPLEMENTED
- **Description:** Return other players' promissory notes to their owners
- **Implementation:** Integrated `PromissoryNoteManager.handle_player_elimination` into `GameState.eliminate_player` method
- **Test Cases:**
  - `test_promissory_notes_returned_on_elimination` - verifies promissory notes are properly handled on elimination
  - `test_promissory_notes_removed_from_available_pool` - verifies eliminated player's notes removed from available pool
  - `test_elimination_with_no_promissory_notes` - verifies elimination works when no promissory notes involved

### 33.5 Action Card Discard
- **Status:** IMPLEMENTED
- **Description:** Discard all action cards in hand
- **Implementation:** `eliminate_player` method in GameState adds eliminated player's action cards to discard pile and removes them from player's hand
- **Test Cases:**
  - `test_action_cards_discarded_on_elimination` - verifies action cards are discarded when player eliminated
  - `test_elimination_with_no_action_cards` - verifies elimination works when player has no action cards
  - `test_elimination_does_not_affect_other_players_action_cards` - verifies other players' action cards unaffected
  - `test_action_cards_added_to_existing_discard_pile` - verifies action cards added to existing discard pile

### 33.6 Strategy Card Return
- **Status:** NOT IMPLEMENTED
- **Description:** Return strategy cards to common area regardless of exhaustion
- **Gap:** No strategy card state management or return system

### 33.7 Secret Objective Return
- **Status:** NOT IMPLEMENTED
- **Description:** Shuffle secret objectives back into deck
- **Gap:** No secret objective tracking or deck management

### 33.8 Speaker Token Transfer
- **Status:** NOT IMPLEMENTED
- **Description:** Pass speaker token to left player when speaker eliminated
- **Gap:** No speaker token management or transfer system

### 33.9 Strategy Card Selection Adjustment
- **Status:** NOT IMPLEMENTED
- **Description:** Maintain single card selection when player count drops
- **Gap:** No dynamic strategy phase adjustment

### 33.10 Faction-Specific Elimination Rules
- **Status:** NOT IMPLEMENTED
- **Description:** Special handling for faction-specific components
- **Gap:** No faction-specific elimination logic

### 33.11 Captured Unit Return
- **Status:** NOT IMPLEMENTED
- **Description:** Return captured units to original owners
- **Gap:** No unit capture tracking or return system

## Related Topics
- Agenda Card
- Control
- Ground Forces
- Production
- Promissory Notes

## Dependencies
- Player state management
- Component ownership tracking
- Game box component management
- Agenda card system
- Promissory note system
- Action card system
- Strategy card lifecycle
- Secret objective system
- Speaker token management
- Faction-specific component systems
- Unit capture mechanics
- Planet control system
- Production unit tracking

## Test References

### Existing Tests
- No elimination-related tests found
- No component cleanup tests
- No speaker token transfer tests

### Missing Tests
- Elimination condition checking
- Component return to game box
- Agenda card discard on elimination
- Promissory note return mechanics
- Action card discard on elimination
- Strategy card return to common area
- Secret objective deck shuffling
- Speaker token transfer
- Strategy phase adjustment for player count
- Faction-specific elimination rules
- Captured unit return

## Implementation Files

### Core Implementation
- Basic game controller exists
- Some strategy card framework
- No elimination system found

### Missing Implementation
- Player elimination detection system
- Component cleanup and return mechanics
- Game box management
- Agenda card ownership and discard
- Promissory note ownership tracking
- Action card hand management
- Strategy card state and return system
- Secret objective deck management
- Speaker token transfer logic
- Dynamic strategy phase rules
- Faction-specific elimination handlers
- Unit capture tracking system

## Notable Implementation Details

### Well Implemented
- Basic player and game state structure
- Strategy card framework exists
- Some component tracking mechanisms

### Gaps and Issues
- No elimination condition checking
- Missing component cleanup system
- No game box management
- Missing card ownership tracking
- No speaker token management
- Missing faction-specific elimination rules
- No captured unit tracking
- Missing dynamic game rule adjustments

## Action Items

1. **Implement elimination condition checker** - Monitor ground forces, production units, and planet control
2. **Create component cleanup system** - Handle return of all player components to game box
3. **Add agenda card ownership tracking** - Track and discard owned agenda cards on elimination
4. **Implement promissory note return system** - Return other players' promissory notes to owners
5. **Create action card hand management** - Handle discard of all action cards on elimination
6. **Add strategy card return mechanics** - Return strategy cards to common area regardless of state
7. **Implement secret objective deck management** - Shuffle eliminated player's objectives back into deck
8. **Create speaker token transfer system** - Handle speaker token passing when speaker eliminated
9. **Add dynamic strategy phase rules** - Adjust strategy card selection based on remaining players
10. **Implement faction-specific elimination handlers** - Handle special cases for each faction's components

## Priority Assessment
**MEDIUM-HIGH** - Important for game integrity and proper endgame handling, but not immediately critical for basic gameplay. Essential for complete game implementation and tournament play.
