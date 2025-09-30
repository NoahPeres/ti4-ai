"""
Exhaustible technology card base implementation.

This module provides the base class for technology cards that can be exhausted.
"""

from typing import TYPE_CHECKING, Optional

from ti4.core.abilities import Ability

from .technology_card import BaseTechnologyCard

if TYPE_CHECKING:
    from ti4.core.constants import Technology


class ExhaustibleTechnologyCard(BaseTechnologyCard):
    """
    Base implementation for exhaustible technology cards.

    This class provides the exhaustion mechanics for technology cards
    that can be exhausted to activate abilities. This includes:
    - ACTION abilities (like traditional exhaustible cards)
    - Triggered abilities that exhaust the card (like AI Development Algorithm)
    - Any other ability that requires exhausting the technology
    """

    def __init__(self, technology_enum: "Technology", name: str) -> None:
        """
        Initialize the exhaustible technology card.

        Args:
            technology_enum: The Technology enum value for this card
            name: Display name of the technology
        """
        super().__init__(technology_enum, name)
        self._exhausted = False

    def is_exhausted(self) -> bool:
        """Check if this technology is exhausted."""
        return self._exhausted

    def exhaust(self) -> None:
        """Exhaust this technology."""
        if self._exhausted:
            raise ValueError(f"Technology {self.name} is already exhausted")
        self._exhausted = True

    def ready(self) -> None:
        """Ready this technology."""
        self._exhausted = False

    def get_exhaustible_abilities(self) -> list[Ability]:
        """
        Get all abilities that can exhaust this card.

        This includes ACTION abilities, triggered abilities, and any other
        abilities that require exhausting the technology card to activate.

        Default implementation returns empty list. Subclasses should override
        to provide their specific exhaustible abilities.

        Returns:
            List of abilities that can exhaust this card
        """
        return []

    def get_action_ability(self) -> Optional[Ability]:
        """
        Get the ACTION ability that exhausts this card (if any).

        This is a convenience method for cards that have ACTION abilities.
        For cards with other types of exhaustible abilities, use
        get_exhaustible_abilities() instead.

        Returns:
            The ACTION ability, or None if no ACTION ability exists
        """
        from ti4.core.abilities import TimingWindow

        exhaustible_abilities = self.get_exhaustible_abilities()
        for ability in exhaustible_abilities:
            if hasattr(ability, "timing") and ability.timing == TimingWindow.ACTION:
                return ability
        return None
