# Implementation Plan - Rule 92: Trade Strategy Card

Convert the feature design into a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step. Focus ONLY on tasks that involve writing, modifying, or testing code.

## Implementation Tasks

- [x] 1. Research existing strategy card patterns and set up test foundation
  - Examine existing strategy card implementations (Leadership, Politics, Construction) for integration patterns
  - Create comprehensive test file `tests/test_rule_92_end_to_end_integration.py` following existing test patterns
  - Implement basic TradeStrategyCard class inheriting from BaseStrategyCard with proper interface compliance
  - Write tests for basic properties (initiative value 5, card type TRADE) following existing test patterns
  - Ensure integration with existing BaseStrategyCard framework and StrategyCardAbilityResult patterns
  - _Requirements: 1.1, 1.2, 1.3, 6.1, 6.2_

- [x] 2. Implement primary ability Step 1 - Gain Trade Goods
  - Write failing tests for trade goods gain (3 trade goods awarded to active player)
  - Implement _gain_trade_goods() method with resource management integration
  - Add validation for commodity limits
  - Write comprehensive tests for trade goods gain scenarios including edge cases
  - _Requirements: 2.1, 2.2, 2.3, 7.1_

- [x] 3. Implement primary ability Step 2 - Replenish Commodities
  - Write failing tests for commodity replenishment to faction maximum
  - Implement _replenish_commodities() method with faction limit integration
  - Add validation for players already at maximum commodities
  - Write tests for various faction commodity limits and current commodity levels
  - _Requirements: 3.1, 3.2, 3.3, 7.2_

- [x] 4. Implement primary ability Step 3 - Choose Players for Free Secondary
  - Write failing tests for player selection mechanism
  - Implement _process_chosen_players() method to track selected players
  - Add validation for player selection (valid player IDs, cannot choose self)
  - Write tests for player selection scenarios (all players, no players, invalid players)
  - _Requirements: 4.1, 4.2, 4.3, 8.1, 9.1_

- [x] 5. Integrate primary ability steps into complete workflow
  - Write failing tests for complete primary ability execution sequence
  - Implement execute_primary_ability() method orchestrating all three steps
  - Add comprehensive error handling and rollback capability
  - Write integration tests for complete primary ability workflow
  - _Requirements: 6.1, 6.2, 9.2, 9.3_

- [x] 6. Implement secondary ability with command token validation
  - Write failing tests for secondary ability command token cost
  - Implement execute_secondary_ability() method with command token spending
  - Add validation for command token availability in strategy pool
  - Write tests for secondary ability scenarios (with/without tokens, free execution)
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 7.3_

- [x] 7. Implement multi-player secondary ability support
  - Write failing tests for multiple players using secondary ability concurrently
  - Enhance secondary ability to handle chosen players (free execution)
  - Add tracking for which players were chosen by active player
  - Write comprehensive tests for multi-player scenarios and concurrent execution
  - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [x] 8. Integrate with strategy card coordinator and game state management
  - Write failing tests for strategy card registration and coordinator integration
  - Update strategy card registry to include TradeStrategyCard with proper StrategyCardType.TRADE mapping
  - Ensure proper integration with StrategyCardCoordinator execution workflow and initiative ordering
  - Validate integration with existing BaseStrategyCard interface and StrategyCardAbilityResult patterns
  - Write integration tests for complete strategy card system integration including phase management
  - _Requirements: 6.3, 6.4, 1.3_

- [x] 9. Implement comprehensive error handling and validation
  - Write failing tests for all error conditions (invalid players, missing resources, corrupted state)
  - Implement TradeValidationError and related exception classes
  - Add comprehensive input validation for all public methods
  - Write tests for error handling and graceful degradation scenarios
  - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [x] 10. Performance optimization and quality assurance
  - Write performance tests to validate execution time requirements (<50ms primary, <25ms secondary)
  - Optimize resource management operations for batch updates
  - Add performance benchmarking and monitoring
  - Ensure 95%+ test coverage and all quality gates pass
  - _Requirements: 11.1, 11.2, 11.3, 11.4_

- [x] 11. Update documentation and tracking files
  - Update `.trae/lrr_analysis/92_trade_strategy_card.md` with complete implementation status
  - Update `IMPLEMENTATION_ROADMAP.md` to mark Rule 92 as complete
  - Update `CRITICAL_PATH_IMPLEMENTATION_SEQUENCE.md` with progress
  - Add comprehensive docstrings and code documentation
  - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [x] 12. Validate integration with existing game frameworks and systems
  - Write integration tests with ResourceManagement system for trade goods and commodities
  - Validate integration with CommandTokenSystem for strategy pool token spending
  - Test integration with GameState management and player resource tracking
  - Verify compatibility with existing strategy card execution patterns used by other cards
  - Ensure proper integration with multi-player game mechanics and turn management
  - _Requirements: 6.4, 7.1, 7.2, 7.3, 8.4_

- [x] 13. Final integration testing and production readiness
  - Write end-to-end integration tests with complete game scenarios including other strategy cards
  - Validate Trade card works correctly in initiative order with other strategy cards
  - Perform regression testing to ensure no existing functionality is broken
  - Test integration with game phase management and round progression
  - Complete final quality assurance and mark Rule 92 as production ready
  - _Requirements: 6.4, 7.4, 11.4_
