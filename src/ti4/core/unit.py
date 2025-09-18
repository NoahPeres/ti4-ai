"""Unit structure for TI4 game pieces."""

import uuid
from typing import Optional, Union

from .constants import UnitType, Faction, Technology
from .unit_stats import UnitStats, UnitStatsProvider


class Unit:
    """Represents a game unit with type and owner."""

    def __init__(
        self,
        unit_type: Union[UnitType, str],
        owner: str,
        faction: Optional[Union[Faction, str]] = None,
        technologies: Optional[set[Union[Technology, str]]] = None,
        stats_provider: Optional[UnitStatsProvider] = None,
        unit_id: Optional[str] = None,
    ) -> None:
        self.id = unit_id or str(uuid.uuid4())
        
        # Convert enum to string value if needed for backward compatibility
        if isinstance(unit_type, UnitType):
            self.unit_type = unit_type.value
        else:
            self.unit_type = unit_type
            
        self.owner = owner
        
        # Convert enum to string value if needed for backward compatibility
        if isinstance(faction, Faction):
            self.faction = faction.value
        else:
            self.faction = faction
            
        # Convert technology enums to string values if needed
        if technologies:
            self.technologies = {
                tech.value if isinstance(tech, Technology) else tech
                for tech in technologies
            }
        else:
            self.technologies = set()
            
        self._stats_provider = stats_provider or UnitStatsProvider()
        self._cached_stats: Optional[UnitStats] = None
        self._sustained_damage = False

    def get_stats(self) -> UnitStats:
        """Get the current statistics for this unit."""
        if self._cached_stats is None:
            self._cached_stats = self._stats_provider.get_unit_stats(
                self.unit_type, self.faction, self.technologies
            )
        return self._cached_stats

    def get_capacity(self) -> int:
        """Get the capacity of this unit."""
        return self.get_stats().capacity

    def get_combat_value(self) -> Optional[int]:
        """Get the combat value of this unit."""
        return self.get_stats().combat_value

    def get_movement(self) -> int:
        """Get the movement value of this unit."""
        return self.get_stats().movement

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
