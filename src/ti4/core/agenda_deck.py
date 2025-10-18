"""Agenda deck system for TI4.

This module implements the agenda deck mechanics, including deck management
and card manipulation for the Politics strategy card.
"""


class AgendaDeck:
    """Manages the agenda deck and card manipulation."""

    def __init__(self) -> None:
        """Initialize the agenda deck."""
        self.cards: list[str] = []
        self.discard_pile: list[str] = []
        self._initialize_deck()

    def _initialize_deck(self) -> None:
        """Initialize the deck with sample agenda cards."""
        # Add some sample agenda cards for testing
        sample_cards = [
            "Anti-Intellectual Revolution",
            "Classified Document Leaks",
            "Committee Formation",
            "Conventions of War",
            "Core Mining",
            "Crown of Emphidia",
            "Crown of Thalnos",
            "Demilitarized Zone",
            "Enforced Travel Ban",
            "Executive Sanctions",
        ]
        self.cards = sample_cards.copy()

    def look_at_top_cards(self, count: int) -> list[str]:
        """Look at the top cards of the agenda deck.

        Args:
            count: Number of cards to look at

        Returns:
            List of agenda card names from the top of the deck
        """
        return self.cards[:count]

    def rearrange_top_cards(self, cards: list[str]) -> bool:
        """Rearrange the top cards of the agenda deck.

        Args:
            cards: List of card names in new order

        Returns:
            True if cards were successfully rearranged, False otherwise
        """
        if len(cards) > len(self.cards):
            return False

        # Verify all cards are actually at the top of the deck
        top_cards = self.cards[: len(cards)]
        if set(cards) != set(top_cards):
            return False

        # Rearrange the top cards
        remaining_cards = self.cards[len(cards) :]
        self.cards = cards + remaining_cards
        return True

    def draw_card(self) -> str | None:
        """Draw the top card from the agenda deck.

        Returns:
            The name of the drawn card, or None if deck is empty
        """
        if not self.cards and self.discard_pile:
            # Reshuffle discard pile into deck
            self.cards = self.discard_pile.copy()
            self.discard_pile.clear()

        if self.cards:
            return self.cards.pop(0)
        return None

    def discard_card(self, card_name: str) -> None:
        """Discard a card to the discard pile.

        Args:
            card_name: The name of the card to discard
        """
        self.discard_pile.append(card_name)

    def cards_remaining(self) -> int:
        """Get the number of cards remaining in the deck.

        Returns:
            Number of cards in deck
        """
        return len(self.cards)

    def peek_top_card(self) -> str | None:
        """Peek at the top card without drawing it.

        Returns:
            The name of the top card, or None if deck is empty
        """
        return self.cards[0] if self.cards else None
