# Rule 81: Status Phase Completion - Implementation Tasks

## Implementation Plan

Convert the Rule 81 (Status Phase) completion design into a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step. Focus ONLY on tasks that involve writing, modifying, or testing code.

## Task List

- [x] 1. Create core status phase infrastructure and data models
  - Create StatusPhaseResult and StepResult data classes with comprehensive fields
  - Create StatusPhaseStepHandler abstract base class with required methods
  - Create StatusPhaseError exception hierarchy for error handling
  - Add type hints and docstrings following project standards
  - _Requirements: 1.1, 11.1, 11.2, 12.4_

- [x] 2. Implement StatusPhaseOrchestrator for step coordination
  - Create StatusPhaseOrchestrator class with step execution logic
  - Implement execute_complete_status_phase method with 8-step sequence
  - Implement execute_step method for individual step execution
  - Add step validation and error handling with graceful degradation
  - _Requirements: 1.1, 1.2, 1.3, 11.3_

- [x] 2.1 Write unit tests for StatusPhaseOrchestrator
  - Test complete status phase execution sequence
  - Test individual step execution and validation
  - Test error handling and graceful degradation scenarios
  - _Requirements: 1.1, 12.3_

- [x] 3. Implement Step 1: Score Objectives functionality
  - Create ScoreObjectivesStep handler class extending StatusPhaseStepHandler
  - Implement initiative order processing for objective scoring
  - Add validation for 1 public + 1 secret objective scoring limits
  - Integrate with existing objective system (Rule 61) for scoring validation
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 10.1_

- [x] 3.1 Write unit tests for ScoreObjectivesStep
  - Test initiative order processing
  - Test objective scoring limits and validation
  - Test integration with objective system
  - _Requirements: 2.1, 12.3_

- [x] 4. Implement Step 2: Reveal Public Objective functionality
  - Create RevealObjectiveStep handler class extending StatusPhaseStepHandler
  - Implement speaker identification and objective revealing logic
  - Add handling for cases when no unrevealed objectives remain
  - Integrate with existing objective system for objective management
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 10.1_

- [x] 4.1 Write unit tests for RevealObjectiveStep
  - Test speaker identification and objective revealing
  - Test edge cases with no unrevealed objectives
  - Test integration with objective system
  - _Requirements: 3.1, 12.3_

- [x] 5. Implement Step 3: Draw Action Cards functionality
  - Create DrawActionCardsStep handler class extending StatusPhaseStepHandler
  - Implement initiative order processing for action card drawing
  - Add handling for empty action card deck scenarios
  - Integrate with existing action card system (Rule 2) for card management
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 10.2_

- [x] 5.1 Write unit tests for DrawActionCardsStep
  - Test initiative order processing for card drawing
  - Test empty deck handling
  - Test integration with action card system
  - _Requirements: 4.1, 12.3_

- [x] 6. Implement Steps 4-5: Command Token Management functionality
  - Create RemoveCommandTokensStep handler for removing tokens from board
  - Create GainRedistributeTokensStep handler for gaining and redistributing tokens
  - Implement token removal, gaining, and redistribution logic
  - Integrate with existing command token system (Rule 20) for token management
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 10.3_

- [x] 6.1 Write unit tests for command token management steps
  - Test token removal from board for all players
  - Test token gaining and redistribution logic
  - Test integration with command token system
  - _Requirements: 5.1, 12.3_

- [x] 7. Enhance Step 6: Ready Cards functionality
  - Create ReadyCardsStep handler that wraps existing ready_all_cards functionality
  - Ensure integration with existing agent readying implementation
  - Add validation that all cards are properly readied
  - Maintain backward compatibility with existing code
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 10.5_

- [x] 7.1 Write unit tests for enhanced ReadyCardsStep
  - Test integration with existing agent readying functionality
  - Test comprehensive card readying validation
  - Test backward compatibility
  - _Requirements: 6.1, 12.3_

- [x] 8. Implement Step 7: Repair Units functionality
  - Create RepairUnitsStep handler class extending StatusPhaseStepHandler
  - Implement damaged unit identification and repair logic
  - Add handling for cases when no damaged units exist
  - Integrate with existing unit system for damage management
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 8.1 Write unit tests for RepairUnitsStep
  - Test damaged unit identification and repair
  - Test edge cases with no damaged units
  - Test integration with unit system
  - _Requirements: 7.1, 12.3_

- [x] 9. Implement Step 8: Return Strategy Cards functionality
  - Create ReturnStrategyCardsStep handler class extending StatusPhaseStepHandler
  - Implement strategy card collection and return to common area logic
  - Add validation that all cards are properly returned
  - Integrate with existing strategy card system (Rule 83) for card management
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 10.4_

- [x] 9.1 Write unit tests for ReturnStrategyCardsStep
  - Test strategy card collection and return logic
  - Test validation of card return completion
  - Test integration with strategy card system
  - _Requirements: 8.1, 12.3_

- [x] 10. Implement StatusPhaseValidator for validation logic
  - Create StatusPhaseValidator class with comprehensive validation methods
  - Implement game state validation for status phase readiness
  - Add step prerequisite validation for each of the 8 steps
  - Add specific validation for objective scoring and token redistribution
  - _Requirements: 11.1, 11.2, 11.4, 11.5_

- [x] 10.1 Write unit tests for StatusPhaseValidator
  - Test game state validation logic
  - Test step prerequisite validation
  - Test specific validation methods
  - _Requirements: 11.1, 12.3_

- [x] 11. Implement RoundTransitionManager for phase transitions
  - Create RoundTransitionManager class with phase transition logic
  - Implement next phase determination (agenda vs strategy phase)
  - Add round counter management and game state updates
  - Integrate with existing phase management system
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 11.1 Write unit tests for RoundTransitionManager
  - Test phase transition logic and determination
  - Test round counter management
  - Test integration with phase management system
  - _Requirements: 9.1, 12.3_

- [x] 12. Enhance StatusPhaseManager with complete functionality
  - Enhance existing StatusPhaseManager class with new orchestrator integration
  - Implement execute_complete_status_phase method as main entry point
  - Add execute_single_step method for individual step execution
  - Maintain existing ready_all_cards method for backward compatibility
  - _Requirements: 1.1, 1.4, 6.5, 12.5_

- [x] 12.1 Write integration tests for enhanced StatusPhaseManager
  - Test complete status phase execution end-to-end
  - Test individual step execution
  - Test backward compatibility with existing functionality
  - _Requirements: 1.1, 12.3, 12.5_

- [x] 13. Implement comprehensive error handling and recovery
  - Add error handling to all step handlers with specific error types
  - Implement graceful degradation for non-critical step failures
  - Add state validation and rollback mechanisms for critical failures
  - Ensure all error messages are descriptive and actionable
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [x] 13.1 Write error handling tests
  - Test error handling for each step handler
  - Test graceful degradation scenarios
  - Test state validation and rollback mechanisms
  - _Requirements: 11.1, 12.3_

- [x] 14. Performance optimization and benchmarking
  - Optimize status phase execution for <500ms total execution time
  - Optimize individual steps for <100ms execution time each
  - Add performance monitoring and benchmarking capabilities
  - Implement memory usage optimization for large game states
  - _Requirements: 12.1, 12.2_

- [x] 14.1 Write performance tests
  - Test complete status phase execution time benchmarks
  - Test individual step execution time benchmarks
  - Test memory usage optimization
  - _Requirements: 12.1, 12.2, 12.3_

- [x] 15. Integration testing and system validation
  - Create comprehensive integration tests with existing game systems
  - Test end-to-end round progression from action phase through status phase
  - Validate agenda phase transition when custodians token removed
  - Validate new round transition when no agenda phase active
  - _Requirements: 9.1, 9.2, 9.3, 10.1, 10.2, 10.3, 10.4, 10.5_

- [x] 15.1 Write comprehensive integration tests
  - Test integration with all existing game systems
  - Test complete round progression scenarios
  - Test phase transition validation
  - _Requirements: 9.1, 10.1, 12.3_

- [x] 16. Documentation and code quality finalization
  - Add comprehensive docstrings to all new classes and methods
  - Update existing StatusPhaseManager documentation
  - Add LRR rule references to all relevant methods
  - Ensure all code passes type checking and linting requirements
  - _Requirements: 12.4, 12.5_

- [x] 16.1 Write documentation tests
  - Test that all public methods have proper docstrings
  - Test that LRR references are accurate and complete
  - Test code quality standards compliance
  - _Requirements: 12.4_

## Success Criteria

Implementation is complete when:
- ✅ All 8 status phase steps are implemented and tested
- ✅ Complete integration with existing game systems (objectives, action cards, command tokens, strategy cards, leaders)
- ✅ 95%+ test coverage achieved across all new functionality
- ✅ Performance benchmarks met (<500ms total, <100ms per step)
- ✅ Round progression functional (status → agenda/strategy phase)
- ✅ Backward compatibility maintained with existing agent readying functionality
- ✅ All code passes type checking and linting requirements
- ✅ Comprehensive error handling and graceful degradation implemented
