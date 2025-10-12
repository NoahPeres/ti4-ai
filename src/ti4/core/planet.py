"""Planet structure for TI4 systems."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .custodians_token import CustodiansToken
    from .exploration import ExplorationCard
    from .unit import Unit


class Planet:
    """Represents a planet within a system."""

    def __init__(self, name: str, resources: int, influence: int) -> None:
        self.name = name
        self._resources = resources
        self._influence = influence
        self.controlled_by: str | None = None
        self.units: list[Unit] = []
        self._exhausted = False  # Rule 34: Track exhausted state
        self.traits: list[str] = []  # Rule 35: Planet traits for exploration
        self.attached_cards: list[
            ExplorationCard
        ] = []  # Rule 35: Cards attached to this planet
        self._custodians_token: CustodiansToken | None = (
            None  # Rule 27: Custodians token
        )

    def set_control(self, player_id: str) -> None:
        """Set the controlling player of this planet."""
        self.controlled_by = player_id

    def place_unit(self, unit: Unit) -> None:
        """Place a unit on this planet."""
        self.units.append(unit)

    def remove_unit(self, unit: Unit) -> None:
        """Remove a unit from this planet."""
        self.units.remove(unit)

    # Rule 34: Exhausted state mechanics
    def is_exhausted(self) -> bool:
        """Check if this planet is exhausted."""
        return self._exhausted

    def is_faceup(self) -> bool:
        """Check if this planet is faceup (readied)."""
        return not self._exhausted

    def exhaust(self) -> None:
        """Exhaust this planet (flip facedown)."""
        if self._exhausted:
            raise ValueError("Card is already exhausted")
        self._exhausted = True

    def ready(self) -> None:
        """Ready this planet (flip faceup)."""
        self._exhausted = False

    def can_spend_resources(self) -> bool:
        """Check if this planet can spend resources.

        Note: Control validation is handled by GameState elsewhere.
        """
        return not self._exhausted

    def can_spend_influence(self) -> bool:
        """Check if this planet can spend influence.

        Note: Control validation is handled by GameState elsewhere.
        """
        return not self._exhausted

    @property
    def resources(self) -> int:
        """Get the resource value of this planet."""
        return self._resources

    @property
    def influence(self) -> int:
        """Get the influence value of this planet."""
        return self._influence

    def get_resources(self) -> int:
        """Get the resource value of this planet."""
        return self._resources

    def get_influence(self) -> int:
        """Get the influence value of this planet."""
        return self._influence

    def spend_resources(self, amount: int) -> int:
        """Spend resources from this planet, exhausting it."""
        if self._exhausted:
            raise ValueError("Cannot spend from exhausted planet")
        if amount > self._resources:
            raise ValueError(
                f"Cannot spend {amount} resources, planet only has {self._resources}"
            )

        self.exhaust()
        return amount

    def spend_influence(self, amount: int) -> int:
        """Spend influence from this planet, exhausting it."""
        if self._exhausted:
            raise ValueError("Cannot spend from exhausted planet")
        if amount > self._influence:
            raise ValueError(
                f"Cannot spend {amount} influence, planet only has {self._influence}"
            )

        self.exhaust()
        return amount

    # Rule 88.5: Support for ground forces and structures
    def can_hold_ground_forces(self) -> bool:
        """Check if ground forces can be placed on this planet (Rule 88.5)."""
        return True  # All planets can hold ground forces

    def can_hold_structures(self) -> bool:
        """Check if structures can be placed on this planet (Rule 88.5)."""
        return True  # All planets can hold structures

    def get_units(self) -> list[Unit]:
        """Get all units on this planet."""
        return self.units.copy()

    # Rule 27: Custodians token support
    def set_custodians_token(self, token: CustodiansToken) -> None:
        """Set the custodians token on this planet (for Mecatol Rex)."""
        self._custodians_token = token
        # Ensure token state is synchronized - token should be on Mecatol Rex
        if not token.is_on_mecatol_rex():
            # This shouldn't happen in normal gameplay, but ensure consistency
            token._on_mecatol_rex = True

    def remove_custodians_token(self) -> None:
        """Remove the custodians token from this planet."""
        if self._custodians_token is not None:
            # Synchronize token state when removing from planet
            self._custodians_token.remove_from_mecatol_rex()
        self._custodians_token = None

    def has_custodians_token(self) -> bool:
        """Check if this planet has the custodians token."""
        return (
            self._custodians_token is not None
            and self._custodians_token.is_on_mecatol_rex()
        )

    def can_land_ground_forces(self, player_id: str) -> bool:
        """
        Check if ground forces can land on this planet.

        LRR 27.1: Players cannot land ground forces on Mecatol Rex while
        the custodians token is on that planet.
        """
        # Check if custodians token prevents landing
        if self.has_custodians_token():
            return False

        # Otherwise, ground forces can land (subject to other game rules)
        return True
