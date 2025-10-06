# Git Command Guidelines for AI Agents

## Critical Rule: Avoid Git Commands with Pagers

**NEVER use git commands that invoke pagers or require manual intervention to exit.**

### Forbidden Commands
- `git log` (without `--oneline` or `--no-pager`)
- `git diff` (without `--no-pager` when output is large)
- `git show` (without `--no-pager`)
- Any git command that might invoke a pager

### Safe Alternatives

#### For Git Log
```bash
# ❌ NEVER: git log
# ✅ USE:
git log --oneline -10
git --no-pager log --oneline
```

#### For Git Diff
```bash
# ❌ NEVER: git diff (for large outputs)
# ✅ USE:
git diff --name-only
git diff --stat
git --no-pager diff
```

#### For Git Show
```bash
# ❌ NEVER: git show
# ✅ USE:
git --no-pager show --stat
git show --name-only
```

### General Guidelines

1. **Always use `--no-pager`** when output might be large
2. **Use `--oneline`** for log commands
3. **Use `--stat` or `--name-only`** for diff/show commands
4. **Limit output** with `-n` or `--max-count` flags
5. **Test commands** in small repositories first

### Why This Matters

Pager commands require manual intervention to exit (pressing 'q'), which:
- Blocks automated workflows
- Requires human intervention
- Can cause infinite waiting in CI/CD
- Breaks the autonomous development flow

### Enforcement

All AI agents must follow these guidelines to maintain smooth, uninterrupted development workflows.
