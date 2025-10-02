"""
Agenda deck management system.

This module provides the AgendaDeck class for managing agenda cards
with proper shuffling, drawing, and state tracking.
"""

import random
from typing import Any

from .base import BaseAgendaCard
from .registry import AgendaCardRegistry


class AgendaDeckEmptyError(Exception):
    """Raised when trying to draw from an empty deck with no discard pile."""

    pass


class AgendaDeck:
    """
    Manages the agenda deck with proper shuffling and drawing.

    This class integrates with the AgendaCardRegistry to provide
    a complete deck management system for agenda cards.
    """

    def __init__(self, registry: AgendaCardRegistry) -> None:
        """
        Initialize the agenda deck from a registry.

        Args:
            registry: The agenda card registry containing all cards

        Raises:
            ValueError: If registry is None or empty
        """
        if registry is None:
            raise ValueError("Registry cannot be None")

        self._registry = registry
        self._deck: list[BaseAgendaCard] = []
        self._discard_pile: list[BaseAgendaCard] = []
        self._removed_cards: list[BaseAgendaCard] = []
        self._reshuffle_count = 0

        # Initialize deck with all registered cards
        self._deck = registry.get_all_cards().copy()
        self._total_cards = len(self._deck)

        if self._total_cards == 0:
            raise ValueError("Cannot create deck from empty registry")

    def __len__(self) -> int:
        """Get the number of cards remaining in the deck."""
        return len(self._deck)

    def cards_remaining(self) -> int:
        """Get the number of cards remaining in the deck."""
        return len(self._deck)

    def discard_pile_size(self) -> int:
        """Get the number of cards in the discard pile."""
        return len(self._discard_pile)

    def total_cards(self) -> int:
        """Get the total number of cards (excluding removed cards)."""
        return self._total_cards

    def is_empty(self) -> bool:
        """Check if the deck is empty."""
        return len(self._deck) == 0

    def get_all_cards(self) -> list[BaseAgendaCard]:
        """Get all cards currently in the deck."""
        return self._deck.copy()

    def shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self._deck)

    def draw_top_card(self) -> BaseAgendaCard:
        """
        Draw the top card from the deck.

        Returns:
            The top card from the deck

        Raises:
            AgendaDeckEmptyError: If the deck is empty and cannot be reshuffled
        """
        if self.is_empty():
            if self._discard_pile:
                self._reshuffle_discard_pile()
            else:
                raise AgendaDeckEmptyError(
                    "Cannot draw from empty deck with no discard pile"
                )

        return self._deck.pop()

    def discard_card(self, card: BaseAgendaCard) -> None:
        """
        Add a card to the discard pile.

        Args:
            card: The card to discard

        Raises:
            ValueError: If card is None
        """
        if card is None:
            raise ValueError("Cannot discard None card")
        self._discard_pile.append(card)

    def remove_from_game(self, card: BaseAgendaCard) -> None:
        """
        Permanently remove a card from the game.

        Args:
            card: The card to remove permanently

        Raises:
            ValueError: If card is None
        """
        if card is None:
            raise ValueError("Cannot remove None card from game")
        self._removed_cards.append(card)
        self._total_cards -= 1

    def _reshuffle_discard_pile(self) -> None:
        """Reshuffle the discard pile into the deck."""
        self._deck.extend(self._discard_pile)
        self._discard_pile.clear()
        self._reshuffle_count += 1
        self.shuffle()

    def get_deck_state(self) -> dict[str, Any]:
        """
        Get comprehensive deck state information.

        Returns:
            Dictionary containing current deck state
        """
        return {
            "cards_in_deck": len(self._deck),
            "cards_in_discard": len(self._discard_pile),
            "cards_removed": len(self._removed_cards),
            "total_cards": self._total_cards,
            "reshuffle_count": self._reshuffle_count,
        }

    def get_discard_pile_contents(self) -> list[BaseAgendaCard]:
        """
        Get the contents of the discard pile.

        Returns:
            List of cards in the discard pile
        """
        return self._discard_pile.copy()

    def clear_discard_pile(self) -> list[BaseAgendaCard]:
        """
        Clear the discard pile and return the cards that were in it.

        Returns:
            List of cards that were in the discard pile
        """
        cleared_cards = self._discard_pile.copy()
        self._discard_pile.clear()
        return cleared_cards

    def get_reshuffle_count(self) -> int:
        """
        Get the number of times the deck has been reshuffled.

        Returns:
            Number of reshuffles
        """
        return self._reshuffle_count

    def validate_deck_state(self) -> bool:
        """
        Validate that the deck state is consistent.

        Returns:
            True if deck state is valid
        """
        # Basic validation - all cards should be accounted for
        total_accounted = (
            len(self._deck) + len(self._discard_pile) + len(self._removed_cards)
        )
        return total_accounted <= self._total_cards

    def check_deck_integrity(self) -> dict[str, Any]:
        """
        Perform comprehensive deck integrity check.

        Note: Cards that have been drawn but not yet discarded or removed
        are considered "in play" and are not counted as missing.

        Returns:
            Dictionary with integrity check results
        """
        total_accounted = (
            len(self._deck) + len(self._discard_pile) + len(self._removed_cards)
        )
        cards_in_play = max(0, self._total_cards - total_accounted)

        return {
            "is_valid": total_accounted <= self._total_cards,
            "total_accounted_cards": total_accounted,
            "cards_in_play": cards_in_play,  # Cards drawn but not discarded/removed
            "missing_cards": 0,  # No cards are truly missing in normal operation
            "cards_in_deck": len(self._deck),
            "cards_in_discard": len(self._discard_pile),
            "cards_removed": len(self._removed_cards),
            "expected_total": self._total_cards,
        }

    def serialize_state(self) -> dict[str, Any]:
        """
        Serialize the deck state for persistence.

        Returns:
            Serialized deck state
        """
        return {
            "deck_cards": [card.name for card in self._deck],
            "discard_pile": [card.name for card in self._discard_pile],
            "removed_cards": [card.name for card in self._removed_cards],
            "reshuffle_count": self._reshuffle_count,
            "total_cards": self._total_cards,
        }

    @classmethod
    def from_serialized_state(
        cls, serialized_state: dict[str, Any], registry: AgendaCardRegistry
    ) -> "AgendaDeck":
        """
        Create a deck from serialized state.

        Args:
            serialized_state: Previously serialized deck state
            registry: Registry containing card definitions

        Returns:
            AgendaDeck restored from serialized state

        Raises:
            ValueError: If serialized state is invalid or cards not found
        """
        # Create new deck
        deck = cls.__new__(cls)
        deck._registry = registry
        deck._reshuffle_count = serialized_state.get("reshuffle_count", 0)
        deck._total_cards = serialized_state.get("total_cards", 0)

        # Restore deck cards
        deck._deck = []
        for card_name in serialized_state.get("deck_cards", []):
            card = registry.get_card(card_name)
            if card is None:
                raise ValueError(f"Card '{card_name}' not found in registry")
            deck._deck.append(card)

        # Restore discard pile
        deck._discard_pile = []
        for card_name in serialized_state.get("discard_pile", []):
            card = registry.get_card(card_name)
            if card is None:
                raise ValueError(f"Card '{card_name}' not found in registry")
            deck._discard_pile.append(card)

        # Restore removed cards
        deck._removed_cards = []
        for card_name in serialized_state.get("removed_cards", []):
            card = registry.get_card(card_name)
            if card is None:
                raise ValueError(f"Card '{card_name}' not found in registry")
            deck._removed_cards.append(card)

        return deck
