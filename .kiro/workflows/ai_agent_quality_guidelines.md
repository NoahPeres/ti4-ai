# AI Agent Quality Guidelines

## Overview
This document provides guidelines for AI agents working on this codebase to ensure consistent quality standards and practices.

## Type Checking Standards

### Default Quality Checks
When running quality checks, always use the following approach:

- **Production Code (`src/` directory)**: Use **strict** mypy type checking
- **Test Code (`tests/` directory)**: Use **standard** (non-strict) mypy type checking

### Rationale
- Production code should maintain the highest type safety standards
- Test code can be more flexible to prioritize readability and testing patterns
- This approach balances type safety with development productivity

### Commands to Use

#### Standard Quality Check (Recommended)
```bash
make type-check
```
This runs:
- `mypy src --strict --warn-unused-ignores` for production code
- `mypy tests --show-error-codes` for test code

#### Full Quality Gate
```bash
make quality-gate
```
Runs all quality checks including linting, formatting, security, and tests.

#### Strict Check (All Code)
```bash
make strict-check
```
Only use when specifically requested - applies strict checking to both src and tests.

## Quality Check Results Interpretation

### Expected Results
- **src/ directory**: Should pass all strict mypy checks (0 errors)
- **tests/ directory**: May have type annotation violations - this is acceptable
- **All other checks**: Should pass (linting, formatting, tests, security)

### Common Test Code Violations (Acceptable)
- `[no-untyped-def]`: Missing type annotations on test functions
- `[return-value]`: Test helpers with flexible return types
- `[override]`: Test mocks with simplified interfaces
- `[no-any-return]`: Dynamic test data returning Any
- `[abstract]`: Direct instantiation of abstract classes in tests

## Best Practices for AI Agents

1. **Always run quality checks** before completing tasks
2. **Use `make type-check`** as the default quality verification
3. **Fix production code issues** immediately - src/ must be type-safe
4. **Document test code issues** but don't require fixing unless specifically requested
5. **Run full quality gate** for major changes or when explicitly requested

## Repository Health Indicators

### Green Light (Ready for Production)
- ✅ All tests pass (90%+ coverage)
- ✅ Linting passes
- ✅ Formatting is consistent
- ✅ src/ passes strict mypy checks
- ✅ Security checks pass

### Yellow Light (Acceptable for Development)
- ⚠️ Test files have mypy violations (non-strict mode)
- ⚠️ Minor documentation gaps

### Red Light (Requires Attention)
- ❌ Tests failing
- ❌ src/ has type errors
- ❌ Linting failures
- ❌ Security vulnerabilities

## Quick Reference Commands

```bash
# Standard quality check (use this by default)
make type-check

# Full quality gate
make quality-gate

# Individual checks
make test          # Run tests with coverage
make lint          # Check code style
make format        # Auto-format code
make security-check # Security analysis

# Fix common issues
make format        # Auto-fix formatting
uv run ruff check src tests --fix  # Auto-fix linting
```

## Notes for Future Development

- The codebase maintains excellent type safety in production code
- Test code flexibility is intentional and should be preserved
- Any changes to type checking standards should be documented here
- Consider gradual improvement of test type annotations over time, but it's not a priority