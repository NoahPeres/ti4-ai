"""
Manual confirmation protocol enforcement.

This module implements the manual confirmation protocol that ensures all
technology specifications are explicitly confirmed before implementation.
"""

from ti4.core.constants import Technology
from ti4.core.technology_cards.exceptions import TechnologySpecificationError


def require_confirmation(technology: Technology, attribute: str) -> None:
    """
    Enforce manual confirmation for technology attributes.

    This function implements the manual confirmation protocol by checking
    if a technology specification has been confirmed. If not, it raises
    a TechnologySpecificationError with a clear message guiding the
    developer to ask the user for confirmation.

    Args:
        technology: The Technology enum to check
        attribute: The attribute name being accessed (for error messages)

    Raises:
        TechnologySpecificationError: If technology is not confirmed
        TypeError: If technology is not a Technology enum

    Example:
        >>> require_confirmation(Technology.FIGHTER_II, "color")
        TechnologySpecificationError: Technology Fighter II color not confirmed.
        Please ask user for specification.
    """
    if not isinstance(technology, Technology):
        raise TypeError(f"Expected Technology enum, got {type(technology)}")

    # Get the list of confirmed technologies from the registry
    confirmed_technologies = _get_confirmed_technologies()

    if technology not in confirmed_technologies:
        raise TechnologySpecificationError(
            f"Technology {technology.name} {attribute} not confirmed. "
            f"Please ask user for specification."
        )


def _get_confirmed_technologies() -> set[Technology]:
    """
    Get the set of confirmed technologies from the specification registry.

    Returns:
        Set of Technology enums that have confirmed specifications
    """
    from ti4.core.technology_cards.specifications import TechnologySpecificationRegistry

    registry = TechnologySpecificationRegistry()
    return {spec.technology for spec in registry.get_all_specifications()}
