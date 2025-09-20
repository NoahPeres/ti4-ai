# Quality Check Workflow

## Subtask Completion Quality Check

When completing any subtask or making significant code changes, always run the following quality checks in order:

1. **Format all code**:
   ```
   uv run ruff format src tests
   ```

2. **Run mypy type checking**:
   ```
   uv run mypy src
   ```

3. **Run ruff linting checks**:
   ```
   uv run ruff check --fix src tests
   ```

4. **Run all software tests**:
   ```
   uv run pytest tests/ -v
   ```

## Important Guidelines

- **Never skip checks**: All checks must pass before considering a task complete
- **Fix issues immediately**: Address any failures as soon as they appear
- **Maintain code quality**: Be vigilant about preserving code quality standards
- **Document resolutions**: Note any significant issues and their resolutions
- **Refactor when needed**: Take proactive steps to improve code quality

## Common Issues and Resolutions

### Type Checking Issues
- Ensure all function signatures have proper type hints
- Verify generic types are used correctly
- Check for proper Optional/Union usage

### Linting Issues
- Follow consistent naming conventions
- Maintain proper import order
- Avoid unused imports and variables

### Test Failures
- Verify test expectations match implementation
- Check for race conditions in tests
- Ensure test isolation (no test should depend on another)

## Complete Validation

For comprehensive validation before major commits or releases, run:
```
make check-all
```

This will execute all checks and ensure the codebase meets quality standards.
