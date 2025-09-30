"""
Passive technology card base implementation.

This module provides the base class for technology cards with passive abilities.
"""

from typing import TYPE_CHECKING

from .technology_card import BaseTechnologyCard

if TYPE_CHECKING:
    from ti4.core.constants import Technology


class PassiveTechnologyCard(BaseTechnologyCard):
    """
    Base implementation for passive technology cards.

    This class provides a foundation for technology cards that have
    continuous effects that don't require exhaustion or activation.
    """

    def __init__(self, technology_enum: "Technology", name: str) -> None:
        """
        Initialize the passive technology card.

        Args:
            technology_enum: The Technology enum value for this card
            name: Display name of the technology
        """
        super().__init__(technology_enum, name)
