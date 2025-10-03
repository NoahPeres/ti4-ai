"""
Agenda card registry system.

This module provides the registry for managing concrete agenda card implementations.
"""

from typing import Optional

from .base import BaseAgendaCard


class AgendaCardRegistry:
    """
    Registry for all concrete agenda card implementations.

    This class manages the mapping between agenda card names and their
    concrete implementations, providing lookup and registration functionality.
    """

    def __init__(self) -> None:
        """Initialize the agenda card registry."""
        self._cards: dict[str, BaseAgendaCard] = {}

    def register_card(self, card: BaseAgendaCard) -> None:
        """
        Register an agenda card implementation.

        Args:
            card: The agenda card implementation to register

        Raises:
            ValueError: If card is None or already registered with this name
        """
        if card is None:
            raise ValueError("Cannot register None as an agenda card")
        if card.get_name() in self._cards:
            raise ValueError(f"Agenda card '{card.get_name()}' is already registered")
        self._cards[card.get_name()] = card

    def get_card(self, name: str) -> Optional[BaseAgendaCard]:
        """
        Get an agenda card implementation.

        Args:
            name: The name of the agenda card to get

        Returns:
            The agenda card implementation, or None if not registered
        """
        return self._cards.get(name)

    def get_all_cards(self) -> list[BaseAgendaCard]:
        """
        Get all registered agenda cards.

        Returns:
            List of all registered agenda card implementations
        """
        return list(self._cards.values())

    def get_all_card_names(self) -> list[str]:
        """
        Get names of all registered agenda cards.

        Returns:
            List of all registered agenda card names
        """
        return list(self._cards.keys())

    def is_registered(self, name: str) -> bool:
        """
        Check if an agenda card is registered.

        Args:
            name: The name of the agenda card to check

        Returns:
            True if the agenda card is registered
        """
        return name in self._cards

    def __contains__(self, name: str) -> bool:
        """
        Check if an agenda card is registered (supports 'in' operator).

        Args:
            name: The name of the agenda card to check

        Returns:
            True if the agenda card is registered
        """
        return name in self._cards

    def __len__(self) -> int:
        """
        Get the number of registered agenda cards.

        Returns:
            The number of registered agenda cards
        """
        return len(self._cards)

    def unregister_card(self, name: str) -> bool:
        """
        Unregister an agenda card.

        Args:
            name: The name of the agenda card to unregister

        Returns:
            True if the card was unregistered, False if it wasn't registered
        """
        if name in self._cards:
            del self._cards[name]
            return True
        return False

    def clear(self) -> None:
        """Clear all registered agenda cards."""
        self._cards.clear()
