"""Faction-specific data and configuration for TI4 factions."""

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from .constants import Faction


class FactionData:
    """Centralized faction data and configuration."""

    COMMODITY_VALUES: Final[Mapping[Faction, int]] = MappingProxyType(
        {
            Faction.SOL: 4,
            Faction.HACAN: 6,  # Trade-focused faction
            Faction.XXCHA: 4,
            Faction.JORD: 4,
            Faction.YSSARIL: 3,
            Faction.NAALU: 3,
            Faction.BARONY: 2,
            Faction.SAAR: 3,
            Faction.MUAAT: 4,
            Faction.ARBOREC: 3,
            Faction.L1Z1X: 2,
            Faction.WINNU: 3,
        }
    )

    @classmethod
    def get_commodity_value(cls, faction: Faction) -> int:
        """Get the commodity value for a faction.

        Args:
            faction: The faction to get the commodity value for

        Returns:
            The commodity value for the faction

        Raises:
            ValueError: If the faction is not recognized
        """
        value = cls.COMMODITY_VALUES.get(faction)
        if value is None:
            raise ValueError(f"Unknown faction: {faction}")
        return value
