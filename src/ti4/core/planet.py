"""Planet structure for TI4 systems."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
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
        """Check if this planet can spend resources."""
        return not self._exhausted

    def can_spend_influence(self) -> bool:
        """Check if this planet can spend influence."""
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
