"""
Technology card registry system.

This module provides the registry for managing concrete technology card implementations.
"""

from typing import Optional

from ti4.core.constants import Technology

from .protocols import TechnologyCardProtocol


class TechnologyCardRegistry:
    """
    Registry for all concrete technology card implementations.

    This class manages the mapping between Technology enums and their
    concrete implementations, providing lookup and registration functionality.
    """

    def __init__(self) -> None:
        """Initialize the technology card registry."""
        self._cards: dict[Technology, TechnologyCardProtocol] = {}

    def register_card(self, card: TechnologyCardProtocol) -> None:
        """
        Register a technology card implementation.

        Args:
            card: The technology card implementation to register

        Raises:
            ValueError: If a card is already registered for this technology
        """
        if card.technology_enum in self._cards:
            raise ValueError(
                f"Technology card {card.technology_enum} is already registered"
            )
        self._cards[card.technology_enum] = card

    def get_card(self, technology: Technology) -> Optional[TechnologyCardProtocol]:
        """
        Get a technology card implementation.

        Args:
            technology: The technology to get the card for

        Returns:
            The technology card implementation, or None if not registered
        """
        return self._cards.get(technology)

    def get_all_cards(self) -> list[TechnologyCardProtocol]:
        """
        Get all registered technology cards.

        Returns:
            List of all registered technology card implementations
        """
        return list(self._cards.values())

    def is_registered(self, technology: Technology) -> bool:
        """
        Check if a technology card is registered.

        Args:
            technology: The technology to check

        Returns:
            True if the technology card is registered
        """
        return technology in self._cards

    def unregister_card(self, technology: Technology) -> bool:
        """
        Unregister a technology card.

        Args:
            technology: The technology to unregister

        Returns:
            True if the card was unregistered, False if it wasn't registered
        """
        if technology in self._cards:
            del self._cards[technology]
            return True
        return False

    def clear(self) -> None:
        """Clear all registered technology cards."""
        self._cards.clear()

    def get_card_with_confirmation(
        self, technology: Technology
    ) -> TechnologyCardProtocol:
        """
        Get a technology card implementation with manual confirmation enforcement.

        This method enforces the manual confirmation protocol by checking
        if the technology specification has been confirmed before returning the card.

        Args:
            technology: The technology to get the card for

        Returns:
            The technology card implementation

        Raises:
            TechnologySpecificationError: If technology is not confirmed
            ValueError: If technology card is not registered
        """
        from ti4.core.technology_cards.confirmation import require_confirmation

        require_confirmation(technology, "card")

        card = self.get_card(technology)
        if card is None:
            raise ValueError(f"Technology card {technology} is not registered")

        return card
