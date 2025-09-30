# Validation Requirements for New Conditions

## Overview

This document defines the requirements and standards for implementing validation logic for new `AbilityCondition` enum values. All new conditions must follow these requirements to maintain system reliability and consistency.

## Core Requirements

### 1. Fail-Closed Validation

**MANDATORY**: All condition validation must implement fail-closed behavior.

- **Explicit Handling**: Every condition must have explicit validation logic
- **No Fallthrough**: Unimplemented conditions must raise `NotImplementedError`
- **Descriptive Errors**: Error messages must clearly identify the unimplemented condition

```python
# ✅ Correct: Explicit fail-closed behavior
def validate_ability_conditions(conditions: list[Any], context: dict[str, Any]) -> bool:
    for condition in conditions:
        if condition == AbilityCondition.IMPLEMENTED_CONDITION:
            return validate_implemented_condition(context)
        else:
            raise NotImplementedError(
                f"Validation for condition {condition.value} is not implemented. "
                "All ability conditions must have explicit validation logic."
            )

# ❌ Incorrect: Silent fallthrough
def validate_ability_conditions(conditions: list[Any], context: dict[str, Any]) -> bool:
    for condition in conditions:
        if condition == AbilityCondition.IMPLEMENTED_CONDITION:
            return validate_implemented_condition(context)
        # WRONG: Missing else clause allows silent success
    return True  # DANGEROUS: Unhandled conditions pass silently
```

### 2. Type Safety

**MANDATORY**: All validation functions must enforce type safety.

```python
def validate_condition(condition: AbilityCondition, context: dict[str, Any]) -> bool:
    # Validate input types
    if not isinstance(condition, AbilityCondition):
        raise TypeError(f"Expected AbilityCondition enum, got {type(condition)}")

    # Validate context is a dictionary
    if not isinstance(context, dict):
        raise TypeError(f"Expected dict context, got {type(context)}")

    # Continue with validation logic...
```

### 3. Context Validation

**MANDATORY**: All validation functions must validate required context keys.

```python
def validate_has_ships_condition(context: dict[str, Any]) -> bool:
    # Check for required context keys
    required_keys = ["player_id", "system_id", "game_state"]
    missing_keys = [key for key in required_keys if key not in context]

    if missing_keys:
        # Option 1: Return False for missing context (recommended)
        return False

        # Option 2: Raise error for missing context (if critical)
        # raise ValueError(f"Missing required context keys: {missing_keys}")

    # Continue with validation logic...
```

### 4. Error Handling

**MANDATORY**: All validation functions must handle errors gracefully.

```python
def validate_condition_with_game_state(context: dict[str, Any]) -> bool:
    try:
        game_state = context["game_state"]
        player = game_state.get_player(context["player_id"])
        # ... validation logic
        return True

    except KeyError as e:
        # Handle missing context keys
        print(f"Warning: Missing context key: {e}")
        return False

    except AttributeError as e:
        # Handle missing game state methods/attributes
        print(f"Warning: Game state missing expected attribute: {e}")
        return False

    except Exception as e:
        # Handle unexpected errors
        print(f"Error during condition validation: {e}")
        return False
```

## Implementation Standards

### 1. Function Naming

- **Pattern**: `validate_{condition_name}_condition`
- **Example**: `validate_has_ships_in_system_condition`

### 2. Documentation Requirements

```python
def validate_new_condition(context: dict[str, Any]) -> bool:
    """
    Validate NEW_CONDITION in the given context.

    This condition checks if [specific requirement description].

    Args:
        context: Game state context containing:
            - "required_key1": Description of what this key contains
            - "required_key2": Description of what this key contains
            - "optional_key": Description (optional)

    Returns:
        True if condition is met, False otherwise

    Raises:
        TypeError: If context is not a dictionary

    Example:
        >>> context = {"required_key1": "value1", "required_key2": "value2"}
        >>> validate_new_condition(context)
        True
    """
```

### 3. Test Requirements

**MANDATORY**: Every new condition must have comprehensive tests.

```python
def test_new_condition_success():
    """Test condition validation success case."""
    context = {
        "required_key1": "valid_value",
        "required_key2": "valid_value"
    }
    assert validate_new_condition(context) is True

def test_new_condition_failure():
    """Test condition validation failure case."""
    context = {
        "required_key1": "invalid_value",
        "required_key2": "valid_value"
    }
    assert validate_new_condition(context) is False

def test_new_condition_missing_context():
    """Test condition validation with missing context."""
    context = {"required_key1": "value"}  # Missing required_key2
    assert validate_new_condition(context) is False

def test_new_condition_empty_context():
    """Test condition validation with empty context."""
    assert validate_new_condition({}) is False

def test_new_condition_invalid_context_type():
    """Test condition validation with invalid context type."""
    with pytest.raises(TypeError):
        validate_new_condition("not_a_dict")
```

## Integration Requirements

### 1. Enum Addition

**MANDATORY**: Add new condition to `AbilityCondition` enum with documentation.

```python
class AbilityCondition(Enum):
    """Enumeration of ability conditions for technology framework."""

    # ... existing conditions ...

    NEW_CONDITION = "new_condition"
    """
    Condition that checks [specific requirement].

    Required context keys:
    - "required_key1": Description
    - "required_key2": Description

    Example usage:
    - Technology X uses this condition to validate Y
    """
```

### 2. Main Validation Function Integration

**MANDATORY**: Add condition to main validation function.

```python
def validate_ability_conditions(conditions: list[Any], context: dict[str, Any]) -> bool:
    # ... existing validation logic ...

    for condition in conditions:
        # ... existing condition checks ...

        elif condition == AbilityCondition.NEW_CONDITION:
            if not validate_new_condition(context):
                return False

        # ... continue with other conditions ...

        else:
            # Fail-closed behavior - MANDATORY
            raise NotImplementedError(
                f"Validation for condition {condition.value} is not implemented. "
                "All ability conditions must have explicit validation logic."
            )

    return True
```

### 3. Documentation Updates

**MANDATORY**: Update all relevant documentation.

1. **API Reference**: Add condition to API documentation
2. **Enum Reference**: Add to enum systems documentation
3. **Development Guidelines**: Add usage examples
4. **Integration Guide**: Update integration examples

## Quality Assurance

### 1. Validation Checklist

Before submitting new condition validation:

- [ ] **Enum Added**: Condition added to `AbilityCondition` enum with documentation
- [ ] **Validation Function**: Dedicated validation function implemented
- [ ] **Type Safety**: Input types validated and enforced
- [ ] **Context Validation**: Required context keys checked
- [ ] **Error Handling**: Graceful error handling implemented
- [ ] **Integration**: Added to main validation function
- [ ] **Fail-Closed**: Explicit `NotImplementedError` for unhandled conditions
- [ ] **Tests**: Comprehensive test coverage (success, failure, edge cases)
- [ ] **Documentation**: All documentation updated

### 2. Testing Requirements

**MANDATORY**: All conditions must pass these test categories:

1. **Success Cases**: Condition met with valid context
2. **Failure Cases**: Condition not met with valid context
3. **Missing Context**: Required context keys missing
4. **Invalid Context**: Context has wrong types or invalid values
5. **Edge Cases**: Boundary conditions and unusual scenarios
6. **Error Handling**: Graceful handling of unexpected errors

### 3. Performance Considerations

- **Efficient Validation**: Avoid expensive operations when possible
- **Early Returns**: Return False as soon as condition fails
- **Caching**: Cache expensive lookups when appropriate
- **Minimal Dependencies**: Avoid unnecessary external dependencies

## Common Patterns

### 1. Player-Based Conditions

```python
def validate_player_condition(context: dict[str, Any]) -> bool:
    """Validate condition related to player state."""
    player_id = context.get("player_id")
    game_state = context.get("game_state")

    if not player_id or not game_state:
        return False

    try:
        player = game_state.get_player(player_id)
        # Validate player-specific condition
        return player.meets_condition()
    except (AttributeError, KeyError):
        return False
```

### 2. System-Based Conditions

```python
def validate_system_condition(context: dict[str, Any]) -> bool:
    """Validate condition related to system state."""
    system_id = context.get("system_id")
    game_state = context.get("game_state")

    if not system_id or not game_state:
        return False

    try:
        system = game_state.get_system(system_id)
        # Validate system-specific condition
        return system.meets_condition()
    except (AttributeError, KeyError):
        return False
```

### 3. Unit-Based Conditions

```python
def validate_unit_condition(context: dict[str, Any]) -> bool:
    """Validate condition related to unit state."""
    units = context.get("units", [])
    player_id = context.get("player_id")

    if not units or not player_id:
        return False

    # Filter units by player
    player_units = [unit for unit in units if unit.owner == player_id]

    # Validate unit-specific condition
    return any(unit.meets_condition() for unit in player_units)
```

## Migration Guide

### Updating Existing Conditions

When updating existing condition validation:

1. **Maintain Backward Compatibility**: Don't break existing usage
2. **Add Deprecation Warnings**: If changing behavior significantly
3. **Update Tests**: Ensure all tests still pass
4. **Update Documentation**: Reflect any behavior changes

### Removing Conditions

When removing unused conditions:

1. **Deprecation Period**: Mark as deprecated first
2. **Usage Analysis**: Ensure no active usage
3. **Clean Removal**: Remove from enum, validation, tests, and docs
4. **Migration Guide**: Provide alternatives if needed

## Conclusion

Following these validation requirements ensures:

- **System Reliability**: No silent failures or unexpected behavior
- **Code Quality**: Consistent, well-tested validation logic
- **Maintainability**: Clear patterns and comprehensive documentation
- **Extensibility**: Easy to add new conditions following established patterns

Remember: **Fail-closed validation is not optional - it's a critical safety requirement.**
