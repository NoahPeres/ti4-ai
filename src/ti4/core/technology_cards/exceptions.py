"""
Technology card framework exceptions.

This module defines custom exceptions for the technology card framework,
particularly for enforcing the manual confirmation protocol.
"""


class TechnologySpecificationError(Exception):
    """
    Exception raised when technology specifications are not confirmed.

    This exception enforces the manual confirmation protocol by preventing
    access to unconfirmed technology specifications.

    The manual confirmation protocol requires that all technology specifications
    be explicitly confirmed by the user before implementation to ensure accuracy
    and prevent assumptions about game rules.
    """

    def __init__(self, message: str) -> None:
        """
        Initialize the exception with a descriptive message.

        Args:
            message: Descriptive error message explaining what needs confirmation
        """
        super().__init__(message)
