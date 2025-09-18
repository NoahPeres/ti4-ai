"""Unit statistics system for TI4."""

from dataclasses import dataclass
from typing import Any, Optional

from .constants import Faction, Technology, UnitType


@dataclass(frozen=True)
class UnitStats:
    """Represents the statistics of a unit."""

    capacity: int = 0
    combat_value: Optional[int] = None
    combat_dice: int = 1
    movement: int = 1
    cost: float = 1
    sustain_damage: bool = False
    anti_fighter_barrage: bool = False
    space_cannon: bool = False
    bombardment: bool = False
    deploy: bool = False
    planetary_shield: bool = False
    production: int = 0

    def with_modifications(self, **kwargs: Any) -> "UnitStats":
        """Create a new UnitStats with modifications."""
        return UnitStats(
            capacity=kwargs.get("capacity", self.capacity),
            combat_value=kwargs.get("combat_value", self.combat_value),
            combat_dice=kwargs.get("combat_dice", self.combat_dice),
            movement=kwargs.get("movement", self.movement),
            cost=kwargs.get("cost", self.cost),
            sustain_damage=kwargs.get("sustain_damage", self.sustain_damage),
            anti_fighter_barrage=kwargs.get(
                "anti_fighter_barrage", self.anti_fighter_barrage
            ),
            space_cannon=kwargs.get("space_cannon", self.space_cannon),
            bombardment=kwargs.get("bombardment", self.bombardment),
            deploy=kwargs.get("deploy", self.deploy),
            planetary_shield=kwargs.get("planetary_shield", self.planetary_shield),
            production=kwargs.get("production", self.production),
        )


class UnitStatsProvider:
    """Provides unit statistics based on type, faction, and technologies."""

    # Base unit statistics
    BASE_STATS = {
        "carrier": UnitStats(
            capacity=4, combat_value=9, combat_dice=1, movement=1, cost=3
        ),
        "cruiser": UnitStats(
            capacity=0, combat_value=7, combat_dice=1, movement=2, cost=2
        ),  # Base cruiser has no capacity
        "cruiser_ii": UnitStats(
            capacity=1, combat_value=6, combat_dice=1, movement=2, cost=2
        ),  # Upgraded cruiser
        "dreadnought": UnitStats(
            capacity=1,
            combat_value=5,
            combat_dice=1,
            movement=1,
            cost=4,
            sustain_damage=True,
            bombardment=True,
        ),
        "destroyer": UnitStats(
            capacity=0,
            combat_value=9,
            combat_dice=1,
            movement=2,
            cost=1,
            anti_fighter_barrage=True,
        ),
        "fighter": UnitStats(
            capacity=0, combat_value=9, combat_dice=1, movement=0, cost=0.5
        ),  # Base fighter needs capacity
        "fighter_ii": UnitStats(
            capacity=0, combat_value=8, combat_dice=1, movement=1, cost=0.5
        ),  # Fighter II independent
        "infantry": UnitStats(
            capacity=0, combat_value=8, combat_dice=1, movement=0, cost=0.5
        ),
        "mech": UnitStats(
            capacity=0,
            combat_value=6,
            combat_dice=1,
            movement=0,
            cost=2,
            sustain_damage=True,
            deploy=True,
        ),
        "pds": UnitStats(
            capacity=0,
            combat_value=6,
            combat_dice=1,
            movement=0,
            cost=2,
            space_cannon=True,
            planetary_shield=True,
        ),
        "space_dock": UnitStats(
            capacity=0, combat_dice=0, movement=0, cost=4, production=2
        ),  # No combat, has production
        "war_sun": UnitStats(
            capacity=6,
            combat_value=3,
            combat_dice=3,
            movement=2,
            cost=12,
            sustain_damage=True,
            bombardment=True,
        ),
    }

    def __init__(self) -> None:
        """Initialize the unit stats provider."""
        self._faction_modifiers: dict[str, dict[str, UnitStats]] = {}
        self._technology_modifiers: dict[str, dict[str, UnitStats]] = {}

    def get_unit_stats(
        self,
        unit_type: UnitType,
        faction: Optional[Faction] = None,
        technologies: Optional[set[Technology]] = None,
    ) -> UnitStats:
        """Get unit statistics with faction and technology modifications."""
        # Convert technologies to frozenset for hashability
        tech_key = (
            frozenset(tech.value for tech in technologies)
            if technologies
            else frozenset()
        )
        return self._get_cached_unit_stats(
            unit_type.value, faction.value if faction else None, tech_key
        )

    def _get_cached_unit_stats(
        self,
        unit_type: str,
        faction: Optional[str],
        technologies: frozenset[str],
    ) -> UnitStats:
        """Cached version of unit stats calculation."""
        base_stats = self.BASE_STATS.get(unit_type)
        if base_stats is None:
            raise ValueError(f"Unknown unit type: {unit_type}")

        # Apply faction modifications
        if faction and faction in self._faction_modifiers:
            faction_mods = self._faction_modifiers[faction].get(unit_type)
            if faction_mods:
                base_stats = self._apply_modifications(base_stats, faction_mods)

        # Apply technology modifications
        if technologies:
            for tech in technologies:
                if tech in self._technology_modifiers:
                    tech_mods = self._technology_modifiers[tech].get(unit_type)
                    if tech_mods:
                        base_stats = self._apply_modifications(base_stats, tech_mods)

        return base_stats

    def _apply_modifications(
        self, base: UnitStats, modifications: UnitStats
    ) -> UnitStats:
        """Apply modifications to base stats."""
        return UnitStats(
            capacity=base.capacity + modifications.capacity,
            combat_value=modifications.combat_value
            if modifications.combat_value is not None
            else base.combat_value,
            combat_dice=base.combat_dice + modifications.combat_dice,
            movement=base.movement + modifications.movement,
            cost=base.cost + modifications.cost,
            sustain_damage=base.sustain_damage or modifications.sustain_damage,
            anti_fighter_barrage=base.anti_fighter_barrage
            or modifications.anti_fighter_barrage,
            space_cannon=base.space_cannon or modifications.space_cannon,
            bombardment=base.bombardment or modifications.bombardment,
            deploy=base.deploy or modifications.deploy,
            planetary_shield=base.planetary_shield or modifications.planetary_shield,
            production=base.production + modifications.production,
        )

    def register_faction_modifier(
        self, faction: Faction, unit_type: UnitType, stats: UnitStats
    ) -> None:
        """Register faction-specific unit modifications."""
        faction_key = faction.value
        unit_type_key = unit_type.value
        if faction_key not in self._faction_modifiers:
            self._faction_modifiers[faction_key] = {}
        self._faction_modifiers[faction_key][unit_type_key] = stats
        # Clear cache when modifiers change (cache removed for now)
        # self._get_cached_unit_stats.cache_clear()

    def register_technology_modifier(
        self, technology: Technology, unit_type: UnitType, stats: UnitStats
    ) -> None:
        """Register technology-based unit modifications."""
        technology_key = technology.value
        unit_type_key = unit_type.value
        if technology_key not in self._technology_modifiers:
            self._technology_modifiers[technology_key] = {}
        self._technology_modifiers[technology_key][unit_type_key] = stats
        # Clear cache when modifiers change (cache removed for now)
        # self._get_cached_unit_stats.cache_clear()
