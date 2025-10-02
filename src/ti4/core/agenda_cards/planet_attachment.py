"""
Planet attachment system for agenda cards.

This module provides functionality for agenda cards that can attach to planets,
such as Core Mining, Demilitarized Zone, Senate Sanctuary, and Terraforming Initiative.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ti4.core.planet import Planet


@dataclass
class PlanetAttachment:
    """
    Represents an agenda card attached to a planet.

    This data structure tracks agenda cards that have been attached to specific
    planets and their associated effects.
    """

    agenda_card_name: str
    planet_name: str
    attached_round: int
    effect_description: str


class PlanetAttachmentManager:
    """
    Manages agenda card attachments to planets.

    This class handles attaching agenda cards to planets, tracking their effects,
    and managing the lifecycle of planet attachments.
    """

    def __init__(self) -> None:
        """Initialize the planet attachment manager."""
        self._attachments: list[PlanetAttachment] = []

    def attach_card_to_planet(
        self, agenda_card_name: str, planet: Planet, effect_description: str
    ) -> None:
        """
        Attach an agenda card to a planet.

        Args:
            agenda_card_name: Name of the agenda card to attach
            planet: Planet to attach the card to
            effect_description: Description of the card's effect

        Raises:
            ValueError: If any parameter is invalid
        """
        # Validation
        if not agenda_card_name or not agenda_card_name.strip():
            raise ValueError("Agenda card name cannot be empty")

        if planet is None:
            raise ValueError("Planet cannot be None")

        if not effect_description or not effect_description.strip():
            raise ValueError("Effect description cannot be empty")

        # Create attachment
        attachment = PlanetAttachment(
            agenda_card_name=agenda_card_name.strip(),
            planet_name=planet.name,
            attached_round=1,  # TODO: Get actual round from game state
            effect_description=effect_description.strip(),
        )

        self._attachments.append(attachment)

    def get_attachments_for_planet(self, planet_name: str) -> list[PlanetAttachment]:
        """
        Get all agenda card attachments for a specific planet.

        Args:
            planet_name: Name of the planet to get attachments for

        Returns:
            List of attachments for the specified planet
        """
        return [
            attachment
            for attachment in self._attachments
            if attachment.planet_name == planet_name
        ]

    def remove_attachment_from_planet(
        self, agenda_card_name: str, planet_name: str
    ) -> bool:
        """
        Remove an agenda card attachment from a planet.

        Args:
            agenda_card_name: Name of the agenda card to remove
            planet_name: Name of the planet to remove the attachment from

        Returns:
            True if attachment was removed, False if not found
        """
        for i, attachment in enumerate(self._attachments):
            if (
                attachment.agenda_card_name == agenda_card_name
                and attachment.planet_name == planet_name
            ):
                self._attachments.pop(i)
                return True
        return False

    def get_state_data(self) -> dict[str, Any]:
        """
        Get state data for persistence.

        Returns:
            Dictionary containing attachment state data
        """
        return {
            "attachments": [
                {
                    "agenda_card_name": attachment.agenda_card_name,
                    "planet_name": attachment.planet_name,
                    "attached_round": attachment.attached_round,
                    "effect_description": attachment.effect_description,
                }
                for attachment in self._attachments
            ]
        }

    def restore_state_data(self, state_data: dict[str, Any]) -> None:
        """
        Restore state data from persistence.

        Args:
            state_data: Dictionary containing attachment state data
        """
        self._attachments = []

        if "attachments" in state_data:
            for attachment_data in state_data["attachments"]:
                attachment = PlanetAttachment(
                    agenda_card_name=attachment_data["agenda_card_name"],
                    planet_name=attachment_data["planet_name"],
                    attached_round=attachment_data["attached_round"],
                    effect_description=attachment_data["effect_description"],
                )
                self._attachments.append(attachment)
