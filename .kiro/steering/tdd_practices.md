# TDD Practices for TI4 AI Implementation

## Core TDD Principles

### Red-Green-Refactor Cycle
1. **Red**: Write a failing test that describes the desired functionality
2. **Green**: Write the minimal code necessary to make the test pass
3. **Refactor**: Clean up the code while keeping tests green

**CRITICAL**: Refactoring is **mandatory** and must be tracked as an explicit step in all development tasks.

### Test-First Development
- Always write tests before implementation
- Tests should describe the expected behavior clearly
- Use descriptive test names that explain what is being tested

## Implementation Guidelines

### Test Structure
- Use clear, descriptive test method names
- Follow the Arrange-Act-Assert pattern
- Keep tests focused on a single behavior
- Use helper methods to reduce duplication
- **NEW**: Create parameterized tests for comprehensive coverage
- **NEW**: Add descriptive error messages in assertions

### Code Quality
- Write the simplest code that makes tests pass
- Refactor only when tests are green
- Maintain high test coverage
- Follow SOLID principles
- **NEW**: Add comprehensive input validation
- **NEW**: Implement defensive programming practices

## LRR Rule Implementation Process

### Phase 1: Analysis
1. Read and understand the LRR rule
2. Identify key components and behaviors
3. Break down into testable units
4. Create implementation plan
5. **NEW**: Include explicit refactoring tasks in planning

### Phase 2: Test Development
1. Write failing tests for each behavior
2. Start with the simplest cases
3. Add edge cases and error conditions
4. Ensure comprehensive coverage
5. **NEW**: Create helper methods to eliminate test duplication

### Phase 3: Implementation
1. Write minimal code to pass tests
2. Focus on correctness over optimization
3. Keep implementation simple and clear
4. Add necessary error handling
5. **NEW**: Include LRR rule references in docstrings

### Phase 4: Refactoring (MANDATORY)
1. **Implementation Refactoring**:
   - Clean up code structure
   - Eliminate duplication
   - Improve readability
   - Extract methods with single responsibilities
   - Add comprehensive documentation
   - Implement robust error handling
2. **Test Refactoring**:
   - Create helper methods for common setup
   - Use parameterized tests where appropriate
   - Add descriptive error messages
   - Improve test organization and readability
3. **Quality Assurance**:
   - Ensure all tests still pass
   - Add edge case tests
   - Verify error handling works correctly
   - Maintain test coverage

## Quality Assurance

### Test Quality Metrics
- All tests must pass
- Tests should be fast and reliable
- Test names should be self-documenting
- Tests should be independent of each other
- **NEW**: Edge cases must be thoroughly tested
- **NEW**: Error conditions must have dedicated tests

### Code Quality Metrics
- No code duplication
- Clear method and variable names
- Proper error handling
- Comprehensive documentation
- **NEW**: Single responsibility principle applied
- **NEW**: Input validation implemented
- **NEW**: Immutability protection where appropriate

## Documentation Standards

### Code Documentation
- Include docstrings for all public methods
- Reference relevant LRR rules with specific numbers
- Provide usage examples
- Document error conditions
- **NEW**: Include parameter and return value documentation
- **NEW**: Document all exceptions that can be raised

### Test Documentation
- Use descriptive test names
- Include comments for complex test logic
- Document test data and expectations
- Reference specific rule requirements
- **NEW**: Include rule references in test docstrings

## Refactoring Best Practices

### Systematic Approach
1. **Before Refactoring**: Ensure all tests pass
2. **During Refactoring**: Make incremental changes, test after each
3. **After Refactoring**: Add additional edge case tests

### Refactoring Priorities
1. **Eliminate Code Duplication** (DRY principle)
2. **Improve Method Cohesion** (Single Responsibility)
3. **Enhance Error Handling** (Defensive Programming)
4. **Improve Documentation** (Self-Documenting Code)
5. **Add Input Validation** (Robustness)

### Quality Gates
- ✅ All tests must pass after refactoring
- ✅ No new code duplication introduced
- ✅ Error handling must be comprehensive
- ✅ Documentation must be updated
- ✅ Edge cases must be covered

## Process Enforcement

### Mandatory Steps for Every Feature
1. **Analysis and Planning** (include refactoring tasks)
2. **Test Development** (comprehensive coverage)
3. **Implementation** (minimal, correct code)
4. **Explicit Refactoring** (both code and tests)
5. **Quality Validation** (all tests pass, edge cases covered)
6. **Documentation Update** (capture learnings)

### Never Skip
- ❌ **Never skip the refactoring step**
- ❌ **Never leave code duplication**
- ❌ **Never skip edge case testing**
- ❌ **Never leave methods without proper documentation**