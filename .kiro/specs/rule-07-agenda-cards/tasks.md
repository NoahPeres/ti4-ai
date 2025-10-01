# Implementation Plan: Rule 7 - AGENDA CARDS

## Overview

Convert the Rule 7: AGENDA CARDS design into a series of TDD implementation tasks. Each task builds incrementally on existing systems, following strict RED-GREEN-REFACTOR methodology and the established technology card framework patterns.

## Implementation Tasks

- [ ] 1. Set up agenda card framework infrastructure
  - Create test file `tests/test_rule_07_agenda_cards.py` with basic test structure
  - Implement base agenda card classes (`BaseAgendaCard`, `LawCard`, `DirectiveCard`)
  - Create `AgendaCardRegistry` following technology card registry patterns
  - Write failing tests for basic agenda card interface
  - _Requirements: 1.1, 1.2, 1.3_

- [ ] 2. Implement agenda card type system and enums
  - [ ] 2.1 Create agenda card enums and constants
    - Write failing tests for `AgendaType` enum (LAW, DIRECTIVE)
    - Implement voting outcome constants and patterns
    - Add agenda card identification methods
    - Create agenda card metadata structures
    - _Requirements: 2.1, 2.2, 2.3_

  - [ ] 2.2 Implement base agenda card protocols
    - Write failing tests for agenda card interface compliance
    - Create `AgendaCardProtocol` following technology card patterns
    - Implement base card validation methods
    - Add card name and type identification
    - _Requirements: 2.1, 2.2, 2.4, 2.5_

- [ ] 3. Enhance agenda deck management system
  - [ ] 3.1 Extend existing AgendaDeck with card framework integration
    - Write failing tests for agenda deck with concrete card instances
    - Integrate `AgendaCardRegistry` with existing `AgendaDeck`
    - Implement deck initialization with registered cards
    - Add deck shuffling and drawing with proper card instances
    - _Requirements: 5.1, 5.2, 5.3_

  - [ ] 3.2 Implement agenda deck state management
    - Write failing tests for deck persistence and state tracking
    - Add discard pile management for agenda cards
    - Implement deck reshuffling when empty
    - Create deck state validation and error handling
    - _Requirements: 5.4, 5.5_

- [ ] 4. Implement law persistence and tracking system
  - [ ] 4.1 Create ActiveLaw data structure and manager
    - Write failing tests for law persistence across game rounds
    - Implement `ActiveLaw` dataclass with law metadata
    - Create `LawManager` for tracking active laws
    - Add law application and removal methods
    - _Requirements: 6.1, 6.2, 6.3_

  - [ ] 4.2 Integrate law system with game state
    - Write failing tests for law effects on game mechanics
    - Extend existing `GameState` to track active laws
    - Implement law effect checking during game actions
    - Add law conflict detection and resolution
    - _Requirements: 6.4, 6.5_

- [ ] 5. Create agenda effect resolution system
  - [ ] 5.1 Implement AgendaEffectResolver
    - Write failing tests for agenda outcome resolution
    - Create `AgendaEffectResolver` class with outcome handling
    - Implement law enactment vs directive execution logic
    - Add election outcome processing
    - _Requirements: 3.1, 3.2, 3.3_

  - [ ] 5.2 Add voting outcome validation and processing
    - Write failing tests for voting outcome validation
    - Implement outcome validation against card specifications
    - Add election target validation and processing
    - Create comprehensive error handling for invalid outcomes
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 6. Implement first concrete agenda cards (Laws)
  - [ ] 6.1 Implement Anti-Intellectual Revolution law card
    - Write failing tests for Anti-Intellectual Revolution effects
    - Create concrete `AntiIntellectualRevolution` class extending `LawCard`
    - Implement FOR effect (destroy ship after tech research)
    - Implement AGAINST effect (exhaust planets for technologies)
    - _Requirements: 7.1, 7.2, 7.3_

  - [ ] 6.2 Implement Fleet Regulations law card
    - Write failing tests for Fleet Regulations effects
    - Create concrete `FleetRegulations` class extending `LawCard`
    - Implement FOR effect (4 token fleet pool limit)
    - Implement AGAINST effect (add fleet pool token)
    - _Requirements: 7.1, 7.2, 7.3_

- [ ] 7. Implement first concrete agenda cards (Directives)
  - [ ] 7.1 Implement Classified Document Leaks directive
    - Write failing tests for Classified Document Leaks mechanics
    - Create concrete `ClassifiedDocumentLeaks` class extending `DirectiveCard`
    - Implement reveal condition checking (no scored secrets)
    - Implement election outcome (make secret objective public)
    - _Requirements: 7.1, 7.2, 7.4_

  - [ ] 7.2 Implement Committee Formation directive
    - Write failing tests for Committee Formation mechanics
    - Create concrete `CommitteeFormation` class extending `DirectiveCard`
    - Implement pre-vote election override mechanics
    - Add special voting bypass functionality
    - _Requirements: 7.1, 7.2, 7.4_

- [ ] 8. Implement election-based agenda cards
  - [ ] 8.1 Create election outcome handling framework
    - Write failing tests for planet and player election mechanics
    - Implement election target validation (cultural/industrial/hazardous planets)
    - Add player election validation and processing
    - Create election result integration with agenda effects
    - _Requirements: 4.1, 4.2, 4.5_

  - [ ] 8.2 Implement Minister cards (elected player effects)
    - Write failing tests for Minister of Commerce card
    - Create concrete `MinisterOfCommerce` class with elected player mechanics
    - Implement ongoing elected player abilities
    - Add minister card ownership and effect tracking
    - _Requirements: 7.1, 7.2, 7.3, 7.5_

- [ ] 9. Integrate with existing agenda phase system
  - [ ] 9.1 Enhance AgendaPhase with card framework
    - Write failing tests for agenda phase with concrete cards
    - Integrate `AgendaCardRegistry` with existing `AgendaPhase`
    - Update agenda revelation to use concrete card instances
    - Modify voting integration to work with card-specific outcomes
    - _Requirements: 4.1, 4.2, 4.3_

  - [ ] 9.2 Update voting system integration
    - Write failing tests for voting with agenda card validation
    - Enhance existing `VotingSystem` to validate against card outcomes
    - Implement election voting mechanics for agenda cards
    - Add agenda-specific voting validation and error handling
    - _Requirements: 4.4, 4.5_

- [ ] 10. Implement comprehensive agenda card set (Base Game)
  - [ ] 10.1 Implement remaining law cards
    - Write failing tests for all remaining base game law cards
    - Create concrete implementations for: Conventions of War, Enforced Travel Ban, Executive Sanctions, Homeland Defense Act, Publicize Weapon Schematics, Regulated Conscription, Shared Research, Wormhole Reconstruction
    - Implement all FOR/AGAINST effects for each law
    - Add proper law persistence and game integration
    - _Requirements: 7.1, 7.2, 7.3_

  - [ ] 10.2 Implement remaining directive cards
    - Write failing tests for all remaining base game directive cards
    - Create concrete implementations for all planet attachment cards (Core Mining, Demilitarized Zone, Senate Sanctuary, Terraforming Initiative)
    - Implement all research team cards with technology prerequisite effects
    - Add special directive cards (Shard of the Throne, Crown cards)
    - _Requirements: 7.1, 7.2, 7.4_

- [ ] 11. Implement advanced agenda mechanics
  - [ ] 11.1 Add planet attachment system
    - Write failing tests for agenda cards that attach to planets
    - Implement planet attachment mechanics for relevant cards
    - Add attached card effect tracking and persistence
    - Create planet attachment validation and error handling
    - _Requirements: 3.4, 3.5_

  - [ ] 11.2 Implement victory point agenda cards
    - Write failing tests for victory point granting agenda cards
    - Create Shard of the Throne and Crown cards with VP mechanics
    - Implement VP gain/loss on ownership transfer
    - Add combat and control-based ownership changes
    - _Requirements: 3.3, 3.4, 3.5_

- [ ] 12. Create comprehensive error handling and validation
  - [ ] 12.1 Implement agenda card validation system
    - Write failing tests for all error scenarios
    - Create `AgendaCardValidationError` and related exceptions
    - Implement comprehensive input validation for all card operations
    - Add graceful error recovery and user feedback
    - _Requirements: 8.1, 8.2, 8.3_

  - [ ] 12.2 Add law conflict detection and resolution
    - Write failing tests for law conflict scenarios
    - Implement law replacement detection (e.g., multiple Minister cards)
    - Add automatic law removal when conflicts occur
    - Create clear conflict resolution messaging
    - _Requirements: 8.4, 8.5_

- [ ] 13. Implement game state integration and persistence
  - [ ] 13.1 Extend GameState for agenda card tracking
    - Write failing tests for agenda card state persistence
    - Add agenda deck state to existing `GameState`
    - Implement active law persistence across game saves
    - Create agenda card state synchronization
    - _Requirements: 6.1, 6.2, 6.5_

  - [ ] 13.2 Add agenda card effect integration with existing systems
    - Write failing tests for agenda effects on existing game mechanics
    - Integrate law effects with movement, production, combat systems
    - Add agenda card interaction with technology research
    - Create comprehensive cross-system effect validation
    - _Requirements: 3.1, 3.2, 3.3, 6.3, 6.4_

- [ ] 14. Create comprehensive integration tests and documentation
  - [ ] 14.1 Implement end-to-end agenda card scenarios
    - Write integration tests for complete agenda phase workflows
    - Test law enactment and persistent effects across multiple rounds
    - Test directive execution and immediate effects
    - Test election mechanics with all card types
    - _Requirements: All requirements integration_

  - [ ] 14.2 Update documentation and create usage examples
    - Create comprehensive agenda card framework documentation
    - Add examples for implementing new agenda cards
    - Update existing agenda phase documentation
    - Create troubleshooting guide for agenda card issues
    - _Requirements: Documentation and framework extensibility_

## Quality Gates

Each task must meet the following criteria before proceeding:
- ✅ All tests pass with proper RED-GREEN-REFACTOR cycle
- ✅ Type checking passes with `make type-check`
- ✅ Code formatting and linting pass
- ✅ Integration with existing agenda phase maintained
- ✅ Comprehensive error handling implemented
- ✅ Documentation updated with card implementation examples

## Success Criteria

- All base game agenda cards implemented as individual classes
- Complete law persistence system integrated with game state
- Full integration with existing voting and agenda phase systems
- Comprehensive test coverage (95%+) with clear test case to card mapping
- All existing tests continue to pass (backward compatibility)
- Performance meets established benchmarks (<100ms response time)
- Framework ready for Prophecy of Kings expansion cards
- Documentation includes clear examples for adding new agenda cards

## Framework Extensibility

The implementation should provide:
- Clear patterns for implementing new agenda cards
- Extensible base classes for different agenda card types
- Registry system that automatically discovers new card implementations
- Comprehensive testing patterns for agenda card validation
- Integration points for expansion content (POK agenda cards)
