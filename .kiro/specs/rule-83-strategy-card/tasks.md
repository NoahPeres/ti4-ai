# Implementation Plan

- [x] 1. Create core strategy card coordinator with existing system integration
  - Implement lightweight StrategyCardCoordinator class that integrates with existing StrategicActionManager
  - Add basic card assignment and tracking functionality
  - Implement initiative order calculation as pure function
  - Create integration points with existing game state system
  - _Requirements: 1.1, 1.2, 1.3, 6.1, 6.2_

- [x] 2. Implement strategy phase card selection mechanics
  - Add card selection workflow that integrates with existing phase management
  - Implement speaker order-based selection process
  - Add card availability tracking and validation
  - Create player assignment management with existing player system integration
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 3. Create initiative order determination system
  - Implement initiative calculation logic using existing StrategyCardType enum
  - Add player ordering based on strategy card initiative numbers
  - Create initiative order query methods for action and status phases
  - Integrate with existing game phase management system
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 4. Implement strategy card state management
  - Add readied/exhausted state tracking for strategy cards
  - Implement card state transitions during strategic actions
  - Create status phase card readying functionality
  - Integrate state management with existing StrategicActionManager
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 5. Extend strategic action manager for strategy card integration
  - Enhance existing StrategicActionManager to work with StrategyCardCoordinator
  - Add strategy card validation to existing strategic action workflow
  - Implement card exhaustion during strategic action resolution
  - Ensure backward compatibility with existing Rule 82 and Rule 91 implementations
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 6. Create primary and secondary ability framework
  - Implement ability restriction validation using existing strategic action patterns
  - Add primary ability access control for card owners
  - Create secondary ability framework for non-owners
  - Integrate with existing strategic action participant tracking
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 7. Add multi-player game support
  - Implement flexible player count handling (3-8 players)
  - Add support for unselected cards in smaller games
  - Create dynamic speaker order management
  - Integrate with existing player management system
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 8. Implement strategy card information access for AI
  - Create comprehensive card information query methods
  - Add AI-friendly strategy card evaluation interfaces
  - Implement game state analysis methods for strategic planning
  - Integrate with existing AI decision-making frameworks
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [x] 9. Add comprehensive error handling and validation
  - Implement robust input validation following existing patterns
  - Add descriptive error messages for invalid operations
  - Create edge case handling for system state inconsistencies
  - Integrate with existing error handling and logging systems
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 10. Implement round management and card reset functionality
  - Add round transition handling for strategy card reset
  - Implement card redistribution to common play area
  - Create round lifecycle management integration
  - Add proper cleanup and state reset between rounds
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [x] 11. Create base strategy card implementation pattern
  - Implement BaseStrategyCard class following TechnologyStrategyCard pattern
  - Create strategy card registry system for all 8 cards
  - Add card-specific ability framework using existing patterns
  - Ensure compatibility with existing strategic action resolution
  - _Requirements: 5.1, 5.7, 6.1, 6.3_

- [x] 12. Implement individual strategy card classes
  - Create LeadershipStrategyCard following established patterns
  - Implement DiplomacyStrategyCard with proper ability definitions
  - Add PoliticsStrategyCard and ConstructionStrategyCard implementations
  - Create TradeStrategyCard and WarfareStrategyCard classes
  - Implement ImperialStrategyCard (Technology already exists from Rule 91)
  - _Requirements: 1.1, 5.1, 8.1_

- [x] 13. Add comprehensive integration testing
  - Create integration tests with existing Rule 82 (Strategic Action) system
  - Test compatibility with existing Rule 91 (Technology Strategy Card)
  - Add game state integration testing for strategy card assignments
  - Create end-to-end workflow tests for complete card selection and usage cycles
  - _Requirements: 6.1, 6.2, 6.3, 6.5_

- [x] 14. Implement game state extensions
  - Add minimal strategy card tracking fields to existing GameState
  - Implement state persistence for card assignments and exhaustion
  - Create state synchronization with StrategyCardCoordinator
  - Ensure backward compatibility with existing game state management
  - _Requirements: 1.3, 4.5, 6.2, 10.2_

- [x] 15. Add comprehensive system validation and testing
  - Run full test suite to ensure no regressions in existing systems
  - Validate integration with all existing strategy card implementations
  - Test multi-player scenarios with different player counts
  - Verify AI decision-making interfaces work correctly
  - Create performance testing for strategy card operations
  - _Requirements: 6.4, 7.1, 8.5, 9.4_