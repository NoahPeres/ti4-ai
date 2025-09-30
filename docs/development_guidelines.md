# Development Guidelines

## Overview

This document provides comprehensive guidelines for developers working on the TI4 game framework, with special focus on ability system implementation, trigger usage, and validation practices.

## Canonical Trigger Usage

### Core Principle: Use Enum Values, Never Hardcoded Strings

**CRITICAL**: All ability triggers must use canonical enum values from `AbilityTrigger` instead of hardcoded strings.

#### ✅ Correct Usage

```python
from ti4.core.constants import AbilityTrigger

# In technology implementations
ability = AbilitySpecification(
    trigger=AbilityTrigger.AFTER_TACTICAL_ACTION,  # Use enum
    effect=AbilityEffectType.EXPLORE_FRONTIER_TOKEN,
    conditions=[AbilityCondition.SYSTEM_CONTAINS_FRONTIER]
)

# In tests
def test_ability_triggers():
    # Use the same enum values as production code
    trigger = AbilityTrigger.AFTER_TACTICAL_ACTION.value
    assert ability.trigger.value == trigger
```

#### ❌ Incorrect Usage

```python
# NEVER use hardcoded strings
ability = AbilitySpecification(
    trigger="tactical_action_in_frontier_system",  # WRONG
    effect=AbilityEffectType.EXPLORE_FRONTIER_TOKEN,
    conditions=[AbilityCondition.SYSTEM_CONTAINS_FRONTIER]
)

# NEVER use different strings in tests
def test_ability_triggers():
    # This creates test-production misalignment
    assert ability.trigger == "some_hardcoded_string"  # WRONG
```

### Available Trigger Types

The `AbilityTrigger` enum provides these canonical trigger values:

```python
class AbilityTrigger(Enum):
    """Enumeration of ability triggers for technology framework."""

    ACTION = "action"                           # Exhaustible abilities
    AFTER_ACTIVATE_SYSTEM = "after_activate_system"
    AFTER_TACTICAL_ACTION = "after_tactical_action"  # Most common
    WHEN_RESEARCH_TECHNOLOGY = "when_research_technology"
    START_OF_TURN = "start_of_turn"
    END_OF_TURN = "end_of_turn"
    WHEN_RETREAT_DECLARED = "when_retreat_declared"
    BEFORE_COMBAT = "before_combat"
    AFTER_COMBAT = "after_combat"
    WHEN_PRODUCING_UNITS = "when_producing_units"
    START_OF_PHASE = "start_of_phase"
    END_OF_PHASE = "end_of_phase"
```

### Implementation Guidelines

1. **Always Import the Enum**
   ```python
   from ti4.core.constants import AbilityTrigger
   ```

2. **Use Enum Values Consistently**
   ```python
   # In specifications
   trigger=AbilityTrigger.AFTER_TACTICAL_ACTION

   # When comparing values
   if ability.trigger == AbilityTrigger.AFTER_TACTICAL_ACTION:
       # Handle trigger
   ```

3. **Test-Production Alignment**
   ```python
   # Tests should use the same enum values
   expected_trigger = AbilityTrigger.AFTER_TACTICAL_ACTION.value
   assert technology.abilities[0].trigger.value == expected_trigger
   ```

## Fail-Closed Validation Approach

### Core Principle: Explicit Validation for All Conditions

The framework implements a **fail-closed** approach to ability condition validation. This means:

- **Every condition must have explicit validation logic**
- **Unimplemented conditions raise `NotImplementedError`**
- **No silent failures or fallthrough behavior**

#### ✅ Correct Implementation

```python
def validate_ability_conditions(conditions: list[Any], context: dict[str, Any]) -> bool:
    """Validate conditions with explicit fail-closed behavior."""

    for condition in conditions:
        if condition == AbilityCondition.HAS_SHIPS_IN_SYSTEM:
            if not context.get("has_ships", False):
                return False
        elif condition == AbilityCondition.SYSTEM_CONTAINS_FRONTIER:
            if not context.get("has_frontier_token", False):
                return False
        # ... explicit handling for each condition
        else:
            # Fail-closed: explicitly reject unhandled conditions
            raise NotImplementedError(
                f"Validation for condition {condition.value} is not implemented. "
                "All ability conditions must have explicit validation logic."
            )

    return True
```

#### ❌ Incorrect Implementation

```python
def validate_ability_conditions(conditions: list[Any], context: dict[str, Any]) -> bool:
    """WRONG: Allows silent failures."""

    for condition in conditions:
        if condition == AbilityCondition.HAS_SHIPS_IN_SYSTEM:
            if not context.get("has_ships", False):
                return False
        # WRONG: Missing explicit handling for other conditions
        # This allows unimplemented conditions to silently pass

    return True  # DANGEROUS: Silent success for unhandled conditions
```

### Benefits of Fail-Closed Validation

1. **Prevents Silent Bugs**: Unimplemented conditions are caught immediately
2. **Forces Complete Implementation**: Developers must handle all conditions
3. **Clear Error Messages**: Descriptive errors guide implementation
4. **System Reliability**: No unexpected ability activations

### Adding New Conditions

When adding new `AbilityCondition` enum values, follow the comprehensive requirements in [Validation Requirements](validation_requirements.md).

**Quick Summary**:

1. **Add to the enum** with documentation
2. **Add explicit validation** with fail-closed behavior
3. **Write comprehensive tests** for all scenarios
4. **Update documentation** and integration points

**See [Validation Requirements](validation_requirements.md) for complete implementation standards.**

## Code Review Checklist

### Trigger Validation

- [ ] **No hardcoded trigger strings**: All triggers use `AbilityTrigger` enum values
- [ ] **Consistent imports**: `from ti4.core.constants import AbilityTrigger`
- [ ] **Test alignment**: Tests use same trigger values as production code
- [ ] **Proper enum usage**: Using `.value` when string comparison needed

### Condition Validation

- [ ] **Explicit condition handling**: All conditions have explicit validation logic
- [ ] **No fallthrough behavior**: No silent success for unhandled conditions
- [ ] **Descriptive error messages**: `NotImplementedError` includes helpful details
- [ ] **Complete test coverage**: Both success and failure cases tested

### General Quality

- [ ] **Type hints**: All functions have proper type annotations
- [ ] **Documentation**: Docstrings explain behavior and requirements
- [ ] **Error handling**: Edge cases and invalid inputs handled
- [ ] **Integration tests**: End-to-end scenarios tested

## Prevention Measures

### Linting Rules

The following linting rules help detect common issues:

1. **Hardcoded Trigger Detection**
   ```python
   # Custom rule to detect hardcoded trigger strings
   # Add to .ruff.toml or similar configuration
   ```

2. **Import Validation**
   ```python
   # Ensure AbilityTrigger is imported when used
   ```

### Templates

#### New Ability Implementation Template

```python
"""
Template for implementing new technology abilities.
"""

from ti4.core.constants import AbilityTrigger, AbilityEffectType, AbilityCondition
from ti4.core.technology_cards.specifications import AbilitySpecification

def create_new_technology_ability() -> AbilitySpecification:
    """
    Create ability specification for [Technology Name].

    CONFIRMED SPECIFICATIONS - DO NOT MODIFY WITHOUT USER APPROVAL:
    - Trigger: [User confirmed trigger]
    - Effect: [User confirmed effect]
    - Conditions: [User confirmed conditions]
    - Confirmed by user on [date]

    Returns:
        AbilitySpecification for the technology
    """
    return AbilitySpecification(
        trigger=AbilityTrigger.AFTER_TACTICAL_ACTION,  # Use enum
        effect=AbilityEffectType.EXPLORE_FRONTIER_TOKEN,  # Use enum
        conditions=[AbilityCondition.SYSTEM_CONTAINS_FRONTIER],  # Use enum
        mandatory=False
    )
```

#### New Condition Validation Template

```python
def validate_new_condition(condition: AbilityCondition, context: dict[str, Any]) -> bool:
    """
    Validate [condition name] in the given context.

    Args:
        condition: The AbilityCondition to validate
        context: Game state context

    Returns:
        True if condition is met, False otherwise

    Raises:
        NotImplementedError: If condition validation is not implemented
    """
    if condition == AbilityCondition.NEW_CONDITION:
        # Implement specific validation logic
        required_value = context.get("required_key")
        if required_value is None:
            return False
        # Add specific validation logic here
        return bool(required_value)
    else:
        raise NotImplementedError(
            f"Validation for condition {condition.value} is not implemented. "
            "All ability conditions must have explicit validation logic."
        )
```

## Testing Guidelines

### Trigger Testing

```python
def test_ability_uses_canonical_trigger():
    """Test that ability uses canonical enum trigger."""
    ability = create_technology_ability()

    # Verify enum usage
    assert isinstance(ability.trigger, AbilityTrigger)
    assert ability.trigger == AbilityTrigger.AFTER_TACTICAL_ACTION

    # Verify string value when needed
    assert ability.trigger.value == "after_tactical_action"
```

### Condition Testing

```python
def test_condition_validation_fail_closed():
    """Test that unimplemented conditions raise NotImplementedError."""
    from ti4.core.constants import AbilityCondition

    # Create a new condition that's not implemented
    new_condition = AbilityCondition.NEW_UNIMPLEMENTED_CONDITION

    with pytest.raises(NotImplementedError) as exc_info:
        validate_ability_conditions([new_condition], {})

    # Verify descriptive error message
    assert "not implemented" in str(exc_info.value).lower()
    assert new_condition.value in str(exc_info.value)
```

## Migration Guide

### Updating Existing Code

1. **Find hardcoded triggers**:
   ```bash
   # Search for potential hardcoded triggers
   grep -r "tactical_action" src/ --include="*.py"
   ```

2. **Replace with enum values**:
   ```python
   # Before
   trigger="tactical_action_in_frontier_system"

   # After
   trigger=AbilityTrigger.AFTER_TACTICAL_ACTION
   ```

3. **Update tests**:
   ```python
   # Before
   assert ability.trigger == "some_string"

   # After
   assert ability.trigger == AbilityTrigger.AFTER_TACTICAL_ACTION
   ```

### Validation Updates

1. **Add explicit condition handling**:
   ```python
   # Add to validate_ability_conditions function
   elif condition == AbilityCondition.YOUR_CONDITION:
       # Add specific validation logic
       return validate_your_condition(context)
   ```

2. **Remove fallthrough behavior**:
   ```python
   # Remove any implicit success cases
   # Replace with explicit NotImplementedError
   ```

## Best Practices Summary

### Do's ✅

- **Use enum values** for all triggers and conditions
- **Import enums explicitly** from `ti4.core.constants`
- **Implement fail-closed validation** for all conditions
- **Write descriptive error messages** for unimplemented features
- **Test both success and failure cases** thoroughly
- **Align test and production code** trigger usage

### Don'ts ❌

- **Never use hardcoded strings** for triggers
- **Never allow silent failures** in validation
- **Never skip condition validation** implementation
- **Never assume fallthrough behavior** is acceptable
- **Never implement without user confirmation** for game components
- **Never skip testing** edge cases and error conditions

## Quality Assurance

### Automated Checks

Run these commands to verify compliance:

```bash
# Type checking
uv run mypy src --strict

# Linting
uv run ruff check src tests

# Tests
uv run pytest tests/ -v

# Full quality gate
make quality-gate
```

### Manual Review Points

1. **Trigger Usage**: All abilities use `AbilityTrigger` enum values
2. **Condition Validation**: All conditions have explicit validation logic
3. **Error Handling**: Unimplemented features raise `NotImplementedError`
4. **Test Coverage**: Both positive and negative test cases exist
5. **Documentation**: Code is well-documented with clear examples

## Conclusion

Following these guidelines ensures:

- **System Reliability**: No silent failures or unexpected behavior
- **Code Consistency**: Uniform patterns across all implementations
- **Maintainability**: Clear, explicit code that's easy to understand
- **Extensibility**: Well-defined patterns for adding new features
- **Quality**: Comprehensive testing and validation

Remember: **When in doubt, fail closed and ask for clarification.**
