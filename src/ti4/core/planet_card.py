"""Planet card structure for TI4 game."""

from typing import Optional


class PlanetCard:
    """Represents a planet card in a player's play area."""

    def __init__(
        self, name: str, resources: int, influence: int, trait: Optional[str] = None
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
        return f"PlanetCard({self.name}, {self.resources}R/{self.influence}I, {status})"
