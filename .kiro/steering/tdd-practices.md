---
inclusion: always
---

# Test-Driven Development (TDD) Practices

## Core TDD Cycle: RED-GREEN-REFACTOR

### RED Phase (Test Fails)
- **CRITICAL**: Write a test that fails on an ASSERTION, not on compilation/syntax/import errors
- Before writing any production code, ensure you have a failing test that demonstrates the missing functionality
- The test must be able to run and fail with a clear assertion error message
- **Anti-pattern**: Tests that fail due to missing modules, syntax errors, or compilation issues are NOT valid RED phases
- **Proper RED**: `AssertionError: assert False` or `AssertionError: assert 'expected' == 'actual'`

### GREEN Phase (Make Test Pass)
- Write the MINIMAL amount of code to make the failing test pass
- Don't implement more functionality than what the current test requires
- Focus on making the test pass, not on perfect implementation
- Resist the urge to add "obvious" features that aren't tested yet

### REFACTOR Phase (Improve Code Quality)
- **MANDATORY**: Always explicitly consider refactoring after each GREEN phase
- Look for code duplication, unclear naming, complex logic, or design issues
- Make an INTENTIONAL DECISION whether to refactor or not
- If choosing NOT to refactor, provide clear justification (e.g., "code is minimal and clear", "YAGNI principle applies", "premature optimization")
- Common early-stage reasons to skip refactoring:
  - Code is still minimal with little duplication
  - Requirements are not yet clear enough to warrant abstraction
  - Current implementation is readable and maintainable

## TDD Discipline Rules

### One Test at a Time
- Write ONE failing test, make it pass, then refactor
- Don't write multiple tests before implementing functionality
- Don't skip ahead to implement features not yet tested

### Minimal Implementation
- Always write the simplest code that makes the test pass
- Don't anticipate future requirements
- Let the tests drive the design

### Proper Test Structure
- Ensure all syntax/imports are correct BEFORE writing assertion-based tests
- Create minimal scaffolding (empty classes, basic imports) to enable proper RED phases
- Focus tests on behavior, not implementation details

### Restraint and Focus
- TDD is about restraint - only implement what's tested
- Don't implement "obvious" functionality without tests
- Stay focused on the current failing test

## Example of Proper TDD Cycle

```python
# 1. RED: Write failing test (assertion-based failure)
def test_player_has_id():
    player = Player(id="test")
    assert player.id == "wrong_id"  # This will fail with AssertionError

# 2. GREEN: Fix test to pass with minimal code
def test_player_has_id():
    player = Player(id="test")
    assert player.id == "test"  # Now passes

# 3. REFACTOR: Explicitly consider improvements
# Decision: No refactor needed - code is minimal and clear
```

## Anti-Patterns to Avoid

- Writing tests that fail on import errors instead of assertions
- Implementing multiple features before writing tests
- Skipping the refactor consideration phase
- Writing complex implementations when simple ones suffice
- Adding untested functionality "because it's obvious"

## Commands for TDD Workflow

- Run single test: `uv run pytest path/to/test.py::test_function_name -v`
- Run all tests in file: `uv run pytest path/to/test.py -v`
- Always use `-v` flag for verbose output to see test names and results clearly
- Format code: `uv run ruff format src tests` (recommended) or `make format`
- Check/fix linting: `uv run ruff check --fix src tests`
- Type checking: `uv run mypy src` or `make type-check`
- All quality checks: `make check-all` (recommended before committing)

Remember: TDD is a discipline that requires intentional practice of the RED-GREEN-REFACTOR cycle with proper consideration of each phase.
