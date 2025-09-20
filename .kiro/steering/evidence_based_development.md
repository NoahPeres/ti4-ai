# Evidence-Based Development Guidelines

## Core Principle: Never Assume, Always Verify

This project requires rigorous, evidence-based development practices. Assumptions and guesswork lead to bugs, technical debt, and wasted time.

## Critical Rules

### 1. Zero Tolerance for Guessing
- **NEVER** make assumptions about code behavior, API responses, or system state
- If you're not 100% certain of a fact, you MUST:
  - Research in existing documentation
  - Examine the actual codebase
  - Run tests or experiments to verify
  - Ask the user for clarification
- **Better to ask than to be wrong**

### 2. Data-Driven Decision Making
- Do not dismiss tool warnings (mypy, ruff, pytest) as "false positives" without investigation
- If you hypothesize something is incorrect, **PROVE IT** with concrete evidence
- Document your findings when you discover the root cause of issues
- Example: If mypy reports an error, investigate the type system issue rather than assuming it's wrong

### 3. Explicit Knowledge Gaps
- When you encounter unfamiliar patterns or unclear requirements:
  - State what you don't know explicitly
  - Research available documentation first
  - Ask specific, targeted questions rather than guessing
  - Document new knowledge for future reference

### 4. Rigorous Development Cycle
- **Always** run the full validation suite after changes:
  - `uv run pytest` - Run all tests
  - `uv run mypy src` - Type checking
  - `uv run ruff check src tests` - Linting
  - `make check-all` - Complete validation
- Don't skip steps because you "think" they'll pass
- Each change can have unexpected ripple effects

## Project-Specific Practices

### Code Quality Standards
- Follow TDD practices strictly (RED-GREEN-REFACTOR)
- Maintain type hints for all public interfaces
- Use descriptive variable and function names
- Write comprehensive tests for edge cases

### Error Handling
- Validate inputs explicitly rather than assuming they're correct
- Handle edge cases that might seem "impossible"
- Use proper exception types with descriptive messages
- Test error conditions as thoroughly as success paths

### Documentation Requirements
- Update docstrings when changing function behavior
- Document complex algorithms and business logic
- Maintain architectural decision records for significant changes
- Keep README and usage examples current

## Red Flags That Indicate Assumption-Making

- Using phrases like "probably", "should work", "I think"
- Skipping validation steps "to save time"
- Implementing features without corresponding tests
- Ignoring tool warnings without investigation
- Making changes without understanding the full impact

## Recovery from Mistakes

When you realize you've made an assumption:
1. Stop and acknowledge the assumption explicitly
2. Gather the actual facts through research/testing
3. Correct the implementation based on evidence
4. Add tests to prevent similar issues
5. Document the learning for future reference

Remember: Precision and diligence now prevent debugging sessions later.
