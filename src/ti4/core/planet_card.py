"""Planet card structure for TI4 game."""

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from .game_state import GameState


class PlanetCard:
    """Represents a planet card in a player's play area."""

    def __init__(
        self,
        name: str,
        resources: int,
        influence: int,
        trait: Optional[str] = None,
        game_state: Optional["GameState"] = None,
    ) -> None:
        if not name or not isinstance(name, str):
            raise ValueError("Planet name must be a non-empty string")
        if not isinstance(resources, int) or resources < 0:
            raise ValueError("Resources must be a non-negative integer")
        if not isinstance(influence, int) or influence < 0:
            raise ValueError("Influence must be a non-negative integer")

        self.name = name
        self.resources = resources
        self.influence = influence
        self.trait = trait
        self._exhausted = False
        self._attached_cards: list[Any] = []  # Cards attached to this planet card
        self._game_state = game_state  # Reference to game state for token management

    def is_exhausted(self) -> bool:
        """Check if this planet card is exhausted."""
        return self._exhausted

    def is_readied(self) -> bool:
        """Check if this planet card is readied (faceup)."""
        return not self._exhausted

    def exhaust(self) -> None:
        """Exhaust this planet card (flip facedown)."""
        if self._exhausted:
            raise ValueError("Planet card is already exhausted")
        self._exhausted = True

    def ready(self) -> None:
        """Ready this planet card (flip faceup)."""
        self._exhausted = False

    def can_spend_resources(self) -> bool:
        """Check if this planet card can spend resources."""
        return not self._exhausted

    def can_spend_influence(self) -> bool:
        """Check if this planet card can spend influence."""
        return not self._exhausted

    def spend_resources(self, amount: int) -> int:
        """Spend resources from this planet card, exhausting it."""
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Spend amount must be a positive integer")
        if self._exhausted:
            raise ValueError("Cannot spend from exhausted planet card")
        if amount > self.resources:
            raise ValueError(
                f"Cannot spend {amount} resources, planet card only has {self.resources}"
            )

        self.exhaust()
        return amount

    def spend_influence(self, amount: int) -> int:
        """Spend influence from this planet card, exhausting it."""
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Spend amount must be a positive integer")
        if self._exhausted:
            raise ValueError("Cannot spend from exhausted planet card")
        if amount > self.influence:
            raise ValueError(
                f"Cannot spend {amount} influence, planet card only has {self.influence}"
            )

        self.exhaust()
        return amount

    def __eq__(self, other: object) -> bool:
        """Check equality based on planet name."""
        if not isinstance(other, PlanetCard):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        """Hash based on planet name."""
        return hash(self.name)

    def __repr__(self) -> str:
        """String representation of planet card."""
        status = "exhausted" if self._exhausted else "readied"
        attachments = (
            f", {len(self._attached_cards)} attachments" if self._attached_cards else ""
        )
        return f"PlanetCard({self.name}, {self.resources}R/{self.influence}I, {status}{attachments})"

    # Rule 12: ATTACH - Attachment System
    def attach_card(self, card: Any) -> None:
        """Attach a card to this planet card (Rule 12.1)."""
        if card is None:
            raise ValueError("Cannot attach None card")
        if card in self._attached_cards:
            raise ValueError(f"Card {card} is already attached to this planet")

        self._attached_cards.append(card)

        # Add attachment token to game board (Rule 12.3)
        if self._game_state is not None and hasattr(card, "token_id"):
            if self.name not in self._game_state.planet_attachment_tokens:
                self._game_state.planet_attachment_tokens[self.name] = set()
            self._game_state.planet_attachment_tokens[self.name].add(card.token_id)

    def detach_card(self, card: Any) -> None:
        """Detach a card from this planet card."""
        if card not in self._attached_cards:
            raise ValueError(f"Card {card} is not attached to this planet")

        self._attached_cards.remove(card)

        # Remove attachment token from game board (Rule 12.3)
        if self._game_state is not None and hasattr(card, "token_id"):
            if self.name in self._game_state.planet_attachment_tokens:
                self._game_state.planet_attachment_tokens[self.name].discard(
                    card.token_id
                )
                # Clean up empty sets
                if not self._game_state.planet_attachment_tokens[self.name]:
                    del self._game_state.planet_attachment_tokens[self.name]

    def get_attached_cards(self) -> list[Any]:
        """Get all cards attached to this planet card."""
        return self._attached_cards.copy()

    def has_attached_cards(self) -> bool:
        """Check if this planet card has any attached cards."""
        return len(self._attached_cards) > 0

    def purge_attachments(self) -> list[Any]:
        """Remove and return all attached cards (for card purge/removal scenarios)."""
        purged_cards = self._attached_cards.copy()

        # Remove all attachment tokens from game board (Rule 12.3)
        if (
            self._game_state is not None
            and self.name in self._game_state.planet_attachment_tokens
        ):
            del self._game_state.planet_attachment_tokens[self.name]

        self._attached_cards.clear()
        return purged_cards

    def clone_for_state(self, new_game_state: "GameState") -> "PlanetCard":
        """Create a clone of this PlanetCard bound to a new GameState."""
        cloned_card = PlanetCard(
            name=self.name,
            resources=self.resources,
            influence=self.influence,
            trait=self.trait,
            game_state=new_game_state,
        )
        cloned_card._exhausted = self._exhausted
        cloned_card._attached_cards = self._attached_cards.copy()
        return cloned_card
