"""Unit structure for TI4 game pieces."""

import logging
import uuid
from typing import Any

from .constants import Faction, Technology, UnitType
from .unit_stats import UnitStats, UnitStatsProvider

logger = logging.getLogger(__name__)

# Unit categorization for game mechanics
FIGHTER_TYPE_UNITS = {UnitType.FIGHTER, UnitType.FIGHTER_II}
# Future expansion: Add faction-specific fighters here
# FIGHTER_TYPE_UNITS.update({UnitType.FACTION_FIGHTER_VARIANT, ...})


def _normalize_technologies(
    technologies: set[Technology | str] | set[Technology] | None, *, strict: bool = True
) -> set[Technology]:
    """Normalize technologies to Technology enums.

    Args:
        technologies: Mixed set of Technology enums and/or strings
        strict: If True, raise TypeError for invalid types; if False, log warning and skip

    Returns:
        Set of Technology enums
    """
    if not technologies:
        return set()

    normalized: set[Technology] = set()
    for t in technologies:
        if isinstance(t, Technology):
            normalized.add(t)
        elif isinstance(t, str):
            try:
                normalized.add(Technology(t))
            except ValueError:
                if strict:
                    # Skip unknown tech strings for robustness; alternatively, raise
                    continue
                else:
                    logger.warning(f"Skipping unknown technology: {t}")
                    continue
        else:
            msg = f"Invalid technology type: {type(t).__name__}"
            if strict:
                raise TypeError(msg)
            else:
                logger.warning(f"Skipping {msg}: {t}")
    return normalized


class Unit:
    """Represents a game unit with type and owner."""

    # Instance variable type annotations
    id: str
    unit_type: UnitType
    owner: str
    faction: Faction | None
    technologies: set[Technology]
    _stats_provider: UnitStatsProvider
    _cached_stats: UnitStats | None
    _sustained_damage: bool

    def __init__(
        self,
        unit_type: UnitType,
        owner: str,
        faction: Faction | None = None,
        technologies: set[Technology] | None = None,
        stats_provider: UnitStatsProvider | None = None,
        unit_id: str | None = None,
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

        # Normalize technologies to Technology enums
        self.technologies = _normalize_technologies(technologies, strict=True)

        self._stats_provider = stats_provider or UnitStatsProvider()
        self._cached_stats = None
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

    def get_combat_value(self) -> int | None:
        """Get the combat value for this unit."""
        return self.get_stats().combat_value

    def get_combat(self) -> int | None:
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

    def get_anti_fighter_barrage_value(self) -> int:
        """Get the anti-fighter barrage value of this unit."""
        stats = self.get_stats()
        if not stats.anti_fighter_barrage or stats.anti_fighter_barrage_value is None:
            raise AttributeError(
                f"Unit {self.unit_type} does not have anti-fighter barrage ability"
            )
        return stats.anti_fighter_barrage_value

    def get_anti_fighter_barrage_dice_count(self) -> int:
        """Get the number of anti-fighter barrage dice this unit rolls."""
        stats = self.get_stats()
        if not stats.anti_fighter_barrage:
            raise AttributeError(
                f"Unit {self.unit_type} does not have anti-fighter barrage ability"
            )
        # Default to 1 die if present but dice count is 0; raise on negative for consistency with Combat
        if stats.anti_fighter_barrage_dice < 0:
            raise ValueError("AFB dice count cannot be negative")
        return stats.anti_fighter_barrage_dice or 1

    def validate_anti_fighter_barrage_context(self, context: str) -> bool:
        """Validate that AFB is being used in the appropriate context."""
        if not self.has_anti_fighter_barrage():
            return False
        # AFB can only be used in space combat
        return isinstance(context, str) and context.strip().lower() == "space_combat"

    def can_perform_anti_fighter_barrage(self, context: str) -> bool:
        """Check if this unit can perform anti-fighter barrage in the given context."""
        return (
            self.has_anti_fighter_barrage()
            and self.validate_anti_fighter_barrage_context(context)
        )

    def is_fighter_type(self) -> bool:
        """Check if this unit is a fighter-type unit (including upgrades and faction variants)."""
        return self.unit_type in FIGHTER_TYPE_UNITS

    def is_valid_afb_target(self) -> bool:
        """Check if this unit is a valid target for anti-fighter barrage."""
        # AFB can only target fighter-type units (including upgraded variants and future faction-specific fighters)
        return self.is_fighter_type()

    @staticmethod
    def filter_afb_targets(units: list["Unit"]) -> list["Unit"]:
        """Filter a list of units to only include valid AFB targets (fighters)."""
        return [unit for unit in units if unit.is_valid_afb_target()]

    @staticmethod
    def filter_enemy_afb_targets(
        units: list["Unit"], attacking_player: str
    ) -> list["Unit"]:
        """Filter a list of units to only include enemy fighters that can be targeted by AFB."""
        return [
            unit
            for unit in units
            if unit.is_valid_afb_target() and unit.owner != attacking_player
        ]

    def has_space_cannon(self) -> bool:
        """Check if this unit has space cannon ability."""
        return self.get_stats().space_cannon

    def has_bombardment(self) -> bool:
        """Check if this unit has bombardment ability."""
        return self.get_stats().bombardment

    def get_bombardment_value(self) -> int:
        """Get the bombardment value of this unit."""
        stats = self.get_stats()
        if not stats.bombardment or stats.bombardment_value is None:
            raise AttributeError(
                f"Unit {self.unit_type} does not have bombardment ability"
            )
        return stats.bombardment_value

    def get_bombardment_dice_count(self) -> int:
        """Get the number of bombardment dice this unit rolls."""
        stats = self.get_stats()
        if not stats.bombardment:
            raise AttributeError(
                f"Unit {self.unit_type} does not have bombardment ability"
            )
        # Default to 1 dice if bombardment ability is present but dice count is 0
        return stats.bombardment_dice if stats.bombardment_dice > 0 else 1

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
        raw_techs = unit_data.get("technologies", [])
        tech_enums = _normalize_technologies(
            set(raw_techs) if raw_techs else None, strict=False
        )

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
