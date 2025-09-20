# Implementation Plan

- [x] 1. Fix existing test failures and stabilize codebase
- [x] 1.1 Fix game controller exception test
  - Update test to expect `InvalidPlayerError` instead of `ValueError`
  - Verify exception message matching works correctly
  - Ensure proper import of custom exception in test
  - _Requirements: 1.1, 1.4_

- [x] 1.2 Fix movement validation logic
  - Debug why `MovementValidator.is_valid_movement()` returns False for adjacent systems
  - Implement proper adjacency checking in movement validation
  - Add missing galaxy coordinate system integration
  - Write unit tests for movement validator edge cases
  - _Requirements: 1.1, 1.3_

- [x] 1.3 Fix integration test failures
  - Resolve faction-specific unit statistics calculation issues
  - Fix unit movement range calculations in integration scenarios
  - Ensure proper technology upgrade application in tests
  - Add debugging output for failed integration test scenarios
  - _Requirements: 1.1, 1.2_

- [x] 1.4 Verify all tests pass consistently
  - Run full test suite and confirm zero failures
  - Add any missing test coverage for fixed issues
  - Update test documentation for changed behavior
  - _Requirements: 1.1, 1.5_

- [x] 2. Implement Command pattern for game actions
- [x] 2.1 Create base command interface and infrastructure
  - Implement `GameCommand` abstract base class with execute/undo methods
  - Create `CommandManager` class for command history and execution
  - Add command validation interface with `can_execute` method
  - Write unit tests for command interface contract
  - _Requirements: 2.1, 2.2_

- [x] 2.2 Convert existing actions to command pattern
  - Refactor `MovementAction` to implement `GameCommand` interface
  - Add undo data collection for movement commands
  - Implement undo logic for movement (restore previous positions)
  - Write tests for movement command execute/undo cycle
  - _Requirements: 2.1, 2.3_

- [x] 2.3 Implement command history and replay system
  - Add command storage and retrieval in `CommandManager`
  - Implement replay functionality from initial game state
  - Create command serialization for persistence
  - Write integration tests for command replay scenarios
  - _Requirements: 2.4, 2.5_

- [x] 2.4 Add undo/redo functionality to game controller
  - Integrate `CommandManager` into `GameController`
  - Add public methods for undo/redo operations
  - Implement stack-based undo with proper ordering
  - Write tests for multi-command undo scenarios
  - _Requirements: 2.4, 2.1_

- [x] 3. Implement Observer pattern for game events
- [x] 3.1 Create event system infrastructure
  - Implement `GameEventBus` class with subscribe/unsubscribe methods
  - Create base `GameEvent` class with common event properties
  - Add event publishing mechanism with error isolation
  - Write unit tests for event bus functionality
  - _Requirements: 3.1, 3.4_

- [x] 3.2 Define core game events
  - Create `UnitMovedEvent`, `CombatStartedEvent`, `PhaseChangedEvent` classes
  - Add event data structures with all necessary context
  - Implement event factory methods for consistent creation
  - Write tests for event creation and data validation
  - _Requirements: 3.2, 3.5_

- [x] 3.3 Integrate event publishing into game actions
  - Add event publishing to movement execution
  - Publish phase transition events from game controller
  - Add combat initiation event publishing
  - Write integration tests for event publication during gameplay
  - _Requirements: 3.1, 3.2_

- [x] 3.4 Create example event observers
  - Implement logging observer for game events
  - Create statistics collector observer
  - Add AI training data collector observer
  - Write tests for observer registration and notification
  - _Requirements: 3.1, 3.4_

- [-] 4. Implement State Machine for game phases
- [x] 4.1 Create game phase state machine
  - Implement `GameStateMachine` class with phase transition validation
  - Define valid phase transitions in transition map
  - Add current phase tracking and state queries
  - Write unit tests for phase transition validation
  - _Requirements: 5.1, 5.2_

- [ ] 4.2 Integrate state machine into game controller
  - Replace simple phase enum with state machine in `GameController`
  - Add phase transition validation before phase changes
  - Implement automatic phase progression where appropriate
  - Write tests for invalid phase transition rejection
  - _Requirements: 5.2, 5.3_

- [ ] 4.3 Add phase-specific action validation
  - Implement phase constraint checking in action validation
  - Add phase-specific legal move filtering
  - Create phase transition condition checking
  - Write integration tests for phase-specific behavior
  - _Requirements: 5.3, 5.4_

- [ ] 4.4 Enhance phase transition debugging
  - Add detailed logging for phase transitions
  - Implement phase state inspection methods
  - Create debugging utilities for phase-related issues
  - Write tests for phase state information access
  - _Requirements: 5.5, 7.5_

- [x] 5. Implement Builder pattern for test scenarios
- [x] 5.1 Create game scenario builder infrastructure
  - Implement `GameScenarioBuilder` class with fluent interface
  - Add builder methods for players, galaxy, and phase configuration
  - Implement validation for builder configuration consistency
  - Write unit tests for builder interface and validation
  - _Requirements: 4.1, 4.2_

- [x] 5.2 Add complex scenario building capabilities
  - Implement unit placement methods in builder
  - Add resource and technology configuration options
  - Create preset scenario factory methods
  - Write tests for complex scenario construction
  - _Requirements: 4.3, 4.4_

- [x] 5.3 Integrate builder into existing tests
  - Refactor integration tests to use scenario builder
  - Replace manual test setup with builder patterns
  - Add builder-based test utilities for common scenarios
  - Verify all refactored tests pass with new builder
  - _Requirements: 4.1, 4.5_

- [x] 5.4 Create comprehensive test scenario library
  - Implement standard game scenarios (early game, mid game, combat)
  - Add faction-specific test scenarios
  - Create edge case scenarios for boundary testing
  - Write documentation for scenario library usage
  - _Requirements: 4.3, 4.5_

- [x] 6. Implement performance optimization layer
- [x] 6.1 Add caching for expensive operations
  - Implement `GameStateCache` for legal move generation
  - Add caching for pathfinding and adjacency calculations
  - Create cache invalidation strategies for state changes
  - Write performance tests for cache effectiveness
  - _Requirements: 6.1, 6.4_

- [x] 6.2 Optimize critical performance paths
  - Profile game state operations to identify bottlenecks
  - Optimize unit statistics calculation and lookup
  - Improve movement validation performance
  - Write benchmark tests for performance regression detection
  - _Requirements: 6.1, 6.2_

- [x] 6.3 Add resource management and monitoring
  - Implement memory usage tracking for game states
  - Add performance metrics collection
  - Create resource cleanup for long-running games
  - Write tests for resource management effectiveness
  - _Requirements: 6.2, 6.3_

- [x] 6.4 Implement concurrent game support
  - Add thread safety to shared components
  - Implement game instance isolation
  - Create concurrent game testing framework
  - Write stress tests for multiple simultaneous games
  - _Requirements: 6.5, 6.3_

- [x] 7. Enhance error handling and logging
- [x] 7.1 Implement comprehensive exception hierarchy
  - Create `CommandExecutionError` and `PhaseTransitionError` classes
  - Add context information to all custom exceptions
  - Implement exception chaining for root cause analysis
  - Write tests for exception creation and context preservation
  - _Requirements: 7.2, 7.4_

- [x] 7.2 Add structured logging system
  - Implement `GameLogger` class with structured data logging
  - Add command execution logging with context
  - Create event logging for game state changes
  - Write tests for logging output and formatting
  - _Requirements: 7.1, 7.5_

- [x] 7.3 Implement error recovery mechanisms
  - Add graceful degradation for non-critical failures
  - Implement automatic retry for transient errors
  - Create error recovery strategies for different failure types
  - Write tests for error recovery scenarios
  - _Requirements: 7.3, 7.4_

- [x] 7.4 Add debugging and diagnostic tools
  - Create game state inspection utilities
  - Implement command history analysis tools
  - Add performance profiling helpers
  - Write integration tests for diagnostic tool accuracy
  - _Requirements: 7.5, 7.1_

- [x] 8. Code quality improvements and cleanup
- [x] 8.1 Eliminate code duplication
  - Extract common validation logic into shared utilities
  - Create reusable components for similar functionality
  - Refactor repeated patterns into helper methods
  - Write tests to ensure refactored code maintains behavior
  - _Requirements: 8.1, 8.5_

- [x] 8.2 Replace magic numbers and strings with constants
  - Move hardcoded values to constants module
  - Create named constants for game rules and limits
  - Add configuration classes for complex settings
  - Write tests to verify constant usage correctness
  - _Requirements: 8.2, 8.5_

- [x] 8.3 Improve method and variable naming
  - Rename unclear variables and methods for better readability
  - Add comprehensive docstrings to public interfaces
  - Standardize naming conventions across the codebase
  - Update tests to reflect renamed components
  - _Requirements: 8.4, 8.5_

- [x] 8.4 Break down complex methods
  - Identify methods with high cyclomatic complexity
  - Extract helper methods for complex logic
  - Simplify conditional statements and loops
  - Write unit tests for extracted helper methods
  - _Requirements: 8.3, 8.5_

- [x] 9. Final integration and validation
- [x] 9.1 Run comprehensive test suite
  - Execute all unit tests and verify 100% pass rate
  - Run integration tests with new patterns
  - Perform property-based testing for invariants
  - Validate test coverage meets requirements (>85%)
  - _Requirements: 1.1, 1.5_

- [x] 9.2 Performance validation and benchmarking
  - Run performance benchmarks for all optimized components
  - Validate memory usage stays within acceptable limits
  - Test concurrent game scenarios for stability
  - Document performance characteristics and limitations
  - _Requirements: 6.1, 6.2, 6.5_

- [x] 9.3 Documentation and code review
  - Update API documentation for all new interfaces
  - Create usage examples for new patterns
  - Conduct thorough code review of all changes
  - Update project documentation with architectural changes
  - _Requirements: 8.5, 7.5_
