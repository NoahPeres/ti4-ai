# TI4 AI Development Standards - MANDATORY FOR ALL AI AGENTS

## 🚨 CRITICAL: READ THIS FIRST

This document establishes **MANDATORY** development standards for the TI4 AI project. These standards were established after a comprehensive implementation status audit revealed exceptional quality in completed systems and identified the practices that must be maintained to prevent technical debt and ensure production-ready code.

**ALL AI AGENTS working on this project MUST follow these standards without exception.**

## 🚨 ABSOLUTE PROHIBITION: NEVER IGNORE PRODUCTION CODE QUALITY

**CRITICAL RULE: NEVER ignore mypy checks or failing tests on ANY production code (`src/` directory).**

- ❌ **NEVER use `# type: ignore` without specific error codes** in production code
- ❌ **NEVER bypass failing tests** in production code
- ❌ **NEVER commit code that fails type checking** in the `src/` directory
- ❌ **NEVER use `--no-verify` or similar bypass mechanisms**

**Why this is non-negotiable:**
- Production code type safety is what enables our 90%+ test coverage and zero-bug deployment record
- Type errors in production code lead to runtime failures that break the entire game engine
- Bypassing quality checks creates technical debt that compounds exponentially
- Our strict type safety is a competitive advantage that must be preserved

**If you encounter type errors in production code:**
1. **FIX the underlying type issue** - don't ignore it
2. **Add proper type annotations** where missing
3. **Use specific type ignores with error codes** only when absolutely necessary
4. **Ask for help** if you're unsure how to resolve the type issue

**Test code (`tests/` directory) can have relaxed type checking, but production code must be pristine.**

---

## 📊 Project Quality Achievements (DO NOT COMPROMISE)

### Current Quality Standards Achieved
- ✅ **51/101 rules (50.5%) fully implemented** with production-ready quality
- ✅ **2,500+ comprehensive test cases** across all implemented systems
- ✅ **90%+ test coverage** for completed rules with strict quality standards
- ✅ **Complete type safety compliance** throughout production code
- ✅ **Mature architectural patterns** supporting complex game mechanics

### Quality Metrics That MUST Be Maintained
- **Test Coverage**: 90%+ minimum for all new implementations, 95%+ for critical path rules
- **Type Safety**: Strict mypy compliance with zero type ignores in production code
- **Performance**: <100ms response time for all game actions
- **Documentation**: Complete LRR analysis for every rule implementation

---

## 🎯 MANDATORY DEVELOPMENT WORKFLOW

### 1. Test-Driven Development (TDD) - NON-NEGOTIABLE

**EVERY implementation MUST follow strict RED-GREEN-REFACTOR cycle:**

#### RED Phase (Test Fails)
- **CRITICAL**: Write a test that fails on an ASSERTION, not on compilation/syntax/import errors
- Before writing any production code, ensure you have a failing test that demonstrates the missing functionality
- The test must be able to run and fail with a clear assertion error message
- **Anti-pattern**: Tests that fail due to missing modules, syntax errors, or compilation issues are NOT valid RED phases

#### GREEN Phase (Make Test Pass)
- Write the MINIMAL amount of code to make the failing test pass
- Don't implement more functionality than what the current test requires
- Focus on making the test pass, not on perfect implementation

#### REFACTOR Phase (MANDATORY - Never Skip)
- **ALWAYS explicitly consider refactoring** after each GREEN phase
- Look for code duplication, unclear naming, complex logic, or design issues
- Make an INTENTIONAL DECISION whether to refactor or not
- If choosing NOT to refactor, provide clear justification

### 2. Quality Gates - NEVER BYPASS

**NEVER, UNDER ANY CIRCUMSTANCES, USE `--no-verify` OR ANY OTHER METHOD TO BYPASS QUALITY GATES**

#### Forbidden Commands
❌ **NEVER USE:**
- `git commit --no-verify`
- `git commit -n`
- `git push --no-verify`
- Any other bypass mechanism

#### Correct Approach When Hooks Fail
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

### 3. Evidence-Based Development - NO ASSUMPTIONS

**NEVER make assumptions about code behavior, API responses, or system state**

#### Zero Tolerance for Guessing
- If you're not 100% certain of a fact, you MUST:
  - Research in existing documentation
  - Examine the actual codebase
  - Run tests or experiments to verify
  - Ask the user for clarification
- **Better to ask than to be wrong**

#### Manual Confirmation Protocol for TI4 Components
**BEFORE implementing ANY specific game component details not explicitly outlined in the LRR, you MUST:**
1. **STOP** - Do not proceed with implementation
2. **ASK** the user for explicit confirmation of the component's specifications
3. **WAIT** for user response before continuing
4. **DOCUMENT** the confirmed specifications in code comments
5. **IMPLEMENT** only after receiving explicit approval

---

## 📋 IMPLEMENTATION STANDARDS

### 1. Test Coverage Requirements

#### Minimum Coverage Standards
- **Critical Path Rules (27, 92, 81, 89)**: 95%+ coverage
- **All Other Rules**: 90%+ coverage
- **Integration Tests**: 100% coverage for complete gameplay scenarios
- **Edge Cases**: Comprehensive coverage for error conditions and boundary cases

#### Test Quality Standards
```python
# ✅ GOOD: Descriptive test names and comprehensive scenarios
def test_custodians_token_removal_requires_six_influence_and_ships_in_system():
    # Arrange: Set up game state with player having 6 influence and ships in Mecatol Rex
    # Act: Attempt to remove custodians token
    # Assert: Token removal succeeds and player gains 1 victory point

# ❌ BAD: Vague test names and incomplete scenarios
def test_token_removal():
    # Incomplete test that doesn't specify requirements
```

#### Test Structure Requirements
- **Arrange-Act-Assert pattern** for all tests
- **Descriptive test method names** that explain what is being tested
- **Helper methods** to reduce duplication
- **Parameterized tests** for comprehensive coverage
- **Descriptive error messages** in assertions

### 2. Type Safety Standards

#### Static Type Checking (MyPy)
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

#### Key Rules
- **No `# type: ignore` comments** allowed in production code
- **All functions must have complete type annotations**
- **Generic types must be properly parameterized**
- **Any usage is strictly controlled**

#### Runtime Type Checking
```python
from src.ti4.core.runtime_type_checking import runtime_type_check

@runtime_type_check
def process_game_state(state: GameState) -> ActionResult:
    # Function will validate types at runtime
    pass
```

### 3. Documentation Standards

#### Code Documentation Requirements
- **Include docstrings for all public methods**
- **Reference relevant LRR rules with specific numbers**
- **Provide usage examples**
- **Document error conditions**
- **Include parameter and return value documentation**
- **Document all exceptions that can be raised**

#### LRR Analysis Requirements
Every rule implementation MUST have a corresponding LRR analysis file in `.trae/lrr_analysis/` with:
- **Complete sub-rule breakdown**
- **Implementation status tracking**
- **Test coverage documentation**
- **Integration points identification**
- **Success criteria definition**

### 4. Performance Standards

#### Response Time Requirements
- **Individual game actions**: <100ms
- **Complete tactical action**: <200ms
- **Complete status phase**: <500ms
- **End-to-end game turn**: <2 seconds

#### Performance Monitoring
- **Benchmark all critical operations**
- **Profile performance during development**
- **Optimize before committing**
- **Monitor regression in CI/CD**

---

## 🏗️ ARCHITECTURAL STANDARDS

### 1. Code Organization

#### File Structure
```
src/ti4/
├── core/           # Core game mechanics (rules implementation)
├── actions/        # Player actions and validation
├── commands/       # Command pattern implementations
├── players/        # Player management
└── testing/        # Test utilities and scenarios
```

#### Class Design Principles
- **Single Responsibility Principle**: Each class does one thing well
- **Dependency Injection**: Use constructor injection for dependencies
- **Immutable Game State**: Game state changes return new state objects
- **Type Safety**: All public interfaces fully typed

### 2. Integration Patterns

#### Game State Management
```python
# ✅ GOOD: Immutable state updates
def execute_action(self, action: Action, game_state: GameState) -> GameState:
    # Validate action
    if not self.is_valid_action(action, game_state):
        raise InvalidActionError("Action not valid")

    # Create new state with changes
    new_state = game_state.apply_action(action)
    return new_state

# ❌ BAD: Mutable state modifications
def execute_action(self, action: Action, game_state: GameState) -> None:
    # Modifies state in place - breaks immutability
    game_state.player_resources[action.player_id] -= action.cost
```

#### Error Handling
```python
# ✅ GOOD: Specific exception types with descriptive messages
class InsufficientResourcesError(TI4GameError):
    """Raised when player lacks required resources for action."""

    def __init__(self, player_id: str, required: int, available: int):
        super().__init__(
            f"Player {player_id} needs {required} resources but only has {available}"
        )

# ❌ BAD: Generic exceptions without context
raise ValueError("Not enough resources")
```

### 3. Testing Architecture

#### Test Organization
```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for system interactions
├── end_to_end/     # Complete gameplay scenario tests
└── performance/    # Performance and load tests
```

#### Test Utilities
```python
# ✅ GOOD: Reusable test builders and scenarios
class GameStateBuilder:
    def with_player(self, player_id: str) -> 'GameStateBuilder':
        # Builder pattern for test setup

    def with_resources(self, player_id: str, resources: int) -> 'GameStateBuilder':
        # Fluent interface for test data

    def build(self) -> GameState:
        # Create configured game state
```

---

## 🚨 CRITICAL PATH FOCUS

### Current Priority: 4 Critical Blocking Rules

**80% of development effort MUST focus on these rules in this order:**

1. **Rule 27: Custodians Token** (4 weeks) - HIGHEST PRIORITY BLOCKER
   - Unlocks agenda phase activation
   - Enables political gameplay layer
   - **Success Criteria**: Agenda phase can be activated via token removal

2. **Rule 92: Trade Strategy Card** (3 weeks) - ECONOMIC SYSTEM COMPLETION
   - Completes economic strategy options
   - Enables commodity trading mechanics
   - **Success Criteria**: Complete economic strategy gameplay

3. **Rule 81: Status Phase** (2 weeks) - ROUND MANAGEMENT COMPLETION
   - Enables proper round progression
   - Completes game flow mechanics
   - **Success Criteria**: Complete round transitions functional

4. **Rule 89: Tactical Action** (3 weeks) - CORE GAMEPLAY COMPLETION
   - Completes tactical action workflow
   - Integrates movement, combat, production
   - **Success Criteria**: Complete tactical gameplay operational

### Implementation Sequence Rules
- **Complete each rule before moving to the next**
- **Achieve 95%+ test coverage before considering rule complete**
- **Validate integration with existing systems**
- **Performance benchmark all new functionality**

---

## 🔧 DEVELOPMENT COMMANDS

### Quality Assurance Commands
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

### TDD Workflow Commands
```bash
# Run single test during TDD
uv run pytest path/to/test.py::test_function_name -v

# Run all tests in file
uv run pytest path/to/test.py -v

# Always use -v flag for verbose output
```

---

## ⚠️ COMMON ANTI-PATTERNS TO AVOID

### 1. Development Anti-Patterns
❌ **Writing tests that fail on import errors instead of assertions**
❌ **Implementing multiple features before writing tests**
❌ **Skipping the refactor consideration phase**
❌ **Writing complex implementations when simple ones suffice**
❌ **Adding untested functionality "because it's obvious"**

### 2. Quality Anti-Patterns
❌ **Using `# type: ignore` to bypass type checking**
❌ **Skipping test coverage for "simple" functions**
❌ **Bypassing pre-commit hooks with `--no-verify`**
❌ **Making assumptions about game component specifications**
❌ **Implementing without LRR analysis documentation**

### 3. Architecture Anti-Patterns
❌ **Modifying game state in place (breaks immutability)**
❌ **Using generic exceptions without specific error types**
❌ **Creating circular dependencies between modules**
❌ **Mixing business logic with presentation logic**
❌ **Ignoring performance implications of design decisions**

---

## 📈 SUCCESS METRICS

### Quality Metrics (Monitored Continuously)
- **Test Coverage**: >90% for all code, >95% for critical path
- **Type Safety**: 0 mypy errors in production code
- **Performance**: All benchmarks within acceptable ranges
- **Documentation**: 100% of public APIs documented

### Development Velocity Metrics
- **Critical Rule Completion**: 1 rule per 3-week cycle (including testing)
- **Bug Rate**: <3 minor bugs per rule release, 0 critical bugs
- **Integration Health**: 100% integration test pass rate
- **Code Review**: All code reviewed before merge

### Project Health Indicators
- **Green**: On schedule, quality metrics met, tests passing
- **Yellow**: Minor delays, quality concerns, some test failures
- **Red**: Major delays, quality issues, significant test failures

---

## 🎯 ENFORCEMENT AND ACCOUNTABILITY

### Automated Enforcement
- **Pre-commit hooks** prevent bad commits from entering repository
- **CI/CD pipeline** blocks merges that fail quality checks
- **Coverage requirements** prevent undertested code from being merged
- **Security scanning** catches vulnerabilities automatically

### Manual Review Requirements
- **All code must be reviewed** before merging
- **Architecture reviews** required for complex changes
- **Performance reviews** required for critical path implementations
- **Security reviews** required for sensitive operations

### Escalation Process
1. **Quality gate failures**: Fix issues, don't bypass
2. **Repeated violations**: Document and address root cause
3. **Architectural concerns**: Escalate to project maintainer
4. **Performance issues**: Immediate optimization required

---

## 🚀 CONCLUSION

These standards represent the foundation of the TI4 AI project's success. They were established based on comprehensive analysis of what works and what prevents technical debt.

**Key Principles for All AI Agents:**
1. **Quality First**: Never compromise on test coverage or type safety
2. **Evidence-Based**: Never assume, always verify
3. **TDD Discipline**: RED-GREEN-REFACTOR cycle is mandatory
4. **Critical Path Focus**: 80% effort on Rules 27, 92, 81, 89
5. **Documentation Excellence**: Every implementation fully documented

**Remember**: These standards exist to maintain the exceptional quality already achieved and ensure the project delivers a production-ready TI4 AI system. Following them strictly will result in faster development, fewer bugs, and a more maintainable codebase.

**When in doubt, ask the user rather than making assumptions. Quality and correctness are more important than speed.**

## 🚨 CRITICAL REMINDER: NEVER IGNORE MYPY CHECKS OR TESTS

**This rule was added based on code review feedback and is absolutely mandatory:**

- ❌ **NEVER use `# type: ignore` without specific error codes** in production code (`src/` directory)
- ❌ **NEVER bypass failing tests** in production code
- ❌ **NEVER commit code that fails type checking** in the `src/` directory
- ❌ **NEVER use `--no-verify` or similar bypass mechanisms**

**If you encounter type errors in production code:**
1. **FIX the underlying type issue** - don't ignore it
2. **Add proper type annotations** where missing
3. **Use specific type ignores with error codes** only when absolutely necessary
4. **Ask for help** if you're unsure how to resolve the type issue

**Production code type safety is what enables our 90%+ test coverage and zero-bug deployment record. This is non-negotiable.**

## 🚨 ABSOLUTE PROHIBITION: NEVER USE TYPE IGNORES

**NEVER use `# type: ignore` comments in production code under any circumstances:**

- ❌ **NEVER use `# type: ignore[attr-defined]`** - Fix the class design instead
- ❌ **NEVER use `# type: ignore[no-any-return]`** - Add proper type annotations
- ❌ **NEVER use any other type ignore variants** - Address the root cause

**If you encounter type errors:**
1. **REFACTOR the code structure** to be type-safe by design
2. **ADD proper type annotations** and class definitions
3. **USE proper inheritance and composition** instead of dynamic attributes
4. **DESIGN classes with static structure** that mypy can understand

**Type ignores indicate poor design and must be eliminated through proper refactoring.**
