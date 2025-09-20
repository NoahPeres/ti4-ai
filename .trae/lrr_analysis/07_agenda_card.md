# LRR Rule Analysis: Section 7 - AGENDA CARD

## Category Overview
Agenda cards represent galactic laws and policies that can permanently change the rules of the game or provide one-time effects. During each agenda phase, players cast votes for specific outcomes on two agenda cards. This system is fundamental to the political aspect of Twilight Imperium 4th Edition.

## Sub-Rules Analysis

### 7.1 Types of Agenda Cards 🔴 HIGH
**Raw LRR Text**: "There are two types of agenda cards: laws and directives."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No agenda card system exists
- **Tests**: No agenda card tests found
- **Assessment**: Fundamental agenda system missing - no card types defined
- **Priority**: HIGH
- **Dependencies**: Requires agenda card base class and type system
- **Notes**: Laws and directives have different resolution mechanics

### 7.2 Laws Change Rules Permanently 🔴 HIGH
**Raw LRR Text**: "Laws can permanently change the rules of the game."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No law system or rule modification framework
- **Tests**: No law implementation tests
- **Assessment**: Core political mechanic missing - no permanent rule changes
- **Priority**: HIGH
- **Dependencies**: Requires rule modification system and law persistence
- **Notes**: Laws remain in effect until discarded

### 7.3 Law Resolution - "For" Outcomes 🔴 HIGH
**Raw LRR Text**: "When resolving a law, if a 'For' outcome received the most votes, or if the law requires an election, the law's ability becomes a permanent part of the game. Players resolve the outcome and place the agenda card either in the common play area or in a player's play area, as dictated by the card."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No voting system or outcome resolution
- **Tests**: No voting resolution tests
- **Assessment**: Voting mechanics completely missing
- **Priority**: HIGH
- **Dependencies**: Requires voting system, outcome tracking, and card placement
- **Notes**: Laws can be owned by players or be common

### 7.4 Law Ownership 🟡 MEDIUM
**Raw LRR Text**: "If a law is in a player's play area as opposed to the common play area, that player owns that law."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No law ownership system
- **Tests**: No ownership tests
- **Assessment**: Player-specific law effects not implemented
- **Priority**: MEDIUM
- **Dependencies**: Requires player play area and law ownership tracking
- **Notes**: Owned laws may have different effects or benefits

### 7.5 Law Discard Effects 🟡 MEDIUM
**Raw LRR Text**: "If a law is discarded from play, that law's ability is no longer in effect. Place that card on the top of the agenda card discard pile."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No law discard system or effect removal
- **Tests**: No discard effect tests
- **Assessment**: Law lifecycle management missing
- **Priority**: MEDIUM
- **Dependencies**: Requires discard pile and effect cleanup system
- **Notes**: Laws can be removed by various game effects

### 7.7 Directive One-Time Effects 🔴 HIGH
**Raw LRR Text**: "Directives provide one-time game effects."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No directive system
- **Tests**: No directive tests
- **Assessment**: One-time political effects missing
- **Priority**: HIGH
- **Dependencies**: Requires directive resolution system
- **Notes**: Directives are resolved once and discarded

### 7.8 Directive Resolution 🔴 HIGH
**Raw LRR Text**: "When resolving a directive, players resolve the outcome that received the most votes and discard the agenda card."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No directive resolution or auto-discard
- **Tests**: No directive resolution tests
- **Assessment**: Directive lifecycle not implemented
- **Priority**: HIGH
- **Dependencies**: Requires voting system and automatic discard
- **Notes**: Directives always go to discard pile after resolution

## Dependencies Summary

### Critical Dependencies
- **Agenda Phase System**: Core phase for agenda resolution (Rule 8)
- **Voting System**: Player voting mechanics with influence values
- **Card Management**: Agenda deck, discard pile, and card drawing
- **Player Play Areas**: For law ownership and placement
- **Rule Modification Framework**: For permanent law effects

### Related Systems
- **Politics Strategy Card**: Provides agenda deck manipulation (Rule 66)
- **Speaker System**: Controls agenda revelation and tie-breaking (Rule 80)
- **Influence System**: Determines voting power via planet exhaustion
- **Status Phase**: May interact with agenda effects
- **Victory Points**: Some agendas award victory points

## Test References
- **Phase Transitions**: `test_game_state_machine.py` includes AGENDA phase
- **No Agenda-Specific Tests**: No voting, law, or directive tests found
- **Missing Coverage**: Agenda card types, voting mechanics, law persistence

## Action Items
1. **Implement agenda card base system** with law/directive types
2. **Create voting mechanics** with influence-based vote casting
3. **Build law persistence system** for permanent rule changes
4. **Implement directive resolution** with one-time effects
5. **Add agenda phase integration** with proper card revelation
6. **Create comprehensive test suite** for all agenda mechanics
7. **Implement speaker tie-breaking** and agenda deck manipulation
