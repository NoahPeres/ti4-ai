"""Planet structure for TI4 systems."""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .unit import Unit


class Planet:
    """Represents a planet within a system."""

    def __init__(self, name: str, resources: int, influence: int):
        self.name = name
        self.resources = resources
        self.influence = influence
        self.controlled_by: Optional[str] = None
        self.units: list[Unit] = []

    def set_control(self, player_id: str) -> None:
        """Set the controlling player of this planet."""
        self.controlled_by = player_id

    def place_unit(self, unit: "Unit") -> None:
        """Place a unit on this planet."""
        self.units.append(unit)

    def remove_unit(self, unit: "Unit") -> None:
        """Remove a unit from this planet."""
        self.units.remove(unit)
