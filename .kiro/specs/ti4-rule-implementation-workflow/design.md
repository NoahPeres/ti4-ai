# Design Document

## Overview

This design outlines a manual, systematic workflow for implementing TI4 game rules with strict TDD methodology, comprehensive documentation, and evidence-based progress tracking. The focus is on semantic understanding of rule interactions and maintaining high-quality implementations through disciplined human judgment rather than automated validation.

## Architecture

### Core Workflow Components

#### 1. Manual Rule Status Verification
- **Purpose**: Human verification of actual implementation status vs documentation
- **Process**:
  - Manually run tests for specific rules to validate completion status
  - Compare documentation claims with actual test results using human judgment
  - Update tracking documents when discrepancies are found
  - Manually calculate and update accurate progress metrics

#### 2. Human-Driven Rule Prioritization
- **Purpose**: Expert analysis to identify the next highest-priority rule
- **Process**:
  - Manually analyze rule dependencies from `.trae/lrr_analysis/` files
  - Apply domain knowledge to assess implementation complexity and impact
  - Use human judgment to determine optimal implementation order
  - Provide reasoned estimates and expected benefits

#### 3. Disciplined TDD Implementation Process
- **Purpose**: Human-guided strict TDD methodology
- **Process**:
  - Manually read and thoroughly understand complete LRR text for target rule
  - Human validation that RED phase failures are assertion-based, not syntax errors
  - Disciplined minimal implementations in GREEN phase
  - Explicit human consideration and documentation of REFACTOR phase decisions
  - Conscious prevention of implementing untested functionality

#### 4. Manual Documentation Maintenance
- **Purpose**: Human-maintained accurate rule-to-test mappings
- **Process**:
  - Manually update both `.trae/lrr_analysis/` and `docs/` directories
  - Human mapping of test cases to specific LRR sub-rules
  - Maintain consistent documentation format through careful review
  - Manual updates to IMPLEMENTATION_ROADMAP.md progress metrics

#### 5. Manual Quality Assurance
- **Purpose**: Human-executed quality checks
- **Process**:
  - Manually execute test suites with `uv run pytest`
  - Run comprehensive quality checks with `make check-all`
  - Validate type checking with `uv run mypy src`
  - Ensure linting compliance with `uv run ruff check`

## Manual Process Guidelines

### Rule Status Verification Process
1. **Manual Test Execution**: Run `uv run pytest tests/test_rule_{number}_{name}.py -v` to verify actual status
2. **Human Analysis**: Compare test results with documentation claims using domain knowledge
3. **Documentation Updates**: Manually update `.trae/lrr_analysis/{number}_{name}.md` with accurate status
4. **Progress Tracking**: Update IMPLEMENTATION_ROADMAP.md with verified completion status

### Rule Prioritization Process
1. **Dependency Analysis**: Manually review `.trae/lrr_analysis/` files to understand rule dependencies
2. **Impact Assessment**: Use TI4 game knowledge to assess which rules enable the most downstream functionality
3. **Complexity Evaluation**: Apply development experience to estimate implementation difficulty
4. **Priority Decision**: Make reasoned choice based on dependency order, impact, and complexity

### TDD Implementation Process
1. **LRR Study**: Thoroughly read and understand the complete LRR text for the target rule
2. **RED Phase**: Write failing tests that demonstrate missing functionality with assertion-based failures
3. **GREEN Phase**: Write minimal code to make tests pass, resisting over-implementation
4. **REFACTOR Phase**: Explicitly consider and document refactoring decisions, even if choosing not to refactor

### Documentation Maintenance Process
1. **Test Mapping**: Manually document which test cases demonstrate each LRR sub-rule
2. **Format Consistency**: Follow established patterns from existing rule documentation
3. **Cross-Reference Updates**: Update both `.trae/lrr_analysis/` and `docs/` directories
4. **Progress Metrics**: Manually calculate and update completion percentages

## Documentation Standards

### Rule Analysis Document Format
Each `.trae/lrr_analysis/{number}_{name}.md` file should contain:
- **Implementation Status**: ✅ COMPLETED, ⚠️ PARTIAL, or ❌ NOT IMPLEMENTED
- **Test Cases Demonstrating Implementation**: Specific test file and method names
- **Sub-Rules Coverage**: Which LRR sub-rules are covered by which tests
- **Dependencies**: What other rules must be implemented first
- **Quality Metrics**: Test count, coverage, and compliance status

### Test-to-Rule Mapping Format
For each implemented rule, document:
- **Rule Number and Sub-Rule**: e.g., "58.4a: Ships must end in active system"
- **Test Reference**: e.g., `test_rule_58_movement.py::TestRule58MoveShipsStep::test_ships_must_end_in_active_system`
- **Test Description**: Human-readable explanation of what the test validates
- **LRR Compliance**: Direct reference to specific LRR text

### Progress Tracking Format
In IMPLEMENTATION_ROADMAP.md:
- **Overall Progress**: X.X% with calculation methodology
- **Completed Rules**: List with completion dates and test counts
- **Next Priority Rules**: Ordered list with rationale
- **Quality Metrics**: Test counts, coverage percentages, and quality gate status

## Quality Constraints

### Critical Implementation Guidelines
- **CAREFUL**: Import/syntax/attribute errors are NOT proper RED phases - implement minimal interfaces and get it to fail on asserts only
- **REMEMBER**: Before proceeding to next rule implementation, double check it isn't already done! Update tracking docs if so
- **MANDATORY**: Read the rule in question THOROUGHLY before creating your first test to ensure holistic understanding
- **STRICT LRR COMPLIANCE**: Do NOT add any tests or functionality which hallucinates rules that don't actually exist
- **NO CONTRADICTIONS**: Do NOT add any tests or functionality which contradicts or is inconsistent with the LRR
- **CONFLICT RESOLUTION**: If you run into any conflict or issue (implementation wise or rules wise), PROMPT THE USER for clarification with recommended options and strategies

### TDD Discipline Requirements
- **RED Phase Validation**: Ensure test failures are assertion-based, not import/syntax errors
- **GREEN Phase Restraint**: Implement only the minimal code needed to pass current tests
- **REFACTOR Phase Consideration**: Explicitly document refactoring decisions, including reasons for not refactoring
- **LRR Compliance**: Never implement functionality not explicitly described in the LRR text

### Implementation Quality Gates
- **Test Coverage**: All new functionality must have corresponding tests
- **Type Safety**: All code must pass `uv run mypy src` with strict checking
- **Code Quality**: All code must pass `uv run ruff check src tests` linting
- **Integration**: All existing tests must continue to pass after new implementations

### Documentation Quality Standards
- **Accuracy**: Documentation must reflect actual implementation status, not aspirational status
- **Completeness**: All sub-rules must be explicitly addressed, even if not yet implemented
- **Consistency**: Follow established format patterns from existing rule documentation
- **Traceability**: Clear mapping from LRR text to test cases to implementation code

## Rule Implementation Strategy

### Rule Selection Criteria
1. **Dependency Order**: Implement foundational rules before dependent rules
2. **Gameplay Impact**: Prioritize rules that enable core game mechanics
3. **Implementation Complexity**: Balance high-impact rules with achievable complexity
4. **Test Infrastructure**: Ensure supporting test utilities exist or can be created

### TDD Implementation Approach
1. **Comprehensive LRR Study**: Read and understand the complete rule text before writing any code
2. **Sub-Rule Breakdown**: Identify all sub-rules and create tests for each
3. **Incremental Implementation**: Implement one sub-rule at a time with full TDD cycles
4. **Integration Validation**: Ensure new rule integrates properly with existing systems

### Quality Assurance Process
1. **Test Execution**: Run rule-specific tests with `uv run pytest tests/test_rule_{number}_{name}.py -v`
2. **Full Test Suite**: Verify all existing tests still pass with `uv run pytest`
3. **Type Checking**: Ensure type safety with `uv run mypy src`
4. **Code Quality**: Validate linting with `uv run ruff check src tests`
5. **Comprehensive Check**: Run `make check-all` for complete validation

### Documentation Update Requirements
- **Dual Location Updates**: Update both `/Users/noahperes/Developer/Code/kiro_test/ti4_ai/.trae/lrr_analysis` and `/Users/noahperes/Developer/Code/kiro_test/ti4_ai/docs`
- **Test Case Mapping**: For each new rule, make explicit notes about which test cases demonstrate the implementation of the rule (look at previous rules for format)
- **Status Verification**: Check records of relevant test cases in lrr_analysis folder before starting new implementations
- **Progress Tracking**: Reference `/Users/noahperes/Developer/Code/kiro_test/ti4_ai/IMPLEMENTATION_ROADMAP.md` to understand current game rule coverage

## Implementation Workflow

### Phase 1: Rule Status Verification
1. **Current Status Check**: Manually verify which rules are actually implemented vs documented
2. **Documentation Sync**: Update `.trae/lrr_analysis/` files to reflect reality
3. **Progress Baseline**: Establish accurate baseline metrics in IMPLEMENTATION_ROADMAP.md
4. **Next Rule Identification**: Determine the highest-priority unimplemented rule

### Phase 2: Rule Implementation Execution
1. **LRR Study**: Thoroughly read and understand the target rule's complete LRR text
2. **Test Planning**: Identify all sub-rules and plan corresponding test cases
3. **TDD Cycles**: Implement each sub-rule with strict RED-GREEN-REFACTOR methodology
4. **Integration Testing**: Ensure new rule works with existing game systems

### Phase 3: Documentation and Quality Assurance
1. **Test Mapping**: Document which test cases demonstrate each sub-rule implementation
2. **Quality Validation**: Run comprehensive quality checks and fix any issues
3. **Documentation Updates**: Update both `.trae/lrr_analysis/` and `docs/` directories
4. **Progress Tracking**: Update IMPLEMENTATION_ROADMAP.md with completion status

### Phase 4: Iteration and Continuous Improvement
1. **Rule Completion Review**: Verify all sub-rules are properly implemented and tested
2. **Next Rule Selection**: Apply lessons learned to select the next priority rule
3. **Process Refinement**: Improve workflow based on implementation experience
4. **Quality Maintenance**: Ensure all existing functionality remains working

## Success Criteria

### Implementation Quality Standards
- **LRR Compliance**: All implementations strictly adhere to Living Rules Reference text
- **Test Coverage**: Every sub-rule has corresponding test cases that demonstrate implementation
- **TDD Discipline**: All functionality implemented through proper RED-GREEN-REFACTOR cycles
- **Integration Stability**: New rules don't break existing functionality
- **Documentation Accuracy**: Tracking documents reflect actual implementation status

### Process Effectiveness Measures
- **Steady Progress**: Consistent completion of rules without regression
- **Quality Maintenance**: All quality gates pass throughout implementation
- **Documentation Synchronization**: Both `.trae/lrr_analysis/` and `docs/` remain current
- **Dependency Respect**: Rules implemented in proper dependency order
- **Knowledge Retention**: Implementation decisions documented for future reference

### Long-term Sustainability Goals
- **Maintainable Codebase**: Code remains readable and modifiable as complexity grows
- **Comprehensive Test Suite**: Test coverage enables confident refactoring and enhancement
- **Accurate Progress Tracking**: Realistic assessment of completion status and remaining work
- **Scalable Process**: Workflow remains effective as rule count and complexity increase
- **Team Knowledge**: Implementation approach can be understood and continued by other developers
