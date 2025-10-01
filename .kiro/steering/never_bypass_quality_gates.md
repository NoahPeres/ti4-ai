# CRITICAL: Never Bypass Quality Gates

## 🚨 ABSOLUTE PROHIBITION

**NEVER, UNDER ANY CIRCUMSTANCES, USE `--no-verify` OR ANY OTHER METHOD TO BYPASS QUALITY GATES**

## Forbidden Commands

❌ **NEVER USE:**
- `git commit --no-verify`
- `git commit -n`
- `git push --no-verify`
- Any other bypass mechanism

## Why This Is Critical

1. **Quality Assurance**: Pre-commit hooks are our first line of defense against bugs
2. **Type Safety**: Bypassing mypy checks can introduce type errors into production
3. **Code Standards**: Linting and formatting ensure consistent, readable code
4. **Security**: Security checks prevent vulnerabilities from entering the codebase
5. **Test Coverage**: Coverage requirements ensure adequate testing

## Correct Approach When Hooks Fail

When pre-commit hooks fail:

1. **READ THE ERROR MESSAGES** - They tell you exactly what's wrong
2. **FIX THE UNDERLYING ISSUES** - Don't bypass, fix the root cause
3. **Run quality checks manually** if needed:
   ```bash
   make type-check
   make lint
   make format
   make test
   ```
4. **Only commit when all checks pass**

## Documentation Issues

If documentation consistency checks fail:
1. Investigate what references are broken
2. Update documentation to match code changes
3. Fix cross-references and file paths
4. Ensure all links are valid

## Emergency Situations

Even in emergencies, bypassing quality gates is **NEVER ACCEPTABLE**. If there's a critical issue:

1. Fix the quality issues first
2. Make minimal, targeted changes
3. Ensure all checks pass
4. Then commit and deploy

## Enforcement

- Any commit that bypasses quality gates must be immediately reverted
- The underlying issues must be fixed properly
- A new commit must be made that passes all quality checks

## Remember

Quality gates exist to protect the codebase and our users. Bypassing them is like removing safety equipment - it might seem faster in the moment, but it creates dangerous technical debt and potential failures.

**When in doubt, fix the issue properly rather than bypassing the check.**
