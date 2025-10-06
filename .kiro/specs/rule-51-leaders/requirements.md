# Requirements Document

## Introduction

This document outlines the requirements for implementing Rule 51: LEADERS in the TI4 AI system. Leaders are faction-specific character cards that provide unique abilities throughout the game. Each faction has three types of leaders: one agent, one commander, and one hero, each with distinct mechanics for unlocking, using, and managing their abilities.

## Requirements

### Requirement 1: Leader Types and Basic Structure

**User Story:** As a player, I want each faction to have three distinct leader types (agent, commander, hero) so that I can utilize faction-specific abilities throughout the game.

#### Acceptance Criteria

1. WHEN a faction is selected THEN the system SHALL provide exactly three leader cards: one agent, one commander, and one hero
2. WHEN a leader is created THEN the system SHALL assign it a specific leader type (AGENT, COMMANDER, or HERO)
3. WHEN a leader is queried THEN the system SHALL return its type, faction, name, and current state
4. IF a faction requests more than three leaders THEN the system SHALL reject the request
5. WHEN leaders are initialized THEN each SHALL have faction-specific abilities and unlock conditions

### Requirement 2: Agent Mechanics

**User Story:** As a player, I want to use my faction's agent abilities from the start of the game so that I can gain strategic advantages through repeatable actions.

#### Acceptance Criteria

1. WHEN the game starts THEN agents SHALL begin in a readied state without requiring unlock
2. WHEN an agent ability is used THEN the agent SHALL become exhausted
3. WHEN the status phase "Ready Cards" step occurs THEN exhausted agents SHALL become readied
4. WHEN an agent is exhausted THEN its abilities SHALL be unavailable until readied
5. IF an agent ability is attempted while exhausted THEN the system SHALL reject the action

### Requirement 3: Commander Mechanics and Unlock System

**User Story:** As a player, I want to unlock my commander by meeting specific conditions so that I can access powerful ongoing abilities.

#### Acceptance Criteria

1. WHEN the game starts THEN commanders SHALL begin in a locked state
2. WHEN unlock conditions are met THEN the commander SHALL become unlocked automatically
3. WHEN a commander is unlocked THEN its abilities SHALL become available for use
4. WHEN a commander is unlocked THEN it SHALL remain unlocked for the rest of the game
5. WHEN a commander ability is used THEN the commander SHALL NOT become exhausted
6. IF commander abilities are attempted while locked THEN the system SHALL reject the action

### Requirement 4: Hero Mechanics and Unlock System

**User Story:** As a player, I want to unlock my hero by meeting specific conditions and use its powerful one-time ability so that I can create game-changing moments.

#### Acceptance Criteria

1. WHEN the game starts THEN heroes SHALL begin in a locked state
2. WHEN unlock conditions are met THEN the hero SHALL become unlocked automatically
3. WHEN a hero ability is resolved THEN the hero SHALL be purged from the game
4. WHEN a hero is purged THEN its abilities SHALL become permanently unavailable
5. WHEN a hero ability is used THEN it SHALL NOT cause exhaustion (since it's purged)
6. IF hero abilities are attempted while locked THEN the system SHALL reject the action
7. IF hero abilities are attempted after purging THEN the system SHALL reject the action

### Requirement 5: Leader Sheet Integration

**User Story:** As a player, I want my leaders to be properly placed on my leader sheet during setup so that I can track their states and abilities.

#### Acceptance Criteria

1. WHEN game setup occurs THEN all leaders SHALL be placed on the player's leader sheet
2. WHEN a leader state changes THEN the leader sheet SHALL reflect the updated state
3. WHEN leaders are queried THEN the system SHALL provide their current positions and states
4. WHEN the leader sheet is accessed THEN it SHALL show all three leaders with their current states
5. IF leaders are accessed outside the leader sheet THEN the system SHALL redirect to the leader sheet

### Requirement 6: Alliance Promissory Note Integration

**User Story:** As a player, I want to share my commander's ability with another player through the Alliance promissory note so that I can form strategic partnerships.

#### Acceptance Criteria

1. WHEN an Alliance promissory note is played THEN the target player SHALL gain access to the commander's ability
2. WHEN a shared commander ability is used THEN it SHALL function identically to the original
3. WHEN the Alliance promissory note is returned THEN the shared access SHALL be revoked
4. WHEN multiple Alliance notes are active THEN each SHALL provide independent access
5. IF a commander is locked THEN Alliance promissory notes SHALL NOT provide access to its abilities

### Requirement 7: Faction-Specific Leader Abilities

**User Story:** As a player, I want each faction's leaders to have unique abilities that reflect their faction's theme so that different factions provide distinct gameplay experiences.

#### Acceptance Criteria

1. WHEN leaders are created THEN each SHALL have faction-specific abilities defined
2. WHEN leader abilities are used THEN they SHALL produce faction-appropriate effects
3. WHEN unlock conditions are checked THEN they SHALL be faction-specific and thematically appropriate
4. WHEN multiple factions are in play THEN each SHALL have completely different leader abilities
5. IF generic leader abilities are requested THEN the system SHALL reject the request

### Requirement 8: Leader State Management

**User Story:** As a player, I want the system to properly track leader states (locked/unlocked, readied/exhausted, active/purged) so that leader mechanics function correctly throughout the game.

#### Acceptance Criteria

1. WHEN leader states change THEN the system SHALL persist the new state
2. WHEN game state is saved/loaded THEN leader states SHALL be preserved accurately
3. WHEN leader states are queried THEN the system SHALL return current, accurate information
4. WHEN invalid state transitions are attempted THEN the system SHALL reject them with clear error messages
5. WHEN the game progresses THEN leader states SHALL be automatically updated based on game events

### Requirement 9: Leader Ability Validation and Timing

**User Story:** As a player, I want leader abilities to be validated for proper timing and game state so that they can only be used when legally allowed.

#### Acceptance Criteria

1. WHEN leader abilities are attempted THEN the system SHALL validate current game phase and timing
2. WHEN prerequisites are not met THEN the system SHALL reject the ability with explanatory messages
3. WHEN abilities have resource costs THEN the system SHALL validate resource availability
4. WHEN abilities target other players/components THEN the system SHALL validate target legality
5. IF abilities are used out of sequence THEN the system SHALL provide guidance on proper timing

### Requirement 10: Leader Integration with Game Systems

**User Story:** As a player, I want leader abilities to properly integrate with other game systems (combat, production, movement, etc.) so that they enhance gameplay without breaking existing mechanics.

#### Acceptance Criteria

1. WHEN leader abilities affect combat THEN they SHALL integrate with the combat system properly
2. WHEN leader abilities affect resources THEN they SHALL integrate with the resource management system
3. WHEN leader abilities affect movement THEN they SHALL integrate with the movement system
4. WHEN leader abilities create ongoing effects THEN they SHALL be tracked by the appropriate game systems
5. WHEN leader abilities conflict with other rules THEN the system SHALL resolve conflicts according to LRR precedence rules
