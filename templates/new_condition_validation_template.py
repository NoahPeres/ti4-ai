"""
Template for implementing new ability condition validation.

This template provides a standardized approach for adding validation
for new AbilityCondition enum values while maintaining fail-closed behavior.

USAGE:
1. Add new condition to AbilityCondition enum in constants.py
2. Copy this template and implement the specific validation logic
3. Add the validation to the main validate_ability_conditions function
4. Write comprehensive tests for both success and failure cases

IMPORTANT: All conditions must have explicit validation - no fallthrough!
"""

from typing import Any

from ti4.core.constants import AbilityCondition


def validate_new_condition_template(
    condition: AbilityCondition, context: dict[str, Any]
) -> bool:
    """
    Template for validating a new ability condition.

    This function demonstrates the pattern for implementing condition validation
    that follows the fail-closed approach required by the framework.

    Args:
        condition: The AbilityCondition enum to validate
        context: Game state context containing relevant information

    Returns:
        True if the condition is met, False otherwise

    Raises:
        NotImplementedError: If condition validation is not implemented
        TypeError: If condition is not an AbilityCondition enum

    Example Context Keys:
        - "player_id": ID of the player whose condition is being checked
        - "system_id": ID of the system where the condition applies
        - "planet_id": ID of the planet where the condition applies
        - "units": List of units relevant to the condition
        - "game_state": Current game state object
        - "phase": Current game phase
        - Additional keys specific to the condition being validated
    """

    # STEP 1: Validate input types
    if not isinstance(condition, AbilityCondition):
        raise TypeError(f"Expected AbilityCondition enum, got {type(condition)}")

    # STEP 2: Implement specific condition validation
    if condition == AbilityCondition.NEW_CONDITION_EXAMPLE:
        # Example: Check if player has ships in the system
        return _validate_new_condition_example(context)

    elif condition == AbilityCondition.ANOTHER_NEW_CONDITION:
        # Example: Check if system contains specific features
        return _validate_another_new_condition(context)

    # STEP 3: Fail-closed behavior for unhandled conditions
    else:
        raise NotImplementedError(
            f"Validation for condition {condition.value} is not implemented. "
            f"All ability conditions must have explicit validation logic. "
            f"Please implement validation for this condition or remove it from use."
        )


def _validate_new_condition_example(context: dict[str, Any]) -> bool:
    """
    Validate NEW_CONDITION_EXAMPLE condition.

    Args:
        context: Game state context

    Returns:
        True if condition is met, False otherwise

    Required Context Keys:
        - "player_id": Player whose condition is being checked
        - "system_id": System where condition applies
        - "game_state": Current game state
    """
    # STEP 1: Extract required context values
    player_id = context.get("player_id")
    system_id = context.get("system_id")
    game_state = context.get("game_state")

    # STEP 2: Validate required context is present
    if player_id is None:
        return False

    if system_id is None:
        return False

    if game_state is None:
        return False

    # STEP 3: Implement specific validation logic
    try:
        # Example: Check if player has ships in the specified system
        game_state.get_player(player_id)
        system = game_state.get_system(system_id)

        # Check for ships in the system
        player_ships = [
            unit for unit in system.units if unit.owner == player_id and unit.is_ship()
        ]

        return len(player_ships) > 0

    except (AttributeError, KeyError) as e:
        # Handle missing game state components gracefully
        print(f"Warning: Could not validate condition due to missing game state: {e}")
        return False


def _validate_another_new_condition(context: dict[str, Any]) -> bool:
    """
    Validate ANOTHER_NEW_CONDITION condition.

    Args:
        context: Game state context

    Returns:
        True if condition is met, False otherwise

    Required Context Keys:
        - "system_id": System where condition applies
        - "required_feature": Feature that must be present
        - "game_state": Current game state
    """
    # STEP 1: Extract required context values
    system_id = context.get("system_id")
    required_feature = context.get("required_feature")
    game_state = context.get("game_state")

    # STEP 2: Validate required context is present
    if not all([system_id, required_feature, game_state]):
        return False

    # STEP 3: Implement specific validation logic
    try:
        system = game_state.get_system(system_id)

        # Example: Check if system has the required feature
        return hasattr(system, required_feature) and getattr(system, required_feature)

    except (AttributeError, KeyError) as e:
        # Handle missing game state components gracefully
        print(f"Warning: Could not validate condition due to missing game state: {e}")
        return False


# STEP 4: Integration with main validation function
"""
To integrate these new conditions with the main validation function,
add them to the validate_ability_conditions function in abilities_integration.py:

def validate_ability_conditions(conditions: list[Any], context: dict[str, Any]) -> bool:
    # ... existing validation logic ...

    for condition in conditions:
        # ... existing condition checks ...

        elif condition == AbilityCondition.NEW_CONDITION_EXAMPLE:
            if not _validate_new_condition_example(context):
                return False

        elif condition == AbilityCondition.ANOTHER_NEW_CONDITION:
            if not _validate_another_new_condition(context):
                return False

        # ... continue with other conditions ...

        else:
            # Fail-closed behavior
            raise NotImplementedError(
                f"Validation for condition {condition.value} is not implemented. "
                "All ability conditions must have explicit validation logic."
            )

    return True
"""


# STEP 5: Test template
"""
Example test cases for the new conditions:

def test_new_condition_example_validation():
    '''Test NEW_CONDITION_EXAMPLE validation.'''
    from ti4.core.constants import AbilityCondition

    # Test success case
    context = {
        "player_id": "player1",
        "system_id": "system1",
        "game_state": mock_game_state_with_ships()
    }
    assert validate_new_condition_template(
        AbilityCondition.NEW_CONDITION_EXAMPLE,
        context
    )

    # Test failure case
    context = {
        "player_id": "player1",
        "system_id": "system1",
        "game_state": mock_game_state_without_ships()
    }
    assert not validate_new_condition_template(
        AbilityCondition.NEW_CONDITION_EXAMPLE,
        context
    )

    # Test missing context
    context = {"player_id": "player1"}  # Missing system_id and game_state
    assert not validate_new_condition_template(
        AbilityCondition.NEW_CONDITION_EXAMPLE,
        context
    )


def test_unimplemented_condition_raises_error():
    '''Test that unimplemented conditions raise NotImplementedError.'''
    from ti4.core.constants import AbilityCondition

    # Create a new condition that's not implemented
    with pytest.raises(NotImplementedError) as exc_info:
        validate_new_condition_template(
            AbilityCondition.UNIMPLEMENTED_CONDITION,
            {}
        )

    # Verify error message is descriptive
    assert "not implemented" in str(exc_info.value).lower()
    assert "UNIMPLEMENTED_CONDITION" in str(exc_info.value)
"""


# STEP 6: Documentation requirements
"""
When adding new conditions, update the following documentation:

1. Add to AbilityCondition enum in constants.py with descriptive docstring
2. Add to enum documentation in docs/enum_systems_reference.md
3. Add validation example to docs/development_guidelines.md
4. Update API reference documentation
5. Add usage examples to relevant technology implementations

Example enum addition:

class AbilityCondition(Enum):
    # ... existing conditions ...

    NEW_CONDITION_EXAMPLE = "new_condition_example"
    '''Condition that checks if player has ships in the system.'''

    ANOTHER_NEW_CONDITION = "another_new_condition"
    '''Condition that checks if system contains required feature.'''
"""
