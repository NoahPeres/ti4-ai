"""Planet structure for TI4 systems."""

from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .unit import Unit


@dataclass(frozen=True)
class Planet:
    """Represents a planet within a system."""

    name: str
    resources: int
    influence: int
    controlled_by: Optional[str] = None
    units: list["Unit"] = field(default_factory=list)
    is_exhausted: bool = False

    def set_control(self, player_id: str) -> "Planet":
        """Set the controlling player of this planet, returning a new instance."""
        return replace(self, controlled_by=player_id)

    def place_unit(self, unit: "Unit") -> "Planet":
        """Place a unit on this planet, returning a new instance."""
        new_units = self.units + [unit]
        return replace(self, units=new_units)

    def remove_unit(self, unit: "Unit") -> "Planet":
        """Remove a unit from this planet, returning a new instance."""
        new_units = [u for u in self.units if u != unit]
        return replace(self, units=new_units)

    def exhaust(self) -> "Planet":
        """Exhaust this planet, returning a new instance."""
        if self.is_exhausted:
            raise ValueError(f"Planet {self.name} is already exhausted")
        return replace(self, is_exhausted=True)

    def refresh(self) -> "Planet":
        """Refresh this planet, returning a new instance."""
        if not self.is_exhausted:
            raise ValueError(f"Planet {self.name} is already refreshed")
        return replace(self, is_exhausted=False)

    def can_collect_resources(self) -> bool:
        """Check if resources can be collected from this planet."""
        return not self.is_exhausted

    def can_collect_influence(self) -> bool:
        """Check if influence can be collected from this planet."""
        return not self.is_exhausted

    def get_resource_value(self) -> int:
        """Get the resource value of this planet."""
        return self.resources

    def get_influence_value(self) -> int:
        """Get the influence value of this planet."""
        return self.influence
