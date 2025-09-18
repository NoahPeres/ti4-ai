# Quality Assurance Workflow

This document outlines the comprehensive quality assurance measures implemented in the TI4 AI project to maintain high code quality and prevent regressions.

## Overview

Our quality assurance strategy is built on multiple layers of validation:

1. **Static Analysis** - Catch issues before runtime
2. **Runtime Validation** - Verify types and contracts during execution  
3. **Automated Testing** - Comprehensive test coverage
4. **Continuous Integration** - Automated quality gates
5. **Pre-commit Hooks** - Prevent bad commits from entering the repository

## Quality Gates

### Level 1: Pre-commit Hooks
Runs automatically before each commit:
- Code formatting with `ruff format`
- Linting with `ruff check`
- Type checking with `mypy --strict`
- Basic file validation (YAML, JSON, TOML)
- Debug statement detection
- Test naming conventions

### Level 2: Local Development
Available via Makefile targets:
```bash
make quality-gate  # Run all quality checks
make strict-check  # Strictest mypy settings
make security-check # Security analysis
make runtime-check # Runtime type validation
```

### Level 3: Continuous Integration
GitHub Actions workflow with:
- Multi-Python version testing (3.9-3.12)
- Strict type checking (no type ignores allowed)
- Security analysis with bandit
- 90% minimum test coverage requirement
- Runtime type checking validation

## Type Safety Strategy

### Static Type Checking (MyPy)
Configuration in `pyproject.toml`:
```toml
[tool.mypy]
strict = true
disallow_any_generics = true
disallow_any_unimported = true
disallow_any_decorated = true
disallow_subclassing_any = true
warn_unused_ignores = true
extra_checks = true
```

**Key Rules:**
- No `# type: ignore` comments allowed in production code
- All functions must have complete type annotations
- Generic types must be properly parameterized
- Any usage is strictly controlled

### Runtime Type Checking
Using `beartype` and `typeguard` for runtime validation:

```python
from src.ti4.core.runtime_type_checking import runtime_type_check

@runtime_type_check
def process_game_state(state: GameState) -> ActionResult:
    # Function will validate types at runtime
    pass
```

**When to Use:**
- Critical game logic functions
- Public API boundaries
- Data validation points
- Performance-critical paths (with caution)

## Code Quality Standards

### Linting Rules (Ruff)
- `E`: pycodestyle errors
- `W`: pycodestyle warnings  
- `F`: pyflakes
- `I`: isort (import sorting)
- `B`: flake8-bugbear
- `C4`: flake8-comprehensions
- `UP`: pyupgrade (modern Python syntax)

### Test Coverage Requirements
- Minimum 90% line coverage
- All public APIs must be tested
- Critical game logic requires 100% coverage
- Integration tests for complex workflows

### Security Standards
- Regular security scanning with bandit
- No hardcoded secrets or credentials
- Input validation for all external data
- Secure handling of game state serialization

## Development Workflow

### Setting Up Development Environment
```bash
make dev-setup  # Installs dependencies and pre-commit hooks
```

### Before Committing
```bash
make quality-gate  # Run all quality checks locally
```

### Handling Type Issues
1. **Fix the root cause** - Don't use type ignores
2. **Improve type annotations** - Make them more specific
3. **Use proper generics** - Parameterize generic types
4. **Runtime validation** - Add runtime checks for complex types

### Adding New Code
1. Write type-annotated code from the start
2. Add runtime type checking for critical functions
3. Write comprehensive tests
4. Run quality gate before committing
5. Ensure CI passes before merging

## Enforcement Mechanisms

### Automated Prevention
- Pre-commit hooks prevent bad commits
- CI blocks merges that fail quality checks
- Coverage requirements prevent undertested code
- Security scanning catches vulnerabilities

### Manual Review Process
- Code reviews focus on type safety
- Architecture reviews for complex changes
- Performance reviews for critical paths
- Security reviews for sensitive operations

## Monitoring and Metrics

### Quality Metrics Tracked
- Type checking error count (target: 0)
- Test coverage percentage (target: >90%)
- Security vulnerability count (target: 0)
- Code complexity metrics
- Performance benchmarks

### Regular Maintenance
- Weekly dependency updates
- Monthly security audits
- Quarterly architecture reviews
- Annual tooling evaluation

## Troubleshooting Common Issues

### MyPy Errors
- **"error: Missing type annotation"** - Add proper type hints
- **"error: Incompatible types"** - Check type compatibility
- **"error: Any is not allowed"** - Use specific types instead of Any

### Runtime Type Errors
- Check function signatures match type hints
- Verify generic type parameters
- Ensure proper inheritance hierarchies

### Performance Issues
- Profile runtime type checking overhead
- Use selective decoration for hot paths
- Consider compile-time alternatives

## Future Enhancements

### Planned Improvements
- Integration with IDE type checking
- Custom type validators for game concepts
- Performance optimization for runtime checks
- Enhanced security scanning rules

### Experimental Features
- Property-based testing with Hypothesis
- Mutation testing for test quality
- Static analysis for game rule violations
- Automated performance regression detection

## Resources

- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Beartype Documentation](https://beartype.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Pre-commit Documentation](https://pre-commit.com/)