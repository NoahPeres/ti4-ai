# Implementation Plan

- [x] 1. Set up core resource management data structures
  - Create `ResourceSources` and `InfluenceSources` dataclasses for resource breakdown tracking
  - Create `SpendingPlan`, `ResourceSpending`, and `InfluenceSpending` dataclasses for spending operations
  - Create `ProductionCost` dataclass for production cost calculations
  - Write unit tests for all data structure creation and validation
  - _Requirements: 1.1, 5.1, 6.1, 7.1_

- [x] 2. Implement ResourceManager core functionality
  - Create `ResourceManager` class with game state integration
  - Implement `calculate_available_resources()` method using controlled planets and trade goods
  - Implement `calculate_available_influence()` method with voting restrictions
  - Implement `get_resource_sources()` and `get_influence_sources()` methods for detailed breakdowns
  - Write comprehensive unit tests for resource/influence calculations
  - _Requirements: 1.1, 1.2, 5.1, 5.2, 10.1_

- [x] 3. Create spending plan system
  - Implement `create_spending_plan()` method for resource and influence spending
  - Add validation logic for spending plan feasibility
  - Implement `can_afford_spending()` method for quick affordability checks
  - Add support for voting vs non-voting influence calculations
  - Write unit tests for spending plan creation and validation
  - _Requirements: 6.1, 6.2, 6.3, 9.2, 9.4_

- [x] 4. Implement spending plan execution
  - Implement `execute_spending_plan()` method with atomic planet exhaustion
  - Add rollback capability for failed spending operations
  - Integrate with existing Planet exhaustion mechanics
  - Integrate with existing Player trade goods spending
  - Write unit tests for spending execution and error handling
  - _Requirements: 1.4, 1.5, 6.5, 10.1, 10.2_

- [x] 5. Create CostValidator for unit cost calculations
  - Create `CostValidator` class with UnitStatsProvider integration
  - Implement `get_unit_cost()` method with faction and technology modifiers
  - Implement `get_production_cost()` method handling dual production rules
  - Add `can_produce_without_cost()` method for structure validation
  - Write unit tests for cost calculations and modifier applications
  - _Requirements: 2.1, 2.5, 3.1, 3.2, 4.4, 8.1, 8.2_

- [x] 6. Implement dual production cost handling
  - Add dual production logic to `get_production_cost()` method
  - Implement cost validation for producing 1 unit when 2 are normally produced
  - Add reinforcement validation for actual units produced vs cost paid
  - Integrate with existing ProductionManager dual production logic
  - Write unit tests for all dual production scenarios
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 7. Create production cost validation system
  - Implement `validate_production_cost()` method integrating ResourceManager and CostValidator
  - Add comprehensive validation for resource availability vs production costs
  - Create detailed error messages for insufficient resources
  - Add suggested spending plan generation for failed validations
  - Write unit tests for production cost validation scenarios
  - _Requirements: 2.1, 2.2, 2.3, 7.1, 7.2, 7.3_

- [x] 8. Enhance ProductionManager with cost integration
  - Extend existing ProductionManager with ResourceManager and CostValidator dependencies
  - Implement `validate_production()` method with integrated cost, reinforcement, and placement validation
  - Implement `execute_production()` method with atomic cost payment and unit placement
  - Maintain backward compatibility with existing production system
  - Write integration tests for enhanced production system
  - _Requirements: 7.4, 7.5, 10.3, 10.5_

- [x] 9. Add Construction strategy card cost exemptions
  - Implement structure cost exemption logic in CostValidator
  - Add Construction strategy card integration for cost-free structure placement
  - Validate that units without cost cannot be produced normally
  - Integrate with existing strategy card system
  - Write unit tests for Construction strategy card scenarios
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 10. Implement technology and faction cost modifiers
  - Integrate with existing UnitStatsProvider for cost modifier application
  - Add support for technology-based cost modifications
  - Add support for faction-specific cost modifications
  - Handle multiple modifier stacking and negative cost prevention
  - Write unit tests for all cost modifier scenarios
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [x] 11. Create agenda phase voting integration
  - Integrate ResourceManager influence calculations with existing agenda phase voting
  - Implement trade goods restriction for voting (Rule 47.3)
  - Add planet exhaustion tracking for voting operations
  - Ensure compatibility with existing VotingSystem
  - Write integration tests for agenda phase voting with influence spending
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 12. Add Leadership strategy card integration
  - Integrate influence spending with Leadership strategy card command token gain
  - Add validation for influence availability when using Leadership
  - Ensure proper planet exhaustion when gaining command tokens via Leadership
  - Maintain compatibility with existing Leadership strategy card implementation
  - Write integration tests for Leadership strategy card scenarios
  - _Requirements: 5.5, 10.1, 10.2_

- [x] 13. Implement comprehensive error handling
  - Create custom exception classes for resource-related errors
  - Add detailed error messages with resource availability vs requirements
  - Implement atomic operation rollback for failed spending
  - Add logging and debugging support for resource operations
  - Write unit tests for all error scenarios and recovery
  - _Requirements: 2.2, 3.3, 6.4, 7.3, 7.4_

- [x] 14. Add performance optimizations and caching
  - Implement caching for resource/influence calculations when game state unchanged
  - Add lazy evaluation for detailed resource breakdowns
  - Optimize planet lookup and filtering operations
  - Add batch operation support for multiple cost validations
  - Write performance tests and benchmarks
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [x] 15. Create comprehensive integration test suite
  - Test complete production flow from cost validation to unit placement
  - Test agenda phase voting with planet exhaustion
  - Test strategy card integration (Leadership, Construction, Politics)
  - Test error handling and rollback scenarios
  - Test performance with maximum players and planets
  - _Requirements: All requirements integration testing_

- [x] 16. Add backward compatibility validation
  - Ensure all existing production tests continue to pass
  - Verify existing agenda phase tests work with new influence system
  - Validate existing strategy card tests remain functional
  - Test existing game state management compatibility
  - Add migration support if needed for existing game states
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
