"""
Planet-attachable agenda card base implementation.

This module provides the base class for agenda cards that can attach to planets.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .directive_card import DirectiveCard

if TYPE_CHECKING:
    from ti4.core.agenda_cards.planet_attachment import PlanetAttachmentManager
    from ti4.core.planet import Planet


class PlanetAttachableCard(DirectiveCard, ABC):
    """
    Base class for agenda cards that can attach to planets.

    This class provides functionality for agenda cards that attach to planets
    and provide ongoing effects, such as Core Mining, Demilitarized Zone, etc.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize the planet-attachable card.

        Args:
            name: Display name of the agenda card
        """
        super().__init__(name)

    def can_attach_to_planet(self) -> bool:
        """Check if this card can attach to planets."""
        return True

    def attach_to_planet(
        self, planet: "Planet", attachment_manager: "PlanetAttachmentManager"
    ) -> None:
        """
        Attach this agenda card to a planet.

        Args:
            planet: Planet to attach the card to
            attachment_manager: Manager to handle the attachment

        Raises:
            ValueError: If planet or attachment_manager is None
        """
        if planet is None:
            raise ValueError("Planet cannot be None")

        if attachment_manager is None:
            raise ValueError("Attachment manager cannot be None")

        # Get the effect description for this card
        effect_description = self.get_attachment_effect_description()

        # Attach the card to the planet
        attachment_manager.attach_card_to_planet(
            agenda_card_name=self.get_name(),
            planet=planet,
            effect_description=effect_description,
        )

    @abstractmethod
    def get_attachment_effect_description(self) -> str:
        """
        Get the description of the effect when this card is attached to a planet.

        Returns:
            Description of the attachment effect
        """
        ...
