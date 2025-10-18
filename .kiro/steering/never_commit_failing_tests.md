# CRITICAL: Never Commit Failing Tests

## 🚨 ABSOLUTE PROHIBITION

**NEVER, UNDER ANY CIRCUMSTANCES, COMMIT CODE WITH FAILING TESTS**

This is a fundamental violation of our quality standards and must never happen.

## Why This Is Critical

1. **Broken Build**: Failing tests indicate broken functionality
2. **Regression Risk**: Other developers pull broken code
3. **CI/CD Pipeline**: Breaks automated deployment and integration
4. **Quality Assurance**: Undermines our entire testing strategy
5. **Team Productivity**: Wastes time debugging issues that shouldn't exist

## Pre-Commit Hook Requirements

Our pre-commit hooks MUST include:

```yaml
- id: pytest-with-coverage
  name: pytest-with-coverage
  entry: uv run pytest --cov=src/ti4 --cov-report=term-missing --tb=short
  language: system
  pass_filenames: false
  always_run: true
```

## Mandatory Workflow

### Before Every Commit:
1. **Run all tests locally**: `uv run pytest`
2. **Verify all tests pass**: 0 failures, 0 errors
3. **Check test coverage**: Maintain >90% coverage
4. **Run quality gate**: `make quality-gate`
5. **Only commit when everything passes**

### If Tests Fail:
1. **STOP** - Do not commit
2. **FIX** the failing tests immediately
3. **INVESTIGATE** the root cause
4. **VERIFY** the fix works
5. **RUN** full test suite again
6. **COMMIT** only after all tests pass

## Enforcement Mechanisms

### Pre-Commit Hooks
- **MUST** run pytest with coverage
- **MUST** fail the commit if any test fails
- **MUST** require minimum coverage threshold
- **CANNOT** be bypassed with `--no-verify`

### CI/CD Pipeline
- **MUST** run full test suite on every push
- **MUST** block merges if tests fail
- **MUST** notify team of test failures immediately
- **MUST** prevent deployment of failing code

## Emergency Procedures

### If Failing Tests Are Discovered in Main Branch:
1. **IMMEDIATE REVERT** of the offending commit
2. **HOTFIX BRANCH** to address the issue
3. **FULL TEST VALIDATION** before re-merging
4. **POST-MORTEM** to understand how it happened
5. **PROCESS IMPROVEMENT** to prevent recurrence

### No Exceptions Policy:
- ❌ **No "temporary" commits with failing tests**
- ❌ **No "will fix later" commits**
- ❌ **No bypassing hooks for "urgent" changes**
- ❌ **No partial implementations that break existing tests**

## Quality Standards

### Test Requirements:
- **All tests must pass**: 0 failures, 0 errors
- **Coverage threshold**: >90% line coverage
- **Performance tests**: Must meet benchmarks
- **Integration tests**: Must validate end-to-end workflows
- **Type checking**: Must pass strict mypy validation

### Code Quality Gates:
```bash
# Standard quality check (MUST pass before commit)
make quality-gate

# Individual checks that MUST all pass:
uv run pytest                    # All tests pass
uv run mypy src --strict        # Type checking
uv run ruff check src tests     # Linting
uv run ruff format src tests    # Formatting
```

## Monitoring and Alerts

### Continuous Monitoring:
- **Test failure notifications** to team channels
- **Coverage regression alerts** for drops below threshold
- **Performance regression detection** for slow tests
- **Flaky test identification** and remediation

### Metrics Tracking:
- **Test pass rate**: Must be 100%
- **Test coverage**: Must be >90%
- **Test execution time**: Monitor for performance
- **Commit rejection rate**: Track pre-commit hook effectiveness

## Team Responsibilities

### All Developers Must:
- **Run tests locally** before every commit
- **Fix failing tests immediately** when discovered
- **Report test infrastructure issues** promptly
- **Maintain test quality** and coverage
- **Never bypass quality gates**

### Code Reviewers Must:
- **Verify all tests pass** in CI/CD
- **Check test coverage** for new code
- **Validate test quality** and completeness
- **Reject PRs** with failing tests
- **Ensure proper test documentation**

## Consequences

### Immediate Actions for Violations:
1. **Automatic commit rejection** by pre-commit hooks
2. **CI/CD pipeline failure** and merge blocking
3. **Immediate notification** to team and violator
4. **Required remediation** before any further commits
5. **Process review** to prevent recurrence

### Escalation Process:
1. **First violation**: Education and process reminder
2. **Repeated violations**: Mandatory training on TDD practices
3. **Persistent issues**: Architecture review and pair programming
4. **Systemic problems**: Process and tooling improvements

## Tools and Commands

### Essential Commands:
```bash
# Run all tests (MUST pass)
uv run pytest

# Run with coverage (MUST be >90%)
uv run pytest --cov=src/ti4 --cov-report=term-missing

# Run quality gate (MUST pass)
make quality-gate

# Check specific test file
uv run pytest tests/test_specific_file.py -v

# Run tests with detailed output
uv run pytest --tb=short -v
```

### Pre-Commit Setup:
```bash
# Install pre-commit hooks (MANDATORY)
pre-commit install

# Test pre-commit hooks
pre-commit run --all-files

# Update pre-commit hooks
pre-commit autoupdate
```

## Documentation and Training

### Required Knowledge:
- **TDD practices**: Red-Green-Refactor cycle
- **Test writing**: Unit, integration, and end-to-end tests
- **Coverage analysis**: Understanding and improving coverage
- **Debugging**: Identifying and fixing test failures
- **Quality tools**: pytest, mypy, ruff, coverage

### Resources:
- [TDD Practices Documentation](.kiro/steering/tdd_practices.md)
- [Quality Assurance Workflow](.kiro/steering/quality_assurance_workflow.md)
- [Never Bypass Quality Gates](.kiro/steering/never_bypass_quality_gates.md)
- [Evidence-Based Development](.kiro/steering/evidence_based_development.md)

## Conclusion

**Failing tests are a red line that must never be crossed.**

This policy exists to maintain the exceptional quality standards that have made this project successful. Every commit must represent working, tested, production-ready code.

**When in doubt, fix the tests first, then commit.**

---

*This policy was established after discovering the critical importance of maintaining test integrity for project success and team productivity.*
