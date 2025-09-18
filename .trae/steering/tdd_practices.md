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

### Commands for TDD Workflow

- Run single test: `uv run pytest path/to/test.py::test_function_name -v`
- Run all tests in file: `uv run pytest path/to/test.py -v`
- Always use `-v` flag for verbose output to see test names and results clearly
- Format code: `uv run ruff format src tests` (recommended) or `make format`
- Check/fix linting: `uv run ruff check --fix src tests`
- Type checking: `uv run mypy src` or `make type-check`
- All quality checks: `make check-all` (recommended before committing)