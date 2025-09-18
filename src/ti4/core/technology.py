"""Technology system for TI4."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from .constants import Technology as TechnologyEnum
from .constants import UnitType


class TechnologyColor(Enum):
    """Technology colors in TI4."""

    BLUE = "blue"
    GREEN = "green"
    RED = "red"
    YELLOW = "yellow"


@dataclass(frozen=True)
class Technology:
    """Represents a technology in TI4."""

    name: str
    color: TechnologyColor
    prerequisites: list[str]


class TechnologyTree:
    """Manages technology tree navigation and validation."""

    def can_research(
        self, technology: Technology, player_technologies: list[str]
    ) -> bool:
        """Check if a player can research a given technology."""
        # If technology has no prerequisites, it can always be researched
        if not technology.prerequisites:
            return True

        # Check if all prerequisites are satisfied
        for prerequisite in technology.prerequisites:
            if prerequisite not in player_technologies:
                return False

        return True


class TechnologyEffectSystem:
    """Manages technology effects on game mechanics."""

    def __init__(self, unit_stats_provider: Optional[Any] = None) -> None:
        """Initialize the technology effect system."""
        from .unit_stats import UnitStatsProvider

        self._unit_stats_provider = unit_stats_provider or UnitStatsProvider()

    def register_technology_effect(
        self, technology_name: TechnologyEnum, unit_type: UnitType, stat_modifier: Any
    ) -> None:
        """Register a technology effect on unit stats."""
        self._unit_stats_provider.register_technology_modifier(
            technology_name, unit_type, stat_modifier
        )
