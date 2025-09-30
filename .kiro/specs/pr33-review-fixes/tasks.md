# Implementation Plan

- [x] 1. Fix Hook Configuration
  - Restore file patterns in `.kiro/hooks/subtask-quality-check.kiro.hook`
  - Replace empty patterns array with comprehensive file type coverage
  - Test hook triggering with file edits
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 2. Fix Critical Ability Trigger System
  - [x] 2.1 Update Dark Energy Tap ability trigger
    - Import `AbilityTrigger` from `ti4.core.constants` in `dark_energy_tap.py`
    - Replace hardcoded `"tactical_action_in_frontier_system"` with `AbilityTrigger.AFTER_TACTICAL_ACTION.value`
    - Verify ability creation still works correctly
    - _Requirements: 3.1, 3.2_

  - [x] 2.2 Update integration tests to use canonical triggers
    - Update `test_technology_card_framework_integration.py` to use `AbilityTrigger.AFTER_TACTICAL_ACTION.value`
    - Find and replace all occurrences of `"tactical_action_in_frontier_system"` in tests
    - Ensure tests still pass with canonical trigger values
    - _Requirements: 3.3, 3.4_

- [x] 3. Implement Fail-Closed Ability Condition Validation
  - [x] 3.1 Add explicit validation for all ability conditions
    - Update `validate_ability_conditions` in `abilities_integration.py`
    - Replace fallthrough logic with explicit `NotImplementedError` for unhandled conditions
    - Add descriptive error messages for each unimplemented condition
    - _Requirements: 4.1, 4.3_

  - [x] 3.2 Test fail-closed validation behavior
    - Write tests to verify `NotImplementedError` is raised for unimplemented conditions
    - Test that implemented conditions still work correctly
    - Verify error messages are descriptive and helpful
    - _Requirements: 4.2, 4.4_

- [x] 4. Fix Documentation Consistency
  - [x] 4.1 Update README.md enum file references
    - Fix line ~180 to reference `specifications.py` instead of `constants.py`
    - Fix lines ~275-278 to reference `specifications.py` consistently
    - Ensure troubleshooting section aligns with file organization section
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 4.2 Verify documentation consistency
    - Review all documentation files for similar inconsistencies
    - Create automated check to prevent future documentation drift
    - Update any other references to enum file locations
    - _Requirements: 2.1, 2.2, 2.3_

- [x] 5. Comprehensive Testing and Validation
  - [x] 5.1 Run full test suite validation
    - Execute `uv run pytest` to ensure all tests pass
    - Run `uv run mypy src` for type checking
    - Run `uv run ruff check src tests` for linting
    - Execute `make check-all` for complete validation
    - _Requirements: 1.1, 2.1, 3.1, 4.1_

  - [x] 5.2 Manual verification of fixes
    - Test hook triggering by editing files
    - Verify ability triggers work in integration scenarios
    - Confirm documentation references are correct
    - Test error handling for unimplemented conditions
    - _Requirements: 1.3, 2.3, 3.2, 4.4_

- [x] 6. Update Development Guidelines
  - [x] 6.1 Document canonical trigger usage
    - Add guidelines for using enum values instead of hardcoded strings
    - Update code review checklist to include trigger validation
    - Document fail-closed validation approach
    - _Requirements: 3.1, 4.1_

  - [x] 6.2 Create prevention measures
    - Add linting rules to detect hardcoded trigger strings
    - Create template for new ability implementations
    - Document validation requirements for new conditions
    - _Requirements: 3.4, 4.2_
