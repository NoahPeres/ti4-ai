"""
Exceptions for agenda card validation and operations.

This module provides custom exceptions for agenda card validation errors
and other agenda card-related operations.
"""

from typing import Any, Optional


class AgendaCardValidationError(Exception):
    """
    Exception raised when agenda card validation fails.

    This exception provides detailed information about validation failures
    including context information and recovery suggestions.
    """

    def __init__(
        self,
        message: str,
        card_name: Optional[str] = None,
        field_name: Optional[str] = None,
        invalid_value: Any = None,
    ) -> None:
        """
        Initialize the validation error.

        Args:
            message: The error message
            card_name: Name of the card that failed validation (optional)
            field_name: Name of the field that failed validation (optional)
            invalid_value: The invalid value that caused the error (optional)
        """
        super().__init__(message)
        self.card_name = card_name
        self.field_name = field_name
        self.invalid_value = invalid_value

    def get_recovery_suggestions(self) -> list[str]:
        """
        Get recovery suggestions for this validation error.

        Returns:
            List of suggested actions to fix the validation error
        """
        suggestions = []

        if self.field_name == "name":
            suggestions.extend(
                [
                    "Provide a non-empty card name",
                    "Ensure the card name contains only valid characters",
                    "Check that the card name is not just whitespace",
                ]
            )
        elif self.field_name == "outcomes":
            suggestions.extend(
                [
                    "Provide at least one voting outcome",
                    "Ensure all outcomes are non-empty strings",
                    "Use standard voting outcomes like 'For', 'Against', or 'Elect Player'",
                ]
            )
        elif self.field_name == "agenda_type":
            suggestions.extend(
                [
                    "Use AgendaType.LAW or AgendaType.DIRECTIVE",
                    "Ensure the agenda type is not None",
                ]
            )
        elif self.field_name == "metadata":
            suggestions.extend(
                [
                    "Provide metadata as a dictionary",
                    "Include required fields like 'expansion'",
                    "Ensure metadata values are valid",
                ]
            )
        else:
            suggestions.append("Check the validation requirements for this field")

        return suggestions

    def __str__(self) -> str:
        """Get string representation of the error."""
        base_message = super().__str__()

        if self.card_name:
            base_message = f"Card '{self.card_name}': {base_message}"

        if self.field_name:
            base_message = f"{base_message} (field: {self.field_name})"

        return base_message


class AgendaCardOperationError(Exception):
    """
    Exception raised when agenda card operations fail.

    This exception is used for runtime errors during agenda card operations
    such as deck management, effect resolution, etc.
    """

    def __init__(self, message: str, operation: Optional[str] = None) -> None:
        """
        Initialize the operation error.

        Args:
            message: The error message
            operation: The operation that failed (optional)
        """
        super().__init__(message)
        self.operation = operation

    def __str__(self) -> str:
        """Get string representation of the error."""
        base_message = super().__str__()

        if self.operation:
            base_message = f"Operation '{self.operation}': {base_message}"

        return base_message


class AgendaCardNotFoundError(AgendaCardOperationError):
    """
    Exception raised when a requested agenda card is not found.
    """

    def __init__(self, card_name: str) -> None:
        """
        Initialize the not found error.

        Args:
            card_name: Name of the card that was not found
        """
        super().__init__(f"Agenda card '{card_name}' not found", "card_lookup")
        self.card_name = card_name


class AgendaCardRegistrationError(AgendaCardOperationError):
    """
    Exception raised when agenda card registration fails.
    """

    def __init__(self, message: str, card_name: Optional[str] = None) -> None:
        """
        Initialize the registration error.

        Args:
            message: The error message
            card_name: Name of the card that failed registration (optional)
        """
        super().__init__(message, "card_registration")
        self.card_name = card_name
