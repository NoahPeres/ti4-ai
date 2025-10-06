# Implementation Plan

- [x] 1. Set up core leader system foundation
  - Create base leader enums and data structures
  - Implement abstract BaseLeader class with state management
  - Create LeaderAbilityResult for standardized ability outcomes
  - _Requirements: 1.1, 1.2, 1.3, 8.1, 8.2, 8.3_

- [ ] 2. Implement leader type classes
- [x] 2.1 Create Agent class with ready/exhaust mechanics
  - Implement Agent class extending BaseLeader
  - Add exhaust() and ready() methods for agent-specific state management
  - Implement can_use_ability() validation for readied state
  - Write unit tests for agent state transitions
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 2.2 Create Commander class with unlock mechanics
  - Implement Commander class extending BaseLeader
  - Add unlock() method and unlock condition checking
  - Implement can_use_ability() validation for unlocked state
  - Write unit tests for commander unlock mechanics
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [x] 2.3 Create Hero class with unlock and purge mechanics
  - Implement Hero class extending BaseLeader
  - Add unlock() and purge() methods for hero lifecycle
  - Implement can_use_ability() validation for unlocked but not purged state
  - Write unit tests for hero unlock and purge mechanics
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_

- [ ] 3. Create leader sheet integration
- [x] 3.1 Implement LeaderSheet data structure
  - Create LeaderSheet class to hold player's three leaders
  - Add methods to get leaders by type and retrieve all leaders
  - Integrate LeaderSheet into Player class
  - Write unit tests for leader sheet functionality
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 3.2 Add leader sheet setup and initialization
  - Create leader initialization during game setup
  - Ensure each player gets exactly three leaders for their faction
  - Add validation to prevent invalid leader configurations
  - Write integration tests for leader sheet setup
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 4. Implement leader manager and lifecycle
- [x] 4.1 Create LeaderManager class
  - Implement LeaderManager for coordinating leader operations
  - Add methods for unlock condition checking and ability execution
  - Create leader validation and error handling framework
  - Write unit tests for leader manager functionality
  - _Requirements: 8.1, 8.2, 8.3, 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 4.2 Add status phase integration for agent readying
  - Integrate agent readying into status phase "Ready Cards" step
  - Ensure exhausted agents become readied automatically
  - Add validation to prevent manual agent readying outside status phase
  - Write integration tests for status phase agent readying
  - _Requirements: 2.3, 8.4_

- [ ] 5. Create leader registry and factory system
- [x] 5.1 Implement LeaderRegistry for faction leader definitions
  - Create registry system to store faction-specific leader definitions
  - Add factory methods to create leaders for specific factions
  - Implement leader lookup and validation functionality
  - Write unit tests for registry and factory operations
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 5.2 Add leader ability validation framework
  - Create comprehensive validation for leader ability execution
  - Add timing validation for proper game phase and sequence
  - Implement resource and target validation for abilities
  - Write unit tests for all validation scenarios
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 6. Implement concrete leader examples for architecture validation
- [x] 6.1 Create placeholder leader implementations for testing
  - Implement 2-3 simple placeholder leaders to validate architecture
  - Create leaders with different ability patterns (simple, complex, conditional)
  - Add basic unlock conditions and ability effects for testing
  - Write comprehensive tests for placeholder leader functionality
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 6.2 Test leader ability integration with game systems
  - Validate leader abilities can integrate with combat system
  - Test leader abilities can integrate with resource management
  - Verify leader abilities can integrate with movement system
  - Write integration tests for cross-system leader effects
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 7. Add Alliance promissory note integration
- [x] 7.1 Implement commander ability sharing mechanism
  - Create system for sharing commander abilities via Alliance promissory note
  - Add validation to ensure only unlocked commanders can be shared
  - Implement ability access control for shared commanders
  - Write unit tests for Alliance promissory note sharing
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 7.2 Add Alliance promissory note lifecycle management
  - Integrate Alliance note activation with leader ability access
  - Handle Alliance note return and access revocation
  - Support multiple simultaneous Alliance notes
  - Write integration tests for Alliance note lifecycle
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 8. Create comprehensive error handling and validation
- [x] 8.1 Implement leader-specific exception classes
  - Create LeaderError hierarchy for different error types
  - Add specific exceptions for state errors, unlock errors, and ability errors
  - Implement clear error messages with context information
  - Write unit tests for all error scenarios
  - _Requirements: 8.4, 9.5_

- [x] 8.2 Add comprehensive leader validation framework
  - Create validation for all leader operations and state transitions
  - Add validation for ability execution prerequisites
  - Implement validation for unlock condition checking
  - Write comprehensive validation tests covering edge cases
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 9. Integration testing and system validation
- [x] 9.1 Create end-to-end leader workflow tests
  - Test complete leader lifecycle from setup to ability use
  - Validate agent ready/exhaust cycles through multiple turns
  - Test commander unlock and ongoing ability usage
  - Test hero unlock, ability use, and purging
  - _Requirements: All requirements integrated_

- [x] 9.2 Add game state persistence and loading tests
  - Verify leader states are properly saved and restored
  - Test leader state consistency across game save/load cycles
  - Validate leader ability effects persist correctly
  - Write tests for game state integrity with leaders
  - _Requirements: 8.2, 8.3_

- [ ] 10. Documentation and architecture finalization
- [x] 10.1 Create leader implementation guidelines
  - Document patterns for implementing new faction leaders
  - Create guidelines for ability implementation and integration
  - Document unlock condition patterns and validation
  - Provide examples of different ability complexity levels
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 10.2 Document rule implementation with specific test cases
  - Update .trae/lrr_analysis/51_leaders.md with detailed implementation status
  - Document which test cases demonstrate each sub-rule (51.1-51.12) implementation
  - Add explicit notes about which test methods validate each LRR requirement
  - Include test file references and specific test case names for each sub-rule
  - _Requirements: All requirements documented with test evidence_

- [x] 10.3 Update tracking documents and roadmap
  - Update IMPLEMENTATION_ROADMAP.md to mark Rule 51 as complete
  - Document any architectural decisions and trade-offs made
  - Create foundation for future leader implementations
  - Update overall progress tracking (40/101 rules complete)
  - _Requirements: All requirements documented_
