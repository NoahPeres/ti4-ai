"""Unit statistics system for TI4."""

from dataclasses import dataclass
from typing import Any, Optional

from .constants import Faction, Technology, UnitType


@dataclass(frozen=True)
class UnitStats:
    """Represents the statistics of a unit.

    Organized into two semantic groups:
    1. Fundamental Unit Properties: Basic stats that define the unit
    2. Unit Abilities: Special capabilities the unit may have
    """

    # === FUNDAMENTAL UNIT PROPERTIES ===
    cost: float = 0
    combat_value: Optional[int] = None
    combat_dice: int = 0
    movement: int = 0
    capacity: int = 0
    production: int = 0

    # === UNIT ABILITIES ===
    sustain_damage: bool = False
    anti_fighter_barrage: bool = False
    bombardment: bool = False
    deploy: bool = False
    planetary_shield: bool = False
    space_cannon: bool = False
    space_cannon_value: Optional[int] = None
    space_cannon_dice: int = 1
    has_production: bool = False  # Whether unit has production ability (separate from production value)

    def with_modifications(self, **kwargs: Any) -> "UnitStats":
        """Create a new UnitStats with modifications."""
        return UnitStats(
            # Fundamental properties
            cost=kwargs.get("cost", self.cost),
            combat_value=kwargs.get("combat_value", self.combat_value),
            combat_dice=kwargs.get("combat_dice", self.combat_dice),
            movement=kwargs.get("movement", self.movement),
            capacity=kwargs.get("capacity", self.capacity),
            production=kwargs.get("production", self.production),
            # Unit abilities
            sustain_damage=kwargs.get("sustain_damage", self.sustain_damage),
            anti_fighter_barrage=kwargs.get(
                "anti_fighter_barrage", self.anti_fighter_barrage
            ),
            bombardment=kwargs.get("bombardment", self.bombardment),
            deploy=kwargs.get("deploy", self.deploy),
            planetary_shield=kwargs.get("planetary_shield", self.planetary_shield),
            space_cannon=kwargs.get("space_cannon", self.space_cannon),
            space_cannon_value=kwargs.get(
                "space_cannon_value", self.space_cannon_value
            ),
            space_cannon_dice=kwargs.get("space_cannon_dice", self.space_cannon_dice),
            has_production=kwargs.get("has_production", self.has_production),
        )


class UnitStatsProvider:
    """Provides unit statistics based on type, faction, and technologies."""

    # Base unit statistics
    BASE_STATS = {
        UnitType.CARRIER: UnitStats(
            cost=3, combat_value=9, combat_dice=1, movement=1, capacity=4
        ),
        UnitType.CRUISER: UnitStats(
            cost=2, combat_value=7, combat_dice=1, movement=2, capacity=0
        ),  # Base cruiser has no capacity
        UnitType.CRUISER_II: UnitStats(
            cost=2, combat_value=6, combat_dice=1, movement=3, capacity=1
        ),  # Upgraded cruiser
        UnitType.DREADNOUGHT: UnitStats(
            cost=4,
            combat_value=5,
            combat_dice=1,
            movement=1,
            capacity=1,
            sustain_damage=True,
            bombardment=True,
        ),
        UnitType.DESTROYER: UnitStats(
            cost=1,
            combat_value=9,
            combat_dice=1,
            movement=2,
            capacity=0,
            anti_fighter_barrage=True,
        ),
        UnitType.FIGHTER: UnitStats(
            cost=0.5, combat_value=9, combat_dice=1, movement=0, capacity=0
        ),  # Base fighter needs capacity
        UnitType.INFANTRY: UnitStats(
            cost=0.5, combat_value=8, combat_dice=1, movement=0, capacity=0
        ),
        UnitType.MECH: UnitStats(
            cost=2,
            combat_value=6,
            combat_dice=1,
            movement=0,
            capacity=0,
            sustain_damage=True,
            deploy=True,
        ),
        UnitType.PDS: UnitStats(
            combat_dice=0,  # PDS don't have combat dice, only space cannon
            movement=0,
            capacity=0,
            space_cannon=True,
            space_cannon_value=6,
            space_cannon_dice=1,
            planetary_shield=True,
        ),
        UnitType.SPACE_DOCK: UnitStats(
            cost=0,  # Space docks cannot be produced directly
            combat_value=None,
            combat_dice=0,
            movement=0,
            capacity=0,
            production=0,  # Production is dynamic: planet resources + 2
            sustain_damage=False,
            anti_fighter_barrage=False,
            space_cannon=False,
            bombardment=False,
            deploy=False,
            planetary_shield=False,
            has_production=True,  # Space dock has production ability
        ),
        UnitType.WAR_SUN: UnitStats(
            cost=12,
            combat_value=3,
            combat_dice=3,
            movement=2,
            capacity=6,
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
        # Convert string unit_type to enum for lookup
        try:
            unit_type_enum = UnitType(unit_type)
        except ValueError:
            raise ValueError(f"Unknown unit type: {unit_type}")
            
        base_stats = self.BASE_STATS.get(unit_type_enum)
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
            # Fundamental properties
            cost=base.cost + modifications.cost,
            combat_value=modifications.combat_value
            if modifications.combat_value is not None
            else base.combat_value,
            combat_dice=base.combat_dice + modifications.combat_dice,
            movement=base.movement + modifications.movement,
            capacity=base.capacity + modifications.capacity,
            production=base.production + modifications.production,
            # Unit abilities
            sustain_damage=base.sustain_damage or modifications.sustain_damage,
            anti_fighter_barrage=base.anti_fighter_barrage
            or modifications.anti_fighter_barrage,
            bombardment=base.bombardment or modifications.bombardment,
            deploy=base.deploy or modifications.deploy,
            planetary_shield=base.planetary_shield or modifications.planetary_shield,
            space_cannon=base.space_cannon or modifications.space_cannon,
            space_cannon_value=modifications.space_cannon_value
            if modifications.space_cannon_value is not None
            else base.space_cannon_value,
            space_cannon_dice=base.space_cannon_dice + modifications.space_cannon_dice,
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
