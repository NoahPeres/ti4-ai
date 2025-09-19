# Implementation Plan

- [x] 1. Verify Current Rule Implementation Status
  - Manually verify Rule 58 (MOVEMENT) completion status by running tests
  - Update `.trae/lrr_analysis/58_movement.md` if status is confirmed complete
  - Update IMPLEMENTATION_ROADMAP.md to reflect verified Rule 58 completion
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 2. Identify Next Priority Rule for Implementation
  - Review IMPLEMENTATION_ROADMAP.md next priority rules list
  - Analyze Rule 99 (WARFARE STRATEGY CARD) dependencies and complexity
  - Verify Rule 99 is not already implemented by checking test files
  - Confirm Rule 99 as next target based on dependency analysis
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 3. Implement Rule 99 (WARFARE STRATEGY CARD) with Strict TDD
  - Read complete LRR text for Rule 99 thoroughly before writing any tests
  - Create `tests/test_rule_99_warfare_strategy_card.py` with proper test structure
  - Implement Rule 99.1 (Command Token Removal) with RED-GREEN-REFACTOR cycles
  - Implement Rule 99.2 (Command Token Redistribution) with TDD methodology
  - Implement Rule 99.3 (Secondary Ability) following TDD discipline
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [x] 4. Create Minimal Production Code for Rule 99
  - Implement WarfareStrategyCard class with minimal functionality
  - Add command token removal mechanics to game system
  - Create command token redistribution system
  - Integrate warfare card with existing strategy card framework
  - Ensure all implementations pass type checking and linting
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 5.3, 5.4_

- [x] 5. Update Documentation for Rule 99 Implementation
  - Update `.trae/lrr_analysis/99_warfare_strategy_card.md` with implementation status
  - Document which test cases demonstrate each Rule 99 sub-rule implementation
  - Update `docs/` directory with corresponding rule documentation
  - Map all test methods to specific LRR sub-rules following established format
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 6. Execute Comprehensive Quality Assurance
  - Run rule-specific tests: `uv run pytest tests/test_rule_99_warfare_strategy_card.py -v`
  - Verify all existing tests still pass: `uv run pytest`
  - Check type safety: `uv run mypy src`
  - Validate code quality: `uv run ruff check src tests`
  - Run comprehensive validation: `make check-all`
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 7. Update Progress Tracking and Metrics
  - Update IMPLEMENTATION_ROADMAP.md with Rule 99 completion
  - Calculate new overall progress percentage
  - Update completed rules count and test metrics
  - Identify next priority rule based on updated status
  - Document lessons learned and process improvements
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 8. Validate Workflow Effectiveness
  - Verify all documentation is synchronized across directories
  - Confirm test-to-rule mappings are complete and accurate
  - Validate that implementation strictly adheres to LRR text
  - Ensure no functionality was implemented without corresponding tests
  - Review refactoring decisions and document rationale
  - _Requirements: 1.4, 4.4, 6.1, 6.4, 6.5_

- [x] 9. Meta Task: Identify and Plan Next Rule Implementation Cycle
  - Analyze current implementation status across all 101 TI4 rules
  - Review dependency chains to identify next highest-priority unimplemented rule
  - Assess implementation complexity and expected impact of candidate rules
  - Create new task items for the next rule implementation cycle
  - Update IMPLEMENTATION_ROADMAP.md with revised priority order and rationale
  - Ensure continuous development momentum by always having next steps defined
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 7.4, 7.5_