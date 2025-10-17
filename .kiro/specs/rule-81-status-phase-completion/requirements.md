# Rule 81: Status Phase Completion - Requirements Document

## Introduction

This specification addresses the completion of Rule 81 (Status Phase) implementation for the TI4 AI system. The status phase is the fifth and final phase of each game round, where players score objectives, reveal new public objectives, draw action cards, and prepare for the next round.

**Current Status**: ~30% implemented (only agent readying functionality exists)
**Priority**: HIGH - Critical blocker for complete round management
**Estimated Effort**: 2 weeks development + testing

## Requirements

### Requirement 1: Complete Status Phase Orchestration

**User Story:** As a game system, I want to execute all 8 status phase steps in proper sequence, so that rounds can progress correctly and game state is properly maintained.

#### Acceptance Criteria

1. WHEN the status phase begins THEN the system SHALL execute all 8 steps in the correct LRR sequence
2. WHEN each step completes THEN the system SHALL validate the step was successful before proceeding
3. WHEN any step fails THEN the system SHALL provide clear error messages and halt progression
4. WHEN all steps complete THEN the system SHALL transition to the next game phase appropriately

### Requirement 2: Step 1 - Score Objectives Implementation

**User Story:** As a player, I want to score up to one public and one secret objective during the status phase, so that I can gain victory points according to the rules.

#### Acceptance Criteria

1. WHEN the score objectives step begins THEN the system SHALL process players in initiative order
2. WHEN a player's turn arrives THEN the system SHALL allow scoring up to 1 public objective
3. WHEN a player's turn arrives THEN the system SHALL allow scoring up to 1 secret objective  
4. WHEN a player scores an objective THEN the system SHALL validate the objective requirements are met
5. WHEN a player scores an objective THEN the system SHALL award the appropriate victory points
6. WHEN a player cannot score any objectives THEN the system SHALL skip to the next player

### Requirement 3: Step 2 - Reveal Public Objective Implementation

**User Story:** As the speaker, I want to reveal the next unrevealed public objective during the status phase, so that new objectives become available for future scoring.

#### Acceptance Criteria

1. WHEN the reveal objective step begins THEN the system SHALL identify the current speaker
2. WHEN the speaker is identified THEN the system SHALL reveal the next unrevealed public objective
3. WHEN no unrevealed objectives remain THEN the system SHALL skip this step gracefully
4. WHEN an objective is revealed THEN the system SHALL make it available for future scoring
5. WHEN the objective is revealed THEN the system SHALL notify all players of the new objective

### Requirement 4: Step 3 - Draw Action Cards Implementation

**User Story:** As a player, I want to draw one action card during the status phase, so that I have new action cards available for the next round.

#### Acceptance Criteria

1. WHEN the draw action cards step begins THEN the system SHALL process players in initiative order
2. WHEN a player's turn arrives THEN the system SHALL draw one action card for that player
3. WHEN a player draws a card THEN the system SHALL add it to their hand
4. WHEN the action card deck is empty THEN the system SHALL handle this gracefully
5. WHEN all players have drawn cards THEN the system SHALL proceed to the next step

### Requirement 5: Steps 4-5 - Command Token Management Implementation

**User Story:** As a player, I want my command tokens to be removed from the board and redistributed during the status phase, so that I can prepare for the next round.

#### Acceptance Criteria

1. WHEN step 4 begins THEN the system SHALL remove all command tokens from the game board for all players
2. WHEN tokens are removed THEN the system SHALL return them to each player's reinforcements
3. WHEN step 5 begins THEN the system SHALL give each player 2 additional command tokens
4. WHEN tokens are gained THEN the system SHALL allow redistribution among strategy, tactic, and fleet pools
5. WHEN redistribution occurs THEN the system SHALL validate pool limits are respected

### Requirement 6: Step 6 - Ready Cards Implementation (Enhancement)

**User Story:** As a player, I want all my exhausted cards to be readied during the status phase, so that they are available for use in the next round.

#### Acceptance Criteria

1. WHEN the ready cards step begins THEN the system SHALL ready all exhausted strategy cards
2. WHEN cards are readied THEN the system SHALL ready all exhausted planet cards for all players
3. WHEN cards are readied THEN the system SHALL ready all exhausted technology cards for all players
4. WHEN cards are readied THEN the system SHALL ready all exhausted agent leaders for all players
5. WHEN readying completes THEN the system SHALL verify all cards are in the readied state

### Requirement 7: Step 7 - Repair Units Implementation

**User Story:** As a player, I want all my damaged units to be repaired during the status phase, so that they are at full strength for the next round.

#### Acceptance Criteria

1. WHEN the repair units step begins THEN the system SHALL identify all damaged units for all players
2. WHEN damaged units are found THEN the system SHALL repair them by removing damage tokens
3. WHEN units are repaired THEN the system SHALL update their status to undamaged
4. WHEN no damaged units exist THEN the system SHALL skip this step gracefully
5. WHEN repair completes THEN the system SHALL verify all units are undamaged

### Requirement 8: Step 8 - Return Strategy Cards Implementation

**User Story:** As a player, I want my strategy card to be returned to the common area during the status phase, so that strategy cards are available for the next strategy phase.

#### Acceptance Criteria

1. WHEN the return strategy cards step begins THEN the system SHALL collect all strategy cards from players
2. WHEN cards are collected THEN the system SHALL return them to the common play area
3. WHEN cards are returned THEN the system SHALL reset their exhausted status
4. WHEN all cards are returned THEN the system SHALL make them available for the next strategy phase
5. WHEN return completes THEN the system SHALL verify no players have strategy cards

### Requirement 9: Round Transition Logic Implementation

**User Story:** As a game system, I want to properly transition to the next phase after the status phase, so that the game continues with correct flow.

#### Acceptance Criteria

1. WHEN all status phase steps complete THEN the system SHALL check if the agenda phase is active
2. WHEN the agenda phase is active THEN the system SHALL transition to the agenda phase
3. WHEN the agenda phase is not active THEN the system SHALL start a new round with the strategy phase
4. WHEN transitioning phases THEN the system SHALL update the game state appropriately
5. WHEN the transition completes THEN the system SHALL notify all players of the phase change

### Requirement 10: Integration with Existing Systems

**User Story:** As a developer, I want the status phase to integrate seamlessly with existing game systems, so that the implementation is robust and maintainable.

#### Acceptance Criteria

1. WHEN integrating with objectives THEN the system SHALL use the existing objective scoring system
2. WHEN integrating with action cards THEN the system SHALL use the existing action card system
3. WHEN integrating with command tokens THEN the system SHALL use the existing command token system
4. WHEN integrating with strategy cards THEN the system SHALL use the existing strategy card system
5. WHEN integrating with leaders THEN the system SHALL use the existing leader system (already implemented)

### Requirement 11: Error Handling and Validation

**User Story:** As a game system, I want comprehensive error handling during the status phase, so that the game remains stable and provides clear feedback.

#### Acceptance Criteria

1. WHEN any step encounters an error THEN the system SHALL provide descriptive error messages
2. WHEN validation fails THEN the system SHALL prevent invalid state changes
3. WHEN system integration fails THEN the system SHALL handle gracefully without crashing
4. WHEN edge cases occur THEN the system SHALL have appropriate fallback behavior
5. WHEN errors are resolved THEN the system SHALL allow continuation of the status phase

### Requirement 12: Performance and Quality Standards

**User Story:** As a user, I want the status phase to execute efficiently and maintain high code quality, so that the game runs smoothly.

#### Acceptance Criteria

1. WHEN the complete status phase executes THEN it SHALL complete in under 500ms
2. WHEN individual steps execute THEN each SHALL complete in under 100ms
3. WHEN the implementation is complete THEN it SHALL achieve 95%+ test coverage
4. WHEN code is written THEN it SHALL pass all type checking and linting requirements
5. WHEN integration occurs THEN it SHALL maintain backward compatibility with existing systems