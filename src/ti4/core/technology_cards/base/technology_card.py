"""
Base technology card implementation.

This module provides the abstract base class for all technology card implementations.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from ti4.core.abilities import Ability
from ti4.core.constants import Faction, Technology
from ti4.core.technology import TechnologyColor


class BaseTechnologyCard(ABC):
    """
    Abstract base class for all technology card implementations.

    This class provides common functionality and enforces the interface
    that all concrete technology cards must implement.
    """

    def __init__(self, technology_enum: Technology, name: str) -> None:
        """
        Initialize the base technology card.

        Args:
            technology_enum: The Technology enum value for this card
            name: Display name of the technology
        """
        self._technology_enum = technology_enum
        self._name = name

    @property
    def technology_enum(self) -> Technology:
        """The Technology enum value for this card."""
        return self._technology_enum

    @property
    def name(self) -> str:
        """Display name of the technology."""
        return self._name

    @property
    @abstractmethod
    def color(self) -> Optional[TechnologyColor]:
        """Technology color (None for unit upgrades)."""
        ...

    @property
    @abstractmethod
    def prerequisites(self) -> list[TechnologyColor]:
        """Required prerequisite colors."""
        ...

    @property
    @abstractmethod
    def faction_restriction(self) -> Optional[Faction]:
        """Faction restriction (None if available to all)."""
        ...

    @abstractmethod
    def get_abilities(self) -> list[Ability]:
        """Get all abilities provided by this technology."""
        ...

    def register_with_systems(
        self, ability_manager: Any, unit_stats_provider: Any
    ) -> None:
        """
        Register this technology with game systems.

        Default implementation registers abilities with the ability manager.
        Subclasses can override to provide additional registration logic.

        Args:
            ability_manager: The ability manager to register abilities with
            unit_stats_provider: The unit stats provider for unit modifications
        """
        # Register all abilities with the ability manager
        for ability in self.get_abilities():
            ability_manager.add_ability(ability)
