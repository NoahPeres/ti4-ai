"""Faction-specific data and constants for TI4."""

from .constants import Faction


class FactionData:
    """Provides faction-specific data and constants."""

    # Faction commodity values based on faction sheets
    # These values represent the maximum commodities each faction can have
    COMMODITY_VALUES = {
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

    @classmethod
    def get_commodity_value(cls, faction: Faction) -> int:
        """Get the commodity value for a faction.

        Args:
            faction: The faction to get commodity value for

        Returns:
            The maximum number of commodities this faction can have

        Raises:
            ValueError: If faction is not recognized
        """
        if faction not in cls.COMMODITY_VALUES:
            raise ValueError(f"Unknown faction: {faction}")
        return cls.COMMODITY_VALUES[faction]
