"""Unit structure for TI4 game pieces."""

import uuid
from typing import Any, Optional

from .constants import Faction, Technology, UnitType
from .unit_stats import UnitStats, UnitStatsProvider


class Unit:
    """Represents a game unit with type and owner."""

    # Instance variable type annotations
    id: str
    unit_type: UnitType
    owner: str
    faction: Optional[Faction]
    technologies: set[Technology]
    _stats_provider: UnitStatsProvider
    _cached_stats: Optional[UnitStats]
    _sustained_damage: bool

    def __init__(
        self,
        unit_type: UnitType,
        owner: str,
        faction: Optional[Faction] = None,
        technologies: Optional[set[Technology]] = None,
        stats_provider: Optional[UnitStatsProvider] = None,
        unit_id: Optional[str] = None,
    ) -> None:
        self.id = unit_id or str(uuid.uuid4())

        # Store enums directly for type safety
        # Handle both enum and string inputs for backward compatibility
        if isinstance(unit_type, str):
            self.unit_type = UnitType(unit_type)
        else:
            self.unit_type = unit_type
        self.owner = owner
        if isinstance(faction, str):
            self.faction = Faction(faction)
        else:
            self.faction = faction

        # Store technology enums directly
        if technologies:
            self.technologies = set(technologies)
        else:
            self.technologies = set()

        self._stats_provider = stats_provider or UnitStatsProvider()
        self._cached_stats: Optional[UnitStats] = None
        self._sustained_damage = False

    def get_stats(self) -> UnitStats:
        """Get the current statistics for this unit."""
        if self._cached_stats is None:
            # Convert string values back to enums for the stats provider
            unit_type_enum = self.unit_type
            faction_enum = self.faction
            tech_enums = self.technologies if self.technologies else None

            self._cached_stats = self._stats_provider.get_unit_stats(
                unit_type_enum, faction_enum, tech_enums
            )
        return self._cached_stats

    def get_capacity(self) -> int:
        """Get the capacity of this unit."""
        return self.get_stats().capacity

    def get_combat_value(self) -> Optional[int]:
        """Get the combat value for this unit."""
        return self.get_stats().combat_value

    def get_combat(self) -> Optional[int]:
        """Get the combat value for this unit (alias for get_combat_value)."""
        return self.get_combat_value()

    def get_movement(self) -> int:
        """Get the movement value of this unit."""
        return self.get_stats().movement

    def get_cost(self) -> float:
        """Get the cost of this unit."""
        return self.get_stats().cost

    def has_sustain_damage(self) -> bool:
        """Check if this unit has sustain damage ability."""
        return self.get_stats().sustain_damage

    def has_anti_fighter_barrage(self) -> bool:
        """Check if this unit has anti-fighter barrage ability."""
        return self.get_stats().anti_fighter_barrage

    def has_space_cannon(self) -> bool:
        """Check if this unit has space cannon ability."""
        return self.get_stats().space_cannon

    def has_bombardment(self) -> bool:
        """Check if this unit has bombardment ability."""
        return self.get_stats().bombardment

    def has_deploy(self) -> bool:
        """Check if this unit has deploy ability."""
        return self.get_stats().deploy

    def has_planetary_shield(self) -> bool:
        """Check if this unit has planetary shield ability."""
        return self.get_stats().planetary_shield

    def has_production(self) -> bool:
        """Check if this unit has production ability."""
        return self.get_stats().has_production

    def get_production(self) -> int:
        """Get the production value of this unit."""
        return self.get_stats().production

    def get_combat_dice(self) -> int:
        """Get the number of combat dice this unit rolls."""
        return self.get_stats().combat_dice

    def invalidate_stats_cache(self) -> None:
        """Invalidate the cached stats (call when technologies change)."""
        self._cached_stats = None

    @property
    def has_sustained_damage(self) -> bool:
        """Check if this unit has sustained damage."""
        return self._sustained_damage

    def sustain_damage(self) -> None:
        """Mark this unit as having sustained damage."""
        if not self.has_sustain_damage():
            raise ValueError(f"Unit {self.unit_type} cannot sustain damage")
        self._sustained_damage = True

    def repair_damage(self) -> None:
        """Repair sustained damage on this unit."""
        self._sustained_damage = False

    def add_technology(self, technology: Technology) -> None:
        """Add a technology to this unit."""
        if isinstance(technology, str):
            technology = Technology(technology)
        self.technologies.add(technology)
        self.invalidate_stats_cache()

    @classmethod
    def load_unit(cls, unit_data: dict[str, Any]) -> "Unit":
        """Load a unit from serialized data."""
        # Convert string values back to enums
        unit_type = UnitType(unit_data["unit_type"])
        faction = Faction(unit_data["faction"]) if unit_data.get("faction") else None
        technologies = set(unit_data.get("technologies", []))

        # Convert technology strings to enums if needed
        tech_enums = set()
        for tech in technologies:
            try:
                tech_enums.add(Technology(tech))
            except ValueError:
                # If it's not a valid enum, keep as string for backward compatibility
                tech_enums.add(tech)

        return cls(
            unit_type=unit_type,
            owner=unit_data["owner"],
            faction=faction,
            technologies=tech_enums,
            unit_id=unit_data.get("id"),
        )

    def load_transport_unit(self, unit: "Unit") -> None:
        """Load a unit onto this transport unit."""
        from .exceptions import FleetCapacityError

        # Check if this unit has transport capacity
        capacity = self.get_capacity()
        if capacity == 0:
            raise FleetCapacityError(f"Unit {self.unit_type} has no transport capacity")

        # This is a placeholder for full transport functionality
        # In a complete implementation, we would track loaded units and check against capacity

    def unload_unit(self, unit: "Unit") -> None:
        """Unload a unit from this transport unit."""
        # This is a placeholder for transport functionality
        pass
