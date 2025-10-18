"""
Agenda card validation system.

This module provides comprehensive validation for agenda card data,
operations, and state management.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from ti4.core.constants import AgendaType

from .exceptions import AgendaCardValidationError


@dataclass
class ValidationResult:
    """Result of a validation operation."""

    is_valid: bool
    error_message: str = ""
    card_name: str | None = None
    field_name: str | None = None


class AgendaCardValidator:
    """
    Comprehensive validator for agenda card data and operations.

    This class provides validation methods for all aspects of agenda cards
    including names, types, outcomes, metadata, and complete card data.
    """

    def __init__(self) -> None:
        """Initialize the agenda card validator."""
        self._custom_rules: dict[str, list[Callable[[Any], bool]]] = {}

    def _validate_not_none(
        self, value: Any, field_name: str, error_message: str
    ) -> None:
        """
        Helper method to validate that a value is not None.

        Args:
            value: The value to validate
            field_name: The field name for error context
            error_message: The error message to use

        Raises:
            AgendaCardValidationError: If the value is None
        """
        if value is None:
            raise AgendaCardValidationError(
                error_message, field_name=field_name, invalid_value=value
            )

    def _validate_type(
        self, value: Any, expected_type: type, field_name: str, error_message: str
    ) -> None:
        """
        Helper method to validate that a value is of the expected type.

        Args:
            value: The value to validate
            expected_type: The expected type
            field_name: The field name for error context
            error_message: The error message to use

        Raises:
            AgendaCardValidationError: If the value is not of the expected type
        """
        if not isinstance(value, expected_type):
            raise AgendaCardValidationError(
                error_message, field_name=field_name, invalid_value=value
            )

    def _validate_non_empty_string(
        self, value: str, field_name: str, error_message: str
    ) -> None:
        """
        Helper method to validate that a string is not empty after trimming.

        Args:
            value: The string value to validate
            field_name: The field name for error context
            error_message: The error message to use

        Raises:
            AgendaCardValidationError: If the string is empty after trimming
        """
        if not value.strip():
            raise AgendaCardValidationError(
                error_message, field_name=field_name, invalid_value=value
            )

    def validate_card_name(self, name: Any) -> bool:
        """
        Validate an agenda card name.

        Args:
            name: The card name to validate

        Returns:
            True if the name is valid

        Raises:
            AgendaCardValidationError: If the name is invalid
        """
        self._validate_not_none(name, "name", "Agenda card name cannot be None")
        self._validate_type(name, str, "name", "Agenda card name must be a string")
        self._validate_non_empty_string(
            name, "name", "Agenda card name cannot be empty"
        )

        # Apply custom validation rules
        trimmed_name = name.strip()
        if "name" in self._custom_rules:
            for rule in self._custom_rules["name"]:
                if not rule(trimmed_name):
                    raise AgendaCardValidationError(
                        "Card name failed custom validation rule",
                        field_name="name",
                        invalid_value=name,
                    )

        return True

    def validate_voting_outcomes(self, outcomes: Any) -> bool:
        """
        Validate voting outcomes for an agenda card.

        Args:
            outcomes: The voting outcomes to validate

        Returns:
            True if the outcomes are valid

        Raises:
            AgendaCardValidationError: If the outcomes are invalid
        """
        self._validate_not_none(outcomes, "outcomes", "Voting outcomes cannot be None")
        self._validate_type(
            outcomes, list, "outcomes", "Voting outcomes must be a list"
        )

        if not outcomes:
            raise AgendaCardValidationError(
                "Voting outcomes cannot be empty",
                field_name="outcomes",
                invalid_value=outcomes,
            )

        for i, outcome in enumerate(outcomes):
            self._validate_not_none(
                outcome, "outcomes", "Voting outcome cannot be None"
            )
            self._validate_type(
                outcome,
                str,
                "outcomes",
                f"Voting outcome at index {i} must be a string",
            )
            self._validate_non_empty_string(
                outcome, "outcomes", "Voting outcome cannot be empty"
            )

        return True

    def validate_agenda_type(self, agenda_type: Any) -> bool:
        """
        Validate an agenda type.

        Args:
            agenda_type: The agenda type to validate

        Returns:
            True if the agenda type is valid

        Raises:
            AgendaCardValidationError: If the agenda type is invalid
        """
        self._validate_not_none(
            agenda_type, "agenda_type", "Agenda type cannot be None"
        )
        self._validate_type(
            agenda_type, AgendaType, "agenda_type", "Invalid agenda type"
        )

        return True

    def validate_card_metadata(self, metadata: Any) -> bool:
        """
        Validate agenda card metadata.

        Args:
            metadata: The metadata to validate

        Returns:
            True if the metadata is valid

        Raises:
            AgendaCardValidationError: If the metadata is invalid
        """
        self._validate_not_none(metadata, "metadata", "Card metadata cannot be None")
        self._validate_type(
            metadata, dict, "metadata", "Card metadata must be a dictionary"
        )

        # Validate expansion field if present
        if "expansion" in metadata:
            expansion = metadata["expansion"]
            if not isinstance(expansion, str) or not expansion.strip():
                raise AgendaCardValidationError(
                    "Invalid expansion", field_name="metadata", invalid_value=expansion
                )

        return True

    def validate_election_target(self, target: Any, outcome_type: str) -> bool:
        """
        Validate an election target for a specific outcome type.

        Args:
            target: The election target to validate
            outcome_type: The type of election outcome

        Returns:
            True if the target is valid

        Raises:
            AgendaCardValidationError: If the target is invalid
        """
        self._validate_not_none(
            target, "election_target", "Election target cannot be None"
        )
        self._validate_type(
            target, str, "election_target", "Election target must be a string"
        )
        self._validate_non_empty_string(
            target, "election_target", "Invalid election target"
        )

        # Additional validation based on outcome type could be added here
        # For now, we just ensure it's a non-empty string

        return True

    def validate_complete_card_data(self, card_data: dict[str, Any]) -> bool:
        """
        Validate complete agenda card data.

        Args:
            card_data: The complete card data to validate

        Returns:
            True if all card data is valid

        Raises:
            AgendaCardValidationError: If any part of the card data is invalid
        """
        # Check required fields
        required_fields = ["name", "agenda_type", "outcomes", "metadata"]
        for field_name in required_fields:
            if field_name not in card_data:
                raise AgendaCardValidationError(
                    f"Card data must contain '{field_name}'",
                    field_name=field_name,
                    invalid_value=None,
                )

        # Validate each field
        card_name = card_data["name"]
        self.validate_card_name(card_name)
        self.validate_agenda_type(card_data["agenda_type"])
        self.validate_voting_outcomes(card_data["outcomes"])
        self.validate_card_metadata(card_data["metadata"])

        return True

    def validate_multiple_cards(
        self, card_data_list: list[dict[str, Any]]
    ) -> list[ValidationResult]:
        """
        Validate multiple agenda cards in batch.

        Args:
            card_data_list: List of card data dictionaries to validate

        Returns:
            List of validation results for each card
        """
        results = []

        for i, card_data in enumerate(card_data_list):
            try:
                self.validate_complete_card_data(card_data)
                results.append(
                    ValidationResult(
                        is_valid=True, card_name=card_data.get("name", f"Card {i}")
                    )
                )
            except AgendaCardValidationError as e:
                results.append(
                    ValidationResult(
                        is_valid=False,
                        error_message=str(e),
                        card_name=card_data.get("name", f"Card {i}"),
                        field_name=e.field_name,
                    )
                )

        return results

    def add_custom_validation_rule(
        self, field_name: str, rule: Callable[[Any], bool]
    ) -> None:
        """
        Add a custom validation rule for a specific field.

        Args:
            field_name: The field to apply the rule to
            rule: A function that returns True if the value is valid
        """
        if field_name not in self._custom_rules:
            self._custom_rules[field_name] = []
        self._custom_rules[field_name].append(rule)


@dataclass
class ActionValidationResult:
    """Result of validating an action with law effects."""

    is_valid: bool
    applicable_laws: int = 0
    required_actions: list[str] = field(default_factory=list)
    validation_errors: list[str] = field(default_factory=list)


class AgendaEffectValidator:
    """Validates actions considering active law effects."""

    def __init__(self) -> None:
        """Initialize the agenda effect validator."""
        pass

    def validate_action_with_law_effects(
        self,
        action_type: str,
        player_id: str,
        game_state: Any,
        action_context: dict[str, Any],
    ) -> ActionValidationResult:
        """Validate an action considering active law effects.

        Args:
            action_type: The type of action being performed
            player_id: The player performing the action
            game_state: Current game state
            action_context: Context information for the action

        Returns:
            ActionValidationResult with validation details
        """
        result = ActionValidationResult(is_valid=True)

        # Get law effects for this action type
        law_effects = game_state.get_law_effects_for_action(action_type, player_id)
        result.applicable_laws = len(law_effects)

        # Validate based on action type
        if action_type == "technology_research":
            self._validate_technology_research_action(
                law_effects, action_context, result
            )
        elif action_type == "fleet_pool_management":
            self._validate_fleet_pool_action(law_effects, action_context, result)

        return result

    def _validate_technology_research_action(
        self,
        law_effects: list[Any],
        action_context: dict[str, Any],
        result: ActionValidationResult,
    ) -> None:
        """Validate technology research action with law effects."""
        for law_effect in law_effects:
            if law_effect.agenda_card.get_name() == "Anti-Intellectual Revolution":
                # Anti-Intellectual Revolution requires destroying a non-fighter ship
                available_ships = action_context.get("available_ships", [])

                # Handle both Unit objects and string representations
                non_fighter_ships = []
                for ship in available_ships:
                    if hasattr(ship, "unit_type"):
                        # Unit object
                        if ship.unit_type.value != "fighter":
                            non_fighter_ships.append(ship)
                    elif isinstance(ship, str):
                        # String representation
                        if ship != "fighter":
                            non_fighter_ships.append(ship)

                if non_fighter_ships:
                    result.required_actions.append("destroy_non_fighter_ship")
                else:
                    result.is_valid = False
                    result.validation_errors.append("no_non_fighter_ships_available")

    def _validate_fleet_pool_action(
        self,
        law_effects: list[Any],
        action_context: dict[str, Any],
        result: ActionValidationResult,
    ) -> None:
        """Validate fleet pool management action with law effects."""
        for law_effect in law_effects:
            if law_effect.agenda_card.get_name() == "Fleet Regulations":
                # Fleet Regulations limits fleet pool to 4 tokens
                current_tokens = action_context.get("current_fleet_tokens", 0)
                action = action_context.get("action", "")

                if action == "add_token" and current_tokens >= 4:
                    result.is_valid = False
                    result.validation_errors.append("fleet_pool_limit_exceeded")
