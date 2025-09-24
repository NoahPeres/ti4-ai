"""Reinforcement pool system for TI4 Rule 31: DESTROYED.

This module implements reinforcement pool mechanics according to the TI4 LRR.
Handles tracking of units returned to reinforcements after destruction.
"""

from __future__ import annotations

from .constants import UnitType


class ReinforcementPool:
    """Manages a player's reinforcement pool for destroyed units.

    LRR Reference: Rule 31 - When a unit is destroyed, it is returned to reinforcements.
    """

    def __init__(self, player_id: str) -> None:
        """Initialize reinforcement pool for a player.

        Args:
            player_id: The player who owns this reinforcement pool
        """
        self.player_id = player_id
        self._unit_counts: dict[UnitType, int] = {}
        self._max_capacities: dict[UnitType, int] = {}

    def get_unit_count(self, unit_type: UnitType) -> int:
        """Get the current count of units in reinforcements.

        Args:
            unit_type: The type of unit to count

        Returns:
            Number of units of this type in reinforcements
        """
        return self._unit_counts.get(unit_type, 0)

    def set_unit_count(self, unit_type: UnitType, count: int) -> None:
        """Set the count of units in reinforcements.

        Args:
            unit_type: The type of unit
            count: Number of units to set
        """
        if count < 0:
            raise ValueError(f"Unit count cannot be negative: {count}")
        self._unit_counts[unit_type] = count

    def set_max_capacity(self, unit_type: UnitType, max_count: int) -> None:
        """Set the maximum capacity for a unit type.

        Args:
            unit_type: The type of unit
            max_count: Maximum number of units allowed
        """
        if max_count < 0:
            raise ValueError(f"Max capacity cannot be negative: {max_count}")
        self._max_capacities[unit_type] = max_count

    def return_destroyed_unit(self, unit_type: UnitType) -> None:
        """Return a destroyed unit to reinforcements.

        Args:
            unit_type: The type of unit being returned

        Raises:
            ValueError: If reinforcement pool is at capacity

        LRR Reference: Rule 31 - Destroyed units return to reinforcements
        """
        current_count = self.get_unit_count(unit_type)
        max_capacity = self._max_capacities.get(unit_type)

        if max_capacity is not None and current_count >= max_capacity:
            raise ValueError(f"Reinforcement pool at capacity for {unit_type}")

        self._unit_counts[unit_type] = current_count + 1

    def remove_units(self, unit_type: UnitType, count: int) -> None:
        """Remove units from reinforcements (for production).

        Args:
            unit_type: The type of unit to remove
            count: Number of units to remove

        Raises:
            ValueError: If not enough units available or count is not positive
        """
        if count <= 0:
            raise ValueError(f"Removal count must be positive: {count}")

        current_count = self.get_unit_count(unit_type)

        if count > current_count:
            raise ValueError(
                f"Not enough {unit_type} in reinforcements. "
                f"Requested: {count}, Available: {current_count}"
            )

        self._unit_counts[unit_type] = current_count - count

    def has_units_available(self, unit_type: UnitType, count: int) -> bool:
        """Check if enough units are available in reinforcements.

        Args:
            unit_type: The type of unit to check
            count: Number of units needed

        Returns:
            True if enough units are available

        Raises:
            ValueError: If count is negative
        """
        if count < 0:
            raise ValueError(f"Requested count cannot be negative: {count}")
        return self.get_unit_count(unit_type) >= count

    def get_all_unit_counts(self) -> dict[UnitType, int]:
        """Get all unit counts in reinforcements.

        Returns:
            Dictionary mapping unit types to their counts
        """
        return self._unit_counts.copy()
